# Structured caller repair candidate

Preserve model_free_v1, installed93-fact knowledge, models and sealed evaluation.
Reuse its retrieval, validator and scope behavior; add only a new tool-result adapter
and caller recovery instructions. No model execution inside MCP. Codex is the external
caller authorized by user, not a server dependency.

Contract: first valid plan retrieves normally. Missing plan returns PLAN_REQUIRED
as normal needs_refinement result. Invalid declared conditions/indexes/source excerpts
or contradictory scope return needs_refinement with issue code/path and isError=true.
Unsupported coverage returns unsupported_scope and stop action; no hits return
no_evidence, never proof of nonexistence. Unexpected storage/runtime errors remain
execution failures, never requests to weaken a plan. Typed schema failures still use
SDK validation errors; custom structured feedback covers semantically shaped plans.

All tool calls complete; no server callback, sampling, elicitation, provider request
or workflow state. Caller may make at most two repairs, preserve original request,
never drop requirements to pass, and stop identical submissions/unsupported scope.
This budget is caller policy, not a stateless server enforcement guarantee.

TDD: feedback paths, successful correction, source-grounding/index rejection, scope
conflict/unsupported distinction, no-evidence, backend-integrity error distinction;
real stdio confirms structured/text/isError parity under offline guards. Then freeze
five live scenarios before running: missing condition, missing plan, scope conflict,
unsupported version, and valid one-call path. First defective calls are deliberately
seeded; no answers/repair recipes exposed. Inspect real tool feedback/revised plans
and full returned evidence, not just final prose. At most three lookups per scenario.
No claim of spontaneous error frequency or universal harness compliance.

Review as next increment of model-free architecture: instance2of3 (instance1 reviewed
model_free_v1). No promotion, commit, push or modification to earlier frozen files.
