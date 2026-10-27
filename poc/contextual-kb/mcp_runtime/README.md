# Formly MCP: choose a runtime mode

Both modes are retained. The new entry point defaults to **model-free**. Choose
**model-backed** explicitly when local models and additional hosted inference are
permitted. There is no automatic switch between modes and no cross-mode fallback.
Both consume the same pinned 192-fact, Formly 6.3.12 core/Material DB without rebuilding it.

| | Model-free (default) | Model-backed (opt-in) |
|---|---|---|
|Planning|Calling agent supplies a structured plan|Server's hosted planner derives the plan|
|Extraction/retrieval|Weighted lexical/exact-symbol lookup; no model inference|Frozen advisory GLiNER and lexical/dense retrieval|
|Selection|Calling agent assesses facts, discovers candidates and fetches citations|Existing hosted bounded selector refines the packet|
|Tools|lookup_formly, discover_formly_candidates, get_formly_facts|Existing lookup_formly plus get/set project settings|
|Server prerequisites|Pinned DB/source and MCP Python environment|DB, frozen models/embedding cache, worker environment, authenticated Codex CLI/provider access|
|Inference inside MCP|None|Local model inference and hosted planner/selector calls|
|Final explanation|Calling agent|Calling agent|

Model-free describes the **server**, not an AI-free workflow: Kiro, Claude, Codex or
another capable caller still supplies reasoning under its own policies. The native
Codex connection was exercised; other harness compatibility remains to be verified.
Model-backed still makes its internal Codex CLI/provider calls even when a different
agent invokes it. Neither mode automatically obtains new knowledge or resolves
missing release coverage. Exact 6.3.12 coverage does not prove 6.3.11, 6.4 or 7 compatibility.

## Commands

From a provisioned repository root, use the existing server environment:

```sh
# Model-free default: no GLiNER worker, model cache, Codex executable or login needed.
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_runtime/launcher.py doctor
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_runtime/launcher.py serve

# Explicit model-backed option; retains existing model-backed requirements.
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_runtime/launcher.py doctor --mode model-backed
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_runtime/launcher.py serve --mode model-backed --seed 1701
```

`--mode model-free` is also accepted. `--seed 1701` or `1702` is valid only in
model-backed mode; neither seed is a separate quality tier. `serve` waits for a
stdio MCP client, not an interactive prompt. `doctor` checks local prerequisites;
it does not test the caller, provider authentication/quota or answer quality.
The old `mcp_foundation/launcher.py` remains an unchanged model-backed entry point.

This is still a provisioned POC, not a clean-machine installer. Do not download,
retrain, rebuild or edit manifests merely to bypass missing or mismatched assets.
The model-free pin set includes its frozen source dependencies and DB, not model
assets. Runtime files default to separate `mcp_runtime/test-output/<mode>/` paths.
`--runtime-dir` overrides that destination. Model-free stores project settings there;
model-backed retains its existing settings policy and cache locations. Do not use
the same runtime directory for both modes. `--audit-dir` opts into full lookup-packet
logging; discovery/fetch calls are not covered by that inherited lookup audit.

## Client configuration

Use absolute command/script paths appropriate to your checkout. See
[codex.example.toml](codex.example.toml) for separate server names and an explicitly
disabled model-backed entry, and [generic.example.json](generic.example.json) for
command/args to translate to another harness. These files are examples, not live
client configuration. Do not enable model-backed use at work unless its local and
hosted inference are permitted. No approval settings are overridden.

The two lookup contracts are deliberately different:

- Model-free: `lookup_formly(request, plan, formly_version?, ui_adapter?, project_id?, worktree_id?)`.
  Read [caller protocol](../model_free_repair_v1/CALLER.md). Missing/invalid plans
  return repair feedback; the caller fixes its own plan, preserving the original
  request. Returned facts are candidates, not certified answers.
- For incomplete evidence, `discover_formly_candidates` repeats the exact original
  request, plan and resolved scope; use `next_offset` for another bounded page only
  if needed. Select relevant candidates, then `get_formly_facts` with the same scope
  to obtain full citations. Do not cite discovery summaries alone as full evidence.
- Model-backed: `lookup_formly(request, formly_version?, ui_adapter?, project_id?, worktree_id?)`.
  The server owns its existing planner/extractor/selector stages. See its
  [detailed setup, internal fallbacks and recovery](../mcp_foundation/README.md).

Requests and candidate evidence go to the model-backed hosted planner/selector and
consume provider usage. Model-free does not initiate those calls; its invoking agent
may itself be hosted. Enabling two server names retains both choices but does not
make their schemas interchangeable. Prefer one clearly selected mode per workflow.

## Evidence and limits

The [paired checkpoint](../discovery_qualification_v1/RESULTS.md) found 30/30 supported
covered answers and 6/6 safe controls, with disclosed shared-context limitations.
The [native pilot](../native_discovery_pilot_v1/RESULTS.md) then exercised all three
tools through the app-native connection. These are bounded results, not broad
parity, performance superiority or production readiness. The model-backed evidence
on the same ten covered questions was sufficient too; it is retained as a supported
option, not classified as a failed experiment.

The wrapper reuses frozen implementations in their existing POC paths to avoid
changing measured behavior. No code was imported from retired experiments outside
this POC. Data preparation/transpilation/seeding stays the same for both modes.

Future reviewed knowledge promotions must update and verify both runtime manifests against the same admitted DB. Never change pins merely to suppress a mismatch.

## Material input and textarea knowledge promotion

Both manifests now pin the same 192-fact/36-document DB; runtime implementations and models are unchanged. See [promotion and recovery](https://github.com/dills122/ask-formly/blob/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion/promotion-v13/README.md). Restart existing servers. Local experimental entries pointing directly to model_free_repair_v1/serve.py or parity_v1/serve_discovery.py retain old 93-fact pins: reconnect through this stable launcher instead. No local client configuration is changed automatically.
