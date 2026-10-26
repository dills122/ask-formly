# Independent review record

## Instance 1 of 3

Fresh-context reviewer parity_review inspected implementation before RESULTS.md.
Verdict: Ready with non-blocking follow-ups for retaining the isolated candidate;
not parity or promotion readiness. No discovery/gate/inherited-lookup blocker.

P2: score.py assumed every reference file existed and every row had structuredContent.
Timeout exception rows and early stop would crash scoring. Reproduced KeyError with
an injected timeout; current12 successful rows and reported scores independently
reproduced exactly. 11 tests and802-file preservation passed independently.

Response: Accept. Added explicit observed/failed/unattempted states, receipt checks,
retained-failure accounting and timing denominator/policy. Missing attempted artifacts
are errors rather than being silently treated as unattempted. Added failing tests
before the fix, including end-to-end scoring of timeout+early-stop and inconsistent
receipt. Current results remain unchanged. New total16 tests pass.

Residual: native sketches/expected IDs author-visible; no autonomous selection,
repeated answer accuracy or end-to-end latency claim. Discovery pools require3–6
pages when exhausted. No architecture pivot requested or made.

## Instance 2 of 3

Fresh-context reviewer parity_score_review: Ready for the bounded scorer fix, no
actionable findings. Independently ran16tests, reproduced saved score exactly using
temporary copies, verified contradictory receipts fail and all-unattempted yields
zero completeness, zero timed requests and null median. The intermediate
score-green.txt contains4tests; all-tests.txt/current suite contains16 total tests.
No further review needed for unchanged scope. This does not establish parity,
autonomous discovery accuracy or readiness for promotion.
