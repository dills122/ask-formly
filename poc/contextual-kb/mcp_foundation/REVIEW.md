# Independent engineering review

Review instance: 1 of 3.

## Findings

No actionable correctness or usability defect found in the reviewed launcher, setup instructions, or observed local workflow. Review is limited to `mcp_foundation` and its unchanged factory/server integration at dirty main HEAD `c3091328f49d53de6b41a49c4fe5aa8f1c45e516`. The many unrelated working-tree changes were excluded. Preliminary observations were recorded in REVIEW-PRELIMINARY.md before reading AUTHOR-EXPLANATION.md. Source coverage checks reported POC files as not_tracked, so conclusions use direct source reads rather than graph completeness.

## Plan Review

The implementation follows the bounded wrapper plan: a stable stdio entry point, explicit doctor mode, streaming verification of 75 pinned assets, selected package checks in the two existing environments, executable worker and CLI presence checks, and copyable checkout-specific configuration. `start` delegates to the accepted wording factory and existing MCP server; it does not introduce another planner or retrieval policy. The separate SDK and calling-agent harnesses exercise the intended layers. Startup errors preserve protocol stdout, and local prerequisite success is clearly distinguished from provider availability.

The scope is appropriate for an existing local POC. Installation, universal portability, app inspection, concurrency qualification, and broader library coverage remain explicitly excluded. The changed out-of-scope case is recorded as an authorization adjustment made before execution, with pre/post harness freezes retained. It is not represented as semantic tuning or discarded generated output.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status / consequence |
| --- | --- | --- |
| Accepted component composition is retained | launcher.start, wording_candidate_v1/serve.py, mcp_v1/server.py, retrieval_repair_v1/integration.py | Confirmed by source and real packets |
| Doctor checks local prerequisites without provider access | launcher.preflight and independent doctor execution | Confirmed; no provider-health inference |
| Seven test cases pass after absent-module red state | test_launcher.py, retained red.txt and independent unittest execution | Confirmed; red state is import failure, not seven separately executed behavioral failures |
| Invalid request does not terminate server; restart works | sdk_check.py and two retained SDK initialize/tools/error/ping summaries | Confirmed by retained executed evidence, not independently rerun |
| Real planner/selector/extractor are used in two sessions | native events, receipts, audits, runtime model checks and audit.py | Confirmed; eight planner and six selector receipts exit zero |
| Packets reach the caller unchanged | independent exact structured-result comparison against server audit JSON | Confirmed, 8 of 8 |
| Existing assets are preserved | independent doctor hashes, old final-freeze verification, implementation freeze, author preservation audit | Confirmed within those recorded inventories |
| Missing knowledge and out-of-scope behavior remain explicit | Both final agent responses and raw packets | Confirmed for these two prompts; no general accuracy inference |

## Verification Performed

Executed `poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/mcp_foundation -p 'test_launcher.py' -v`: 7/7 pass. Executed the documented doctor command: exit 0, 75 matching files, expected server/worker package versions, and resolved Codex executable.

Independent read-only JSON/hash checks found no drift in the six-file implementation freeze or the old retrieval (659 files), wording (31 files), and hosted-check (125 files) freezes. These results are retained in review-preservation.json and review-evidence.json. No sealed evaluation content was interpreted.

Each native session completed four calls with no tool errors; each delivered packet exactly matched a server audit. Fourteen provider receipts exited zero. In both sessions the repeated supported question preserves the distinction between retained model value and control unregistration. The validator request is labeled unsupported by the returned evidence, and weather is labeled out of scope. Source facts and citations returned in those packets support the bounded answers; this review does not requalify the library itself. Runtime records show available advisory extraction, unchanged model parameters and unchanged DB. The author's audit additionally reconstructs retrieval/selection and confirms worker reuse within each session and separate workers across sessions.

Final RESULTS.md was inspected against the retained native evidence and audit. Its eight-call, six-selector, timing and bounded-coverage statements agree with the records. The retained configuration check confirms TOML/JSON launch equivalence and doctor success under the example PATH.

No new hosted generation, dependency installation, source modification, publication, or global configuration edit was performed by this review. Review artifacts are the only writes.

## Open Questions And Residual Risks

The manifest is change detection for recorded assets and selected versions, not a signed supply-chain attestation or complete environment lock. Doctor cannot prove authentication, native model loading or future provider availability. The unit seed test checks invocation of start rather than the factory itself; source inspection and the two real seed runs supply the complementary evidence. Retained SDK evidence was inspected rather than rerun. Missing-knowledge safety depends on the caller inspecting candidate facts; the validator query still returns unrelated candidates. That is documented existing behavior, not evidence coverage.

The two-session smoke test is deliberately small. It establishes local usability of the accepted sample and exercised boundaries, not held-out accuracy, all-client portability, speed guarantees or production readiness. Existing unrelated browser qualification remains outside scope and is not converted to a pass.

## Verdict

Ready for the bounded existing-checkout local stdio usage demonstrated here. This verdict does not authorize publication, global configuration changes, or broader quality claims.

## Recommended Next Actions

Use the documented doctor and client configuration for this preserved local checkout. Retain raw evidence and the explicit limits. Any installer, new knowledge coverage, model change or expanded operational guarantee needs separately scoped work and validation.
