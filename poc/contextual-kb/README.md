# Formly knowledge source-format POC

This isolated POC is testing a **fact-first authored source format** for a future
Formly knowledge MCP. The starting knowledge and K/E evidence catalog came
from `skill/ask-formly/references/`; this trial adds four POC-local evidence
records for examples in the same pinned Formly source snapshot. No code from
prior knowledge-engine POCs is used.

The [data foundation and DB status](DATA-FOUNDATION-STATUS.md) explains the
working-session progression, active source-to-DB path, schema, checks, results,
and current boundary. This foundation is workable for the POC and paused for
now while question-to-query retrieval is investigated.
The [question-layer research](QUESTION-LAYER-RESEARCH.md) compares bounded
multi-question planning, hybrid retrieval, and whole-fact selection against
the current trial's actual misses. The [one-pass question pilot](QUESTION-PILOT-RESULTS.md)
records the isolated A/B/C comparison and its limits. It is a diagnostic
harness, not an implemented serving MCP query layer.
The [obligation-level question trial](OBLIGATION-TRIAL-RESULTS.md) compares
per-ask deterministic and local-model planning on a fixed set. Neither arm was
promoted; the report records the fact-coverage and false-support failures.
The [small-catalog bake-off](CATALOG-BAKEOFF-RESULTS.md) compares the current
eight-fact packet with broad contextual retrieval and whole-catalog selection.
It records smaller packets and one extra strict fact-set hit, plus unresolved
answer and false-support failures. No new arm is serving.

The active source files are `authored/*.json`. Seven use selected passages from
the compiled Formly material; two use POC-local source documents grounded in
the pinned default-value and custom-type demos. Their structure is
deterministic, but semantic claims still require source review.

The [review boundary](REVIEW-SCOPE.md) limits assessment to the current source
format, selected fact fidelity, validation, database seeding, and explicit DB
query shapes. Future source authoring workflows are outside this slice.

`python -m kbcompiler all` now validates these source files and replaces the
single `build/knowledge.sqlite` database atomically. It seeds facts, conditions,
limits, source quotes and offsets, K/E evidence links, and explicit `see_also`
links. It also builds FTS5 rows from each fact's contextual fields for a
[direct DB query trial](DB-QUERY-TRIAL.md). It does **not** infer facts from
prose, certify that a citation entails a claim, dissect questions, or answer
them.

## Reproduce

From this directory:

```sh
uv sync --frozen
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m kbcompiler all
.venv/bin/python -m kbcompiler.structured_audit
.venv/bin/python -m kbcompiler inspect
```

`build/` is ignored and can be deleted before a clean rebuild. `lint` validates
authored files without writing; `build` validates and seeds; `all` runs both.
The read-only audit checks the seeded rows against the authored files and their
source spans. Its trial output is saved under `test-output/`.
The old Markdown block compiler remains in `kbcompiler/pipeline.py` solely for
the earlier bounded trial and its regression tests. It is not on the active CLI
or database path. The prior results and their limitations remain in
[EXTRACTION-SPIKE.md](EXTRACTION-SPIKE.md); the format decision and current
trial are in [SOURCE-FORMAT-TRIAL.md](SOURCE-FORMAT-TRIAL.md).
The [expanded source and question trial](EXPANDED-SOURCE-TRIAL.md) records the
seven-file clean rebuild and question answerability results.
The [direct DB query trial](DB-QUERY-TRIAL.md) records the later nine-file seed,
explicit FTS query shapes, and required-fact reachability result.
