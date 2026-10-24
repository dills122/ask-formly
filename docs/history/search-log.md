# Search coverage

Access date: 2026-10-15. This was a bounded discovery pass, not an exhaustive audit of every public or private skill.

## Web queries performed

Twenty-four targeted web queries were issued in six batches. Quotes below preserve the query wording; some engines returned loose or irrelevant matches despite quoting.

| Batch | Queries | Useful outcome |
| --- | --- | --- |
| 1 | `"formly" "SKILL.md"`; `"formly" "agent skill"`; `"formly" "MCP" server`; `ngx-formly v6 documentation version 6` | Located official v6 docs and unrelated Formly products. |
| 2 | `"formly" "SKILL.md"`; `"ngx-formly" "skill" "Claude"`; `"ask-formly"`; `"ngx-formly" "cursor" rules` | OpenEMS testing-skill lead; no verified dedicated expert. |
| 3 | `"formly" site:skills.sh`; `"formly" site:github.com "SKILL.md"`; `"ngx-formly" "Claude" skill`; `"formly" site:context7.com` | Angular skill directory results; traced relevant entries to original repositories. |
| 4 | `"ngx-formly" "agent" "skill" github -site:mail-archive.com`; `"formly" site:skillsmp.com -angular-forms`; `"formly" "MCP" "ngx"`; `"formly" "cursorrules"` | Formly Contract and ng-forge surfaced; inspected original project material. |
| 5 | `"ngx-formly" "Context7"`; `"formly" "skill" site:github.com -awesome-angular -mail -texera`; `"formly" "agent skills"`; `"ngx-formly" "llms.txt"` | Verified Context7 listings; no dedicated v6 LLM corpus established. |
| 6 | `"ngx-formly" "expert" "skill"`; `"formly" site:skills.sh -angular-forms`; `"formly" "SKILL.md" -site:awesomeskill.ai -site:skillsmp.com -site:aiagentskills.net`; `site:angular.dev ai mcp read-only search_documentation version` | Rechecked dedicated candidates; Angular CLI MCP is adjacent framework tooling. |

## Direct GitHub and registry checks

GitHub REST repository search was performed without credentials:

- `"ngx-formly" skill in:name,description,readme`: 20 repositories, `incomplete_results: false`; all result names inspected. Results included Angular resource lists, application repositories, and other form libraries. These were not all source-audited.
- `"ngx-formly" mcp in:name,description,readme`: 14 repositories, `incomplete_results: false`; all result names inspected. Relevant candidates included `dills122/formly-contract` and `ng-forge/ng-forge`.
- Broader `formly skill`, `formly mcp`, quoted `formly`, and `ask-formly` queries returned many irrelevant form/skill/ask matches. Their counts were not used as evidence of availability or absence.
- GitHub code search for `"ngx-formly" filename:SKILL.md` returned HTTP 401. No authenticated global code-search claim is made.

Original skill files were read for Angular, Analog, and OpenEMS. The Formly Contract README was read directly from its repository after a web fetch failed. npm package metadata, the v6 tag object, tagged types, license, and changelog were retrieved directly. The [source table](sources.md) retains URLs and revisions.

## Interpretation and limits

No portable, general-purpose v6 ngx-formly expert skill was verified. A real application-specific Formly testing skill was found. Catalog searches are index-dependent; private skills, poorly indexed repositories, embedded skills without a README mention, and recently published work can be missed. Repeated catalog copies are not independent implementations.

The public repository metadata and docs were inspected; candidate packages were not installed and their advertised behavior was not tested. A marketplace listing for Formly Contract presented it as an MCP server, while its original README explicitly says a production MCP server is not shipped [S18]. The original source governs this comparison.

Stop condition reached: enough evidence exists to choose a reversible first prototype and its evaluation gate. Further broad searching is unlikely to change that next step. Reopen discovery if a specific maintained v6 skill with inspectable source and tests is supplied.

## Deep operational research — 2026-10-15

Shifted from competing-skill discovery to upstream v6 behavior. Web discovery and direct upstream issue/comment reads covered performance and formState, expression timing, async options and validation, hidden fields and arrays, parsers, Material styling/custom controls, standalone setup, hydration, and JSON Schema. The retained issue IDs, dates, URLs, individual comment links, evidence limitations, and content hashes are in the [discussion index](skill/ask-formly/references/discussions.md) and its JSON companion. Counts: 25 cases, 85 comments; four fix diffs inspected. Linked screenshots and StackBlitz applications were not executed or treated as verified reproductions.

Expanded pinned source reading to 83 records across 74 files and 13 official example walkthroughs. Used graph-first structural navigation and direct reads for uncovered docs/examples/tests. Added 17 custom executed probes after source inspection; these are separate from upstream reported reproductions. The bounded stop rule in [task_plan.md](task_plan.md) is satisfied; runtime and answer-quality gaps remain recorded in [coverage](skill/ask-formly/references/coverage.md).
