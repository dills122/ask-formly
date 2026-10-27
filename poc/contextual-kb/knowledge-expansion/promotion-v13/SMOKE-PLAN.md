# Installed192 smoke plan

Run only after authorized promotion installs the exact reviewed candidate database SHA256 `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`, foundation15 and discovery7 manifests declaring 192 facts / 36 documents and promotion-v13. The runner checks these before creating an output or launching a server and verifies the same pins after delivery. It does not invoke the historical source-preservation guard, whose baseline pins intentionally predate promotion.

The model-free stable launcher runs through `model_free_v1/offline_guard.py`. Replay all 44 candidate r1 calls covering 40 requests in the report audit order: API, API-fetch, CONFIG, CONFIG-fetch, CONTROL, REGRESSION, REGRESSION-fetch. Packet bytes must match the reviewed assessment seal. Require zero transport/tool failures, the offline guard marker, and exact complete result equality with each qualified candidate result in order. This validates installed transport/evidence equivalence; it does not create independent new semantic judgments.

The model-backed stable launcher runs five requests per seed 1701 and 1702: API-02 (props), API-09 (updateInitialValue nullish behavior), CONFIG-04 (wrapper registration), CONFIG-11 (absent preset), CONTROL-01 (unsupported version 7). Remove only `plan` from their reviewed lookup arguments. Hosted planning and selection remain active. Delivery success alone is not semantic success: inspect retained facts/citations and coverage responses, record omissions and failures, and make no full-mode accuracy claim.

Each invocation requires a new exclusive name under this directory's `test-output/`. Retain input calls, complete results, stderr, tools, settings (command, seed, installed pins, packet hashes), runtime directory, and a receipt even on interruption/error. Never overwrite a prior output. A successful free run also writes `equivalence.json`. Preserve failed runs and use a fresh name for any repeat.

Fixture checks (no MCP or hosted inference):

```sh
python3 -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v13 -p test_installed_smoke.py
```

Post-promotion commands, from the repository root using the existing provisioned MCP interpreter:

```sh
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/installed_smoke.py --mode model-free --name installed-free-r1
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/installed_smoke.py --mode model-backed --seed 1701 --name installed-backed-1701
poc/contextual-kb/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/installed_smoke.py --mode model-backed --seed 1702 --name installed-backed-1702
```

These are bounded post-promotion checks. Runtime implementation/model bytes and sealed evaluation remain unchanged.
