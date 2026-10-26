# Versioned knowledge candidate results

Status: implementation and qualification complete; independent review2 **Ready**
with no remaining actionable findings. Not promoted. No real release beyond 6.3.12 has been admitted.

## Reconciled baseline

PR8 was verified merged before implementation. Branch codex/versioned-knowledge
starts at d5a82fac7d03136137fbafa7c7faeeb15dbfa1c2. Installed foundation8 has
93 facts / 21 documents, 53 evidence records, 141 fact-evidence links and 81
related-fact links. Schema1 input hash:
`15249496618a06a4728ca81b6b8d1b743c7f1bd6bd93bafde0b20029597ccbed`.
Installed DB SHA256:
`cc67af9eba6daa5024d671dd306dfd4ada4193e2663e05737d4db2bc39d9d63d`.

All 690 tracked-file pins and 89 foundation/asset pins remain unchanged. The
candidate is entirely additive in this directory. The installed DB, models,
compiler, canonical knowledge, runtime manifests and evaluation remain unchanged.
Sealed evaluation and qualification archives were not opened.

## Candidate and deterministic checks

Schema2 candidate DB SHA256:
`a0f102f1bad83dfec7c91148925187644e3092a3ca08cdaa88f586a7e1a0c106`.
Migration preserves exact 6.3.12 support; it does not assert whole-v6 compatibility.
All 93 facts have exact applicability, linked to the existing supporting evidence.

| Check | Observed result |
| --- | --- |
| Original semantic tables | documents, facts, evidence, fact_evidence, fact_links and facts_fts equal |
| Repeated compilation | Byte-identical databases |
| Fixed prepared queries | 105: 12 public diagnostics plus 93 existing fact contexts |
| Rankings | 630/630 exact lexical/dense/hybrid comparisons at limits 8 and 20 |
| Citations | 105/105 original citation payloads unchanged; applicability is additive |
| Related expansion | Matching baseline when room remains in the packet |
| Unsupported v7 | No eligible facts; MCP rejects before hosted planning |
| Candidate unit tests | 13 passed, including malformed-input subtests |
| Existing maintenance | 167 source tests, 133 runtime tests, 89 doctor pins passed |
| Post-fix rebuild | Identical to the tested candidate |
| Isolated rollback | Legacy reader reproduced 12 public-query rankings from restored snapshot |

The fixture tests cover sharing one fact across explicit major scopes, inferred
rationale/support, direct evidence scope, malformed/duplicate scopes, unchanged
provenance, no overwrite, replacement cycles and overlapping ancestors, filtering
before top-k, cross-scope citation/expansion rejection, selector candidate/fallback
containment, and project/version/adapter routing.

## Real MCP operational smoke

The candidate stdio server ran the accepted hosted planner and selector with
native GLiNER seeds 1701 and 1702. Each seed completed three supported requests:
legacy lookup, explicit 6.3.12/core lookup with saved project settings, and a
lookup reusing those settings. All six returned eight facts with citations,
applicability metadata, available advisory extraction, successful selection and
unchanged model parameters/DB. Both separate v7 calls returned unsupported_version.
Explicit/saved core responses contained only core facts.

This establishes operational compatibility, not calling-agent answer accuracy.
There was no new answer-quality score or sealed evaluation run.

The first attempted smoke failed before generation because the sandbox blocked
the provider client's initialization. Its logs were retained separately; it is
not counted as success. The authorized outside-sandbox run then completed all
checks. No provider or model settings were changed to obtain a pass.

## TDD and review history

Initial missing-module RED tests preceded compiler/index/context implementation.
The first complete migration exposed unhandled catalog source_inputs metadata;
a failing provenance regression preceded the correction. The earlier context
command's import-path setup error was corrected before its intended RED run.

Review1: Not ready, one P2 finding. Immediate-edge replacement checks missed
transitive overlap (major6 -> major7 -> exact6.3.12), allowing conflicting facts
into one scope. The failing regression is retained in ancestor-red.txt. The fix
checks every ancestor and passes all13 tests. No runtime behavior changed after
live smoke. The reviewer independently verified preservation, 72 rankings and
12 citation comparisons, and the native/live receipts.

Review2: **Ready** for the isolated candidate scope; no actionable findings remain.
It independently verified 13 tests, existing maintenance, preserved pins, identical
rebuild, semantic tables, 72 rankings, 12 citation comparisons, 12 rollback queries
and all eight raw live receipts. See REVIEW-FIX-FINAL.md.

## Next boundary

This candidate has passed independent review and is ready for a separate promotion
decision. Promotion requires coordinated readers/schema/authored-format/manifests
and restart/rollback handling in a separate authorized change. Existing launcher
and installed DB still serve foundation8. Older/newer Formly sources, general
major-version applicability and catalog expansion are separate reviewed admissions.
Historical failures, including B06/B13, retain their original status.
