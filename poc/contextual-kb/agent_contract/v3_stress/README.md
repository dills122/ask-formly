# v3 repeated fresh development test

Frozen candidate: ../refinement_v3. See PROTOCOL.md for sampling and decision rules.
New requests are development evidence, not the sealed evaluation set. No candidate tuning occurs here.

Run local harness tests: `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v test_assess` from this directory.
Read-only inherited artifact verification: `python3 -B audit.py`.
