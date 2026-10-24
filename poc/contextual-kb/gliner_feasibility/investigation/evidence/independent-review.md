# Independent review

Review instance: 2 of 3

## Preliminary observations (recorded before FINDINGS.md and AUTHOR-EXPLANATION.md)

Reviewed bootstrap, repository/POC guidance, PLAN.md, PHASE1-ANALYSIS.md, both configs, controls, tests, runners, raw native outputs and summary. Scope is the untracked investigation directory on main at c3091328f49d53de6b41a49c4fe5aa8f1c45e516, amid extensive unrelated dirty state. No implementation-history context or author explanation was supplied to this reviewer.

- Raw rows support 87 phase-one and 36 phase-two observations; all variants are applied across the same 12 development cases. Controls are separate diagnostics.
- E9 improves exact API-slot extraction to four of eight designated names, with three generic nonmatches and resetOnHide misclassified as an error message. This is not full question planning, and no intent gold is available.
- E8 splits D02 actions into records but loses their subjects; D08 loses context. E7 adds nested fragments without restoring missing aspects or links.
- Span-validation tests pass (4 tests). They test evidence retention/fidelity, not schema assembly or semantic quality.
- Need to verify frozen hashes and independently recompute summary fields. Summary/decoder artifacts do not have a retained generator in the explicit investigation boundary, making replication less convenient.
- Need to distinguish a demonstrated decoder mechanism from proof of the model's full internal candidate set.

## Findings

No actionable correctness blocker remains for accepting this bounded research investigation. The preliminary reproducibility concern was resolved during review: the author added `analyze.py` and `check_decoder.py`; both were inspected and executed successfully. These reporting helpers were added after the experimental freezes, and do not change the frozen inference code, configuration or results.

This does not establish readiness to implement a complete planner or begin the full A comparison. Missing requested aspects, polarity/context attachment and justified clarification remain substantive candidate limitations, accurately reported rather than hidden harness defects.

## Plan Review

The retained evidence follows the declared 7×12 + 3 diagnostic controls, then 3×12 adaptive-development design. E7–E9 target issues discussed in PHASE1-ANALYSIS.md. Phase manifests cover the actual inference runners/configurations and model files; current bytes match. E0 reproduces the original native results. No full comparison or training was performed by this reviewer, and the reviewed runners do not execute retrieval, DB or a plan adapter.

The eight API targets are consistent with the original development rubric after excluding literal values. This is exposed-development, exact typed-slot coverage, not a pre-frozen independent accuracy measure. E9 changes several factors together, so isolating the causal benefit of label brevity, descriptions or task composition is unsupported. The findings explicitly acknowledge this. Natural records also change mode, anchor dtype and cardinality together; claims are properly limited to that combined intervention.

Tests cover new recursive span validation, retained erroneous native output and no-retry behavior. Four new tests and eight previous tests pass. They do not establish semantic extraction correctness or exhaustively test schema assembly; installed-library source inspection and retained outputs provide the evidence for those narrow wiring claims. Retained red evidence is an absent-module import failure, not a demonstrated failing assertion against an earlier implementation.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| 123 calls, no backend/span-validation errors | Both raw JSONL files, runtime metadata; independently revalidated spans | Confirmed for retained observations; not an independent execution audit proving absence of unrecorded calls |
| E0 reproduces previous output | Original raw JSONL and E0 rows | Confirmed; helper checks repeat 0 and reviewer independently checked native equality |
| E9 obtains 4/8 API hits, three generic nonmatches | Original development rubric, E9 raw rows, summary and analyze.py | Confirmed. Additional resetOnHide→error_message error remains visible; other-label occurrences are not incorrectly credited |
| Natural anchored records split D02 but lose subjects/context | E5/E8 D02 and D08 raw output | Confirmed; record count is not complete decomposition |
| Relation decoding works on controls, custom context links unreliable | C01–C03 and E3 raw output | Confirmed within diagnostic scope; controls do not qualify unseen relations |
| Flat decoding can explain fragmentation | Pinned model config architecture=boundary and overlap_policy=flat; installed boundary/engine.py `_resolve_spans`; overlap.py `resolve_overlaps`; both replay files | Confirmed sufficient mechanism. It is not proof of the complete latent candidate set or universal causality |
| Schema/API wiring forwards intended configuration | experiment.py `schema_for`; phase2.py `targeted_schema`; installed schema.py builders/auto-finish, runtime.py extraction forwarding and classification threshold handling | Confirmed by static source. E9 entity threshold is .5; multi-label intent threshold is .3. E8 natural/action/required_one metadata is stored by the builder |
| Protected and frozen content unchanged | Four manifests and independent SHA-256 recomputation | Confirmed: 60 protected, 17 previous, 11 phase1 and 9 phase2 entries, zero mismatches |
| Training is a future possibility | Recommendation text and absence of training in reviewed runners | Correctly presented as unproven and outside the completed work; no readiness evidence for that proposal |

## Verification Performed

From investigation, executed `PYTHONDONTWRITEBYTECODE=1 ../env/.venv/bin/python -m unittest test_experiment`: 4 passed. From its parent, executed `PYTHONDONTWRITEBYTECODE=1 env/.venv/bin/python -m unittest discover -s tests`: 8 passed.

Independently recomputed retained row totals, unique case coverage, error counts, source-span occurrence counts, medians, requires_context/refers_to counts, ambiguity lists, exact API hits/nonmatches and denominator. All agreed with summary.json. Independently replayed both decoder artifacts using the installed standalone overlap resolver and verified current hashes against all four manifests.

Inspected and executed `PYTHONDONTWRITEBYTECODE=1 ../env/.venv/bin/python analyze.py` and `PYTHONDONTWRITEBYTECODE=1 ../env/.venv/bin/python check_decoder.py`: both passed. The latter emits an existing macOS torch redirect warning while importing the library; no extractor was instantiated or model inference performed.

Read development cases only. Protected bytes were hashed without displaying their contents. No held-out contents, model inference, network, DB connection or compiler execution occurred. Only this report was written by the reviewer. An initial reviewer aggregation snippet had a syntax error before executing; the corrected recomputation passed. Some source-location lookups failed before the actual installed files were located; these were inspection failures, not model samples.

## Open Questions And Residual Risks

Twelve reused development cases cannot establish generalization. No independent intent gold exists, no complete retrieval plan is assembled, and no performance comparison is justified by unpaired timings without warmup. Source-span fidelity does not recover missing polarity or contextual relationships. Loader/audit-hook/signal limitations remain as documented. Historical manifest consistency establishes present byte identity, not cryptographic proof of when a file was created or whether any external activity occurred.

The updated analysis helpers are post-experiment verification tools, not preregistration. They use assertions and should run without Python optimization flags. Full training feasibility, data sufficiency and evaluation design remain unverified.

## Verdict

**Ready** for accepting the completed development investigation and its limited findings. **Not ready to build/promote a complete GLiNER2 question planner or start the full A comparison.** The latter is a boundary on what this evidence supports, not a request to repair the experiment until a model succeeds.

## Recommended Next Actions

Preserve these outputs as research evidence and communicate the narrow improvements alongside the failures. Obtain a separate scope decision before training, additional model experiments, planner integration or full comparison. If adaptation is chosen, define independently annotated requested-aspect/context/negation/ambiguity criteria and fresh evaluation cases before execution. This review does not authorize that work or another review instance.
