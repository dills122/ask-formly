# v6 requested-aspect audit candidate

New same-schema candidate; no existing candidates or downstream code changed. CONTRACT.md is the complete prompt, AUDIT.md the addition, candidate.py the selector and same-POC transport reuse. PROTOCOL.md defines fresh72 and diagnostic15 response gates separately. All raw results retained in test-output.

Verification: `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v6 -p test_candidate.py -v` from repository root. Preservation: `python3 -B poc/contextual-kb/agent_contract/refinement_v6/preserve.py`. Byte-only sealed-payload checks. Unit tests cannot prove semantic completeness; independent review and results are separate evidence.

[RESULTS.md](RESULTS.md): diagnostic15/15; fresh70/72 useful text,60/72 full. Independent review: evidence ready, candidate not accepted. All frozen artifacts unchanged.
