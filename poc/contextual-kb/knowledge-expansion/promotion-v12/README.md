# N1 promotion checkpoint

Installs the reviewed124-fact/27-document radio/native-select/common-registration candidate, foundation14 and model-free discovery6. Both modes share the same exact6.3.12 DB. Runtime implementation and model bytes unchanged; evaluation sealed.

`promote.py` is a historical one-time promotion helper. Its preflight requires the original116DB and refuses an already-promoted installation. Do not repin it to suppress that guard. It recomputes the frozen qualification, checks reviews and source inputs, reproduces candidate DB bytes/tables, and uses the existing guarded transaction. Do not rebuild the installed DB directly.

Recovery snapshots and installed-test receipts live in ignored test-output/install-1 and test-output/model-*. The transaction restores targets on ordinary exceptions/interruption; it is not crash-atomic. Model-backed tests require permitted execution for the existing Codex subprocess. Keep initial sandbox failures as diagnostics; use fresh output names for permitted retries.

Public source includes two additive catalog records and release mappings (K79/K80), both authored documents, and source preservation entries for the supplemental notes/index. DB/model files and raw test packets remain private. See RESULTS.md, FINAL-REVIEW.md and CHECKLIST.md.
