# Fresh review2 bootstrap
Review instance2 of3. Use independent-review and code-review-and-quality skills. Same repository /Users/dsteele/repos/ask-formly, dirty main HEAD c3091328f49d53de6b41a49c4fe5aa8f1c45e516. Scope new advisory_lookup_v1 only. User chose working foundation plus advisory GLiNER plus unchanged full-question retrieval. Existing candidates/models/DB immutable; evaluation sealed.

Read CONTRACT.md, original REVIEW.md/REVIEW-DECISION.json findings and tests before current cli.py/verify_live.py. Focus on P1 final verification must not hide degraded successful retrieval, and P2 harness worker lifecycle cleanup. Inspect actual full integration and failure behavior around these changes. Save REVIEW-2-PRELIMINARY.md before author REVIEW-FIXES.md,AUTHOR-EXPLANATION.md,RESULTS.md.

Current source bound by test-output/final-code-freeze.json.23tests including new composition/cleanup RED→GREEN. Full native evidence remains test-output/live-native (48requests/70derivedquestions permodel,foundation+twoepochs6adapters). Default CLI afterfix: cli-final-native.json. Fault injection with realDB: cli-failure-live.json. Parent may still await defaultCLIcompletion, will notify. Do not rerun native inference/retrieval; offline reconstruction and unit tests allowed.

Audit history accurately: original run used .venv without torch and failed; changed cli/verify_live/README copies reside failed-environment-source for original run-freeze. Successful native panel used run-ready-freeze; pre-fix cli/verify_live copies reside pre-review-fix-source for that manifest. No original evidence overwritten. Persistent localworker uses existing GLiNERenv;parent retrievalenv, no dependency/modelchanges.

Own only REVIEW-2-PRELIMINARY.md,REVIEW-2.md,REVIEW-2-DECISION.json,test-output/review2-*; read-only elsewhere. You are notalone; no fixes/model/dataedits or furtheragents/reviewinstances. Verify48priorchains byte-only and current manifest/evidence; no sealed semantics. Graph ask-formlyOctober16 nottrackedPOC; parent checked reused/newfiles (including transport/worker/tests) and readsourcefallback. Checkanyadditionalpaths, no reindex.

Command: python3 -B -m unittest discover -s poc/contextual-kb/agent_contract/advisory_lookup_v1 -p 'test_*.py'. Return readiness of functional integration separately from annotationaccuracy/productionqualification. Max3instances, no expansion.
