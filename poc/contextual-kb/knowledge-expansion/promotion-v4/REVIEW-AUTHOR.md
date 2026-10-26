# Author explanation: 64 to 70 promotion

Intent: install the already qualified extensions/presets knowledge without changing retrieval, GLiNER models, compiler or sealed evaluation. The transition is foundation4 (64/13) to foundation5 (70/15).

Implementation is confined to promotion-v4. promote.py derives from promotion-v3; changes are the exact transition pins/counts, handling two added authored documents instead of one, and foundation5 metadata. validate_additions rejects unexpected filenames, prior-source drift and draft/candidate mismatch before producing changes. The catalog is semantically identical and is not written. Original guarded replacement and snapshot/rollback machinery is reused. run.py is an unchanged copy of the stable-launcher smoke runner; cases.json is an exact copy of extensions-v2's visible15-case qualification contract.

TDD: two new source-set tests failed because validate_additions was absent, then passed after implementation. The eight existing filesystem/snapshot/rollback fixtures also pass. These eight are reused coverage, not newly red-first tests. Read-only actual-assets preflight succeeded: 70 facts/15 documents/41 evidence, all five canonical rebuild tables equal candidate, all accepted rows preserved, 80 non-DB runtime/model pins unchanged. No installed files have been modified by this implementation task.

The preflight uses the existing compiler, source pins and candidate freezes; it does not substitute count checks for provenance or row equality. The candidate catalog adds no records. Five intended writes: two new authored documents, installed DB, foundation manifest and source preservation manifest. Snapshot includes additional unchanged authored/catalog inputs for recovery context.

Limits: full real-agent installation smoke and independent review remain pending. Five file replacements are not one atomic filesystem transaction. Caught errors restore old values; power-loss recovery remains manual from the retained journal/snapshots. Existing MCP processes need restart. No public model/DB assets should be staged.

Review challenge points: frozen source/qualification bindings, two-addition rollback, unchanged prior rows and model pins, smoke checks for each new fact, and exact source preservation manifest updates. Parent owns apply, post-install testing, public documentation and packaging.
