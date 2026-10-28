# ask-formly model-free alpha

This alpha gives a calling agent source-grounded evidence for **Formly 6.3.12 core/Material**: 192 facts in 36 documents. The agent plans questions, assesses evidence and answers; the server runs no models, providers or Codex CLI. It cannot inspect your application or guarantee whole-library coverage. Model-backed mode remains available separately in the development checkout and is not included here.

## Availability and prerequisites

Obtain the model-free alpha archive and matching `.sha256` from [GitHub Releases](https://github.com/dills122/ask-formly/releases), or build from a provisioned checkout using the instructions below. Use the named model-free asset, not GitHub’s generated source archive. Original project code is MIT-licensed; the archive includes `LICENSE` and `THIRD_PARTY_NOTICES.md`. A Git clone alone does not contain the installed DB. Do not run `install.py` directly from this source directory: the installer requires the built artifact and `ALPHA-MANIFEST.json` beside it.


Requires Python 3.11+ with venv/pip, internet access to PyPI for the initial dependency install, and an absolute **new** writable installation directory. Dependency versions are pinned; wheels must be available for your platform. The initial clean-install target is macOS arm64 with Python 3.14.6. Other platforms are not certified by these instructions.

## Install

In a terminal, enter the directory containing the supplied archive and checksum. Check `python3 --version`; use the Python executable you intend to install with. The tested interpreter was Python 3.14.6. Use the actual supplied filenames if they differ from this example:

```sh
shasum -a 256 -c ask-formly-alpha.tar.gz.sha256
mkdir ask-formly-unpack
tar -xzf ask-formly-alpha.tar.gz -C ask-formly-unpack
python3 ask-formly-unpack/ask-formly-alpha/install.py \
  --prefix /absolute/path/to/ask-formly-alpha-install
```

Stop if checksum verification fails. A checksum detects changes; it is not a publisher signature. Both the scratch directory and installation destination in this example should be new. Replace `/absolute/path/to/ask-formly-alpha-install` with your chosen absolute path, quoting it if it contains spaces. Do not point it at an existing checkout or installation.

The installer verifies package hashes, copies only listed files, creates an isolated `venv`, installs the pinned dependencies without using the pip cache, checks dependency compatibility, runs doctor, and verifies real MCP initialization, tool discovery and a read-only lookup. It never overwrites an existing installation. Dependency/network/doctor failures remove only the new installation it created; retry with a new or absent destination. The source archive and installed development DB are not modified.

The archive includes the existing DB byte-for-byte. Installation does not compile, seed or expand knowledge. No model assets, local environments, request logs, client credentials or sealed evaluation are packaged. There is no model download or fallback to model-backed mode.

## Connect and check

Successful installation exits with status zero, prints a configuration object and writes `mcp-config.json` inside the installation directory. It should report doctor `"ok": true` and:

```text
MCP initialization, tool catalog and read-only lookup passed; answer quality not assessed.
```

Create a **local stdio** MCP connection in your agent client using the generated `command` and `args`. For example, the generic JSON emitted by the installer is:

```json
{
  "mcpServers": {
    "ask-formly": {
      "command": "/absolute/path/to/ask-formly-alpha-install/venv/bin/python",
      "args": [
        "-I",
        "/absolute/path/to/ask-formly-alpha-install/ask_formly.py",
        "serve"
      ]
    }
  }
}
```

Use your generated paths, not the placeholders above. Each argument is a separate list item, so spaces inside a path do not require extra embedded quote characters. Keep `-I`; it isolates Python from ambient import paths. No API key, model file or server URL is required by this package. The calling agent still uses its own model configuration.

Clients use different JSON/TOML wrappers and configuration locations: map these command/argument values into your client's supported UI or format rather than assuming the `mcpServers` wrapper fits every client. No client configuration is changed automatically. Codex calling-agent tests have been performed; Claude/Kiro end-to-end compatibility remains unqualified.

Restart or reconnect the entry, then confirm these tools appear:

- `lookup_formly`
- `discover_formly_candidates`
- `get_formly_facts`

On macOS/Linux, commands are:

```sh
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py doctor
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py self-test
/absolute/path/to/ask-formly-alpha-install/venv/bin/python -I /absolute/path/to/ask-formly-alpha-install/ask_formly.py serve
```

Use the paths emitted in `mcp-config.json` on Windows. `serve` is a stdio server for your MCP client; it waits for protocol messages and is not an interactive chat command. The client should load the supplied server instructions. Ask your agent:

> Use ask-formly. For Formly 6.3.12 with Material, how can I hide a field while retaining its model value? Explain whether its control stays registered.

The agent supplies a plan to `lookup_formly`, repairs indicated omissions while preserving your request, and uses `discover_formly_candidates` / `get_formly_facts` for additional evidence where needed. Scope other than supported 6.3.12 core/Material must be disclosed, not silently substituted. See `runtime/model_free_repair_v1/CALLER.md` for the complete caller contract.

The first-request check should cite evidence and distinguish retained model value from control registration. Do not expect the MCP to inspect your form component or edit application code. If the client reports a structural error, its agent should repair the plan without changing the original request.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ALPHA-MANIFEST.json` missing | Run the installer from the extracted built archive, not the repository source directory. |
| Installation destination already exists | Choose a new path. Keep the prior installation for rollback. |
| Package download or wheel unavailable | Check PyPI/network access and the interpreter/platform. The tested target is macOS arm64/Python 3.14.6. Installation uses binary wheels only. |
| Missing package, hash mismatch or doctor failure | Retain the error, then reinstall the trusted artifact into a new directory. Do not edit integrity pins. |
| Process exits or client cannot connect | Run the generated Python command with `doctor`, then `self-test` instead of `serve`. Check absolute paths and client stderr. |
| `serve` appears to wait without a prompt | Expected: it waits for MCP protocol input from the client. Use `self-test` for a terminal check. |
| Tools are present but agent does not use them | Ask explicitly to use ask-formly; ensure the client loads server instructions and permits the tool calls. |
| `MISSING_SCOPE_METADATA` or `needs_refinement` | The calling agent must supply/repair scope or conditions while preserving the request. |
| `unsupported_scope` | Coverage is limited to Formly 6.3.12 core/Material. Disclose the gap; do not substitute a supported version. |
| `ok` but evidence does not answer the question | Inspect omitted candidates and fetch relevant records. If support remains missing, state that limitation. |

## Upgrade, rollback and uninstall

- Keep the install directory in place: moving a Python virtual environment is unsupported. Reinstall at a new path instead.
- Mutable project settings live under `state/`, separate from `runtime/build/knowledge.sqlite`. `--runtime-dir /another/writable/path` changes the settings location. The knowledge DB is opened read-only.
- Doctor reports missing dependencies or hash mismatches. Restore/reinstall the trusted artifact; do not edit pins to hide drift. Doctor checks prerequisites, not answer accuracy.
- On scope repair feedback, the calling agent must repair its plan; the server does not run another agent. Unsupported scope is a stop.
- Restart the MCP connection after installing a new version. For rollback, keep the previous installation and switch the client entry back. Do not overwrite its state during testing.
- To uninstall, remove the client entry and then your chosen installation directory. Settings in it are local user data; retain them if needed.

## Build from the provisioned repository

From a checkout already containing the pinned DB and source files, create an output directory and use a new archive filename:

```sh
python3 poc/contextual-kb/alpha/package.py \
  --output /absolute/path/to/output/ask-formly-alpha.tar.gz
```

The parent output directory must already exist. The builder writes the archive and `ask-formly-alpha.tar.gz.sha256`. Follow the same install steps above in a separate destination; do not test by replacing your working setup. The archive contains an exact DB copy; building it neither rebuilds nor reseeds the installed DB.

This requires the pinned installed DB and source files. A source-only clone lacks the DB; failure must not be reported as a working release. The builder refuses overwrite and copies only model-free manifest members plus the pinned version catalog, launcher, installer, entry point, startup check, lockfile and this guide. The model-backed recovery bundle is a separate artifact. This command builds locally; it does not upload or publish anything. Public distribution/licensing and release signing remain separate release decisions.
