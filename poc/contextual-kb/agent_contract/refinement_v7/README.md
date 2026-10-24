# v7 ledger clarification and paired construction

Experimental candidate only; existing candidates and data/DB unchanged. LEDGER-RULES.md defines prospective rules; CONTRACT.md embeds them with library-only scope and unchanged JSON. candidate.py selects prompt and reuses frozen same-POC transport. See PROTOCOL.md for fresh/diagnostic gates.

Run tests from root: `python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/refinement_v7 -p test_candidate.py -v`. Byte-only preservation: `python3 -B poc/contextual-kb/agent_contract/refinement_v7/preserve.py`. Unit tests do not prove semantic completeness. Sealed evaluation remains closed.

[RESULTS.md](RESULTS.md): fresh69/72full,23/24all-three; diagnostics18/18. Evidence ready, fullfreshgate fails onF23. No promotion.
