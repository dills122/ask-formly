# Author Explanation

## Intent And Success Criteria

Prepare the authorized 70-to-79-fact installation without changing runtime or models. The installed candidate must exactly match validation-v1's qualified SQLite bytes and reproduce from canonical authored inputs. This packet describes preparation, not a completed promotion.

## Plan-To-Implementation Traceability

PLAN.md defines five writes and the later smoke gate. promote.py implements preflight, guarded replacement and postcheck. promotion-spec.json pins current manifests, exact old/new DB bytes, candidate manifest, both freezes, qualification decision, final checks and candidate review. cases.json copies the visible fixed qualification unchanged.

## Technical Approach And Flow

Verify pins and source identity, preserve every old row, reproduce the candidate using proposed canonical sources, then optionally snapshot/write/postcheck. Default invocation only writes isolated test-output. Apply is explicit and foundation-specific. The copied run.py and merged_run.py launch a fresh real agent against the stable MCP, with lookup-only authorization.

## Changed-Component Walkthrough

promote.py is promotion-v4 with only batch, document names, foundation transition and counts updated. test_promote.py changes the two document names; rollback, failure injection, interruption and source-preservation fixtures are retained. run.py, merged_run.py and test_merged_run.py are byte-identical copies. This is a bounded migration artifact, not new generic infrastructure.

## Decisions And Rejected Alternatives

Reuse the already reviewed guard and stable caller rather than refactor migration/runtime machinery while changing knowledge. Preserve exact candidate DB bytes instead of installing a new rebuild; rebuild equality is checked independently over all five knowledge tables.

## Invariants And Boundary Conditions

No model/runtime/compiler/catalog/schema edits, old authored byte changes, old-row deletion, sealed reads, or installed mutation during preparation. Apply requires serialized maintenance and reconnection afterward. Runtime/model protection is verified through current foundation pins.

## Verification Performed And Results

Retained test-output/tdd-red.txt shows the adapted document-name fixture failing against copied v4 code (12 tests, one expected error). After the narrow update, tdd-green.txt records 12 passing fixtures. Existing rollback tests were reused, not newly invented. preflight-1/receipt.json reports checked-only, exact reviewed candidate hash, 79 facts, 17 documents, 46 evidence, 122 fact_evidence, 70 fact_links, all-five-table canonical reproduction and 85 preserved non-DB pins. No apply or live smoke has run in this preparation.

## Risks, Tradeoffs, And Maintenance Costs

The five writes are atomic individually, not across power loss/SIGKILL. Recovery snapshots/journal support manual recovery; ordinary errors and caught interruption roll back. The pinned transition cannot be reused after promotion without a new explicitly reviewed migration. Copied runner code is intentionally stable historical infrastructure.

## Deviations, Deferrals, And Known Gaps

Installation, project-wide checks, real-agent smoke, outcome review and publishing belong to the parent workflow and remain pending. This work does not expand qualification claims or inspect sealed evaluation.

## Challenge Points For The Reviewer

Verify all five authorized writes, exact candidate pins, both source freezes, catalog/old-source preservation, rollback behavior, current foundation transition, and the narrow per-tool approval. Check that live results are not claimed before execution.
