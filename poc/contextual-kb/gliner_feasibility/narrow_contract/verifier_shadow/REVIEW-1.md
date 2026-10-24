# Independent review

Review instance: 1 of 3

## Preliminary ledger (before author explanation/rule/provenance)

The tests and both 30-question inventories were inspected first, against the six-role contract, verifier label contract and frozen training/calibration text. New cases have twelve contrast pairs (two in each requested category) and six controls. Existing development proposes six removals of type; training proposes six removals. Main unresolved issue: SDEV-013/015 omit key in explicit model-key context whereas VCAL-015/016/017/020 retain key in similar configuration contexts. Exhaustiveness must be reconciled under a consistent written rule. VCAL-018 label, VCAL-026 wrappers, and VCAL-002 model require contextual adjudication. Code shows operational scoring uses only emitted offsets; oracle scoring is separate; no repair is applied. Review binding currently requires only the two data files (extra provided bindings are checked). Unsupported correct spans are also counted as correct abstentions; detailed unsupported counts remain separate.

## Findings

No actionable blocking findings remain. The preliminary key concern resolves under the explicit, consistently applied distinction between the address concept `model key` and the configuration-member shorthand `key 'x'`. VCAL-018 discusses caption content rather than explicitly naming a member; VCAL-026 discusses wrapper components. VCAL-002 coordinates named members with options.formState. These decisions are defensible without consulting model output. I accept the six training and six development type corrections as separately versioned proposals; none authorizes editing training or reinterpreting the original 71-positive result.

## Plan Review

The new panel has 30 questions: 12 pairs, two in each of six requested families, plus two version, two ordinary, and two no-mention controls. I inspected every question and every gold and negative slice. It has 30 gold mentions, 12 semantic negatives and six malformed negatives. All 30 original questions and all original probe coordinates are retained; the adjudicated inventory has 65 gold and 36 negatives, including the six reclassified concept occurrences. The remaining original malformed probes are still fragments or merged mentions. The proposed overlay is source-bound and is not applied by run.py.

The 195-occurrence training audit is exactly exhaustive for whole words type/key/model/wrappers/expressions across 242 rows, including words nested in literals/paths. It is not a full training-inventory certification. Its categories total 59 retained positives, three retained exact-word negatives, six proposed supplied-occurrence negatives, 27 nested unsupervised fragments and 100 other unsupervised occurrences. The unsupervised bare key in rb-train-048 is openly disclosed, not silently treated as a negative. The bounded audit does not authorize further supervision.

The 149 total oracle probes in the two panels all survive native token alignment unchanged, including all 95 gold spans. No unsupported-gold preparation blocker exists. Transport qualification was collate-only with encode/_encode_core guarded to raise, using the existing pinned environment, load_model, schema and align. No model prediction, encoder forward, training, sealed content or historical evaluation content was used in this review.

## Author-Claim Reconciliation

| Claim | Evidence | Judgment |
| --- | --- | --- |
| Every emitted span is scored separately from supplied oracle probes | shadow.collect builds operational offsets only from tokens(raw), then performs a separate oracle loop | Confirmed; no repair path |
| Raw output remains unchanged | deepcopy plus tests for source/output equality | Confirmed |
| Fixed diagnostic thresholds | decision and summary use .5/.5; no threshold search in runner | Confirmed |
| 30 new questions, 12 pairs, six controls, exhaustive inventories | Both JSON panels and source slices inspected | Confirmed under written rule |
| Source preservation and pending author status | Hashes recomputed for all author artifact/source receipts; original text/order/probe coordinates compared | Confirmed |
| No normalized duplicates | Independently recomputed NFKC/casefold/whitespace comparisons against 272 old questions | Confirmed; conceptual overlap is explicitly disclosed |
| Completion follows preservation checks | run.main audits before work and guarded_run executes audits after work/failure before success | Confirmed by source review; full inference run intentionally not executed |

## Verification Performed

- `python3 -B -m unittest discover -s poc/contextual-kb/gliner_feasibility/narrow_contract/verifier_shadow -p 'test_*.py'`: 11 tests passed.
- Recomputed all author-receipt artifact/source SHA-256 bindings; all match.
- Recomputed the six harness-review-freeze bindings; all match.
- Verified overlay old targets and exact text against frozen supplied occurrences; all 12 match.
- Verified original 30 question strings, identity/order, and probe coordinates; unchanged.
- Recomputed the exact 195 whole-word audit-coordinate set; identical.
- Independently ran native collate/alignment: new panel 48/48 probes supported (30 gold); adjudicated original 101/101 supported (65 gold). No snapping, exclusions, encoder calls or predictions.
- Graph search found no target symbols; exact-path coverage reported all relevant Python files not tracked. Conclusions therefore use direct source reads, not an assumed complete graph. Large unrelated dirty state was excluded; the review boundary is the named shadow directory and necessary read-only dependencies.

## Open Questions And Residual Risks

These are exposed development diagnostics, not held-out generalization evidence. Full-model behavior, actual disagreements, operational transport coverage, real conflict frequency and latency remain unmeasured. Author statements about prior process are testimony; artifact consistency does not prove an unobservable absence of prior predictions. The review itself made none.

run.authorize requires the two panel bindings and verifies every additional binding supplied. The ready receipt produced here additionally binds the rule, overlays, audits, provenance, author receipt, explanation, generator, harness code/tests and freeze manifest, so those reviewed materials cannot drift for this approved run. Unsupported operational scores remain explicitly identified, although correct_abstentions includes unsupported cases; interpret the detailed reason and unsupported count together rather than calling those learned rejection. No claim of repair benefit follows from a ready preparation verdict.

## Verdict

Ready for the authorized no-training, development-only shadow diagnostic, using the hash-bound receipt. This approves preparation and diagnostic execution only, not training, a correction policy, serving adoption, or sealed evaluation.

## Recommended Next Actions

Run the frozen two-seed diagnostic through the supplied ready receipt, preserve original and adjudicated panels separately, and report every span score and all losses/disagreements without changing thresholds or labels in response to results.
