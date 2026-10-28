# Model-free alpha packaging checkpoint

Branch `codex/model-free-alpha`, based on merged main `dbf5125` (PR #16). This is a local alpha packaging and installation checkpoint, not a published public release.

## Artifact and installation

The corrected archive contains 25 payload files plus its integrity manifest: current model-free runtime dependencies, the unchanged 192-fact/36-document DB, pinned version catalog, launcher, installer, model-free-only entry point, real stdio health check, 30 exact dependency versions and setup instructions. The included legacy baseline-state file is frozen metadata required by the current runtime pin set; its historical entries are not an instruction to package those assets.

A clean Python virtual environment was created under a new installation path, using a clean home, isolated Python, no system-site packages and uncached dependency downloads from PyPI. Doctor, dependency checks, real MCP initialization, tool catalog and read-only lookup all passed. The real caller used the installed Python/server with an empty PATH and clean home, not the existing native development connection.

Tested platform: macOS arm64, Python 3.14.6, on the existing host. This is clean-environment evidence, not physical fresh-machine or Windows/Linux/Claude/Kiro qualification. Dependency wheels and network are needed during installation; serving performs no model/provider inference. Dependencies are version-pinned, not wheel-hash locked.

Artifact SHA256: `435df867058c3c3b914ed17009c51897807a41dfef98fe3ceb647a2ecf073584`. The local artifact is `poc/contextual-kb/test-output/alpha-packaging/ask-formly-alpha-r2.tar.gz`; this archive, extracted copies, environments and raw test output remain ignored and are not public Git assets.

## Failure discovered and corrected

The initial artifact passed doctor but failed real MCP initialization because the existing model-free manifest omitted `mcp_v1/versions.json`. Two caller startup failures were retained. The alpha builder now includes that exact file using its existing foundation hash, and installation requires real initialization and a read-only lookup before reporting success. No existing runtime implementation or installed manifest was changed. The corrected artifact was installed into another new environment; prior failures were not relabeled as passes.

## Real-agent smoke results

One fresh-context calling agent processed six requests through actual stdio MCP, with 12 case calls plus one tool-catalog call. No source, direct DB, old answers or development MCP connection supplied its answers. All three library tools were exercised. A deliberate null-scope plan was rejected and repaired without changing the request. Formly 7.0.0 correctly returned unsupported scope without substitution.

| Case | Observation |
| --- | --- |
| Custom native/Material field registration | Supported from initial delivered evidence. |
| Hidden value versus registered control | Scope repair worked; final answer required fetching relevant omitted facts. |
| Select label/value mapping | Supported, including distinction from object equality. |
| Array falsy initial value | Correct truthiness boundary and final-value caveat. |
| JSON Schema customization | Initial lookup and all 78 discovery candidates missed central customization facts. Answer became supported only after fetching IDs previously delivered during the first case. **Independent retrieval for this request did not pass.** |
| Unsupported Formly 7 | Correct stop and explicit coverage gap. |

All five final library explanations cited delivered evidence, but this is **not six independent successful request paths**. Four positive cases and the unsupported-scope control succeeded without cross-case evidence; the fifth positive exposes an existing retrieval limitation. No retrieval tuning, knowledge changes or reruns of completed cases were made to improve the result. Packaging/transport readiness is separate from answer-quality qualification.

## Tests, preservation and review

Ten asset-free package/installer tests passed and are wired into normal source checks. They cover exact copying, tamper/private-path/symlink rejection, no overwrite, failure cleanup, deterministic archives and the omitted version-catalog regression. Full `python3 tools/project.py check` passed, including both runtime doctors and the existing 155 active MCP regressions. The source-suite wiring expectation was updated for the additional alpha suite.

All 233 protected file hashes remained unchanged, including models, installed DB, both existing runtime pin sets and source knowledge. Sealed evaluation was not opened. DB copies match SHA256 `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.

Independent review (instance 1 of 3): **Ready with non-blocking follow-ups** for local alpha packaging. No blocking packaging defects were found. The reviewer independently passed all ten package tests and the installed doctor/self-test, verified archive checksum/payload hashes and inspected the actual caller evidence. The S5 independent retrieval failure and public distribution/platform limitations remain explicit. Raw review, clean-install logs, complete tool traces and answers remain under ignored `test-output/alpha-packaging/`.

## Remaining release boundaries

Public artifact publication, repository/knowledge redistribution licensing, release signing, other operating systems and other agent harnesses remain separate release work. No public artifact was uploaded. Existing model-backed usage remains unchanged and is not included in this alpha. The initial isolated JSON Schema limitation remains recorded above; the follow-up below tests a bounded recovery fix. This checkpoint does not replace the broader qualification or establish production accuracy.

## Follow-up: independent JSON Schema recovery

The S5 miss above was investigated separately before release. Knowledge was present: the original query used the combined `FormlyJsonschema.toFieldConfig` token, while the API evidence names class and method separately. Central customization records lacked the exact query wording. They were absent from the entire original 82-candidate list; discovery only paged its 78 omitted candidates and could not recover them.

The bounded model-free fix retains all existing route rankings and appends up to 16 scoped document-context candidates from up to four documents. An anchor must contain both case-sensitive components of a two-segment, uppercase-owner qualified API in its claim/context. The fix uses existing facts and document membership; it adds no API-specific mappings, model inference, DB writes or relevance certification. Unrelated context may be offered, and the calling agent must still assess it. The existing source pin for `model_free_v1/candidate.py` was refreshed in the model-free manifest; model-backed code is unchanged.

The exact original plan now exposes both central customization facts among four additional candidates. Its initial four delivered facts remain unchanged. Replay of discovery takes four pages under the existing 24 KB page budget; lookup + four pages + fetch stays within six calls. A fresh isolated agent using only the revised installed MCP instead selected the relevant IDs directly from lookup's omitted list and fetched them: **two case calls**, no prior-case IDs, no operational failures. Its answer explains `widget.formlyConfig`, `map` return semantics and ordering, with citations and renderer limitations. This repairs the independent recovery path; it does not claim improved initial-packet relevance or universal retrieval accuracy.

Six new fixture regressions cover known qualified APIs, unknown owners/lowercase properties, ranking prefixes, unchanged basic mode, the 16-fact/four-document bounds and version/adapter exclusion. All 168 saved broader-qualification lookup plans retained identical delivered fact packets in baseline/candidate comparison. Those are deterministic regression replays, not new independent answer generations. Full maintenance passed with 161 active MCP regressions; source-only CI now includes the new fixture suite.

The refreshed local artifact is `test-output/json-schema-retrieval-fix/ask-formly-alpha-r3.tar.gz`, SHA256 `9a565388eebec188f2119e808de384ad0a178c0f2d024a4ce14f5ddb010bbba9`. It passed another fresh-environment install, doctor and real stdio self-test before the isolated agent run. Earlier R2 artifacts/results remain unchanged as history. All 231 other protected file hashes, including models and installed DB, match; only the authorized retrieval file and its model-free manifest changed. Evaluation remained sealed.

Independent review of this follow-up (instance 1 of 3): **Ready**, no actionable defects. The reviewer independently verified preserved original candidate ordering, the four scoped additions, six fixture regressions and four source-wiring tests, installed/source retrieval hashes, and the isolated agent’s two-call recovery with complete citations. Initial-ranking and candidate-relevance limitations remain explicit. Raw regression comparisons, complete caller traces, install/check logs and preservation results remain ignored under `test-output/json-schema-retrieval-fix/`. No commit, push or public release was performed.
