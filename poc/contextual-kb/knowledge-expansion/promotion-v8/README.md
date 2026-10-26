# Installed JSON Schema knowledge

Foundation10 (model-backed) and model-free-discovery-2 now share the exact qualified
99-fact/22-document DB. The implementations, model assets and exact Formly 6.3.12
scope are unchanged. This directory records the guarded data promotion, installation
checks and independent review. See [results](RESULTS.md) and [source checklist](CHECKLIST.md).

## Serving and reconnection

Use the stable `mcp_runtime/launcher.py` entry point described in the
[dual-mode guide](../../mcp_runtime/README.md). Restart any existing server after
promotion. Experimental direct entry points keep their original 93-fact pins and
can reject the new DB; a restart alone does not change their configured script.
Repoint such connections to the stable launcher using its client examples. This
promotion does not silently edit local or global client configuration.

## Reproducibility and recovery

Canonical `authored/` plus the existing pinned catalog/compiler reproduce the
installed candidate into a **new isolated output**, never over the installed path.
The promotion preflight verified exact bytes and all eight knowledge tables.
The promoted JSON document is byte-identical to its reviewed candidate input.

`promote.py --name <fresh-name>` is a pre-install verification command; it requires
the original 93-fact baseline and provisioned private candidate/qualification
artifacts. It deliberately rejects an already promoted installation. It is a
historical migration tool, not a fresh-machine installer or routine startup step.
`--apply` additionally performs the guarded replacement only after all gates pass.

Local recovery is under ignored `test-output/install-1/before`: the journal names
all five targets, their old/new hashes, four existing-file snapshots and the newly
added authored document. Caught errors/interrupts restore the old targets and remove
the new source. The operation is atomic per file, not crash-atomic across files.
After an abrupt process/machine failure, stop clients, inspect the journal, restore
all targets together (including both manifests and source pins), remove the new
source if rolling back, and verify both doctors before restarting. Do not restore
only the DB or change hashes to bypass a mismatch.

## Checks

```sh
python3 -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/promotion-v8 -p 'test_*.py'
python3 tools/project.py check
```

`installed_smoke.py --mode model-free --name <fresh-name>` exercises the full fixed
case set and follow-ups through the installed stable launcher; it requires the
private qualification receipts for exact result comparison. Explicit
`--mode model-backed --seed 1701` or `1702` performs the bounded retained-mode smoke,
including that mode's internal hosted calls. Never reuse a run directory or treat
transport success alone as semantic qualification.

Models, DB binaries, raw outputs, local settings and sealed evaluation are not
published. Current knowledge is represented in public Git by authored facts,
provenance, compiler and manifests; exact local DB reproduction retains its pinned
toolchain requirement. The prior failed qualification runs remain historical.
