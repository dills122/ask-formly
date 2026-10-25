# Versioned knowledge: proposed DB and compiler plan

Status: **proposal only**, agreed direction as of 25 October 2026. This document
does not authorize migration, rebuilding the installed DB, changing authored
knowledge, or adding v7 coverage. Implement it in a separate change after the
current main-checkout knowledge work is merged and the baseline is reconciled.

## What is already implemented

[Project/worktree settings and version matching](project-settings.md) provide
persistent version/adapter settings, npm-style matching and explainable coverage
errors around the existing MCP flow. The runtime catalog still contains only
6.3.12; major fallback is implemented but disabled for this knowledge sample.
The current PR changes neither the knowledge DB/schema nor compiler inputs.

## Intended model

Support a few curated major versions, adding minor boundaries only for important
behavior changes. Keep one SQLite knowledge database and one copy of each unique
fact. Separate a fact's supported scope from the exact release of its evidence.

| Record | Proposed responsibility |
| --- | --- |
| Fact | Stable ID, claim, conditions, limits and adapter context; existing provenance retained |
| Applicability | Fact ID, scope kind/value, direct/inferred basis and optional rationale |
| Evidence | Existing evidence identity plus pinned source release, location, quote and hash |
| Applicability–evidence link | Evidence supporting a particular applicability decision |
| Fact relationship | Existing `see_also`, plus `replaces` for changed behavior |

Initially support two scope forms: `exact` (for example `6.3.12`) and `major`
(for example `6`). Exact scope preserves today's evidence boundary during
migration. Major scope supports the intended authoring model. Defer arbitrary
ranges and minor exception syntax until a concrete requirement warrants them.

Applicability is an explicit authoring decision. `direct` means directly
supported by pinned evidence, not that every patch in a major was tested.
`inferred` requires an authored explanation and linked supporting evidence.
Neither the compiler nor runtime may create or widen applicability automatically.
There is no automatically expanding `6–latest` scope.

## Illustrative authored representation

This is synthetic structure, not a verified Formly claim. Final field names and
placement are to be settled against the merged compiler before implementation.

```json
{
  "id": "example/preserve-value",
  "claim": "Option X preserves a hidden field's value.",
  "conditions": ["Option X is enabled"],
  "limits": ["Does not describe control registration"],
  "applicability": [
    {
      "scope": {"kind": "major", "value": "6"},
      "basis": "direct",
      "evidence_ids": ["example/source-v6"]
    },
    {
      "scope": {"kind": "major", "value": "7"},
      "basis": "inferred",
      "reason": "Reviewed the relevant v7 source; found no change affecting this claim.",
      "evidence_ids": ["example/source-v6", "example/review-v7"]
    }
  ]
}
```

Each evidence ID identifies a pinned source record with its own exact release,
source path, hash and quotation. Reusing that record does not duplicate it.
If the behavior or its conditions differ, create a separate fact with its own
applicability and a `replaces` link to the earlier fact. Keep the earlier fact.
Adapter restrictions remain independent of version applicability.

## Implementation sequence

### 1. Reconcile the baseline after the main work merges

- Start from the merged source, compiler, retrieval code and accepted manifests.
- Record the commit, schema version, input hash, DB hash, counts and coverage.
- Preserve a rollback copy and verify it against the accepted manifest.
- Identify every active query and citation consumer of the current schema.

This worktree's settings tests used the original 46-fact DB. The main checkout
had a newer 56-fact DB when inspected. Those numbers are observations, not target
counts: use the accepted dataset at implementation time. Never overwrite newer
knowledge with the older snapshot or repin a mismatched DB to make checks pass.

### 2. Add schema and authored-format support using fixtures

- Retain fact IDs and existing content/provenance columns where practical.
- Add normalized applicability and applicability–evidence relationships with
  foreign keys and uniqueness constraints.
- Extend fact relationships with `replaces`; reject self-links and cycles in
  replacement chains. Existing related-fact links retain their meaning.
- Version the authored format and compiled DB schema explicitly. Keep old-format
  reading only as needed for a deterministic migration; never silently interpret
  an unsupported format or schema as the current one.
- Keep the mutable project-settings database separate.

