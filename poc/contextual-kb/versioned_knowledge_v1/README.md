# Versioned knowledge: isolated candidate

This is an opt-in implementation of [the versioning plan](../../../docs/versioned-knowledge-plan.md).
It does not alter the installed foundation8 DB, compiler, models or launcher.
No new Formly release coverage is claimed. The accepted catalog remains 6.3.12.

## Data contract

Authored schema 2 retains all previous document/fact fields and adds a nonempty
`applicability` list per fact. Each entry contains `scope: {kind, value}`,
`basis` (`direct` or `inferred`), and nonempty `evidence_ids`. `reason` is required
for inferred support. Scope kind is `exact` with a stable exact release or `major`
with a major number. No ranges, prereleases, automatic widening or minor exceptions.

The catalog keeps existing records/source provenance, uses schema_version 2, and
adds `evidence_releases`, mapping each evidence ID to its exact pinned release.
Existing evidence records are retained intact. The compiler cannot establish the
truth of an authored compatibility judgment; source review remains necessary.

Compiled schema 2 retains old content tables/FTS and adds `applicability`,
`applicability_evidence` and `evidence_releases`. `fact_links` additionally permits
`replaces`. Missing references, cycles and scope overlap anywhere in a replacement
chain fail compilation. Do not use replacement links to resolve conflicting facts
at retrieval time. The author must supply non-conflicting supported scopes.

Migration converts schema 1 documents into copies with exact 6.3.12 applicability.
It does not expand to major 6. Existing source content, IDs, quotes, evidence and
links remain unchanged. Repeated migration into the same destination and database
overwrite are rejected. The temporary legacy projection exists only to reuse the
accepted content/provenance validation and unchanged FTS construction.

## Retrieval and MCP

The candidate index embeds each unique fact once. A request scope restricts the
fact dictionary, lexical eligibility and dense vector rows before top-k. The same
restriction governs related expansion, selector candidates and citations. Returned
facts/citations add `applicability`; existing `version` remains the document's source
version, never relabeled to the requested release. Linked evidence includes its
actual source release. Material includes core knowledge; explicit core excludes
Material. No adapter filtering is silently inferred from question text.

The opt-in server reuses the accepted planner, optional capitalization repair,
advisory GLiNER extractors, full-question retrieval and bounded selector. Existing
project/version resolution runs before hosted calls. Unsupported v7 still returns
an explicit coverage result. The candidate backend deliberately only provisions
6.3.12. A future release requires source review, catalog/routing admission and
qualification; changing catalog entries alone cannot enable it.

## Reproduce

Run from repository root in the provisioned checkout:

```sh
export PYTHONPATH=poc/contextual-kb:poc/contextual-kb/mcp_v1
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/versioned_knowledge_v1 -p 'test_*.py'
python3 -B tools/project.py check
poc/contextual-kb/mcp_v1/.venv/bin/python -B -m versioned_knowledge_v1.verify
```

`test-output/baseline.json` records the reconciled merge, original DB/schema/input
hash, counts, 690 tracked source pins and 89 foundation asset pins. `rollback.sqlite`
is its verified byte copy. These private checkpoint inputs are not public assets.
To repeat the complete migration and ranking comparison without overwriting the
first candidate, create a fresh output directory, copy those two checkpoint files
into it, and run `qualify.py --output <new-directory>`. It checks the frozen pins,
migrates canonical inputs into that directory, builds two candidates, compares
all old semantic tables and 105 fixed prepared queries. It does not open evaluation.
For a new accepted baseline, deliberately reconcile and create a new checkpoint;
do not edit old pins to conceal drift.

Real hosted smoke (provider access required):

```sh
poc/contextual-kb/mcp_v1/.venv/bin/python -B poc/contextual-kb/versioned_knowledge_v1/smoke.py
```

This uses an isolated settings DB and candidate stdio server, both native seeds,
legacy/explicit/saved version calls and unsupported v7. It sends only the displayed
public development requests and candidate facts to the existing hosted providers.
Use a fresh copied experiment directory or retain prior receipts before rerunning;
the smoke filenames are per case, not an append-only run history.

## Promotion and recovery

Promotion is not included or authorized here. Before adoption, coordinate schema,
readers, authored/corpus format, source/runtime pins and tooling in a separate
reviewed step. Stop existing readers before switching incompatible code and DB.
Retain the matching old code revision and manifest with the rollback DB; never
repin old code against a new schema. The isolated recovery rehearsal opens a
restored snapshot with the unchanged legacy index and verifies public queries.
The installed path is never used as a restore target by these scripts.

Candidate tests remain separate from installed CI/packaging. All generated DBs,
model caches, migrated copies and raw provider receipts stay under ignored
`test-output/`. Historical failures, including B06/B13, remain unchanged.
