# Repair replay review

Review instance: 1 of 3. Scope: the working-tree repair_replay implementation,
protocol, tests, counterexamples and saved outputs against repair_design. This
directory is untracked within a much larger dirty working tree; this is not a
commit-range review. Only this report was written. No implementation, gold,
prediction, DB, A/v2 or sealed-evaluation artifact was changed.

Independence limit: this reviewer received a scoped handoff containing the
author's headline results before inspection, so a blind first pass was impossible.
It did not inherit the implementation conversation. Counterexample authorship
independence is documented by COUNTEREXAMPLES.md and its frozen read-scope receipt;
file hashes establish content identity, not an independently provable chronology
of what an author saw.

## Findings

1. **P2 — Supported paths fail at ordinary sentence punctuation.**
   `repairs.py:63-66` treats every following period without an identifier as
   unsupported syntax and discards the candidate. Frozen CX-PA-S is
   `Inspect widgetMap['pane'].height.`: the expected complete API is omitted,
   `needs_review` is returned, and the bracket key survives as a standalone value.
   This is a real failure of the promised supported-path case, not a disagreement
   requiring gold revision. A future separately frozen experiment should specify
   punctuation termination and test both prose periods and genuinely incomplete
   member expressions. Do not fix this scored implementation in place.

2. **P2 — API completion accepts a root starting inside another identifier.**
   `repair` checks the preceding character only against `._$` before accepting
   a completed path; `path_end` starts IDENT matching at the supplied candidate
   offset. A review-only probe with text `otherwidgetMap.height` and an API
   prediction for `widgetMap` delivers `widgetMap.height` with status `ok`.
   The resulting span is not a standalone source root. This expands incorrect
   evidence into an asserted path. A future parser needs a complete root-token
   boundary check and prefix/suffix candidate tests. This probe is additional
   review evidence, not a retroactive addition to the frozen 12-case score.

3. **P2 — Duplicate merging mutates earlier event provenance.**
   `repairs.py:156` stores the live `node['ids']` list in an event; the later
   deduplication step extends that same list. In saved CX-UA-S, the first quote
   event has before-kind `model_key` but IDs `[2, 3]`, although prediction 3
   began as `value` and has its own quote and role events. The events therefore
   do not faithfully identify which predictions underwent that particular
   transformation. Envelope scores are unaffected. A future version should
   snapshot event IDs and separately retain merged provenance, with a regression
   asserting historical events remain unchanged after deduplication.

## Plan Review

The experiment implements four cumulative stages over all 48 saved raw rows,
source-preserving boundaries, local role resolution, conflict omission, and
diagnostic retention. It performs no inference or semantic lookup. Stage 0 uses
the hardened adapter; stages 1–3 also change conflict delivery, so the first delta
cannot be attributed solely to quotes. PROTOCOL.md discloses this correctly.

Quote expansion requires an entire literal interior; explicit local bindings
operate per occurrence; established literal ownership suppresses payload tags;
API ownership suppresses interior components. These restrictions are materially
present in code and covered by small tests and counterexamples. A structurally
valid single wrong label remains possible, as explicitly documented.

The acceptance plan is not met. Both supported and unsafe counterexamples were
required to pass, and already-correct occurrences were not to be reduced. The
full described candidate loses 14 raw correct spans (including API/value spans)
through unresolved conflicts and passes only 11/12 counterexamples. Bare full
repair loses 7 and introduces one new wrong delivered/accepted span. Overall
and per-role accepted precision/recall remain below the qualification gate.
Tests are useful but do not establish every advertised boundary: sentence
punctuation, root-token boundaries and immutable event provenance are gaps.

## Author-Claim Reconciliation

