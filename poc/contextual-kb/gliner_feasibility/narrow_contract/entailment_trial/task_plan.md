# Task plan

User authorized recording strongest configurations, a bounded no-training entailment experiment and question-plan usability assessment, with independent review. No changes to A, v2, both baselines or data/DB. Evaluation remains sealed.

- [x] Record strongest configurations before experiment.
- [x] Prepare one fixed NLI model/policy,24 paired development questions, harness with TDD, and existing-v2 output usability panel.
- [x] Independent preparation/code/data review before experiment. Maximum three fresh review instances including final review if needed; no architectural pivot without user agreement.
- [x] Run frozen-model development inference and assess existing v2 outputs with both extractors. No training, prompt search, threshold selection or sealed evaluation.
- [x] Independent results/usability assessment; preservation checks; report bounded decision.

One NLI checkpoint, one policy, no tuning after inference. Existing shadow30 and adjudicated legacy30 are regression panels. Fresh24 is development, not held-out evaluation. Usability is question-plan assessment only, not retrieval/answer testing. Preserve original question text and metadata; role information remains diagnostic, not a hard search filter. Separate cached-extraction replay from newly executed calls.
