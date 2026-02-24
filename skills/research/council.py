"""
LLM Council: 3-stage multi-model research pipeline.

Stage 1 - Collect: Query all models in parallel
Stage 2 - Peer Review: Each model anonymously critiques others
Stage 3 - Synthesize: Chairman produces final integrated answer

Inspired by karpathy/llm-council.
"""

import asyncio
import os
import re
from dataclasses import dataclass

import httpx

TIMEOUT = 300
PROVIDERS = {
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "env_key": "OPENAI_API_KEY",
        "model": os.environ.get("OPENAI_MODEL", "gpt-5.2"),
    },
    "perplexity": {
        "url": "https://api.perplexity.ai/chat/completions",
        "env_key": "PERPLEXITY_API_KEY",
        "model": os.environ.get("PERPLEXITY_MODEL", "sonar-deep-research"),
    },
    "anthropic": {
        "url": "https://api.anthropic.com/v1/messages",
        "env_key": "ANTHROPIC_API_KEY",
        "model": os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-6"),
    },
    "gemini": {
        "env_key": "GOOGLE_CLOUD_PROJECT",
        "model": os.environ.get("GEMINI_MODEL", "gemini-3-pro-preview"),
    },
}
SYSTEM_PROMPTS = {
    "code-review": "You are an expert software architect and code reviewer. Provide detailed, actionable feedback.",
    "research": "You are a technical researcher. Provide current, citation-backed information.",
    "bug-analysis": "You are an expert debugger. Analyze issues systematically with root cause identification.",
    "comparison": "You are a technical analyst. Compare technologies objectively with current information.",
}

# First available provider in the list becomes chairman for synthesis.
CHAIRMAN_PREFERENCE = {
    "code-review": ["gemini", "openai", "anthropic", "perplexity"],
    "research": ["perplexity", "gemini", "openai", "anthropic"],
    "bug-analysis": ["gemini", "openai", "anthropic", "perplexity"],
    "comparison": ["gemini", "openai", "anthropic", "perplexity"],
}

_gemini_client = None


def _get_gemini_client():
    """Lazily create and cache a Gemini client for Vertex AI."""
    global _gemini_client
    if _gemini_client is not None:
        return _gemini_client

    try:
        from google import genai
    except ImportError:
        return None

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project:
        return None

    try:
        _gemini_client = genai.Client(vertexai=True, project=project, location=location)
    except Exception:
        return None
    return _gemini_client


@dataclass
class ModelResponse:
    provider: str
    model: str
    content: str


@dataclass
class PeerReview:
    reviewer: str
    review: str


@dataclass
class CouncilResult:
    query: str
    synthesis: str
    responses: list[ModelResponse]
    reviews: list[PeerReview]
    rankings: list[tuple[str, float]]


def _build_messages(query: str, context: str, task_type: str) -> list[dict]:
    """Build the system + user message list for a query."""
    system_prompt = SYSTEM_PROMPTS.get(task_type, SYSTEM_PROMPTS["research"])
    if task_type == "code-review":
        user_prompt = f"Review this code:\n\nContext: {context}\n\n```\n{query}\n```"
    elif context:
        user_prompt = f"{query}\n\nContext: {context}"
    else:
        user_prompt = query
    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]


def _sanitize_error(e: Exception) -> str:
    """Strip potential API keys/tokens from error messages."""
    msg = str(e)
    # Mask anything that looks like a bearer token or API key
    msg = re.sub(r'(Bearer |sk-|pplx-|key=)[^\s\'"]+', r'\1***', msg)
    msg = re.sub(r'x-api-key:\s*[^\s\'"]+', 'x-api-key: ***', msg)
    return msg