| Claim | Evidence and assessment |
| --- | --- |
| 17 tests pass | Confirmed by independent `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/repair_replay -p 'test_*.py'`. |
| All 48 predictions replayed through four stages | Confirmed: recomputed all 192 results and compared envelopes, logs, raw mentions and duplicate counts to saved replay.json. |
| Described full repair: 52 TP / 4 FP / 38 FN | Confirmed for diagnostic retained mentions only: precision 92.9%, recall 57.8%, F1 71.2%. |
| Described accepted full repair | Confirmed: 32 TP / 4 FP / 58 FN, precision 88.9%, recall 35.6%, F1 50.8%; 13 ok and 11 needs_review, 4/24 exact envelopes. |
| No newly wrong full described spans | Confirmed under the saved raw-relative delivered and baseline-relative accepted comparisons; does not mean no harm, no residual wrong spans, or general safety. Four wrong spans remain and 14 raw correct spans are lost. |
| Boundary/path recovery improves | Confirmed diagnostically: described full recovery is 18/21 quoted spans and 7/8 compound APIs; bare is 14/21 and 1/8. These are not accepted-output success rates. |
| Independent counterexamples 11/12 | Confirmed saved failure is CX-PA-S; hand-authored candidates measure repair behavior, not model generalization. |
| Frozen evidence preserved | Implementation and pilot final-freeze hashes checked successfully. Saved integrity.json reports no changes across its protected manifests; this reviewer did not reread the excluded DB/A/v2 corpus to independently repeat that broader audit. |

## Verification Performed

The 17 unit tests passed without bytecode writes. A read-only Python check verified
implementation-freeze.json and the pilot final-freeze.json, reconstructed all 192
outputs in memory, and independently recomputed every stage's core diagnostic and
accepted per-role metrics, exact counts, statuses and question totals against the
saved scores. No replay writer was invoked and no saved output was overwritten.
The implementation freeze also covers the independent suite, its documentation
and freeze receipt. Review-only candidate probes demonstrated the root-boundary
finding. Static inspection confirmed the provenance alias against saved CX-UA-S.

## Open Questions And Residual Risks

The 24 pilot questions are exposed development evidence. Neither this replay nor
the 12 artificial counterexamples supports a claim of generalization. Hashes
support reproducibility of current content; they cannot alone prove historical
freeze ordering. The saved integrity receipt is evidence of the coordinator's
broader check, not an independently repeated audit here. The lexical parser is
deliberately bounded and does not implement semantic ambiguity detection.

## Verdict

**Not ready. Reject this candidate under the proposed retention gate.** Retain
the frozen experiment as diagnostic evidence. Its 71.2% diagnostic F1 is not
production extraction quality; accepted F1 is 50.8%, and exact delivery is 4/24.
The experiment gives useful evidence that boundaries and local bindings can
recover spans, while conflict handling and missing model evidence remain major
limits. Passing 17 unit tests does not override the failed counterexample or
retention criteria.

## Recommended Next Actions

Preserve this failed run without tuning its extractor, gold or counterexamples.
Stop expanding repair rules in this experiment. Retain the strict validator and
frozen evidence, not this repair pipeline as an accepted extractor. The full
described accepted API recall is 9/37 and value recall is 2/13; improving boundary
serialization alone cannot establish adequate extraction.

The most directly motivated next proposal is a narrowly scoped six-role supervised
feasibility trial on a separately frozen development split, with new independent
evaluation examples. Its question should be whether direct span/role supervision
reduces missing roots and conflicting labels enough to avoid growing lexical
exceptions. This is a hypothesis, not evidence that training will work. An
agent-based narrow-span comparator is also reasonable if the immediate decision
is which extraction approach to adopt, but this replay contains no measurements
of its quality, cost or latency and cannot establish its superiority. Do not start
either new workstream under this review. Any approved follow-up must retain the
same exact-envelope and diagnostic-versus-accepted scoring, independently frozen
counterexamples, and explicit accounting of harmful changes. The parser and
provenance defects above remain recorded constraints if this code is ever reused.
Training, production integration and sealed evaluation are not approved by this
review.
