# Annotation pilot adjudication, before model predictions

Both independent annotators identified 31 aspects and the same two ambiguous
questions (P17/P19). Initial v1 count and ambiguity agreement: 24/24 each.
Exact role/span/attachment micro-F1 was 0.801603; the initial .90 gate failed.
General clarification rules were written and both annotators reapplied them to
all questions without reading each other's labels or model predictions.

V2 count and ambiguity agreement remains 24/24; exact span/attachment F1 is
0.981053 (233 matching features; 239 author, 236 independent). This is raw v2
agreement, not an adjudicated agreement score. Feature definition and per-case
counts are retained in evidence/agreement*.json. Aspect order matches here;
index-based matching is pilot-specific, not a future arbitrary-order scorer.

Three residual disagreements resolved using the clarified guide:

- P04: contiguous `explain registration` is one cue span. Other request keeps
  shared `explain` and separate `removal`. Both records still anchor `the wrapper`.
- P06: author's substring lookup selected `it` inside `without` rather than the
  standalone pronoun. Source equality validation cannot catch this semantic
  annotation error. Use the independent explicit occurrence at [39,41).
- P24: `For the same field` is topical framing, not a condition under v2. Keep
  both asks and their distinct exact API occurrences; do not invent ambiguity.

adjudicated.json uses author v2 labels except those three rows, where the
independent v2 annotation is accepted. All raw versions and builder scripts are
retained. Neither annotator used Formly facts or model outputs. This is a small
agent-annotated training pilot, not human-reviewed deployment gold.

## Additional transport-check correction

The real tokenizer/processor check exposed a shared annotation error in P20:
both annotators' substring helpers selected `disable` inside `props.disabled`
rather than the standalone action after `Does`. The processor expanded that
partial-token span to `disabled`. This is an annotation defect, not evidence that
valid explicit spans are corrupted. Preserve the first adjudicated file/freeze
and failed run. `adjudicated-v2.json` corrects only that cue occurrence; the v2
freeze includes both original and corrected gold. No model predictions or
optimization informed this correction. Agreement numbers remain the raw numbers
above, not recomputed to disguise the common error.
