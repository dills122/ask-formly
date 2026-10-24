# Foundation + advisory GLiNER: working POC integration

The foundation, retained GLiNER extractor and unchanged full-question retrieval now run together through a reusable Python component and a local command. GLiNER is enabled by default. Its annotations are returned to the caller, but cannot rewrite/filter queries or influence ranking. This is functional integration acceptance, not a new extraction-accuracy or final-answer qualification.

## Executed behavior

The caller produces the foundation plan using unchanged qualification_v3/CONTRACT.md. The new CLI accepts original request + question_plan, validates it, runs GLiNER separately on each derived question, then sends only the complete search_requests to the existing hybrid engine through enhanced=False. It returns the authoritative plan, advisory hints/raw extractions/diagnostics, actual query logs and up to eight original candidate facts with conditions and limits. It does not generate final answers or investigate application code.

Both retained role_boundary_adaptation epoch6 adapters remain available, with described six-role labels, threshold0.5, native flat decoding, CPUfloat32 and four threads. Default1701 is an administrative choice, not a quality winner or ensemble;1702 is selectable with --seed1702. Both are tested equally.

## Actual native verification

36 saved realistic foundation plans and12 new first-generation requests produced48 inputs and70 derived questions. The two empty out-of-scope plans execute no extraction or search. All144 result records (foundation,seed1701,seed1702) were saved. Neither native model's outputs were repaired or used to modify queries.

| Check | Seed1701 | Seed1702 |
|---|---:|---:|
| Native question extractions |70|70|
| Core plan and full search projection unchanged |48/48|48/48|
| Actual query text/order/count and fact IDs unchanged |48/48|48/48|
| Complete returned fact records unchanged |48/48|48/48|
| Accepted advisory hints |73|71|
| Native extraction errors |0|0|
| Parameters matching original receipt and before/after |564/564|564/564|

Seed1702 produced two overlapping hints on one replay request; the existing validator rejected them with explicit warnings. Its full-question retrieval remained identical. No annotations are hard filters. Counts and structural acceptance do not establish correct semantic roles; the models' previously measured accuracy limitations remain.

The actual command was run with GLiNER enabled by default. For the example request it returned the quoted registration name 'tax-reference' and model key 'invoice.taxId', one unchanged full-question query and eight candidate facts. The final CLI after review fixes matches the original successful CLI's plan, annotations, IDs and full fact records. Its model integrity check and DB check pass.

## Failure handling and review fixes

31 tests cover query/result independence, condition preservation, lazy loading/reuse, no work for empty plans, malformed outputs, invalid offsets/roles/overlaps, semantically wrong but structurally valid hints, input validation, no-overwrite output, real subprocess transport, timeout/closure, worker failure through the CLI, verification failure, harness exception cleanup and typed model-integrity failures.

- Ordinary extractor loading/inference/transport failure returns a visible degraded advisory status while preserving successful full-question retrieval.
- If post-failure model verification is unavailable, it is explicitly unknown (parameters_unchanged:null), never claimed successful.
- A positively observed checkpoint/parameter mismatch is a typed hard integrity failure. It propagates across worker startup/verification, transport, lookup and CLI. Real retrieval/DB failures also propagate.
- Worker cleanup is guaranteed in CLI and verification-session finally blocks.

Review1 found that the final CLI verification could hide an otherwise successful degraded packet, plus a harness cleanup gap. Review2 caught that the first correction also softened observed integrity mismatches. Both sets of findings are addressed with retained RED→GREEN tests. Final review3 is recorded in REVIEW-3.md and its decision file. No review finding changed the model, extraction schema or retrieval design.

A real read-only DB test with an injected failing subprocess returned the same fact IDs as the successful native CLI, with explicit degraded/unknown-verification status. This is fault-injection evidence, not a native model quality result. Real-pipe tests separately prove observed integrity mismatch still fails hard. Successful native CLI smoke runs verify final packaging and transport; the full48-input native panel was not repeatedly resampled.

## Environment correction, preserved honestly

The first live attempt used the existing retrieval-only .venv and lacked torch. It returned explicit loader diagnostics and failed acceptance; no actual GLiNER prediction occurred. That original run and source snapshots remain in test-output/live and failed-environment-source.

The POC already has separate environments: retrieval .venv contains fastembed, while gliner_feasibility/env/.venv contains GLiNER/torch/peft. A persistent local JSON-lines worker now uses the latter, while retrieval uses the former. Neither environment was modified; no packages/model files were downloaded or trained. Successful native evidence is in test-output/live-native. This local process separation preserves the established dependencies and lets a reused lookup session pay model startup once.

The frozen old run/source manifests are retained; corrected source snapshots and separate ready-code/ready-cli freezes document each review fix. Historical manifests must be checked against their corresponding archived source versions, not misrepresented as matching the final edited source paths.

## Cost and limits

Across70 native calls per seed, extraction plus local transport took16.97 and16.69seconds (about242 and238ms per derived question). Cold worker/model startup measured14.40 and12.04seconds in the full-panel run, including imports and parameter identity checks. Full-question retrieval across48 requests took about0.51 and0.50seconds, with embedding/index setup separate. These are local observations, not service SLAs. A new one-shot CLI pays cold startup; reusable AdvisoryLookup/ProcessExtractor sessions retain the model.

The caller still supplies the foundation reasoning output. This component does not host an LLM or register an MCP server. Foundation and retrieval limitations remain, including previously observed semantic omissions in saved plans; preserving a plan does not certify it correct. No claim of90% annotation accuracy, improved retrieval relevance, complete answerability, final-answer correctness or production readiness follows from parity. Raw candidate facts are explicitly candidate_only.

All existing candidates, both models, DB and prior evidence remain unchanged. All48 inherited protection chains are verified using byte-only preservation; evaluation semantics remain sealed. New code and evidence are contained entirely in advisory_lookup_v1. No staging, commit, publishing, training or source-data edits occurred.

## Use now

From the repository root:

    poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/agent_contract/advisory_lookup_v1/cli.py --input poc/contextual-kb/agent_contract/advisory_lookup_v1/example-input.json

README.md documents the input/output contract, alternate adapter, diagnostic foundation-only switch and reuse lifecycle. This is the concrete POC path carrying the retained GLiNER work forward.