async def _query(client, provider, messages):
    cfg = PROVIDERS[provider]

    if provider == "gemini":
        return await _query_gemini(cfg, messages)

    key = os.environ[cfg["env_key"]]

    if provider == "anthropic":
        system = next((m["content"] for m in messages if m["role"] == "system"), None)
        user_msgs = [m for m in messages if m["role"] != "system"]
        body = {"model": cfg["model"], "max_tokens": 4096, "messages": user_msgs}
        if system:
            body["system"] = system
        resp = await client.post(
            cfg["url"],
            headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
            json=body,
        )
        resp.raise_for_status()
        content = next((b["text"] for b in resp.json()["content"] if b["type"] == "text"), "")
    else:
        body = {"model": cfg["model"], "messages": messages, "temperature": 0.3}
        resp = await client.post(
            cfg["url"],
            headers={"Authorization": f"Bearer {key}"},
            json=body,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

    return ModelResponse(provider.title(), cfg["model"], content)


async def _query_gemini(cfg, messages):
    """Query Gemini via the google-genai SDK (Vertex AI)."""
    from google.genai import types

    gemini = _get_gemini_client()
    if gemini is None:
        raise RuntimeError("Gemini client not available (missing GOOGLE_CLOUD_PROJECT or google-genai)")

    system = next((m["content"] for m in messages if m["role"] == "system"), None)
    user_content = "\n\n".join(m["content"] for m in messages if m["role"] != "system")

    response = await gemini.aio.models.generate_content(
        model=cfg["model"],
        contents=user_content,
        config=types.GenerateContentConfig(
            system_instruction=system,
            max_output_tokens=4096,
            temperature=0.3,
        ),
    )

    # response.text raises ValueError if blocked by safety filters or empty candidates
    try:
        text = response.text
    except (ValueError, AttributeError):
        candidates = getattr(response, "candidates", [])
        if candidates and candidates[0].finish_reason:
            raise RuntimeError(f"Gemini response blocked: {candidates[0].finish_reason}")
        raise RuntimeError("Gemini returned empty response (possibly blocked by safety filters)")

    return ModelResponse("Gemini", cfg["model"], text)


def _available():
    available = []
    for name, cfg in PROVIDERS.items():
        if name == "gemini":
            if os.environ.get("GOOGLE_CLOUD_PROJECT") and _get_gemini_client() is not None:
                available.append(name)
        elif os.environ.get(cfg["env_key"]):
            available.append(name)
    return available


def _select_chairman(providers: list[str], task_type: str) -> str:
    """Pick the best available chairman based on task type preference order."""
    if not providers:
        raise RuntimeError("No providers available for chairman selection")
    preference = CHAIRMAN_PREFERENCE.get(task_type, CHAIRMAN_PREFERENCE["research"])
    for candidate in preference:
        if candidate in providers:
            return candidate
    return providers[0]


def _extract_rankings(text: str, label_to_provider: dict) -> dict[str, list[int]]:
    """Extract rankings from a review's FINAL RANKING section.

    Uses anchored regex to match numbered list items, avoiding false matches
    from free-text mentions of response labels.
    """
    scores: dict[str, list[int]] = {}
    if "FINAL RANKING:" not in text:
        return scores

    ranking_section = text.split("FINAL RANKING:")[1]
    # Match numbered entries like "1. Response A" or "1. **Response A**"
    for match in re.finditer(r"(\d+)\.\s*\*{0,2}Response ([A-Z])\*{0,2}", ranking_section):
        rank = int(match.group(1))
        label = f"Response {match.group(2)}"
        if label in label_to_provider:
            scores.setdefault(label_to_provider[label], []).append(rank)

    return scores


async def _fan_out(client, providers, messages, label="querying"):
    async def _safe(name):
        try:
            print(f"  -> {name} {label}...")
            result = await _query(client, name, messages)
            print(f"  <- {name} done")
            return result
        except Exception as e:
            print(f"  !! {name} failed: {_sanitize_error(e)}")
            return None

    results = await asyncio.gather(*[_safe(n) for n in providers])
    return [r for r in results if r]


async def _peer_review(client, providers, responses, query, context):
    labels = [f"Response {chr(65 + i)}" for i in range(len(responses))]
    label_to_provider = dict(zip(labels, (r.provider for r in responses)))
    anonymized = "\n\n---\n\n".join(f"{l}:\n{r.content}" for l, r in zip(labels, responses))

    messages = [
        {"role": "system", "content": "You are an expert evaluator. Provide critical, fair analysis."},
        {"role": "user", "content": (
            f"You are evaluating AI responses to this query.\n\n"
            f"Original Query: {query}\nContext: {context}\n\n{anonymized}\n\n"
            f"Evaluate each response for accuracy, depth, and usefulness.\n"
            f"End with FINAL RANKING: (best to worst, e.g. \"1. Response A\")"
        )},
    ]

    raw = await _fan_out(client, providers, messages, label="reviewing")

    reviews = []
    all_scores: dict[str, list[int]] = {}
    for r in raw:
        reviews.append(PeerReview(r.provider, r.content))
        for provider, ranks in _extract_rankings(r.content, label_to_provider).items():
            all_scores.setdefault(provider, []).extend(ranks)

    rankings = sorted(
        [(p, round(sum(s) / len(s), 2)) for p, s in all_scores.items()],
        key=lambda x: x[1],
    )
    return reviews, rankings


async def _synthesize(client, chairman, query, context, responses, reviews, rankings):
    responses_text = "\n\n---\n\n".join(f"{r.provider} ({r.model}):\n{r.content}" for r in responses)
    reviews_text = "\n\n---\n\n".join(f"Reviewer {r.reviewer}:\n{r.review}" for r in reviews)
    rankings_text = "\n".join(f"  {i+1}. {p} - avg rank: {r}" for i, (p, r) in enumerate(rankings))

    messages = [
        {"role": "system", "content": "You are the Chairman of an LLM Council. Provide a definitive synthesis."},
        {"role": "user", "content": (
            f"You are the Chairman of an LLM Council.\n\n"
            f"Original Question: {query}\nContext: {context}\n\n"
            f"=== Individual Responses ===\n{responses_text}\n\n"
            f"=== Peer Reviews ===\n{reviews_text}\n\n"
            f"=== Rankings (by peer review) ===\n{rankings_text}\n\n"
            f"Synthesize into a single answer. Give greater weight to higher-ranked "
            f"responses, but incorporate valid points from all. Use these sections:\n"
            f"## Synthesis\n## Agreements\n## Conflicts\n## Recommendation"
        )},
    ]
    result = await _query(client, chairman, messages)
    return result.content


async def run_council(query: str, context: str, task_type: str = "research") -> CouncilResult:
    providers = _available()
    if not providers:
        raise SystemExit(
            "No API keys found. Set OPENAI_API_KEY, PERPLEXITY_API_KEY, "
            "ANTHROPIC_API_KEY, or GOOGLE_CLOUD_PROJECT."
        )

    messages = _build_messages(query, context, task_type)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        print("\n--- Stage 1: Collecting responses ---")
        responses = await _fan_out(client, providers, messages)
        if not responses:
            raise RuntimeError("All models failed.")

        if len(responses) == 1:
            return CouncilResult(query, responses[0].content, responses, [], [])

        print("\n--- Stage 2: Peer review ---")
        reviews, rankings = await _peer_review(client, providers, responses, query, context)

        print("\n--- Stage 3: Synthesis ---")
        chairman = _select_chairman(providers, task_type)
        print(f"  Chairman: {chairman}")
        synthesis = await _synthesize(client, chairman, query, context, responses, reviews, rankings)

        return CouncilResult(query, synthesis, responses, reviews, rankings)


async def query_single(provider: str, query: str, context: str, task_type: str = "research") -> ModelResponse:
    """Query a single provider without running the full council pipeline."""
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}. Available: {list(PROVIDERS.keys())}")

    cfg = PROVIDERS[provider]
    if provider == "gemini":
        if not os.environ.get("GOOGLE_CLOUD_PROJECT") or _get_gemini_client() is None:
            raise RuntimeError(f"Provider '{provider}' not available (missing GOOGLE_CLOUD_PROJECT)")
    elif not os.environ.get(cfg["env_key"]):
        raise RuntimeError(f"Provider '{provider}' not available (missing {cfg['env_key']})")

    messages = _build_messages(query, context, task_type)

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        return await _query(client, provider, messages)
