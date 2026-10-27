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

Fresh-machine provisioning, remote hosting, production scale and unseen overall accuracy remain unqualified. Models, source knowledge and DB remain locked; sealed evaluation is not used by maintenance checks.

The earlier foundation8 installed the reviewed 93-fact Material select candidate. Canonical reproduction and all 15 installation smoke answers passed independent audit; see the [installation checkpoint](https://github.com/dills122/ask-formly/blob/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion/promotion-v7/RESULTS.md) for smoke and independent review status. The planner and models are unchanged. Candidate qualification results remain separate from installation checks.

Foundation9 added version-aware fact applicability and evidence-release tracking to the same 93 facts, with exact 6.3.12 coverage. Foundation10 preserves that runtime implementation and adds the JSON Schema knowledge; the new model-free wrapper changes who reasons about requests, not the knowledge scope. See the [version-aware promotion](../poc/contextual-kb/versioned_promotion_v1/RESULTS.md).

The earlier [JSON Schema promotion](https://github.com/dills122/ask-formly/blob/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion/promotion-v8/RESULTS.md) installed 99 facts/22 documents for both modes. Qualification reused 30 authored answers only after exact repeated evidence equality; it does not establish 90 independent generations. Existing experimental direct-entry connections must switch to the stable launcher before reconnecting to the newly pinned DB.

The current [promotion](../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md) installs 192 facts / 36 documents for both modes. The prior N1 checkpoint remains historical. Qualification remains bounded library-evidence delivery, not whole-library coverage or browser compatibility. Restart existing MCP processes after promotion so they load the new manifest/DB pins.
