"""CLI for the LLM Council research skill.

Usage: python -m research <command> [args]
"""

import argparse
import asyncio
import json
from pathlib import Path

from .council import run_council, query_single, CouncilResult, PROVIDERS, TIMEOUT


def _print_result(result: CouncilResult):
    print("\n=== COUNCIL SYNTHESIS ===\n")
    print(result.synthesis)

    if result.rankings:
        print("\n=== AGGREGATE RANKINGS ===\n")
        for i, (provider, rank) in enumerate(result.rankings):
            print(f"  {i + 1}. {provider} - avg rank: {rank}")

    print("\n=== INDIVIDUAL RESPONSES ===\n")
    for r in result.responses:
        print(f"\n--- {r.provider} ({r.model}) ---\n")
        print(r.content)

    if result.reviews:
        print("\n=== PEER REVIEWS ===\n")
        for r in result.reviews:
            print(f"\n--- Review by {r.reviewer} ---\n")
            print(r.review)


def main():
    parser = argparse.ArgumentParser(prog="research", description="LLM Council: multi-model research")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("research", help="Research a topic")
    p.add_argument("topic", nargs="+")

    p = sub.add_parser("review", help="Code review")
    p.add_argument("file")
    p.add_argument("context", nargs="?", default="Code review")

    p = sub.add_parser("compare", help="Compare technologies")
    p.add_argument("technologies", nargs="+")

    p = sub.add_parser("bug", help="Bug analysis")
    p.add_argument("file")
    p.add_argument("symptoms", nargs="*", default=["Bug reported"])

    p = sub.add_parser("design", help="Architecture review")
    p.add_argument("file")
    p.add_argument("requirements", nargs="*", default=["General review"])

    p = sub.add_parser("validate", help="Validate a decision")
    p.add_argument("decision")
    p.add_argument("context")
    p.add_argument("alternatives", nargs="*")

    p = sub.add_parser("comprehensive", help="Full file review")
    p.add_argument("file")
    p.add_argument("topic", nargs="?", default="")

    p = sub.add_parser("query", help="Query a single provider")
    p.add_argument("provider", choices=list(PROVIDERS.keys()))
    p.add_argument("topic", nargs="+")
    p.add_argument("--context", default="Research query")
    p.add_argument("--task-type", default="research", choices=["research", "code-review", "bug-analysis", "comparison"])

    p = sub.add_parser("review-responses", help="Run peer review on collected responses")
    p.add_argument("query", help="Original query that produced the responses")
    p.add_argument("responses_file", help="JSON file with collected responses")

    args = parser.parse_args()
    cmd = args.command

    if cmd == "query":
        result = asyncio.run(query_single(args.provider, " ".join(args.topic), args.context, args.task_type))
        print(f"\n=== {result.provider} ({result.model}) ===\n")
        print(result.content)
        return

    if cmd == "review-responses":
        _run_review_responses(args)
        return

    if cmd == "research":
        query, context, task = " ".join(args.topic), "Research query", "research"
    elif cmd == "compare":
        query, context, task = ", ".join(args.technologies), "Technology comparison", "comparison"
    elif cmd == "validate":
        alt = f"\nAlternatives: {', '.join(args.alternatives)}" if args.alternatives else ""
        query, context, task = args.decision, f"{args.context}{alt}", "research"
    elif cmd in ("review", "bug", "design", "comprehensive"):
        query = Path(args.file).read_text()
        if cmd == "review":
            context, task = args.context, "code-review"
        elif cmd == "bug":
            context, task = " ".join(args.symptoms), "bug-analysis"
        elif cmd == "design":
            context, task = " ".join(args.requirements), "code-review"
        else:
            context = f"File: {args.file}" + (f" - Topic: {args.topic}" if args.topic else "")
            task = "code-review"

    _print_result(asyncio.run(run_council(query, context, task)))


def _run_review_responses(args):
    """Run peer review on a JSON file of previously collected responses."""
    from .council import _available, _peer_review, ModelResponse as MR

    import httpx

    data = json.loads(Path(args.responses_file).read_text())
    responses = [MR(provider=r["provider"], model=r["model"], content=r["content"]) for r in data]

    providers = _available()
    if not providers:
        raise SystemExit("No API keys found for peer review.")

    async def _run():
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            return await _peer_review(client, providers, responses, args.query, "Peer review")

    reviews, rankings = asyncio.run(_run())

    if rankings:
        print("\n=== AGGREGATE RANKINGS ===\n")
        for i, (provider, rank) in enumerate(rankings):
            print(f"  {i + 1}. {provider} - avg rank: {rank}")

    print("\n=== PEER REVIEWS ===\n")
    for r in reviews:
        print(f"\n--- Review by {r.reviewer} ---\n")
        print(r.review)


if __name__ == "__main__":
    main()
