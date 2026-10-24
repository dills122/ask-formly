# GLiNER2 bounded development feasibility

User scope: GLiNER2 extraction feasibility only, existing 12 development cases. No held-out reads, no A/B rerun, no promotion, no data/DB writes. A and all previously frozen modules/configuration remain byte-identical. New code, environment, caches and evidence stay here inside this POC (latest user instruction).

- [x] Check protected hashes and inspect official APIs.
- [ ] Isolated pinned local dependency/model setup.
- [ ] TDD source-span validation and development-only input guard.
- [ ] One fixed schema for requested outcomes, conditions/negation, identifiers/literals/scope; relation links from outcomes to context; interpretation classification. No regex/domain keyword decomposition and no generative rewrite.
- [ ] Run each of 12 development questions once plus two repeats; preserve native results/errors/timing. No schema/threshold tuning after the first run in this bounded check.
- [ ] Review every output against development rubric: outcome boundaries, context attachments, exact spans and ambiguity. No full-plan score without a full planner.
- [ ] Independent review of implementation and findings before any full comparison. Stop here.

Feasibility gates (not promotion criteria): extraction must identify all outcomes and relevant context with usable links on the three multi-ask development cases D01/D02/D10; exact source copying must be mechanically possible; distinguish D09/D12 ambiguity without labelling all clear cases ambiguous. Report all 12, not just gates. If extraction cannot meet these, do not build a full adapter or start a comparison. Latency is exploratory only (CPU, local hardware, model loading separate), not compared as a benchmark against old A timing. No guaranteed speed target; 60-second per-call diagnostic cap, not the product ten-second deadline.

Model: fastino/gliner2.5-base-v1 revision 54785d51df8d86a0d8f2eb212fec15871aad2c4d; GLiNER2 family boundary architecture selected for longer outcome/condition spans. Package gliner2[local]2.1.0. All inference local, CPU; no question sent to a service. Network only for public package/model setup, offline inference afterwards.

Sources: https://github.com/fastino-ai/GLiNER2 ; https://github.com/fastino-ai/GLiNER2/blob/main/tutorial/6-relation_extraction.md ; https://pypi.org/pypi/gliner2/json . Public package/source interfaces will be verified in installed version before coding.
