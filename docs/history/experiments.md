# Repository experiment history

The active library-information service is the [Formly MCP POC](../../poc/contextual-kb/mcp_foundation/README.md). Its [experiment history](../../poc/contextual-kb/history/EXPERIMENTS.md) covers question planning, GLiNER training, retrieval selection and real-agent qualification. The portable skill and application-indexing tools under skill/ask-formly remain a separate codebase and are not imported into the POC.

## Earlier application-indexing work

Initial work established pinned Formly 6.3.12/Material references, static Angular/TypeScript discovery, scope-qualified registrations, freshness checks and reviewed source records. Public Angular/Nx corpus trials expanded provider/signal/async discovery and workspace coverage. Source inspection, static candidates and executed browser evidence were kept distinct. The older Angular browser qualification retained two known failures (B06/B13); cleanup does not turn those into passes.

Subsequent experiments compared direct code-tool work with project-local lookup, reusable records and a local MCP. Lexical/hybrid matching, source snippets, pagination and persistent search resources improved specific lookup costs. One 24-query MCP reuse trial reported 54.5% lower median lookup latency. These isolated timings did not establish better end-to-end answers or eliminate setup/freshness costs.

Packet and workflow experiments repeatedly found the same limitation: smaller packets and fewer calls did not reliably produce complete answers. One compact workflow reduced returned data 61.5% but remained 14.2% slower than code tools. Later request-focused checks also stayed slower or incomplete. A source-context 20-question trial produced 7/20 complete assisted answers versus 10/20 for the comparison, failing its gate. These are historical panel-specific comparisons, not a current accuracy score.

Research then examined focused source views, candidate records, authored facts, retrieval accuracy and knowledge engines. Controlled trials separated corpus gaps, candidate-retrieval misses, evidence-selection losses and caller omissions. This motivated the isolated contextual-KB POC: a library source of truth rather than an application codebase investigator.

## What remains supported versus archived

- Active portable skill source, project-index/MCP/search regression tests, supplier/runtime fixtures and current maintenance tools remain in place. Pending active indexing edits are not silently reverted or deleted.
- Core extraction/public-corpus provenance and the small original historical research snapshots remain. They explain older evidence and preserve source inventories.
- Obsolete benchmark runners/fixtures, generated run trees, large machine-readable trial results, repeated proposal documents and superseded POC experiments are removed from the active tree after verified recovery archiving.
- Sealed evaluation, the working POC's accepted model/DB files and working environments remain protected. The POC never imports the portable skill's implementation.

## Process and interpreting numbers

Trials used frozen inputs/criteria, first-response retention, matched comparisons, repeated batches, TDD, independent review and explicit unresolved failures. Repeats are correlated. Speed, annotation F1, plan usability, retrieval recall and final-answer completeness are not interchangeable. Later successes do not retroactively erase failed gates or prove unseen performance.

The pre-cleanup POC source is remotely recoverable at commit `e1e4e9c5b37dfe16e9b70f9bd1f01aaf1bcf2819` on draft PR #2. Large model/runtime/raw artifacts are in verified local recovery archives, not the public Git repository. The ignored `local/poc-safety/2026-10-24/` directory contains archive checksums and exact removal inventories. This is protection against cleanup mistakes on this machine, not an off-machine binary backup.
