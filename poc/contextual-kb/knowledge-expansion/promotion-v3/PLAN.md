# Guarded 64-fact promotion

Status: implementation and read-only preflight complete; independent review and explicit apply pending. User approved this session plan. Models and evaluation remain protected.

## Scope

Promote the previously qualified expressions-v1 database (64 facts / 13 documents) as foundation4. Preserve exact candidate bytes and all installed60 rows. Change only canonical expressions-notifications.json, installed DB, foundation DB/id/knowledge metadata, and one new authored source pin. No runtime/model/compiler/catalog changes.

## Repeatable commands

From repository root:

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v3 -p test_promote.py
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v3/promote.py --name preflight-new
# After review, apply once with a fresh output name:
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v3/promote.py --apply --name install-1
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v3/run.py --cases poc/contextual-kb/knowledge-expansion/promotion-v3/cases.json --name stable-live --repeats 1 --batch-size 5
```

Each output directory is exclusive. Repeat preflight with a new name; applying again refuses the old-foundation/DB precondition. Never repin to make a failing precondition pass.

## Mechanism

The promotion spec pins the accepted60 and candidate64 DB hashes, accepted manifests, candidate manifest, frozen experimental input manifests, final preservation receipt and independent review. The script verifies current source/model/runtime pins, candidate inputs and frozen files. It compares all five knowledge tables for accepted-row preservation and rebuilds the proposed canonical sources into a disposable DB before any installed mutation.

Before installation, snapshot oldDB, all12 canonical authored files, catalog and both manifests. Write a recovery journal listing old/new hashes and newly created files. Replace four authorized files atomically per file. Postchecks verify all resulting pins and rebuild from now-canonical sources into another disposable DB; compare all five tables. Any caught exception or interrupt restores old changed files and removes the newly admitted authored file.

This is not an atomic multi-file filesystem transaction. Do not run concurrent maintenance or start a new MCP connection during the brief installation. Existing MCP processes may retain the old DB and must be restarted after completion. A power loss/SIGKILL can leave a prepared journal and partial installation; inspect before/journal.json and restore its pinned snapshots before starting service. Automatic recovery is limited to caught errors/interrupts; no claim of crash-proof rollback.

## Smoke contract

Ten original visible cases, one repeat, seed1701, five cases per batch: E01/E02/E03/E05/E10 plus M03/Q20/Q28/Q21/Q24. Every control must pass; all10 usable answers expected, zero critical and delivery errors. No retries or tuning. This is installation smoke coverage, not a replacement for the already completed90-call comparison and45 paired replays. Preserve grader rules and independently audit outcomes. Missing responses stay failures.

## Verification so far

- TDD initial six tests failed before implementation (missing module), retained in test-output/tdd-red.txt.
- Initial implementation run exposed macOS /var temporary-directory aliases in fixtures; fixtures were normalized to canonical roots as required by the production guard. Retained initial failure and corrected run.
- Eight tests now pass, covering success/snapshot, postcheck rollback, partial-write rollback, interrupt rollback, precondition drift, collision, path/symlink refusal, and recovery-directory collision. The two added robustness tests passed against the existing implementation; they are supplementary, not claimed as red-first fixes.
- Read-only actual-assets preflight passed. All five rebuilt knowledge tables equal the candidate; 80 prior non-DB runtime/model pins preserved. No installed files changed by this worker.
