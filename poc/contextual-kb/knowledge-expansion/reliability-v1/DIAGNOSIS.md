# Development diagnosis and preserved attempts

## Capitalization

The original Q20 ledger used lowercase `an internal Formly source file exports TypeOption`, while the request starts with `An`. The unchanged exact-source validator rejects it. The isolated adapter restores only an opening ordinary article's source capitalization, requires one source occurrence and exact remainder, changes only an existing copy in every explicitly bound question, and re-runs all accepted validation. It never adds a missing condition or changes API/literal spelling.

Nine initial tests produced the expected failure for saved-plan normalization and missing required-server configuration. After the first implementation they passed; additional negative/shared-condition/composed-rewrite tests bring the total to fourteen passing. The actual saved raw failed plan was replayed through real MCP for seeds1701 and1702: both returned the public-registration typing fact, preserved original-plan provenance and reported unchanged DB/model parameters.

## Availability: what the evidence does and does not establish

The historical missing-tool batch has no startup trace. Its exact cause remains unproven. Do not retroactively assign it to a timeout.

Official Codex documentation describes a separate optional-server initial-catalog grace period (default1000ms) and required-server initialization failure behavior: https://learn.chatgpt.com/docs/extend/mcp#other-configuration-options. Installed CLI is0.164.0-alpha.11.1.

Controlled disposable MCP probes revealed **caller behavior as well as a startup safety gap**:

- Original conditional probe instruction, optional delayed3s server: exited successfully but called no tool and said unavailable.
- Required startup alone, and required plus catalog waiting: also no tool calls, including a no-delay control. Thus those settings alone did not fix the probe.
- Instrumentation verified the client requested tools/list. The Python MCP SDK independently listed lookup_formly. A server-ready/tool-list handshake is not proof the model actually used the tool.
- Renaming the shorthand to the fully qualified tool name alone still failed the conditional probe at3s and8s delays.
- Explicit invocation/namespace guidance succeeded. A version permitting discovery succeeded without actually using another tool. The final bounded version requires invoking the actual exposed namespaced tool and does not permit other tools; it succeeded with3s,8s and20s startup delays under required+catalog-wait configuration.
- An injected required-server startup failure exited1 with no generated message or tool call. No retry or synthetic result was used.

Every attempt, including unsuccessful hypotheses, remains under test-output. Only real completed MCP events plus the fixture's lookup_called log establish successful availability. The fixture returns a marker, never Formly evidence, and is never part of the knowledge service.

## Candidate changes

The real caller now uses the explicit MCP tool identifier and namespace guidance, while retaining one exact request, one sequential tool call, no retries and the unchanged answer rubric/schema. The candidate caller also sets required=true and mcp_optional_startup_grace_ms=0 with finite60s startup/600s tool timeouts. These settings are defensive prerequisites, not claimed to be the sole historical cause or a guarantee of model compliance.

The opt-in server records startup milestones and stderr inside the new experiment, wraps the frozen planner with the capitalization adapter, and uses the original backend with the unchanged isolated56-fact DB. All data, models, accepted runtime modules and previous candidate artifacts remain unchanged. Live repeated regression is still required before any readiness claim.
