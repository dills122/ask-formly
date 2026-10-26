# Foundation9 versioned knowledge promotion

The [results](RESULTS.md) record the installed schema2 setup, unchanged93facts,
exact6.3.12 coverage and qualification. `install.py` is a one-time guarded script
for the recorded foundation8 baseline; it intentionally refuses rerunning after
promotion. It uses the existing tested promotion-v7 per-file transaction and
reproduces canonical inputs before/after replacement. It is not a generic updater.

Source/runtime manifests and the recovery bundle allowlist include the new runtime
import closure. `python3 tools/project.py check` runs current compiler, packaging,
context, retrieval and stable-launcher fixtures without hosted calls or sealed data.
`smoke.py` uses the stable launcher and isolated project settings with both frozen
model seeds; public development requests and facts go to the existing providers.

## Coordinated recovery

Do not restore only the DB or only a recovery journal. Schema1 requires the
matching old reader, authored format, compiler interface and manifests.

1. Stop the Formly MCP readers and preserve any subsequent local work.
2. Restore source/code/authored/catalog/manifests from accepted commit
   `d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2`, or the verified `test-output/before`
   snapshot. The snapshot's `before.json` lists all712original source files.
3. Restore `test-output/rollback.sqlite` to the installed DB with same-filesystem
   temporary write and atomic replace. Its hash must be
   `cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d`.
4. Verify the restored old foundation manifest/doctor and local checks before
   restarting readers. Models/environments remain the same; don't repin mismatches.

These are recovery instructions, not steps to run during maintenance. The
`rollback_check.py` rehearsal copies the complete old source and DB to a temporary
isolated checkout, validates source hashes/provenance, imports the old composition,
and reproduces12publicqueryrankings with the old reader. It never writes the
installed path. Private snapshots/DBs/raw receipts are excluded from Git.

Byte-for-byte SQLite reproduction is qualified with the provisioned MCP Python
3.13 / SQLite3.53.1 environment. Other SQLite builds can emit different database
bytes for identical semantic tables. Do not replace accepted hashes based on an
unqualified compiler environment; compare semantic exports and qualify that
build environment separately. Use `mcp_v1/.venv/bin/python` for the recorded
promotion/reproduction commands.
