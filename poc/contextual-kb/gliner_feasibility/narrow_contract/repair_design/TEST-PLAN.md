# Proposed repair evaluation

No tests or comparisons have been executed for this proposal.

## Fixed replay and ablations

Freeze repair code, grammar, rule order and test expectations before scored replay.
Use the pilot's original 24 questions, both sets of 24 raw predictions, unchanged
90-span gold and status annotations. Verify all source hashes. No model calls
needed for the first comparison; the input model is held exactly constant.

For each bare/described set report four cumulative variants:
1. Hardened adapter alone (reproduce frozen baseline).
2. Quote-boundary repair only.
3. Quotes plus whole-API-path completion.
4. Quotes/path completion plus local role and ownership handling.

Also count per-operation repairs, correct repairs, harmful repairs, suppressions,
unresolved conflicts and duplicates. Keep raw predictions and baseline scores
unchanged. Do not select only cases the repair can handle.

## TDD before scored replay

Use small fixtures with new names rather than original case strings:
- Exact literal-interior match expands; partial substring does not.
- Odd/even escape parity; empty string; Unicode before span; differing quote types.
- Ordinary apostrophe, unclosed literal, code backticks and unsupported quoting.
- Adjacent balanced dot/bracket path completes; separate paths do not join.
- Computed expressions/calls/unbalanced brackets do not receive guessed repairs.
- Quotes inside API paths do not become standalone values.
- Identical text at two positions retains independent roles and offsets.
- type/key/defaultValue assignments including colon/equals forms and exclusions.
- "custom type" prose, suffix/prefix property lookalikes and quoted instruction
  payloads cannot trigger a binding.
- Explicit local syntax can resolve a conflict; no supported syntax means review.
- An established literal payload suppresses internal false tags while preserving
  a same-spelled key outside the payload.
- A single uncertain label with no detectable conflict is not claimed resolved.
- Missing/malformed outputs stay errors; all original evidence is retained.
- Every transformation preserves exact source substrings, is idempotent, and
  cannot introduce overlapping accepted spans.
- Permuting raw prediction order does not change the delivered envelope or
  semantic repair decisions; provenance IDs may differ.
- Lowering or raising confidences alone does not select a different role.

Use two test levels: hand-authored raw candidates to prove deterministic rules,
and the real saved GLiNER predictions to measure actual extraction improvement.
Passing artificial fixtures does not establish real-model success.

## Counterexamples for safety and limited generalization

Before final replay, have an independent reviewer author/freeze 12 new minimal
counterexamples, two for each of: quote ownership, escape/boundary behavior,
path adjacency, assignment versus prose, same text/different role, unresolved
ambiguity. Pair a supported repair with a superficially similar unsafe case.
Use independently labeled source and candidate outputs; keep this suite out of
rule tuning until frozen execution. These test the repair algorithm, not GLiNER
generalization. If later real inference on them is desired, declare it separately.

Original 24 remain exposed development cases. Do not call them held out.
Old sealed evaluation cases remain untouched.

## Metrics and acceptance

Reproduce raw and accepted typed-span metrics, per role, per family and per origin.
Count repaired correct spans and newly introduced wrong spans separately.
For needs_review, score retained nonconflicting mentions diagnostically, but never
count it as a fully usable successful envelope or omit the question from recall.
Report the two existing ambiguity cases separately. Keep statuses and issue
regions under exact envelope tests, including the canonical D06 boundary.

Report:
- Whole-path and quoted-name/key/value exact recovery.
- Raw duplicate counts, conflict rate and residual structurally invalid outputs.
- Exact successful envelopes, clear-empty false positives, review/error rates.
- Per-parent unique atoms so repetition cannot inflate the result.
- Total preprocessing/repair/validation time separately from stored inference;
  no reusing old timings as if repair were free.
- Differences for every gained/lost span and every rejected region.

A repair candidate is worth retaining only if it improves exact recovery without
introducing any new wrong accepted span, corrupting string/number/boolean identity,
or reducing already-correct API/name/key/value occurrences on this bounded suite.
Both supported and unsafe counterexamples must behave as specified. Zero observed
harm on 24+12 cases is not a universal safety guarantee.

Overall extraction qualification still requires the existing >=90% precision and
recall per nonempty role and overall, full structural validity and critical
fixtures. Honest needs_review can be preferable to incorrect output while still
failing complete-extraction qualification. Report that distinction.

No relaxed quote scoring, removal of difficult cases, rewritten gold or comparison
of old five-label scores with the new contract. If the candidate fails, preserve
the failures and explain whether the issue is a bad repair or missing/incorrect
model evidence. Independent code and result review comes before more training.

## Scope

All new work would go in a new POC experiment directory, using the existing
hardened entry point where appropriate. This proposal leaves frozen pilot code,
v2, A, data/DB and all downstream layers unchanged. No application inspection,
fact lookup, training or production integration.
