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

## Maintenance and historical implementations

`python3 tools/project.py source` runs the ledger, eligibility and assessment fixture tests along with retained promotion and compiler regression suites. These tests do not call hosted models or open sealed evaluation. `python3 tools/project.py check` additionally verifies the installed runtime assets and runs local regressions.

`assess_run.py` remains a reusable adapter for compatible reviewed batch assessors. It binds cached results to exact request/rubric fields and rejects incomplete attempts or path aliases rather than silently regrading. `eligibility.py` checks the frozen runtime version/adapter profile against a candidate without loading models. These checks complement source compilation; neither certifies answer quality.

For current admission steps use [RUNBOOK.md](RUNBOOK.md). Old batch commands, red/green logs and historical test counts are retained at [checkpoint5dc8a89](https://github.com/dills122/ask-formly/tree/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion/admission). They are historical evidence, not today's provisioning instructions.
