# Phase1 analysis and phase2 decision

87 calls completed (7x12+3 controls), no validation/backend errors. Baseline replay to be checked against prior native outputs in aggregation.

E1 removing descriptions changes outputs, retrieves some API text but breaks D12 ambiguity and splits identifiers. E2 entities alone recovers props.placeholder/options.formState as identifiers but loses aspects/conditions. E3 threshold .2 recovers a few topic-context links and also wrong requires_context/refers_to links; no correct full multi-ask decomposition. E4 short concrete labels conflates circumstances/actions and names. E5 records groups persistence+state+restart meaningfully in D08, but merges D02 actions into one record and misses D01/D10 asks. E6 classification alone worsens ambiguity.

C01 employment/location and C02 surrounds relations work. C03 explicit condition/outcome relation returns none. Decoder is operational; custom semantic relation remains unproven.

User supplied independent researcher notes during phase2 design. Notes align on extraction/planning separation; previous probe already performed only extraction. Proposed concept resolver/DB/retrieval/answer architecture remains outside current permission. Relevant suggestion: narrow explicit Formly slots + broad intent. Malformed pasted code reconstructed via verified public API, not copied/executed. Current model already matches researcher's recommendation.

Final three configs declared before execution: E7 nested overlap only (same baseline schema); E8 natural anchored record mode per official JSON tutorial (same E5 fields); E9 narrow combined formly_api/version/error_message/form_name + multi-label intent at .3, inspired by researcher. This replaces a contemplated singleton-label experiment before it was implemented or run. No additional model, training, DB or concept catalog. All 12 dev cases again. Treat intent labels as diagnostics, not a pre-existing gold-scored metric.

Official API sources: https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/3-json_extraction.md (natural anchor records); installed configuration.py supports nested overlap; https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/4-combined.md . Initial phase2 preparation command had a relative-path error before writing any files; corrected using Path.cwd() before inference.
