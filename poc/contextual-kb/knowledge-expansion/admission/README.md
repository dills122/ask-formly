# Repeatable source admission ledger

`ledger.py` produces and validates a source-section checklist for the three guides in the preserved import manifest. It does not edit sources, authored facts, models, or databases. It uses only the Python standard library and stays inside the POC.

## What is automated, and what remains reviewed

Admission intentionally includes semantic curation: an author decides what a source passage establishes, its version/adapter scope, conditions, limits, and whether an existing fact supplies equivalent support. A text matcher cannot prove those decisions. The ledger makes them explicit and reviewable.

The authored-source compiler already checks source hashes, exact quotations, evidence IDs and related links, and compiles controlled JSON into SQLite. Isolated batch builders snapshot inputs, refuse output-directory reuse, preserve accepted rows and check quotation offsets. This tool does not replace those reviewed mechanisms.

All imported-guide ATX heading sections, including a nonempty preamble, are derived from the manifest. Fenced code headings are ignored. Each section is pinned to its source hash, line/character offsets and section hash. Per-claim decisions record exact excerpts, status, rationale, fact IDs and review notes. Unresolved claims keep a section pending. Reviewers must assess the full section and account for omissions; the tool cannot discover omitted semantic assertions.

`admitted` and `existing_support` require references to supplied authored records. `excluded` requires a rationale and cannot claim fact IDs. `pending` is unresolved, including candidate claims not yet promoted. An optional database check establishes only whether supported IDs occur in the explicitly supplied DB; it neither compares complete records nor proves promotion. Candidate/promotion verification remains responsible for row equality, provenance and runtime qualification.

## Commands

Run from the repository root. Generate output in a new batch's `test-output/`; never overwrite frozen ledgers or experiment inputs.

```sh
python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py inventory \
  > /tmp/formly-admission-skeleton.json

python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py check \
  --ledger path/to/reviewed-ledger.json \
  --database poc/contextual-kb/build/knowledge.sqlite

python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py report \
  --ledger path/to/reviewed-ledger.json \
  > /tmp/formly-source-checklist.md

python3 -B poc/contextual-kb/knowledge-expansion/admission/ledger.py check \
  --ledger path/to/reviewed-ledger.json --require-complete

python3 -B -m unittest discover \
  -s poc/contextual-kb/knowledge-expansion/admission -p 'test_*.py'
```

The default manifest and authored directory come from this checkout. Repeated `--authored-dir` arguments can validate a candidate mapping against canonical and draft records; supplying any replaces the default. Duplicate fact IDs fail. No DB is opened without `--database`; check receipts identify its absolute path and SHA-256 and label the seeded-ID-only scope.

Both `check` and `report` validate first and exit nonzero on failures. `--require-complete` additionally rejects pending sections. A passing check without that flag does **not** mean coverage is complete. `inventory` generates only a pending skeleton; reconcile rather than overwrite reviewed decisions.

## Ledger shape

Top level: `schema_version`, `manifest_sha256`, `documents` in manifest order.

Each document: `id`, repository-relative `source`, full-file `sha256`, `sections` in source order.

Each section retains generated `id`, `heading`, `start_line`, `end_line`, `start_offset`, `end_offset`, `sha256`; review adds `status`, `rationale`, `fact_ids`, `review`, `decisions`.

Each decision: unique section-local `id`, `scope`, exact nonempty `quote` within that section, `status`, `rationale`, `fact_ids`, `review`. Decided entries require a review note. A whole-section review is also required before closure. Section fact IDs equal the union of decision fact IDs. Aggregate precedence: pending, existing_support, admitted, excluded. Mixed supported/excluded sections retain their supported mapping.

## Verification record

Tests preceded the tool; `test-output/red.txt` records the expected missing-module failure. The seeded-ID test failed on its absent parameter (`red-seeded.txt`) before implementation. The final 13 tests cover source/manifest drift, missing/duplicate/forged sections, references, quoted spans, reviews, partial coverage, duplicate decisions, exclusions and read-only seeded-ID coverage; see `test-output/final-tests.txt`.

A real-manifest smoke test produced 18 sections across three guides. Its all-pending skeleton passed structural checks and correctly reported `complete: false`. This is a mechanism check, not source admission or runtime qualification.

## Source-only CI integration

`python3 -B tools/project.py source` (and therefore `check`) runs the 13 ledger unit tests and eight promotion-v3 temporary-fixture tests. The source workflow has 53 tests in total, including a wiring regression that retains real source validation and command construction while intercepting subprocess execution to avoid recursive self-invocation. It does not open the real source ledger, candidate DBs, installed DB or models. Validate actual ledger decisions separately with the explicit commands above.

The wiring regression failed with four scheduled suites instead of six (`test-output/red-wiring.txt`) before integration; the executed full source workflow passed afterward (`test-output/green-wiring.txt`).

## Reproducible post-run assessment

`assess_run.py` invokes an existing batch's reviewed `assess.grade` and `summarize.summary` without copying their grading logic. Run it after the live jobs finish, using the provisioned MCP Python environment because the existing assessor imports the MCP harness:

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B \
  poc/contextual-kb/knowledge-expansion/admission/assess_run.py \
  --implementation extensions-v1 \
  --root poc/contextual-kb/knowledge-expansion/combined-v1/test-output/qualification-1 \
  --cases poc/contextual-kb/knowledge-expansion/combined-v1/cases.json \
  --repeats 3 --arms candidate
```

Use the actual frozen cases and output paths for the run; the example is not an instruction to create or replace a run. Both arms use `--arms baseline,candidate`. The root must be a canonical existing directory inside `knowledge-expansion/<batch>/test-output/`; cases and implementation must also stay within knowledge-expansion. Symlink aliases are rejected.

Only jobs with a receipt and no completed assessment are graded. Missing jobs remain in fixed denominators. A prior `attempt-*` without a result or an invalid existing result stops the command before any new grading; investigate explicitly instead of retrying or deleting the failed attempt. Completed results are reused. This wrapper is not a live watcher and never re-runs callers. Its `summary.json` records selected arms, repeats, input hashes and implementation hashes. It still requires independent result auditing, and automated grading invokes the existing hosted assessor.

Eight additional tests exercise orchestration with a fixture grader and the real reviewed summarizer, without provider calls. The initial missing-module red, intermediate macOS temporary-path alias failure, and final green are retained in `test-output/`. The fixture was corrected to use the canonical temporary path rather than weakening the production path guard. Admission now contributes 21 tests to source CI; source totals increase by eight to 61.

## Retrieval eligibility before live comparison

Compilation validates source records, but the frozen runtime also restricts the searchable version and adapters. This gate uses its actual constants and reads the candidate DB without constructing models:

```sh
python3 -B poc/contextual-kb/knowledge-expansion/admission/eligibility.py \
  --candidate poc/contextual-kb/knowledge-expansion/extensions-v2/candidate-build/knowledge.sqlite \
  --accepted poc/contextual-kb/build/knowledge.sqlite
```

The corrected candidate builder invokes this check automatically before writing its manifest. An unsupported adapter/version or orphaned fact fails admission; successful eligibility does not establish ranking or answer quality. The rejected extensions-v1 `mixed` document is retained as the motivating failure. Five red/green fixture tests and an actual rejected-candidate receipt exercise this boundary.

Cached assessment reuse is also bound to exact saved request and case/rubric fields. The repaired assessor orchestration rejects drift without silently regrading; twelve fixture tests include request/rubric regression cases. Current source-only CI includes all thirty admission tests and eight promotion fixtures, seventy-three source tests in total, including the three combined-runner fixtures.
