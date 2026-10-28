# ask-formly model-free alpha

This alpha gives a calling agent source-grounded evidence for **Formly 6.3.12 core/Material**: 192 facts in 36 documents. The agent plans questions, assesses evidence and answers; the server runs no models, providers or Codex CLI. It cannot inspect your application or guarantee whole-library coverage. Model-backed mode remains available separately in the development checkout and is not included here.

## Install

Requires Python 3.11+ with venv/pip, internet access to PyPI for the initial dependency install, and an absolute **new** writable installation directory. Dependency versions are pinned; wheels must be available for your platform. The initial clean-install target is macOS arm64 with Python 3.14.6. Other platforms are not certified by these instructions.

1. Obtain the alpha archive and its `.sha256` from a trusted distributor. Verify the checksum, for example `shasum -a 256 -c ask-formly-alpha.tar.gz.sha256` on macOS. A checksum detects changes; it is not a publisher signature.
2. Extract into a new scratch directory: `tar -xzf ask-formly-alpha.tar.gz`.
3. Run `python3 ask-formly-alpha/install.py --prefix /absolute/path/to/ask-formly-alpha-install`.

The installer verifies package hashes, copies only listed files, creates an isolated `venv`, installs the pinned dependencies without using the pip cache, checks dependency compatibility, runs doctor, and verifies real MCP initialization, tool discovery and a read-only lookup. It never overwrites an existing installation. Dependency/network/doctor failures remove only the new installation it created; retry with a new or absent destination. The source archive and installed development DB are not modified.

The archive includes the existing DB byte-for-byte. Installation does not compile, seed or expand knowledge. No model assets, local environments, request logs, client credentials or sealed evaluation are packaged. There is no model download or fallback to model-backed mode.

## Connect and check

The installer writes `mcp-config.json` containing absolute `command` and `args`. Copy that server entry into your MCP client's configuration UI/file; no client configuration is changed automatically. Codex, Claude and Kiro have different configuration wrappers; the standard stdio command/arguments are the same, but only actually tested harnesses are qualified.

On macOS/Linux, commands are:

```sh
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py doctor
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py self-test
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py serve
```

Use the paths emitted in `mcp-config.json` on Windows. `serve` is a stdio server for your MCP client; it waits for protocol messages and is not an interactive chat command. The client should load the supplied server instructions. Ask your agent:

> Use ask-formly. For Formly 6.3.12 with Material, how can I hide a field while retaining its model value? Explain whether its control stays registered.

The agent supplies a plan to `lookup_formly`, repairs indicated omissions while preserving your request, and uses `discover_formly_candidates` / `get_formly_facts` for additional evidence where needed. Scope other than supported 6.3.12 core/Material must be disclosed, not silently substituted. See `runtime/model_free_repair_v1/CALLER.md` for the complete caller contract.

## Operation and recovery

- Keep the install directory in place: moving a Python virtual environment is unsupported. Reinstall at a new path instead.
- Mutable project settings live under `state/`, separate from `runtime/build/knowledge.sqlite`. `--runtime-dir /another/writable/path` changes the settings location. The knowledge DB is opened read-only.
- Doctor reports missing dependencies or hash mismatches. Restore/reinstall the trusted artifact; do not edit pins to hide drift. Doctor checks prerequisites, not answer accuracy.
- On scope repair feedback, the calling agent must repair its plan; the server does not run another agent. Unsupported scope is a stop.
- Restart the MCP connection after installing a new version. For rollback, keep the previous installation and switch the client entry back. Do not overwrite its state during testing.
- To uninstall, remove the client entry and then your chosen installation directory. Settings in it are local user data; retain them if needed.

## Build from the provisioned repository

`python3 poc/contextual-kb/alpha/package.py --output /absolute/path/to/new-ask-formly-alpha.tar.gz`

This requires the pinned installed DB and source files. A source-only clone lacks the DB; failure must not be reported as a working release. The builder refuses overwrite and copies only model-free manifest members plus the pinned version catalog, launcher, installer, entry point, startup check, lockfile and this guide. The model-backed recovery bundle is a separate artifact. This command builds locally; it does not upload or publish anything. Public distribution/licensing and release signing remain separate release decisions.
