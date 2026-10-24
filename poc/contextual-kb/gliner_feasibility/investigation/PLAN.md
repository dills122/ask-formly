# GLiNER2 failure investigation

Authorized follow-up: analyze and experiment to rectify GLiNER2 failures if possible. Development only; no full comparison, no model training, no A change, no data/DB/retrieval change. All new artifacts inside this POC. Previous evidence immutable.

Phase1: predeclare seven variants E0–E6 in phase1-variants.json, run each on all12originaldevelopmentcases once, plus3separately labelled diagnostic controls in controls.json. E0replicates previousconfiguration; E1removesdescriptions; E2separatesentities; E3threshold0.2; E4concretelabels; E5recordgrouping; E6isolatesclassification. Nativeoutput preserved; changes not automatically called fixes. All84+3samples retained.

Hypotheses: long descriptions may alter label understanding; combined tasks may interfere; threshold may suppress useful candidates; entity/relation framing may mismatch requested actions; record extraction may associate conditions better. Simple positive-control relations distinguish decoder breakage from unfamiliar relation semantics.

Phase2: at most three additional targeted configurations after phase1analysis, all explicitly recorded before running. Can use minimal development contrast pairs with annotated targets to localize a failure. No held-out tests; no unreported parameter sweeps. Stop if only sparse/incorrect outputs improve.

Assess correct outcome/action completeness, exact-name coverage and negation/context links against developmentrubrics; report spurious results and regressions as well as gains. Mechanical substring equality is not semantic success. Do not report planquality without planassembly. Developmenttiming includes cold/warm distinctions and cannot establish superiority to A.

TDD for new observation/validation logic. Independent review instance2of3 in ongoing feasibilityflow after results. Need a decision before any fullcomparison or training.
