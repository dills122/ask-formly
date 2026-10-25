# 79-fact installation checkpoint

The exact reviewed validation-v1 candidate is installed as foundation6: **79 facts across 17 documents**, with 46 evidence records. DB SHA256: `226c377ecb4a8a220c5c6db541156c3dcad71045d73b21a5d205fbf164b7715b`. All five knowledge tables reproduce from canonical sources; all 85 previous non-DB runtime/model pins are unchanged.

The guarded promotion added two canonical authored documents and updated the installed DB and two manifests. Recovery snapshots and journal are retained under ignored `test-output/install-1`. Twelve fixture tests pass, including rollback and interruption coverage. The preapply independent review is [Ready](REVIEW-PREAPPLY.md).

Local maintenance passed: 128 source tests, 114 runtime regressions and 86 doctor checks. This does not itself establish hosted answer quality.

The installed real-agent smoke passed independent answer audit: **15/15 usable answers**, all five controls, zero critical or delivery errors. It used 15 visible validation cases once, seed 1701, in three batches. Automated assessment agrees: 15/15 usable, zero critical failures. [Final independent review](REVIEW-FINAL.md): **Ready**, with no actionable findings.

Advisory status: 14 available, one not needed. Selection: 12 unchanged, two repaired (V07 and Q20), one not needed. Both repairs preserved supported answers. All 86 asset pins still match after the live run. This installation check is separate from the candidate's earlier three-repeat qualification (45/45 candidate answers versus 15/45 baseline answers, plus 45 matched-plan replays). No whole-library or unseen evaluation claim is made.

Models are unchanged and evaluation remains sealed. Restart existing MCP server processes to load the promoted DB.
