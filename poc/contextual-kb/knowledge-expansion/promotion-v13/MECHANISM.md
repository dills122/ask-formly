# Guarded 124 → 192 promotion

This mechanism promotes the exact reviewed api-contracts-v1 SQLite file, SHA-256 `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`. It changes data and manifest metadata; runtime implementations and models stay byte-identical. The new identities are foundation15 and model-free discovery7.

Run from the repository root with the qualification interpreter:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v13 -p 'test_promote.py'
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/promote.py --name preapply-review
```

The default is a dry run. An explicitly selected `--apply --name UNIQUE_NAME` uses the same preflight and promotion-v7 `guarded_replace` transaction. Existing output names fail closed. A transaction snapshots the five existing targets, records before/after hashes and nine new files, checks preconditions again, and restores changed targets on ordinary errors and interrupts. Individual replacements are atomic; the group is **not crash-atomic**. Keep the generated `test-output/NAME/before/` journal and snapshots for recovery.

The allowed installed writes are exactly:

- Nine authored JSON files named in `promotion-spec.json` (68 facts).
- `poc/contextual-kb/corpus/evidence-catalog.json`.
- `poc/contextual-kb/build/knowledge.sqlite`.
- `poc/contextual-kb/mcp_foundation/foundation.json`.
- `poc/contextual-kb/mcp_runtime/model-free.json`.
- `poc/contextual-kb/packaging/source-files.json`.

All 326 baseline protection pins are verified before promotion. Post-installation, exactly the five explicitly changed existing targets are excluded from those old pins and verified against independently constructed exact replacement bytes. All other 321 protected files remain pinned. All 27 old authored files retain their exact bytes. The candidate catalog must equal the original catalog plus the reviewed additions and exact 6.3.12 release mappings; existing entries and other fields cannot change. Both runtime manifests preserve every field except identity, knowledge metadata and the database hash.

The 299 review/input pins bind the three additive draft batches, input chains, reviews, candidate manifests, report/audit code, assessment seal and saved report. The historical api-contracts-v1 report runs unchanged as a subprocess before writes, including mandatory assessment-seal inventory/hash checks, receipt audits and all three repeat comparisons. Its report must equal the saved report and satisfy the 24 target / 8 regression / 8 control cohort, original ≥90% target gate, all controls/regressions usable, no lost baseline support or critical claim, three passing repeats and exactly 399 calls. These are fixed-plan repeats, not independent generations.

All eight knowledge tables must preserve installed rows. Canonical compilation into a temporary database beneath `promotion-v13/test-output/` must reproduce both all eight tables and the exact candidate bytes. Source preservation adds the nine original draft inputs, nine `derived_from` source-note files, nine sibling `sources.md` files referenced by source quotations, the nine installed authored inputs, and the updated catalog hash.

After successful installation, run:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/knowledge-expansion/promotion-v13/promote.py --verify-installed
```

This independently reconstructs and verifies the exact promoted files, old authored inventory/bytes, preserved runtime/model pins and new provenance pins, then repeats canonical byte/table reproduction. It does not run or edit the old report's installed124 preservation check, and accepts no arbitrary exclusion list or mutable receipt as authority.

Preparation evidence: initial tests failed because the new module did not exist; six focused tests then passed. An initial system-Python dry run failed canonical byte comparison (SQLite3.53.3 versus the qualification environment's3.53.1). With the qualification interpreter, `--name mechanism-preflight` passed. The byte requirement was retained unchanged. No installed writes occurred during mechanism preparation.
