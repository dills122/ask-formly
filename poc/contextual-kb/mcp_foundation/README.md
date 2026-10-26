# Formly MCP — accepted local foundation

Use this directory as the stable entry point. It exposes `lookup_formly(request)` using the accepted planner, bounded wording adapter, frozen advisory GLiNER model, full-question retrieval and hosted bounded selection. It returns candidate facts and citations; the calling agent writes the final answer. Knowledge is the existing 93-fact Formly 6.3.12 core/Material sample, not the whole library.

Project/worktree settings and version arguments are described in the [settings guide](../../../docs/project-settings.md). The settings boundary is new; the historical qualification reports below describe the original runtime. Install the added `semantic-version==2.10.0` dependency in the MCP environment before running doctor.

## 1. Check this checkout

From repository root:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/mcp_foundation/launcher.py doctor
```

Expected: JSON with `ok: true`. This checks 95 recorded source/data/model/cache files, key package versions in both existing environments, and availability of `codex` on PATH. It does not log in, contact a provider, load the native model, read credentials, or prove model access/quota/network availability.

This checkpoint packages the **existing local POC**, not a standalone distribution. Keep the complete POC checkout, existing MCP environment, GLiNER environment, both adapters, base model, offline embedding cache and DB in place. `foundation.json` records component paths, hashes, selected package versions and the qualified CLI version. No command here installs packages, downloads models or rebuilds knowledge. A fresh machine without these artifacts is outside this checkpoint; do not recreate or overwrite frozen assets just to satisfy a check. Restore missing artifacts from their preserved source, or request a separate installation/portability task.

The qualified local CLI is `codex-cli 0.164.0-alpha.11.1`. The hosted planner/selector use `gpt-6-astra` with medium reasoning through the existing authenticated Codex CLI. The account must have access and usage available. Doctor checks CLI presence, not CLI version or authentication. Keep the CLI visible to the client environment; GUI PATH can differ from your terminal.

## 2. Connect a client

Server command:

```sh
/Users/dsteele/repos/ask-formly/poc/contextual-kb/mcp_v1/.venv/bin/python -B /Users/dsteele/repos/ask-formly/poc/contextual-kb/mcp_foundation/launcher.py serve
```

This starts a **stdio MCP server** and waits for a client. It is not an interactive question prompt. Use absolute paths in client configuration. The copyable `codex.example.toml` describes this checkout; merge the stanza into your intended client configuration only when you choose to enable it. We have not edited any client/global configuration.

Codex supports `[mcp_servers.<name>]`, `command`, `args`, `env`, `startup_timeout_sec` and `tool_timeout_sec`; see the [official MCP configuration documentation](https://developers.openai.com/codex/mcp). Its CLI, desktop and IDE clients share host configuration. Choose user versus trusted-project scope deliberately; do not overwrite unrelated entries. `generic.example.json` supplies the basic command/args for other clients, whose timeout settings differ.

The Codex example sets `required = true` and top-level `mcp_optional_startup_grace_ms = 0` so startup must succeed and the initial catalog is awaited. Merge the top-level setting at the TOML root, not inside another table. Settings alone do not force agent tool use: instruct the caller to invoke the exposed `mcp__formly__lookup_formly` tool (server `formly`, tool `lookup_formly`); the absence of an unqualified function is not unavailability. `CALLER.md` retains the tested calling protocol.

Allow 60 seconds for startup and 600 seconds per sequential tool call. The hosted planner and selector each have a 180-second process timeout; native setup and extraction also take time. Requests are serialized. Submit sequentially rather than queueing a large concurrent batch under the same timeout. Typical observed diagnostic calls were roughly 28–31 seconds cold and 10–17 seconds warm, but provider latency can vary. These are not service guarantees.

Defaults: seed 1701; `--seed 1702` selects the other frozen adapter. Neither is advertised as a separate quality tier. `--runtime-dir` defaults to this directory's `runtime/`; `--audit-dir` optionally records full tool packets. Keep test/runtime outputs within the POC. The frozen extractor retains its existing log/cache location under advisory_lookup_v1/test-output/runtime-cache. `--help` lists flags.

## 3. Ask through your agent

Example:

> Use the Formly MCP to explain what `resetOnHide: false` does to the model value and FormControl when a field is hidden. Cite the returned evidence and state any missing support.

The agent should forward the full request, including conditions and exclusions, to `lookup_formly`. It should inspect the facts and their conditions, cite relevant provenance, and distinguish supported information from missing evidence. No app inspection is provided. A validator implementation or a custom component's internals may be outside the current knowledge sample. Version coverage stays 6.3.12; the tool must not be presented as proof for all Formly releases.

Planner requests and selector candidate facts are sent to the configured hosted model and consume usage. Plans, model events and optional packet audits are stored locally. Use only requests you authorize for this service. Credentials remain in the existing CLI login, not in these files. Do not paste credentials into MCP config examples.

## Failures and recovery

| What you see | Meaning and next step |
| --- | --- |
| Doctor/startup says missing file or hash mismatch | An accepted artifact is absent or changed. Stop and restore/check the artifact; do not edit the manifest to suppress the error. Existing assets are locked. |
| Missing package / version mismatch | Use the specified MCP Python environment. The separate GLiNER environment must also match the recorded versions. Do not install into or upgrade frozen environments as a workaround. |
| `codex CLI not found` | Expose the installed CLI directory in the MCP process PATH; the example config includes this checkout's CLI location. |
| Doctor succeeds but lookup fails during planning | Local prerequisites passed; login, network, model access, quota or output validation may still fail. Inspect the returned error and local planner diagnostics. Fix the cause before retrying the request. |
| Request must be nonempty / too long | Supply a nonempty request up to 12,000 characters. The service remains alive after this input error. |
| `selection.status: fallback` | Optional hosted selection failed or was invalid; the original full-question packet remains. The caller should not claim the extra selection succeeded. |
| `advisory.status: degraded` | GLiNER was unavailable or some hints were rejected; full-question retrieval remains available with explicit diagnostics. This is different from an integrity mismatch. |
| Integrity error | Known model/DB drift is fatal for that server instance. Resolve the integrity issue, then restart; repeated calls do not clear it. |
| Unsupported or partial answer | The returned evidence does not cover everything. This is a knowledge limit, not necessarily a server failure. Do not invent the missing recipe. |

To restart, disconnect/reconnect the server through your MCP client. Graceful shutdown closes the index/extractor. Repeated requests reuse those resources inside one process; a fresh process loads them again. No automatic request retry or repair training is introduced.

## Verification and boundaries

See RESULTS.md and REVIEW.md for this checkpoint. Tests exercise startup/doctor, explicit errors, MCP discovery, input-error recovery, restart, repeated requests and real calling-agent behavior. Existing candidates/models/DB stay unchanged and sealed evaluation remains closed. This is local stdio qualification, not remote hosting, public packaging, concurrency scaling or a whole-library accuracy claim.

## Promoted foundation 8

The current installed foundation9 DB contains the same 93 facts across 21 documents in schema2. Canonical facts retain exact6.3.12 applicability and pinned evidence releases. The stable launcher now routes through the version-aware context/backend, including explicit core filtering. Planner, wording adapter, advisory GLiNER models and selector policy remain unchanged. See the [versioned promotion](../versioned_promotion_v1/RESULTS.md); earlier installation and qualification reports remain historical. Models and sealed evaluation are unchanged. Restart an existing server process after promotion; global client configuration is not edited.
