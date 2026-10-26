# Versioned knowledge candidate

Authorized scope: implement the versioned-knowledge proposal with TDD, an
isolated candidate and independent review. No promotion, installed DB writes,
model changes, new real release claims, or sealed evaluation access.

Baseline: merged PR8, d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2,
foundation8, 93 facts / 21 documents, schema 1. Detailed hashes, counts and
rollback DB are private under test-output/. Existing tracked files and all
foundation assets are pinned before work.

Implementation stays in this opt-in package so the accepted compiler, authored
records and runtime remain unchanged. Format/schema 2 adds explicit exact/major
applicability and supporting evidence releases, and replaces relationships.
The legacy compiler is reused for provenance validation and unchanged fact/FTS
construction through a temporary format-1 projection; version eligibility is
validated separately and never inferred by that projection.

1. Tests first: strict format/provenance/scope validation, migration preservation,
   deterministic builds, no overwrite, and replacement graph validation.
2. Candidate compilation: migrate copies of all accepted records to exact
   6.3.12; preserve all five existing semantic tables and source bytes.
3. Opt-in index/backend: eligibility before lexical/dense limits, expansion,
   selector candidates and citations. Shared facts embedded once. Keep existing
   response fields and add applicability metadata; evidence versions stay exact.
4. Compare fixed prepared public diagnostic queries and baseline citations;
   test synthetic two-major sharing and changed behavior. Run maintenance,
   native extractors and real MCP smoke without sealed questions.
5. Fresh-context independent review (maximum three instances). Record results,
   limitations and promotion/rollback requirements. Leave installation untouched.

The current release catalog stays at 6.3.12. Broad requests resolve through the
existing resolver to a provisioned release; this candidate does not invent minor
boundaries or enable v7. A future major scope overlapping a changed-behavior
replacement is rejected until a more precise boundary contract is designed.

## Completion

All five steps completed. Review1 found transitive replacement overlap; the TDD
fix passed review2 (Ready). See RESULTS.md and REVIEW-FIX-FINAL.md. No promotion,
commit or push performed. Existing coverage remains exactly 6.3.12.
