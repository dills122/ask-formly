# Independent hosted integration review

Review instance: 1 of 3.

## Findings

No actionable findings. **Ready** for the bounded, exposed-case hosted integration evidence described in PLAN.md and RESULTS.md. This verdict does not promote the candidate or qualify general answer accuracy.

The neutral bootstrap preceded the implementation inspection; REVIEW-PRELIMINARY.md was recorded before reading AUTHOR-EXPLANATION.md. The reviewer received no implementation conversation. HEAD was c3091328f49d53de6b41a49c4fe5aa8f1c45e516 on the broadly dirty worktree described by the bootstrap. Unrelated repository changes were excluded. Review covered the new harness, retained outputs and relevant frozen launcher/backend/planner/selector/preservation dependencies. Graph searches returned no POC symbols, and coverage reported not_tracked for the twelve inspected code paths; conclusions use direct source and retained evidence.

## Plan Review

The plan was fulfilled without runtime changes: two saved F01 plans exercise normalization with the real remaining pipeline, and eight fresh caller requests span four exposed cases and both extractor seeds. Saved and fresh evidence are clearly separated. Every fresh case was called once; no generation was rerun for review. Exactly ten selector generations and eight fresh planner generations are retained. The source launcher uses the actual selector; only the saved replay injects a saved planner result.

The two saved plans each receive one rewrite; all eight fresh plans receive none. Strict canonical validation and exact original/canonical provenance pass. Full-question baseline replay, supplemental query text/depth, selector input reconstruction and bounded decision replay pass. Original facts and citations match the database; all eight delivered MCP packets equal server audit packets. Existing candidate freezes and the recursive protected snapshot match, including hash-only evaluation preservation. No evaluation contents were interpreted.

## Author-Claim Reconciliation

| Claim | Evidence inspected | Status and consequence |
| --- | --- | --- |
| Actual hosted selector, no substitution | serve.make_service, Selector.__call__, ten input/decision/events/receipt sets | Confirmed: completed raw generations equal recorded decisions; token usage present. |
| Fresh caller and planner, once per case/seed | calling_agent.py, recorded commands/prompts, both caller event streams, eight planner event/receipt sets | Confirmed: four completed MCP calls per batch; original plan equals raw generation. |
| Normalization exercised separately | saved packets, normalization audit, native plans | Confirmed: two saved rewrites, zero fresh rewrites; no false fresh-normalization claim. |
| Full-query, packet/citation and bounded replacement integrity | audit.py plus independent execution, policy.py and retained inputs | Confirmed across ten packets; exactly two M03 one-slot repairs. |
| Answers preserve support limits | All eight answers compared with returned facts and authored citation quotes | Confirmed: F01/M07 supported, M03 partial, M05 not_supported for both seeds. |
| Models/data/old candidates unchanged and evaluation sealed | Recursive snapshot and candidate freeze verification | Confirmed within preserved manifests; no inference about unseen evaluation quality. |
| Small diagnostic only | PLAN.md, AUTHOR-EXPLANATION.md, RESULTS.md, README.md | Confirmed: no broad accuracy, stability, SLA or default-promotion claim. |

M03's string-expression bindings are supported by the delivered authored quote for the modern callback fact, even though the short fact claim only describes the function callback. M07 keeps the condition about relevant associated fields being hidden. F01's short recipe follows the delivered expressions-map and field-model evidence. Missing validator and required-recipe knowledge is acknowledged rather than fabricated.

## Verification Performed

- `python3 -B poc/contextual-kb/wording_hosted_check_v1/review-verify.py`: passed; ten raw selector outputs, eight raw planner outputs, two caller batches, direct manifest hashes. The script checks terminal completion, single responses, output equality and selector token usage without generation.
- Existing virtual-environment Python, `-B`: imported and ran the recursive protected snapshot comparison and both candidate freeze verifiers; passed.
- Existing virtual-environment Python, `-B`: executed the inspected audit.py source with only its output destination replaced in memory by review-audit.json. All assertions passed; review-audit.json is exactly equal to test-output/audit.json. No source was edited. Console retained in review-audit-console.txt.
- Manual review of eight final answers against delivered fact claims, conditions, limits and authored quotes; outcomes above.

An initial generic `python` command was unavailable; Python 3 and the existing virtual environment were used successfully. ONNX emitted a telemetry-ID persistence warning during the audit replay; it used an in-memory identifier and the replay passed. No new inference, hosted calls, unit suites or browser tests were run by this reviewer. Existing browser qualification limitations remain unchanged.

## Open Questions And Residual Risks

The four requests are exposed diagnostic cases, not held-out evaluation. Two seeded extractor runs are not independent repeated stability trials. Fresh generation did not reproduce the normalization trigger; only saved replay directly exercises that path. Existing knowledge still cannot establish a full required-expression recipe or validator/message recipe. Successful transport, valid citations and safe abstention do not establish complete engineering answers across the library. Hosted-execution evidence is local CLI events/receipts plus source wiring, not an independent provider attestation.

## Verdict

**Ready** for this bounded integration evidence. No blocking or non-blocking corrective action is required in this scope.

## Recommended Next Actions

Retain these results separately from earlier rejected/no-op evidence and preserve the frozen candidates. Any future accuracy claim needs a separately authorized and predeclared qualification; this review does not authorize or require one. No further review instance is started.
