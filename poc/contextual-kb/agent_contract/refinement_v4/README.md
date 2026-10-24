# v4 question-layer candidate

A separately selectable prompt revision. `candidate.build_messages` selects CONTRACT.md; validator and advisory hint handling reuse frozen v3, entirely inside this POC. No production integration or schema change. LEDGER-RULES.md is embedded verbatim into CONTRACT.md.

`PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_candidate` from this directory tests the entry point and compatibility. It does not prove semantic completeness. `python3 -B preserve.py` verifies frozen prior artifacts by bytes only.

PROTOCOL.md defines the predeclared actual-generation test and gate. New data/outputs here are development evidence; evaluation remains sealed.
