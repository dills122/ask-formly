# Independent review — GLiNER2 development feasibility

Review instance: 1 of 3.

## Preliminary observations (recorded before author findings/explanation)

- Scope reconstructed from neutral bootstrap, root/POC instructions, STEERING and PLAN. Branch main, HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516; broad pre-existing dirty/untracked tree, including untracked POC. Review boundary is gliner_feasibility only; this report is the sole reviewer edit.
- Eight unit tests pass. All 60 protected-file hashes and all 13 probe-freeze hashes match. Hash-only reads included locked file bytes; no held-out contents, A/B raw outputs, DB connections, compiler calls, model runs or network used.
- Raw JSONL contains precisely 12 development questions in each of three ordered passes, no errors, 81 validated span occurrences; native outputs are identical across repeats. Independent span validation and question matching pass.
- D01 emits no requested outcome; D02 emits register a renderer plus configure (missing object); D10 emits answer only. No relation emitted in any case. These fail the explicit multi-ask gates. D09 is incorrectly clear; D12 is ambiguous. D01/D05/D07 are false ambiguity classifications.
- Exact substring validation proves copying for returned spans, not recall or semantic correctness. All identifier arrays are empty. D03 loses without from its negative constraint.
- Installed Schema.entities/relations/classification explicitly support the supplied dictionaries of descriptions. Loader dispatch honors the boundary architecture. Further check of runtime description forwarding remains pending.
- Median extraction plus validation is 0.1963716245 seconds; range 0.1849368750–0.2506217080. These are development probe observations, not complete planner or comparative timing.
- Preliminary conclusion: negative feasibility on this fixed configuration is supported; no basis for a full comparison. No demonstrated harness defect yet. Author rationale has not been read at this point.

## Findings

No actionable correctness defect found in the bounded probe or its negative feasibility assessment. No API/schema wiring defect was found that would invalidate that assessment. The following are confirmed feasibility failures, not newly introduced harness bugs:

1. **Multi-ask prerequisites fail.** `evidence/raw.jsonl:1`, `:2`, and `:10` show D01 with zero outcomes, D02 with incomplete `configure`, and D10 with only `answer`. Both relation arrays are empty throughout all 36 rows. Against `PLAN.md:13`, none of D01/D02/D10 passes. Building faithful plans would require additional semantic inference; joining nearby spans mechanically would not demonstrate the requested capability. Smallest appropriate action: retain the stop at extraction, with no adapter/comparison.
2. **Ambiguity prerequisites fail.** `evidence/raw.jsonl:9` calls D09 clear; `:12` correctly calls D12 ambiguous without explaining the referent. D01/D05/D07 are false positives. Precision 1/4 and recall 1/2 agree with the rubric. Smallest appropriate action: preserve this limitation in the conclusion; do not represent classification output as reliable planner abstention.
3. **Copy fidelity is narrower than semantic preservation.** `evidence/raw.jsonl:3` labels `removing its control` a negative constraint while dropping `without`; no case emits an identifier. All 81 returned occurrences are exact substrings, but exact copying neither detects missing spans nor makes the semantic labels correct. FINDINGS already states this distinction accurately.

These failures block a full comparison under the agreed gates. They do not block accepting a negative feasibility result.

## Plan Review

The implementation follows the bounded plan: isolated pinned environment, development fixture path plus byte hash, fixed schema, three passes, untouched native results, source-span validation and a complete 12-case assessment. There is no plan adapter, imported project runtime, retrieval execution, or semantic repair. The current code and manifest show the prior implementation/environment and locked DB bytes unchanged.

The plan's unchecked execution boxes (`PLAN.md:6–11`) remain its frozen pre-run state; PROGRESS and this report supply completion evidence. Avoid changing the frozen plan merely to make its checklist current.

