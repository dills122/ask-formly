# Author explanation

The user asked us to investigate GLiNER2 failures more deeply, retaining scope locks. We ran seven predeclared configurations on all12devcases plus3positive/negative controls (87calls), then three adaptive but predeclared follow-ups (36calls), incorporating supplied independent research as E9. No trained weights, baseline code or DB changes.

experiment.py implements phase1 schema variations and recursive source-span validation including structured records; test_experiment.py has four red-to-green retention/validation tests. phase2.py reuses validators/observation and implements natural anchored record mode, nested overlap and narrower entities+intent. It is separate so phase1 code and manifest remain valid. All native outputs/timings retained. Schema construction uses installed GLiNER2 public interfaces; no semantic postprocessing.

Findings: no complete multi-ask remedy; several narrow improvements. E9 correctly types4of8explicitAPIoccurrences vsE0zero (others returnedwrongroles), but adds3genericAPIspans and mislabelsresetOnHide. E8splitsD02records butdropsobjects. E5D08groupspersist+state+restart. Simple relationcontrolswork; condition_forcontrolfails. Thresholdloweringchangesflatweightedoverlap selection; native decoder replays observedcandidateunion reproduceE0/E3D02 exactly. Neither modelcandidate reservoir nor universalcausality claimed. No intentaccuracy metric, no planqualityscore.

Evidence:123callsnoerror; E0exactreplay; 60protected+17priorfiles+11phase1+9phase2hashesm match. Raw code/debug logs retained. No heldoutreads, no modeltuning/training, no Aexecution. Preparatory path/URLlookup errors are described in findings and did not discard modelruns.

Costs/limits: schema-dependent development fitting, limited12cases, no randomization/warmup or benchmark, auditafterloadlimitedPythondefense, softnativealarm. New record mode changes mode+anchorcardinality as one framing intervention; E9changesmultiplelabels/tasks. Findings avoid single-factor causalclaim for those. A future training experiment is proposed, not implemented or claimednecessary/sufficient.

Challenge API wiring, raw-to-summary consistency, semantic exaggeration, whether slotmatchesmeasure the asserted improvement, and whether metadata provides honest provenance. User's research suggests broaderarchitecture; it was not permission to touch downstream/data layers.
