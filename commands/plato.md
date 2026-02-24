---
description: Socratic prompt purification — scrubs false premises, biased framing, and misleading context before ensemble evaluation
allowed_tools: [Task, Bash, Read, Write, Glob, Grep, WebFetch]
---

# Plato — Prompt Purification Pipeline

*"The shadows on the wall are not the thing itself."*

Plato systematically purifies a prompt by surfacing and removing false premises,
leading framing, presupposition traps, and latent biases — then reconstructs a
clean, epistemically neutral version suitable for reliable ensemble evaluation.

**⚠️ CRITICAL**: When invoked, IMMEDIATELY delegate to `/orchestrate` to
coordinate the purification pipeline. DO NOT attempt the analysis yourself.

## Immediate Action Required

Invoke `/orchestrate` with the Plato pipeline context:

```
SlashCommand(
  command: "/orchestrate plato [prompt to purify]"
)
```

Pass the full original prompt verbatim as the argument. The orchestrator
coordinates all phases sequentially below.

---

## Pipeline Phases

### Phase 1: Structural Decomposition

Delegate to `general-purpose` agent to decompose the prompt into a structured
JSON object:

```json
{
  "core_question": "What is actually being asked, stripped of all framing",
  "embedded_premises": ["Every fact assumed true without justification"],
  "framing_language": ["Evaluative, emotional, or leading terms"],
  "context_payload": ["Background information provided by the user"],
  "implicit_exclusions": ["Answers the prompt structurally rules out"]
}
```

Instruct the agent: extract exhaustively — surface implicit premises, not just
explicit ones. "Why is X better?" embeds "X is better" as a premise.

**Gate**: Decomposition must be complete before Phase 2. No partial handoffs.

---

### Phase 2: Premise Verification

For each premise extracted in Phase 1, delegate to `general-purpose` agent to
classify and score:

| Field | Values |
|---|---|
| `type` | factual / causal / temporal / consensus / comparative |
| `confidence` | Verified / Uncertain / Contradicted / Unverifiable |
| `evidence` | Brief justification for the confidence score |
| `action` | Keep / Flag / Remove |

Rules:
- **Verified** → Keep, include in reconstructed prompt
- **Uncertain** → Flag explicitly — include with caveat, never silently
- **Contradicted** → Remove, note in final report
- **Unverifiable** → Flag — treat as assumption, not fact

The agent must **flag, never silently discard** — the report must show what
was removed and why.

**Hard case to always flag**: premises that can only be verified using the
same model that will answer the question (circular verification trap).

---

### Phase 3: Linguistic Analysis

Delegate to `general-purpose` agent to scan for adversarial framing patterns:

**Leading Questions**
> "Why has microservices architecture consistently outperformed monoliths?"
> → Embeds the conclusion in the question

**False Dichotomies**
> "Should we use A or B?"
> → Occludes the full option space

**Presupposition Traps**
> "How long has this been broken?"
> → Assumes it is broken

**Anchor Language**
> "Given that X failed, how should we proceed?"
> → Treats a contested claim as settled

**Loaded Terms**
> "obvious", "clearly", "everyone knows", "naturally", "simply"
> → Assert consensus without evidence

**Implied Urgency / Stakes Inflation**
> "critical", "crisis", "must", "only option"
> → Narrow framing under pressure

Return a tagged list of each identified pattern with its location in the prompt
and a proposed neutral rewrite.

---

### Phase 4: Reconstruction

Delegate to `general-purpose` agent to rebuild the prompt:

1. Start from the `core_question` (Phase 1)
2. Attach only Verified or explicitly-flagged-Uncertain context (Phase 2)
3. Apply all linguistic neutralizations (Phase 3)
4. Convert leading questions to open questions
5. Replace loaded terms with neutral equivalents
6. Append an explicit non-assumption statement:

```
Note: Do not assume [list of removed premises]. These have been flagged as
unverified or contradicted and should not be treated as background facts.
```

The non-assumption statement is mandatory — without it, the model may
reintroduce the bias the scrubbing removed.

---

### Phase 5: Stability Validation

Delegate to `general-purpose` agent to stress-test the reconstructed prompt:

1. Generate 3–5 semantic paraphrases of the reconstructed prompt
2. Predict expected answer variance across paraphrases
3. Compute a **framing sensitivity score** (Low / Medium / High)
   - Low: paraphrases should produce semantically equivalent answers
   - Medium: paraphrases may surface different aspects but same conclusion
   - High: paraphrases likely produce materially different answers → iterate
4. If score is High, identify which remaining phrase is causing sensitivity
   and return to Phase 4

**Gate**: Only exit with Low or Medium sensitivity score.

---

### Phase 6: Final Report

Compile and return a structured purification report, then output the purified
prompt alone as the final element — clearly separated so the user can copy it
directly for use in an ensemble or follow-on query.

```markdown
## Plato Purification Report

### Original Prompt
[verbatim]

### Purified Prompt
[reconstructed, ready for ensemble]

### Removed Premises
| Premise | Type | Confidence | Reason Removed |
|---|---|---|---|

### Linguistic Changes
| Original | Neutralized | Pattern Type |
|---|---|---|

### Flagged (Retained with Caveat)
| Item | Why Flagged | How Noted in Prompt |
|---|---|---|

### Framing Sensitivity Score
[Low / Medium / High] — [explanation]

### Residual Risks
Items that survive scrubbing and require human judgment:
- Circular verification: [any premises only verifiable by the target model]
- Unknown unknowns: [context gaps neither party can detect]
- Reference class ambiguity: [terms whose meaning shifts with population]
- True-but-selective: [factually correct framing chosen to bias conclusion]

---

## Purified Prompt

> [purified prompt only, verbatim, ready to copy]
```

---

## Usage

```bash
# Scrub a leading technical question
/plato "Why has microservices architecture consistently outperformed monoliths for large-scale systems?"

# Scrub a false-premise question
/plato "Given that React is the industry standard, which state management approach should we adopt?"

# Scrub a presupposition trap
/plato "How long has technical debt been slowing down our team?"

# Scrub a full context block before sending to an ensemble
/plato "Our competitor just launched X. Given that we're already behind, what is the fastest way to ship Y?"

# Pipe output directly into ensemble evaluation
/plato "[prompt]"   # → use purified prompt with /orchestrate or multi-agent setup
```

---

## The Allegory

Plato's prisoners in the cave mistake shadows for reality because they have no
other reference point. The shadows are not wrong in themselves — they are
projections of real objects. But they are incomplete, distorted by angle and
distance, and the prisoners have no way to know this without leaving the cave.

A biased prompt is the same: not always false, but always a projection.
Plato's job is to walk the prompt out of the cave and ask what the object
actually looks like in daylight.

---

## Integration with Ensemble Pipelines

```
/plato "[prompt]"         →  Purified prompt + report
                                      ↓
/orchestrate              →  Multi-agent ensemble over purified prompt
                                      ↓
Disagreement analysis     →  Identify residual correlated error vectors
```

The purified prompt reduces correlated framing bias across ensemble agents.
It does not eliminate correlated training-data bias — that requires
post-hoc disagreement analysis and error vector classification.
