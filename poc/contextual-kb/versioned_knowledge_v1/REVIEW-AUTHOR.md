# Author Explanation

## Intent and success criteria

Implement the existing versioned-knowledge plan as an opt-in candidate, without
installing it or adding real release coverage. Preserve foundation8's 93 facts,
conditions, limits, evidence, source offsets, links, ranking and citations.

## Plan-to-implementation traceability

- Reconciled remote PR8 as merged at d5a82fac, fetched origin/main, confirmed no
  tree difference from prior accepted head, and branched codex/versioned-knowledge.
- baseline.json captures commit, schema/input hash, counts, installed DB hash,
  690 tracked-file hashes and 89 foundation pins. rollback.sqlite is a byte copy.
- compiler.py migrates copies, compiles format/schema2, stores normalized explicit
  applicability/evidence links, and validates replaces. Installed compiler and
  canonical authored records are untouched. Candidate catalog retains provenance.
- index.py embeds each fact once per index and applies request eligibility before
  channel truncation. Each scope has a restricted facts dictionary, so inherited
  related expansion and selector candidate presentation remain scoped. citations
  reject out-of-scope IDs and add evidence-release/applicability metadata.
- backend.py reuses original GLiNER advisory, repair selector and integrity checks;
  source_quote and final citations enforce the candidate scope. Only its explicit
  candidate path is used. No installed launcher routing changes.
- context.py reuses original settings and release gate before dispatch. Candidate
  server preserves tool argument surface; core requests now restrict to core.
- qualify.py compares fixed public queries and canonical contexts, not sealed data.
- smoke.py exercises real stdio MCP with hosted planner/selector and both native
  frozen extractors. Live run is ongoing; results are not yet claimed passing.

## Decisions and invariants

The temporary legacy projection deliberately normalizes document version only for
legacy structure/provenance validation, then restores original document values.
It never supplies applicability. Separate validation checks explicit scopes and
supporting evidence releases. Evidence record_json stays byte-equivalent as stored;
new evidence_releases carries release labels. Existing source hash/quote checks
are reused. This avoids mutating an installed pinned compiler for an experiment.

Direct means pinned evidence in the authored scope, not universal compatibility.
Migration carries existing baseline-specific support as exact 6.3.12; it does not
claim v6 or v7. The synthetic multi-version tests make no library claims.

Candidate publication uses atomic exclusive hard-link creation in the same
filesystem; existing destination paths/symlinks cannot be replaced. No promotion
command exists. Rollback is preservation of old code plus unchanged installed DB;
restoring the private rollback copy is not exercised against the installed path.

## Verification performed

Observed RED import failures for new compiler, index, and context modules; then
GREEN. First context command failed on Python import-path setup, corrected before
recording the intended module-missing RED. Full real migration initially rejected
source_inputs metadata; added failing provenance regression then corrected it.
Current 11 tests pass; malformed-applicability cases are subtests.

comparison.json: six legacy tables equal, deterministic candidate builds,
105 fixed queries, 630 exact ranking comparisons, 105 citation comparisons,
related expansion parity, unsupported v7, 690 tracked/89 foundation pins unchanged.
maintenance.log: existing project check passed (167 source, 133 runtime, 89 doctor).

Initial smoke failed before planning because sandbox prevented Codex app-server
initialization. Receipt retained in smoke-sandbox-failed*. Authorized execution
outside sandbox now running. Do not infer success until smoke-summary.json exists.

## Limits and costs

This remains an isolated migration candidate, not promoted support for newer
Formly. Current catalog gate and backend intentionally accept only 6.3.12.
Future real release admission must provision and qualify routing. Candidate tests
are invoked separately; existing source-manifest and CI remain unchanged.
Native index construction uses same frozen model/configuration; embeddings are
recomputed in memory, not persisted or modified. Adapter-specific services own
separate index/extractor instances; sharing across services is future optimization.
105 queries are regression checks, not independent answer accuracy evaluation.
No calling-agent answer score is claimed for the operational MCP smoke.

## Challenge points

Review all applicability failure cases, replacement chains, scoped selector/citation
paths, fact-version versus evidence-release semantics, deterministic provenance,
context dispatch/cancellation and asset preservation. Review fixture sufficiency,
not just the passing count. Live receipts and rollback verification are final gates.
