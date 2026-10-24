# Independent narrow pilot review

Review instance: 1 of 3. Reviewed 2026-10-22. Scope is the working-tree
`narrow_contract/pilot/` against `CONTRACT.md` and `TEST-PLAN.md`; this is not
a review of the repository's numerous unrelated dirty/untracked changes.
Only this report was written. No training, database operation, application
investigation, sealed evaluation read, or production edit was performed.
Review used the code-review-and-quality and independent-review guidance.
The reviewer received a bounded task description rather than implementation
conversation history. The implementation and tests were inspected before the
retained score summary. Annotation rationale and adjudication were available,
so this is an independent audit, not a third blind annotation exercise.

## Findings

**P2, addressed for future callers — Malformed top-level results can escape error conversion.** In
`contract.py:adapt`, both the initial guard and the exception handler evaluate
`'error' in row`. Passing an integer or boolean reaches the handler and raises
another TypeError, rather than returning `extraction_error`. Independently
reproduced with `adapt('q', 'false', 42)` and `True`. TEST-PLAN section 2 requires
malformed results to become scored zero-recall failures. Validate the row type
before membership checks and add a regression covering scalar malformed rows.
The 48 retained predictions are dictionaries, so this does not change this
pilot's scores. During review the author added `hardened.py`, which checks for
non-dictionary rows before delegating to the frozen adapter. Independently read
that implementation and its three tests: scalar/list/string inputs now return
error envelopes and lose recall, and all 48 retained predictions have exactly
the same adaptation and scoring results. The frozen historical runner/scorer
still imports `contract.py`; future callers must explicitly use `hardened.py`.
This is a verified separate fix, not a retroactive alteration of frozen evidence.

No finding invalidates the retained comparison. Neither candidate passes the
qualification gate; this is a measured negative result, not a hidden failure.

## Plan review

Selection contains exactly 24 questions, four in each of six families, with 18
saved v2 strings and six clearly marked developer diagnostics. Independently
matched every saved question and parent ID against `focused_v2/inputs.json`.
Required H01, H13, H16 and R04 are present. Selection and inference freeze hashes
currently match their referenced files. Timestamp order and retained red/green
logs support the stated workflow, but cannot independently prove historical
annotator isolation or prove when files were first frozen.

Both annotations and gold are identical: 90 exact typed occurrences over 24
envelopes. All gold envelopes validate. The reviewer checked the complete
mention lists against the source questions. H19's wrapper/category nouns,
R05's generic type noun, H13's repeated default literals, H14's complete quoted
instruction-as-data, D03's escaped apostrophe and negative scope mentions are
consistent with the occurrence contract. Neither API existence nor active
scope is inferred.

D05 correctly omits the explicitly unresolved registration/model-key mention
and marks that quoted region `role_ambiguous`. D06 retains `props.label`, omits
the incomplete value and marks its opening quote through question end
`boundary_ambiguous`. D06 is **not** an empty-gold question. The scorer's
`needs_review_gold` includes both cases; its ambiguous-empty subgroup contains
only D05. The D06 issue extent is a reasonable pilot adjudication, but the
general contract still needs a canonical boundary rule before broader labels.

The inference code uses unchanged question strings, a pinned local base model,
threshold 0.5, nested overlap policy and alternating schema order. Inspection
of the imported loader confirms CPU float32, four threads and seed 1701.
No trainer or prior adapter is invoked. Both actual schemas and all 48 raw
predictions are retained. No boundary repair or semantic filtering is applied.
The flat schema cannot emit review statuses; the protocol explicitly discloses
this limitation and both ambiguous cases fail exact/status scoring.

## Author-claim reconciliation

| Claim | Review evidence | Status |
| --- | --- | --- |
| 18 saved strings plus six diagnostics | Exact source equality, origin/family counts | Confirmed |
| 24/24 agreement, 90 spans | Full annotation/gold equality and source-span validation | Confirmed; agent agreement only |
| Invalid overlaps remain failures | Adapter plus overlap tests; raw/accepted recomputation | Confirmed |
| Descriptions improve the extractor sufficiently | Not asserted by protocol; measured gate fails | Unsupported as a readiness claim |
| No changes to A/v2/data | Inspected code writes only pilot artifacts; integrity report lists no changed protected files | Supported by retained audit, not a new exhaustive filesystem audit |

