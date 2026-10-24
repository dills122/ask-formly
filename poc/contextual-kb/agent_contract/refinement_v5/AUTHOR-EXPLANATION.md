# Author explanation

## Intent and approach
v4 repaired the no-substitution exclusion, but dependent existence contingencies were still absent from the ledger and prior-hide context had ambiguous grading. v5 adds explicit eligibility-gate auditing, independent from exclusions, and distinguishes preceding history from the requested event outcome. Same-field sequence history may be included or represented by a return-transition alone; explicit after prerequisites remain mandatory; unrelated fields and local method restrictions must not leak.

candidate.py selects v5 CONTRACT.md while reusing unchanged same-POC v3 validation and advisory-hint projection. No schema change, detector, postprocessing, repair loop, training or production integration. LEDGER-RULES.md is inserted into the prior prompt; derivation and Output sections remain byte-identical except version heading. Prompt-diff-check records this and byte costs.

## Plan trace and verification
Seven entry-point/compatibility tests written before candidate implementation; initial missing-module failure retained then seven passes. Tests replay48 saved v4 structures and malformed-hint isolation, and explicitly demonstrate that an omitted undeclared condition still passes the validator. These are transport tests, not evidence of semantic fix. Frozen v4's own seven tests also pass. Prior source coverage lookup found not_tracked files; direct source verification was used, not graph completeness claims.

LEDGER-RULES and protocol precede fresh case authoring. Independent author saw only v2 scope and v5 policy, not full v5 prompt or old cases/outputs.12 fresh requests/rubrics include explicit mandatory/optional/forbidden context. Parent reviewed all before generation with no fresh-rubric changes. Four old cases are exposed diagnostics under explicitly new v5 rubrics; no prior data or grades changed.15 inputs frozen before output generation.

Six native fresh-context generation agents receive only full contract and8 requests, three repeats per batch,48 response slots. No gold rubrics/history/other outputs/validation feedback or selected retries. Internal source-first audit before returning is permitted by contract; no post-submission repair. Raw files frozen before grading. Existing POC stress summarize counts all scheduled slots, structure separately from independent semantic/binding grades; exact JSON equality separate from question meaning.

preserve.py extends the previous chain with v4 final-freeze47:32 prior manifests,38,295 entries (overlaps possible). Sealed/data/weight contents are only byte-hashed, never interpreted. All writes in new refinement_v5, no staging/commits. Dirty main has unrelated changes, excluded from this review.

## Limits and challenge points
Prompt-level improvement may still omit conditions or add unwanted context; there is no mechanical semantic guarantee. Review ALL outputs, especially independent support checks versus gated follow-ups, unless polarity, retracted/quoted restrictions, explicit prerequisites versus optional return history, and different-field leakage. Meaningful source excerpts can combine related constraints; examples are not unique acceptable boundaries. Equivalent optional history must not be mis-scored as regression under the old policy.

Synthetic development panel:12 fresh plus4 exposed diagnostics, correlated repeats, shared context inside each batch. Native inherited agent model has uncontrolled provider revision,temperature,seed; instruction packets are not a pinned production API or latency test. Role independence is context separation, not vendor diversity. File hashes prove preservation, not absence of unseen attempts. No contemporaneous v4 arm, causal comparison, final-answer/retrieval accuracy or sealed qualification claim. Gate failures must remain failures without replacement reviews or same-panel tuning.
