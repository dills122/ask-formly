# Author Explanation

## Intent and scope

User authorized promotion/testing/review/commit/push/PR for reviewed versioned
knowledge, preserving models/evaluation and adding no new coverage. Foundation9
installs the exact schema2 candidate; same93facts/21docs and exact6.3.12 only.

## Changes and rationale

Canonical21authored documents/catalog copied from tested migration. Install script
recompiled them before switch and from installed paths after switch; both match
a0f102f...106 exactly. Existing guarded_replace snapshots/revalidates/atomically
replaces individual files, rolls back ordinary exceptions, and journals completion.
There is no claim of cross-file filesystem atomicity. No legacyreader processes
were present at switch; no unrelated processes were terminated.

current_source is the active schema2 compiler; the original schema1 compiler remains
for the provenance projection/history. CLI build now requires an explicit new
isolated output and refuses installed/existing targets. Maintenance lint uses a
disposable DB, not the installed one. Source CI includes versioned compiler tests.

Stable launcher now constructs a Context through mcp_foundation/versioned, keeping
original MCP tool definitions, annotations and audit path. create_server accepts
an explicit context; old default behavior remains for historical/fake fixtures.
InstalledBackend only changes candidate path validation, retaining reviewed index,
extraction, selection, citations and integrity logic. Candidate default still
rejects installed DB. All runtime additions and changed launch files are pinned.

The local recovery allowlist was extended, but reviewer found the legacy compiler
import missing. Accept that finding; test/fix follows review1. Current working
checkout is unaffected; offline recovery import closure must be corrected.

## Verification

TDD RED: new active compiler/factory tests fail without implementation; 2pass.
Source scheduling RED16!=17 thenGREEN. Source8compiler tests added; local13candidate
and2promotion tests added. Existing launcher test expectation/import path updated
for explicit context; failed maintenance logs retained. maintenance-3 passed:
175source,148runtime,94doctor. Both seeds' real stable MCP runs completed six
supported calls and two unsupported-v7 calls; smoke-summary.json/rawcalls available.
All supported packets have eight facts, native parameter-integrity pass, DBunchanged,
availableadvisory, successfulselector and exactapplicability; core settings persist.
No answer-accuracy score claimed.

## Preservation/recovery and limits

Before edits, copied712sourcefiles (tracked plus candidate public files) to
private test-output/before with before.json, and saved schema1rollback.sqlite.
Guarded data install also records a per-file recovery journal. The old source
snapshot includes old launcher/server/manifests needed with schema1. Old models
remain in place unchanged. Explicit coordinated rollback instructions/rehearsal
are being finalized and will be provided before final readiness.

All docs updated for foundation9 and schema2; earlier candidate logs remain
historical. Candidate verify/preservation commands target the prior baseline and
must use that checkpoint, not repin installed changes. No new release routing,
wholemajor applicability, modeltraining, sealed data or app investigation.

No commit/push performed yet. Reviewer should inspect complete public diff and
untracked modules, not just the minimal promotion delta. Recovery import closure
and coordinated rollback are remaining gates; do not treat pending work as passed.
