# Readiness and limits

The accepted Formly library MCP is the primary project and is qualified for bounded local stdio use in the existing checkout. See [dual-mode setup](../poc/contextual-kb/mcp_runtime/README.md), [model-backed usability checks](../poc/contextual-kb/mcp_foundation/RESULTS.md), and [knowledge pipeline](knowledge-pipeline.md).

The new entry point defaults to model-free and retains an explicit model-backed mode.
Model-free uses caller-owned reasoning and no server model inference; model-backed
retains local GLiNER/embeddings and hosted Codex planning/selection. No automatic
fallback crosses that boundary. The [model-free qualification](../poc/contextual-kb/discovery_qualification_v1/RESULTS.md)
and [native pilot](../poc/contextual-kb/native_discovery_pilot_v1/RESULTS.md) document
bounded evidence, not broad parity or universal harness compatibility. Both modes
still require provisioned knowledge; only model-backed requires frozen model assets.

The 192-fact Formly 6.3.12 core/Material sample does not guarantee whole-library coverage or complete recipes. It does not inspect application components. Question understanding, advisory extraction, retrieval and caller answers have separate failure modes; reporting missing knowledge is required.

The older application-inspection product and competing knowledge-engine POCs are retired. Their failed gates and the two historical browser failures B06/B13 remain in the [history](history/experiments.md). They do not become passes through cleanup.

A [model-free alpha package](../poc/contextual-kb/alpha/README.md) now provides a fresh-venv installer, integrity checks and real stdio self-test. The [alpha checkpoint](../poc/contextual-kb/alpha/RESULTS.md) records clean-environment testing on the existing macOS host and its limitations. Physical fresh-machine provisioning, other platforms/harnesses, remote hosting, production scale and unseen overall accuracy remain unqualified. Models, source knowledge and DB remain locked; sealed evaluation is not used by maintenance checks.

Current knowledge is the [foundation15 checkpoint](../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md): 192 facts / 36 documents for both modes. Earlier admission counts and checks remain in [knowledge history](history/knowledge-expansion.md).

The [current status](current-status.md) separates the published discovery8 RC,
discovery16 source and isolated answer candidate. The latest comparison preserves
required answer support on four new question pairs with lower response bytes,
but callback inputs and some recovery inefficiency remain unresolved. No candidate
promotion or new release is implied. Full local maintenance is currently blocked
in this worktree by its missing compiler environment; passing source checks does
not remove that limitation.
