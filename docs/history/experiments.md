# Repository experiment history

The active library-information service is the [Formly MCP POC](../../poc/contextual-kb/mcp_foundation/README.md). Its [experiment history](../../poc/contextual-kb/history/EXPERIMENTS.md) covers question planning, GLiNER training, retrieval selection and real-agent qualification. The portable skill/application-inspection code is now retired. Its original reference documents remain as frozen knowledge provenance at the paths used by the current compiler. No old implementation is imported into the POC.

## Earlier application-indexing work

Initial work established pinned Formly 6.3.12/Material references, static Angular/TypeScript discovery, scope-qualified registrations, freshness checks and reviewed source records. Public Angular/Nx corpus trials expanded provider/signal/async discovery and workspace coverage. Source inspection, static candidates and executed browser evidence were kept distinct. The older Angular browser qualification retained two known failures (B06/B13); cleanup does not turn those into passes.

Subsequent experiments compared direct code-tool work with project-local lookup, reusable records and a local MCP. Lexical/hybrid matching, source snippets, pagination and persistent search resources improved specific lookup costs. One 24-query MCP reuse trial reported 54.5% lower median lookup latency. These isolated timings did not establish better end-to-end answers or eliminate setup/freshness costs.

Packet and workflow experiments repeatedly found the same limitation: smaller packets and fewer calls did not reliably produce complete answers. One compact workflow reduced returned data 61.5% but remained 14.2% slower than code tools. Later request-focused checks also stayed slower or incomplete. A source-context 20-question trial produced 7/20 complete assisted answers versus 10/20 for the comparison, failing its gate. These are historical panel-specific comparisons, not a current accuracy score.

Research then examined focused source views, candidate records, authored facts, retrieval accuracy and knowledge engines. Controlled trials separated corpus gaps, candidate-retrieval misses, evidence-selection losses and caller omissions. This motivated the isolated contextual-KB POC: a library source of truth rather than an application codebase investigator.

## What remains supported versus archived

- The application-inspection implementation, its tests/CI/release tooling and supplier demo are archived and retired by explicit user decision. Passing historical tests did not make this a selected second product.
- Small original research snapshots remain in docs/history. Detailed extraction/public-corpus reports and inventories are preserved in the private retirement archive.
- Obsolete benchmark runners/fixtures, generated run trees, large machine-readable trial results, repeated proposal documents and superseded POC experiments are removed from the active tree after verified recovery archiving.
- Sealed evaluation, the working POC's accepted model/DB files and working environments remain protected. The POC never imports the portable skill's implementation.

## Process and interpreting numbers

Trials used frozen inputs/criteria, first-response retention, matched comparisons, repeated batches, TDD, independent review and explicit unresolved failures. Repeats are correlated. Speed, annotation F1, plan usability, retrieval recall and final-answer completeness are not interchangeable. Later successes do not retroactively erase failed gates or prove unseen performance.

The pre-cleanup POC source is remotely recoverable at commit `e1e4e9c5b37dfe16e9b70f9bd1f01aaf1bcf2819` on draft PR #2. Large model/runtime/raw artifacts are in verified local recovery archives, not the public Git repository. The ignored `local/poc-safety/2026-10-24/` directory contains archive checksums and exact removal inventories. This is protection against cleanup mistakes on this machine, not an off-machine binary backup.

## Final retirement decision

The separate `poc/knowledge-engine/` tree compared Markdown-to-FTS compilation, direct source serving, reviewed decision cards, contextual retrieval and later evidence/coverage experiments. It contained 179 untracked source/artifact files when retired. These approaches preceded the accepted contextual-KB POC; they are not runtime dependencies of it. Detailed trial scores remain in archived reports rather than being reinterpreted as current performance.

The accepted contextual-KB implementation is now the primary project. Its authored knowledge, original reference provenance, corpus, transpilation/compiler implementation, tests, DB and models are preserved. The former supplier demo, application MCP/search/indexing system and knowledge-engine alternatives are archived, not maintained alongside it. Do not revive an old approach without first reviewing these historical failures and defining a new reason to test it.

A verified private archive at `local/poc-safety/2026-10-24/retirement/legacy-before-retirement.tar.gz` preserves the final legacy working tree, including uncommitted code and environments. Its inventory and SHA-256 receipt are beside it. No sealed evaluation contents were examined. This archive is local recovery, not a remote binary backup.