The broad protected-file manifests were not rehashed by this reviewer because
their contents may include sealed material. The local selection/inference
manifests were independently verified. No absence-of-access claim can be proved
solely from an integrity hash report.

## Verification performed

Executed `python3 -B -m unittest discover -s
poc/contextual-kb/gliner_feasibility/narrow_contract/pilot -p 'test_*.py'`:
Initially 15 tests passed; after the separate hardening addition, reran the same
command and all 18 tests passed. Independently loaded predictions and called `evaluate` for each
arm, asserting complete equality with each retained `scores.json` report.
Independently validated all gold envelopes, annotation equality, both local
freeze manifests, source question identity and family/origin counts. Checked
that no raw prediction contains duplicate identical records. Reproduced the
malformed scalar failure above. No model rerun was necessary for scorer review.

| Measure | Bare | Described |
| --- | ---: | ---: |
| Raw TP / FP / FN | 23 / 36 / 67 | 43 / 66 / 47 |
| Raw precision / recall | 39.0% / 25.6% | 39.4% / 47.8% |
| Accepted TP / FP / FN | 12 / 16 / 78 | 9 / 11 / 81 |
| Accepted precision / recall | 42.9% / 13.3% | 45.0% / 10.0% |
| Structurally invalid questions | 6/24 | 16/24 |
| Exact questions | 2/24 | 1/24 |
| Whole compound API matches | 1/8 | 3/8 |
| Quoted name/key/value exact matches | 0/21 | 0/21 |
| Clear-empty questions with false positives | 1/2 | 2/2 |

Raw overlaps remain visible in precision and per-case records. Rejecting an
invalid output removes its accepted predictions and leaves every gold mention
as a false negative. Accepted precision alone would be misleading; the report
must always retain raw metrics and invalid counts beside it. Missing results
are penalized and empty success cannot pass a nonempty-gold question.

## Open questions and residual risks

- This tiny development selection does not establish generalization. Agent-agent
  agreement is not independent human annotation. Every nonempty role needs
  substantially better evidence before readiness; quote preservation and
  registration/key distinctions are particularly poor.
- Flat entity output cannot satisfy ambiguity status requirements. Entity-only
  training cannot be assumed to fix this; any later approach needs an explicit
  design and independently labeled status tests.
- The scorer uses sets, so identical duplicate predictions are structural
  failures but are collapsed in raw occurrence diagnostics. No retained output
  contains such duplicates. Preserve multiplicity or explicitly report duplicate
  counts if future experiments can emit them.
- The reported boundary diagnostic counts exact matches and misses, rather than
  distinguishing omission from a near-miss boundary. Raw per-case evidence must
  accompany any claim specifically attributing failure to boundary detection.
- The runner imports a loader through older training modules. The reviewed call
  path does not train or load old examples, but a standalone loader and a frozen
  loader/model fingerprint would make future experiment provenance easier to
  audit. Those imported implementation files are outside inference-freeze.json.
- Local timing includes validation, with model load retained separately. One
  alternating pass is not a stable performance benchmark.

## Verdict

**Ready with non-blocking follow-ups as a negative development experiment.**
The retained run is reproducible from its predictions and does not conceal the
candidate failures. **Neither extractor is ready**, and this review authorizes
no training or production integration. Use the verified hardened adapter
when reusing the harness and formalize ambiguity boundaries before expanding
annotation. Any further training requires its own approved scope, preserved
baseline, and independent evaluation design; old sealed evaluation stays sealed.

## Recommended next actions

Retain this run unchanged and publish its failed gate plainly. If another
experiment is authorized, target quote-inclusive spans, registration versus key
roles, complete API paths, and overlap conflicts rather than widening the task.
Keep ambiguity/status capability a separate explicit requirement and preserve
all six-role denominators and raw false positives.