Compiler checks must reject missing evidence or facts, invalid/duplicate scopes,
unknown bases, missing inferred rationale and broken relationships. Keep current
source-hash, exact-quote and citation checks. Evidence belonging only to another
release cannot directly establish an exact-release claim; such reuse needs an
explicit inferred decision. Compiler validation checks structure/provenance, not
the truth of an author's compatibility judgement.

### 3. Convert the accepted facts without changing their meaning

- Produce a reviewable transformation of the accepted authored records.
- Preserve IDs, claims, conditions, limits, source bytes/paths/hashes, evidence
  identities, adapters and existing links.
- Translate current document-level version association into exact applicability
  for each fact. Link the same supporting evidence through that applicability.
- Do not convert exact 6.3.12 support into general v6 support during migration.
- Preserve any already-authored limits; do not label questionable evidence
  `direct` automatically. Stop and report records that cannot map faithfully.
- Require deterministic output and an idempotent migration (or explicit rejection
  of already-migrated input), with no writes to the installed DB.

### 4. Compile a candidate DB and adapt the retrieval read path

Build a separate candidate artifact using the existing temporary-build and
integrity-check pattern. Produce a build receipt and comparison report before
promotion. Do not reseed the installed DB as part of a question call.

Determine eligible fact IDs from resolved version scope and adapter before
ranking/truncating both lexical and dense results. Apply the same eligibility
rules to related-fact expansion, selection and citations. Search/index each fact
once; reuse unchanged embeddings only when their text and model/configuration
match. Keep unsupported scope failures explicit.

A selected source baseline is not the only permissible evidence release:
explicit applicability may make a shared fact eligible across majors. An
exact request must respect any future known boundary instead of inheriting
unqualified whole-major guidance. Major-only requests spanning such a boundary
must get conditional guidance or an explainable ambiguity result.

Maintain existing fact/citation response fields for current consumers. Add
applicability metadata without dropping qualifications or relabelling an evidence
source's actual version. Adding a catalog entry alone must not enable a backend
or coverage that has not been provisioned and accepted.

### 5. Verify before promotion or v7 authoring

| Test | Required outcome |
| --- | --- |
| Old/new semantic export comparison | Same accepted facts, IDs, content, evidence, adapters and relationships |
| Provenance validation | Every original source hash and quotation still validates |
| Synthetic shared fact | Eligible for two explicit major scopes, indexed once |
| Inferred applicability | Missing rationale/support fails; explicit authored decision survives compilation |
| Changed behavior | Separate facts and `replaces` relationship retain correct eligibility |
| Version/adapter filtering | Ineligible facts cannot enter lexical/dense top-k, expansion, selection or citations |
| Fixed prepared queries against old/candidate DBs | Same baseline eligible facts, ranking and citations, with timing excluded |
| Legacy, explicit-version and saved-project MCP calls | Existing baseline flow works and preserves response contracts |
| Unsupported v7 request | Still returns a coverage error; no silent older-version answer |
| Build/migration failure | Installed DB untouched; no partial promotion |
| Rollback rehearsal | Old code/schema and matching DB/manifest can be restored together |

Run `python3 tools/project.py check`, both native extractor checks and live MCP
smokes with the provisioned assets. Use synthetic fixtures and already-public
diagnostic requests; do not open sealed evaluation. Compare deterministic
retrieval using identical prepared inputs. Hosted planning can vary, so separate
its operational smoke results from exact retrieval parity and answer quality.
Keep existing historical failures, including B06/B13, visible.

### 6. Promote as a separate reviewed step

After the comparisons pass, publish the candidate and updated schema/build pins
as a coordinated code/data change. Stop or restart existing readers during the
switch; do not leave an old process using incompatible code and database state.
Retain the prior DB, compatible code revision and manifest for rollback. Run
doctor and live baseline smokes after the switch.

The release catalog remains at the existing accepted coverage. Adding v7 evidence,
reviewing general v6 applicability and enabling major fallback are subsequent
authoring changes, not consequences of the schema migration.

## Completion criteria

The migration is complete only when the merged baseline is preserved, compiler
and retrieval tests pass, real baseline calls succeed, rollback is recorded,
and unsupported v7 remains unsupported. Do not begin this implementation until
the preceding main-checkout work is merged and the baseline has been selected.
