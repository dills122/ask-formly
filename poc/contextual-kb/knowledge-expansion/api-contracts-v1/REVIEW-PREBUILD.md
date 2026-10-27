# Independent prebuild review

Review instance: 1 of 3

## Preliminary ledger (before AUTHOR)

Scope: untracked api-contracts-v1 batch on codex/n1-radio-native-promotion, HEAD 250f83da2d93aababf27f169078807ff66f183ee. Other dirty and untracked work excluded. Read-only except this report. This reviewer received the neutral task summary and expected count/test claims; no implementation conversation or author rationale was inherited.

- Four facts agree with inspected pinned source: FieldType forwards accessors and allocates an unassigned props fallback; initial snapshot uses clone(model ?? field.model); wrapper lookup has one argument and throws for missing names; absent marked presets skip assignment, while literal type resolution remains distinct.
- All eight retained upstream files match source-verification SHA-256 values. No network re-fetch was performed by this reviewer.
- Case obligations cover the declared 24/8/8 cohort without weakening explicit null/undefined/falsy arguments or missing-registry conditions. Grading permits supported composition and requires full obligations.
- candidate.build requires a freeze and fresh canonical output directories, reads the baseline read-only, and compares all eight canonical tables. Existing installed data is checked through preservation hashes. Actual build remains intentionally unexecuted.
- report.main invokes assessment seal verification before preservation/database checks or scoring. Inventory plus content hashes reject changed, extra, or missing scored artifacts. This is a local integrity seal, not an externally authenticated signature.
- Forty batch unit tests passed independently. Their scope does not establish runtime answer quality or a candidate build result.
- Pending before verdict: finalized adjudication, AUTHOR reconciliation, execution-freeze inventory. The lack of a build-time freeze at this preparation stage is expected; do not run build before it exists.

Graph coverage: generation 2026-10-25T14:19:41Z has no batch symbols and the inspected Python paths are not_tracked. Conclusions use direct source reads, not graph completeness.

## Findings

No actionable findings in the bounded prebuild target. Finalized source and adjudication artifacts were reviewed after the initiating task confirmed readiness. K150 is reused from the existing baseline catalog, with its exact getWrapper implementation/signature in lines 189–200; extra-evidence.json is empty.

## Plan Review

The plan orders source mapping and prospective criteria before freezing/building, then real stdio comparison, independent caller grading, sealing, recomputation and final review. This is appropriate for the four-contract admission. The combined 22/24 target gate, eight preservation cases, eight controls, baseline-supported-loss prohibition and critical-claim gate agree with report.summarize. Repeat equality is explicitly checked and described as fixed-plan reproducibility. Recovery audits preserve requests, scope, observed-ID provenance and per-case budgets. No promotion is included.

The final adjudication has exactly the same 40 ordered IDs as cases.json. Target expectations preserve accessor identity/fallback, explicit argument selection, wrapper arity and preset-versus-renderer distinctions. CONTROL-03 correctly allows a bounded core explanation while refusing to equate it with Bootstrap rendering qualification. Source IDs in adjudication are verification references, not permission to supply oracle IDs to callers.

## Author-Claim Reconciliation

| Author claim | Evidence inspected | Status | Review consequence |
| --- | --- | --- | --- |
| Four new exact-release contracts, 188 to 192 facts | Draft four-fact document; admission-spec; candidate count guard; pinned upstream source | Confirmed as source/build specification | Actual 192/36 output remains to be measured |
| Existing evidence reused, including K150 | Baseline catalog K150 record; extra-evidence.json; draft citations | Confirmed | No extra catalog record needed |
| Forty fresh cases retain explicit conditions | cases.json, lookup-calls.json, GRADING.md, adjudication.json and preparation hashes | Confirmed for content/alignment | Independent preparation history is author testimony, not independently reconstructable |
| Mandatory assessment seal before final report | report.verify_assessment_seal and main; five seal tests | Confirmed | Future report must pass this check after all answers/calls are sealed |
| Baseline and protected assets preserved | candidate.preserved and accepted_inputs executed read-only | Confirmed | 326 file hashes, installed DB and accepted baseline inputs/DB match |
| Forty unit tests pass | Independent unittest discovery | Confirmed | Does not qualify future MCP packets or candidate output |
| TDD red phases and parent maintenance passed | Author packet | Unverified by this reviewer | No historical red-phase/full-maintenance claim is used as review evidence |

## Verification Performed

- `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/api-contracts-v1 -p 'test*.py'`: 40 tests passed.
- Read-only Python checks: all eight upstream file SHA-256 values match source-verification.json; CASE-PREPARATION hashes match cases.json, lookup-calls.json and GRADING.md; cases/adjudication IDs agree in order.
- `candidate.preserved()` and `candidate.accepted_inputs()` invoked read-only: 326 protected files and installed DB verified; baseline authored/catalog inventory, input hashes, database hash and 188/35 counts verified.
- Git HEAD and branch match bootstrap. Dirty/untracked boundary inspected; no other work reviewed or changed.
- Graph coverage checked for reviewed batch Python/source paths. All are not_tracked; direct reads supplied source evidence instead.

## Open Questions And Residual Risks

This is prebuild readiness only. No candidate build, live MCP run, full maintenance command, Angular execution, hosted inference or global sealed archive was run/opened by this reviewer. The final execution freeze must include source/adjudication, cases/plans/grading and runner code before build; runtime wiring requires its own freeze before calls. Mutable local hash manifests detect drift relative to their retained bytes, not malicious replacement of both manifest and content. Final answer quality still requires independent packet-based grading and the planned final review. Repeated packets do not expand the semantic sample size.

## Verdict

Ready — for the planned input freeze and isolated build/qualification sequence. This is not qualification of a candidate database, runtime answer quality, the installed database, or promotion.

## Recommended Next Actions

Freeze the finalized inputs and code, build only the new isolated candidate, retain all calls/failures, independently grade actual delivered evidence, seal complete assessment/transport artifacts, and run the mandatory report validation. Return final results for the planned independent final review within the existing three-instance cap.
