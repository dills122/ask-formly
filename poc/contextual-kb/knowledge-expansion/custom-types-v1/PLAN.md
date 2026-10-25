# Review gate and subsequent candidate-build plan

## Checkpoint being delivered now

Inventory the accepted 46 facts, prepare ten draft additions and their pinned evidence, define development requests and comparison criteria, lint the proposed union without building a database, and obtain one fresh-context independent review. Stop at the plan review checkpoint. A review pass is not automatic permission to alter the installed database or promote a new corpus.

The user explicitly requested this checkpoint before building. Historical steering still locks active data and implementation; this proposal does not rewrite those agreements or silently unlock them.

## Review criteria

1. Every addition fills an identifiable gap or makes a currently buried qualification explicit; no new duplicate alias-selection facts.
2. Claims and conditions are supported by the exact pinned source. Example-specific behavior remains labeled as such. Material and core stay distinct.
3. Quotes, hashes, fact IDs, links, and evidence IDs are internally valid. Existing 46 records and existing catalog entries are unchanged in the proposed union.
4. No active compiler input, model, runtime, DB, or sealed evaluation was modified/read as evaluation material.
5. Candidate construction and testing below are feasible without changing the accepted setup. Any harness change is a separately tested addition inside this expansion directory.

## After review and authorization: materialize candidate inputs

Use a separate `candidate-inputs/` directory under this expansion folder. Copy the nine accepted authored JSON documents byte-for-byte and add the two reviewed drafts. Use a candidate-only catalog containing the unchanged accepted records plus reviewed K65–K78 records; preserve the accepted catalog file itself. Keep source hashes and an input manifest for this candidate, not replacement hashes in the accepted preservation manifests.

The current CLI hardcodes `authored/`, `corpus/evidence-catalog.json` and `build/knowledge.sqlite`. **Do not run `python -m kbcompiler build` or `all`.** The existing Python API accepts explicit paths: `lint_sources(source_dir, repo_root, catalog_path)` and `build_sources(source_dir, repo_root, catalog_path, database)`. Use that API only after reviewing a small candidate runner with tests proving that its resolved input/output paths cannot overwrite or alias accepted paths (including symlinks). Output must be a new `candidate-build/knowledge.sqlite` here. Do not change the compiler.

Before/after: compare the installed DB hash and accepted preservation manifests; verify the candidate retains every original fact and evidence record, valid citation offsets, referential integrity, expected 56 facts and 11 documents, and no unintended version/adapter widening. Candidate sources must remain resolvable inside this POC/repository using the existing provenance convention. Do not point the production launcher at this candidate or repin its manifest.

## Qualification design (not run at this checkpoint)

Keep the accepted planner, wording validation, advisory GLiNER, full-question retrieval, embeddings and selector settings fixed. Use a separate test harness to select the accepted versus candidate DB explicitly. If the existing launcher rejects a different DB by design, do not weaken its guards: isolate the comparison harness with candidate-specific integrity checks. Review that harness before hosted runs. Any hosted test data consists only of synthetic library requests and reviewed Formly evidence, under the user's existing authorization for such tests.

1. **Development:** use the 16 visible requests in development-cases.json for diagnostics. They include direct, multi-part, unsupported-scope and baseline-regression requests. They are not sealed or a fair unseen score.
2. **Freeze:** settle authored facts, support rubric, harness, provider/model/settings and IDs before qualification. Prepare a separate fresh 30-request qualification set then; 20 in-scope custom-type requests, five gap/negative controls, five unrelated baseline regression requests. Independent review checks question clarity and answer expectations. This is new work, never the existing sealed evaluation. Do not tune against qualification; report failures as a new experiment if changes are later needed.
3. **Paired retrieval:** save one accepted plan per request/repeat and replay that same plan through both DB arms so planning variation does not masquerade as a corpus gain. Log candidate hits, original eight slots, final slots and exact citations. Alternate arm order; distinguish cold embedding initialization from warm lookup time.
4. **Real-agent usability:** also exercise complete tool calls through a real calling agent, with the identical question batches and provider settings. Run each fixed batch three times. Retain plans, MCP responses, final answers, errors, model/settings and timings. Label this as end-to-end variability rather than a perfectly controlled retrieval comparison.
5. **Score independently:** judge answers against source-grounded required claims and qualifications, permitting semantically equivalent correct evidence. Review output with arm/model labels hidden where feasible. Record omissions, unsupported assertions and disagreement resolutions; the generating agent's self-score is not the verdict.

## Decision criteria fixed before qualification

Report separate measures: authored support availability; requested-aspect coverage in retrieved pool, original packet and final packet; request-level usable grounded answers; and honest gap handling. A usable answer must cover all supported required aspects, preserve material conditions, cite supporting evidence, and explicitly bound unsupported asks. An invented application fact, wrong version/adapter assertion, or materially unsupported Formly behavior is a critical failure. Request counts and per-category denominators accompany every percentage. Do not turn extraction or plan scores into answer-accuracy claims.

- Every proposed addition must have at least one development request that exercises it; schema/provenance checks must all pass.
- Before a positive knowledge-expansion verdict, candidate final-packet supported-aspect coverage must improve on baseline for the expansion cases, with no systematic loss on already-supported aspects. Log each displaced fact and its effect.
- Target at least **27 of 30 usable requests in each of three qualification repeats**, not merely 90% when pooled. Report custom-type, gap-control and regression categories separately so easy controls cannot hide poor expansion coverage; custom-type cases must also reach at least 18/20 per repeat, and all gap controls must avoid unsupported claims. At n=30 one failure is 3.33 percentage points: the previously discussed ±0.50–0.75 point tolerance cannot be meaningfully resolved by this small batch. Do not claim population-level 90% reliability.
- No newly introduced critical failures, and no repeatable regression in baseline-supported requests. A noisy one-off difference requires matched-plan diagnosis; do not dismiss it or silently tune.
- Report cold/warm latency, p50/p95 and failures for each arm; flag a >20% warm median increase for review as a provisional expansion budget, not an established product SLA.
- Even a pass means a bounded expansion candidate is ready for an explicit adoption decision, not that the installed DB can be replaced automatically. Retain the accepted artifact for rollback and never modify model weights.

## Remaining evidence gates

No candidate DB, retrieval comparison, real-agent answers, Angular compilation, or new runtime compatibility evidence exists yet. If generated implementation snippets are included in the later answer rubric, compile a minimal self-contained fixture for the claimed setup and exercise control updates; otherwise label them source-grounded guidance, not a runtime-qualified recipe. Material and non-Material patterns require separate expectations.
