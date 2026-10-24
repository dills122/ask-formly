# v5 conditional-follow-up/history candidate

Separate prompt selection through candidate.build_messages. Same v3 validator and optional advisory hint projection, wholly inside this POC. LEDGER-RULES.md is inserted into CONTRACT.md; no pipeline integration.

Run `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_candidate` in this directory. `python3 -B preserve.py` verifies protected bytes without interpreting sealed evaluation cases. These checks do not establish semantic completeness. PROTOCOL.md defines the actual-generation development test and independent review.
