# Author Explanation — review1 response

Accept P2 transitive replacement scope finding. Added a three-fact chain test;
ancestor-red.txt records the expected failure. Compiler DFS now memoizes all
ancestors and rejects overlapping applicability against any ancestor, while
retaining cycle/missing-target checks. Unit suite now passes 13 tests, including
an actual inherited selector pool/fallback test showing no foreign-version IDs.
No runtime/index/context behavior changed after the successful live run.

The six real supported MCP calls passed across both seeds; both unsupported-v7
calls passed. Native checks confirmed unchanged parameters on each supported call.
Each returned 8 facts. These are operational checks, not calling-agent answer scores.
Sandbox initialization failure is preserved separately and was not counted as a
successful call. Successful receipts are smoke-1701/ and smoke-1702/.

verify.py now performs a disposable post-fix rebuild and compares bytes against
the tested candidate. It also copies the private rollback DB into a temporary
location, reads it with the preserved legacy index, and checks 12 fixed public
queries. This is an isolated rollback rehearsal, not an installed promotion test.
final-verification.json records the result plus 690/89 preserved pins.

Existing REVIEW-AUTHOR.md describes the original complete approach and limitations;
this packet supersedes its '11 tests/live pending' status. README.md documents the
opt-in contract, commands and separate promotion boundary. No other plan changes.
