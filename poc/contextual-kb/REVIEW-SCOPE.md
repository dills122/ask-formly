# Review boundary: source-format, seeding, and direct DB query trial

Use this boundary for reviews of the current `poc/contextual-kb/` work. Give a
verdict on this bounded trial, with concrete evidence for any defect.

## In scope

- The controlled authored JSON format and whether the selected facts faithfully
  preserve the meaning, conditions, limits, version, and provenance of their
  Formly source material. Check substantive claims against pinned Formly v6
  evidence when assessing fact accuracy.
- Deterministic linting and compilation, including duplicate and invalid input
  rejection, source freshness and exact spans, evidence IDs, explicit links,
  and clear failure diagnostics.
- SQLite schema and seeding of these records, atomic replacement, clean rebuild,
  audit coverage, and tests for those behaviors.
- Whether the trial documentation accurately reports what was built and proved.
  Only compiled Formly knowledge may have been reused from earlier POCs.
- Whether the frozen developer questions have enough correct seeded facts for
  the stated manual answerability results. This is a data-coverage assessment,
  not a generated-answer benchmark.
- The FTS5 rows derived from authored facts, version/adapter filtering, direct
  candidate queries, one-hop `see_also` expansion, and fact/evidence packet
  reads in the explicit DB query trial. The query strings are designer supplied;
  grade only what that trial actually measures.

## Outside this review

Do not treat any of these as a missing implementation, acceptance gate, review
finding, or automatic next-task recommendation:

- An AI extraction skill or workflow, AI research and aggregation, LLM prompts,
  AI-authored fact quality, or unattended source authoring. That idea was shared
  as future context only.
- Automatic question decomposition, vector retrieval, an MCP, answer assembly,
  answer latency, or agent response quality. Do not infer those capabilities
  from the direct FTS query trial.
- Conversion of the full corpus, expansion to more Formly versions, or unrelated
  repository work. Inspect historical compiler paths only if needed to establish
  whether they are active or reused in this trial.

Report actual in-scope defects and their impact. Keep possible future work
separate from the verdict; no speculative architecture or small-gain tuning
recommendations are needed for this review.
