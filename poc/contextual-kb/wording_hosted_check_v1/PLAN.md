# Authorized hosted integration check

User explicitly approved sending saved Formly plans and retrieved facts to the hosted selector for this test, requested full setup and independent review. All prior candidates, models, DB and sealed evaluation remain unchanged. Work/evidence only in this new directory. No training or implementation tuning.

Run two bounded checks with both frozen GLiNER seeds (1701/1702):
1. Saved F01 raw plan -> existing wording adapter -> existing strict service -> real frozen GLiNER/retrieval -> actual hosted selector. This deterministically exercises the previously failed wording.
2. Real calling agent -> existing wording_candidate_v1 stdio launcher -> fresh foundation generation -> adapter -> GLiNER/full-question retrieval -> hosted selector -> caller answers. Four exposed diagnostic requests: F01, M03 expression recipe, M05 missing validator knowledge, M07 hide semantics. Run each batch once per seed; no resampling or tuning. Raw errors/fallbacks remain evidence.

Check exact raw/canonical provenance, original-validator acceptance, unchanged original retrieval replay, full-question text, delivered/audited packet parity, original fact/citation parity, bounded replacements, model parameter and DB preservation. Inspect selector receipts to ensure actual hosted calls, not no-op substitutes. Review answers for support/gap honesty; not a broad accuracy claim. Existing final freezes and recursive protected snapshots checked before and after. Evaluation hashes only. One fresh-context independent review of executed evidence and harness; source candidate already reviewed and frozen. No previous scores rewritten, no default promotion implied.
