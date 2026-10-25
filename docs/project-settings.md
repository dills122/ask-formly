# Project settings and version requests

The MCP remembers a project's Formly version and UI adapter, with optional
worktree-specific settings. This adds a request-boundary coverage check; the
knowledge schema, compiler, DB, index and existing question/retrieval flow stay
unchanged. Multi-version knowledge storage and linking remain deferred; see the
[proposed DB/compiler implementation plan](versioned-knowledge-plan.md).

## Tool calls

Existing `lookup_formly(request)` calls still use the 6.3.12 baseline and forward
the request unchanged. New optional arguments are `project_id`, `worktree_id`,
`formly_version` and `ui_adapter`.

Pass this to `set_formly_project_settings` to save settings without a question:

```json
{"project_id":"/work/my-app","formly_version":"v6","ui_adapter":"material"}
```

Then call `lookup_formly`:

```json
{"request":"How do I preserve a hidden field's value?","project_id":"/work/my-app"}
```

`get_formly_project_settings(project_id, worktree_id?)` returns effective settings
and each field's source (project or worktree). Version/adapter arguments on a
lookup **save those fields** when `project_id` is present; this is an update,
not a temporary override. Without a project ID they apply only to that call.
Omitted fields retain saved values; missing worktree fields inherit project
values. Worktree IDs require a project ID. Use the same stable project ID across
its worktrees and a distinct worktree ID for each checkout; paths are sufficient.
No identifiers are inferred and branch switching is not detected.

Unsupported but valid versions/adapters can be saved, so subsequent calls report
missing coverage consistently. Invalid inputs are rejected before saving fields.
There is no agent identity, conversation tracking or expiry.

## Version matching

`semantic-version==2.10.0` supplies npm matching via `NpmSpec`. Accept a stable
major, minor or exact version. Trim whitespace and an optional lowercase `v`
without losing precision. Pick the highest matching stored release, or an
explicitly configured baseline for that same major if there is no match.

The current `mcp_v1/versions.json` contains **only 6.3.12, with no major fallback**:

| Request | Result |
| --- | --- |
| No settings/version | Existing 6.3.12 behavior |
| `v6`, `6`, `6.3`, `6.3.12` | Select 6.3.12, disclosing its exact coverage |
| `6.1`, `6.1.5`, `6.3.13`, `7` | `unsupported_version`; recommend official web lookup |
| `latest`, `^6`, `6.x`, prereleases, malformed versions | Input validation error |

Matching `6` does not establish compatibility across every v6 release. Responses
include `version_context` with requested, normalized and selected versions, match
type, source and a coverage limitation. Saved versions retain the user's precision.
Major fallback is tested with synthetic catalogs but is not enabled for current
knowledge. Catalog expansion alone cannot route another release to the old backend.

Unsupported versions/adapters return structured `status`, `message` and
`recommended_action` fields, with no facts or hosted planning call. These domain
results are not MCP transport failures; malformed inputs are MCP tool errors.
Only core/Material scope is available. No new adapter filtering is introduced.
Natural-language version interpretation remains in the existing planner; callers
should supply the intended version through arguments/settings and keep the
question consistent with it.

## Persistence and setup

The separate settings SQLite file defaults to
`$XDG_STATE_HOME/ask-formly/project-settings.sqlite`, or
`~/.local/state/ask-formly/project-settings.sqlite` if unset. Override it with
`FORMLY_SETTINGS_PATH`. Servers sharing a file share settings. Reads of missing
settings create no file. Writes are transactional; concurrent updates to different
fields retain one another. Same-field updates use the last committed value.
Each lookup uses one settings snapshot, unaffected by later writes.

In a provisioned MCP environment, install only the new dependency using that
environment's interpreter: `python -m pip install 'semantic-version==2.10.0'`.
Do not upgrade other pinned packages or the frozen model environment. Doctor
checks the new dependency. Runtime pins change only for the authorized MCP
boundary, dependency lock and new modules; knowledge/model/compiler pins remain.

For asset-free testing, use a disposable Python 3.13 environment:

```sh
python -m pip install 'markdown-it-py>=3,<5' 'PyYAML>=6,<7' -r poc/contextual-kb/mcp_v1/requirements-context.txt
python -B tools/project.py source
python -B -m unittest discover -s poc/contextual-kb/mcp_v1 -p test_transport.py
python -B -m unittest discover -s poc/contextual-kb/mcp_v1 -p test_service.py
```

Tests cover matching, fallback policy, persistence, worktree/project isolation,
concurrent writes, preservation of the existing service/wording flow and real
stdio MCP calls with a fixture service across restarts. They do not qualify model
inference or the installed DB. Full qualification still requires
`python3 tools/project.py check` in a provisioned checkout.

## Verification with the main checkout's assets

The version/settings worktree passed `python3 tools/project.py check`: 52
source/context tests, all 80 doctor checks and 97 runtime regression tests.
Both frozen extractors (1701 and 1702) passed real inference and parameter
integrity checks. Real hosted stdio calls succeeded for a legacy request and a
saved-v6 request, each returning eight facts with citations and healthy extraction
and selection. A v7 request returned the expected coverage error without planning.
These smoke checks establish operation, not identical hosted output or broad
answer-quality qualification.

The main checkout's current DB had newer knowledge work, so verification used its
preserved 46-fact snapshot matching this worktree's original hash exactly. All 80
pinned files remained unchanged after testing. Main environments were borrowed
without modification; a local MCP environment wrapper adds the new dependency.
Environment links and asset copies are ignored. Sealed evaluation stayed closed.
Detailed receipts are retained locally under `test-output/main-checkout-verification/`.