The manifest was corrected after launch (`FINDINGS.md:50`, PROGRESS); this is a disclosed deviation from ideal prospective provenance. Current hashes establish current file identity against that manifest, not independent proof of the exact code at every historical instant. Retaining this disclosed development run is appropriate; it must not become a claim of a prospectively sealed benchmark. No additional run is warranted for the present stop decision.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Consequence |
| --- | --- | --- | --- |
| 36 successful calls, 81 valid occurrences, identical native repeats | Entire raw JSONL; independent fixture/order/span checks | Confirmed | Reliable retained observations for this fixed configuration |
| Six outcomes over five cases; zero identifiers, unresolved references and links | Native entity/relation arrays and summary reconstruction | Confirmed | Sparse extraction cannot be treated as complete plans |
| Multi-ask and ambiguity gates fail | Raw D01/D02/D09/D10/D12 and development rubric | Confirmed | Stop before full comparison |
| Schema calls use the public installed API | Installed `inference/schema.py:291,343,469`; `inference/runtime.py:244,374,1609`; `processor.py:1112,1162,1212,1295` | Confirmed | Descriptions are accepted and forwarded, including inference-mode label descriptions |
| Boundary checkpoint supports relations | Local config architecture boundary, enable_relations true; `auto.py:105`; boundary engine relation decoding at `:967`; boundary model strict state loading at `:2224` | Confirmed statically | No disabled relation head or wrong architecture dispatch found |
| 60 protected entries and 13 probe/model inputs unchanged | Recomputed SHA-256 for both manifests | Confirmed against retained manifests | Supports unchanged A/data boundary; not retrospective proof of all filesystem activity |
| Package versions and timing aggregates | Installed distribution metadata, runtime, all row durations and summary | Confirmed | Median 196.4 ms, nearest-rank p95 205.9 ms, max 250.6 ms are probe-only timing |
| 10.62-second load and 193,581,591 parameters | Runtime and runner's measurement code | Recorded, not independently rerun | No model was instantiated by reviewer; do not treat as fresh replication |
| No schema tuning after outputs; no historical held-out/network/DB activity | Code, retained hashes, author disclosure and logs | Consistent, not independently provable historically | Limited assurance only; current reviewer did none of these activities |
| TDD retained two red stages then eight green tests | Four retained test logs plus current tests | Confirmed as retained logs | Harness tests do not prove semantic extraction quality |

## Verification Performed

- Ran `PYTHONDONTWRITEBYTECODE=1 env/.venv/bin/python -m unittest discover -s tests` from this directory: eight tests passed. The host login shell emitted a startup parse-error message before unittest; unittest itself exited successfully.
- Used inline, read-only Python checks to recompute all 60 protected hashes and 13 probe-freeze hashes: zero mismatches. Only byte hashing was performed on protected source/DB files.
- Parsed all 36 JSONL rows; verified exact D01–D12 order across repeats 0–2, question equality to the development fixture, no errors, recorded span counts, exact span offsets, and identical native results across all three passes.
- Rebuilt every per-case summary field, total errors/occurrences and median/nearest-rank p95/max: exact matches. Verified recorded package versions against installed distribution metadata.
- Read the installed GLiNER2 2.1.0 schema, runtime, processor, loader and boundary relation implementation. `Schema` descriptions survive normalization and reach processor prompts; relation names with descriptions are mapped back to requested names. Boundary state loading is strict by default. Model-type warnings therefore do not by themselves demonstrate a silently random or mismatched head; no such defect was found.
- Inspected all 12 first-pass outputs against the supplied development rubric; repeats were byte-equivalent as JSON values. Author findings/explanation were read only after the preliminary ledger above was written.
- Did not run `run.py`, model inference, network requests, compiler/DB tests, A/B comparisons, or access held-out fixture contents. This report is the only reviewer-created/modified file.

## Open Questions And Residual Risks

This tests one checkpoint, schema, threshold and exposed development set. It cannot establish that other GLiNER2 configurations, training, or extractive approaches fail. Repeats test consistency here, not statistical generalization. The audit hook is a limited Python defense installed after loading; it is not an OS sandbox. Tests cover the guard function and span mechanics but do not independently replay inference under an enforced sandbox. The post-launch freeze and uncommitted working tree limit historical provenance. These limitations are disclosed and do not reverse the negative gate results.

## Verdict

**Ready** — to accept the bounded feasibility findings and stop this flow. The evidence supports the conclusion that this fixed configuration has not demonstrated the prerequisites for a faithful planner.

**A full comparison is not ready and must not start.** This is not a ranking against A, a production-readiness verdict, or a universal rejection of GLiNER2. No heavy implementation pivot is required to finish the authorized task; the correct completion is the reviewed stop decision.

## Recommended Next Actions

Return the reviewed negative finding to the user, keeping A and the locked data/DB unchanged. Retain the raw evidence and frozen inputs as-is. Any schema tuning, supervised examples/training, alternate checkpoint, or architecture work is a separately proposed follow-up; none is authorized by this review. No new review instance or model run is needed to close this bounded task.
