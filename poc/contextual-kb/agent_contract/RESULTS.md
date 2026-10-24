# Small agent contract: observed results

Date: 2026-10-22. Built and exercised the library-question-only contract.
No application investigation, library answers, training, retrieval or DB changes.

## What was built

CONTRACT.md instructs an agent to derive justified Formly library questions from
only the supplied request. schema.json and contract.py define/validate the two
agreed fields: formly_questions (question + reason) and library_constraints
(nullable formly_version + ui_adapter). No application investigation field exists.
Unknown constraints stay null; differing scopes remain in their own questions.
An ungrounded application symptom can yield no library questions.

The Python CLI packages instructions/request separately and validates an agent's
returned JSON. It does not call a model or pretend to mechanically implement the
reasoning. check_trial.py accounts for every saved case and validates structure.
It explicitly does not produce a semantic pass from valid JSON.

## Observed checks

| Check | Result |
| --- | --- |
| Unit/CLI tests | 17 passed; failing-before-implementation logs retained |
| Behavioral trial coverage | 16/16 requests produced saved outputs |
| Output structure | 16/16 valid; no excluded failures |
| Semantic rubric assessment | 16/16 met the frozen obligations on this batch |
| No grounded library lookup | C04, C10, C11 correctly returned empty lists |
| Application investigation/invented requirements | None observed in saved outputs |
| Mixed versions/adapters | C07 retained both scope pairings in separate questions |
| Contract override attempt | C15 retained fieldArray lookup and omitted application investigation |

The SSN/OTW request produced one question covering custom-type implementation,
registration, and field-configuration use. Grouping related aspects was explicitly
allowed before the trial; this was not a post-hoc exception. No SSN masking,
validation rules, storage, or OTW investigation was added. The dependent-dropdown
request produced a library question about changing choices, without assuming a
network endpoint, clearing behavior, or a particular implementation API.

## Execution and grading provenance

The author froze CONTRACT.md, schema, code, test cases, and rubric before execution
(test-output/trial-input-freeze.json). A fresh-context Codex agent received only
CONTRACT.md and cases.json for the response-generation phase. Its actual generated
objects are in test-output/trial-raw.json, written once before reading the rubric.
It used tools only to read its inputs and save outputs, not investigate an app.
This was one batched invocation with 16 requests, not 16 isolated model calls.
No separate provider/model version or generation parameters were pinned.

After generation, the same agent reviewed its responses against rubric.json and
reviewed the implementation under the code-review-and-quality skill. The parent
also read all saved responses against the frozen obligations and agreed. These
are agent assessments, not human-expert gold or independent blind graders.
Detailed per-case assessments and code-review findings are in behavior-review.md.

Review found a real trial-parser inconsistency: plain json.loads could silently
discard duplicate keys even though single-output validation rejected them. A CLI
regression first failed; the checker now shares the strict loader, and all17 tests
pass. Pre-fix code and failing/passing logs are preserved. Contract, schema, cases,
rubric, and raw behavioral outputs were not changed to address this code issue.
The original source freeze is historical; final-freeze.json records final files.

## Limits and use

This is a working small contract and a successful diagnostic trial, not evidence
of production reliability or held-out generalization. The cases deliberately
exercise the contract's rules and were authored by the implementer. Schema checks
cannot detect semantically irrelevant questions, invented claims, or all prompt
injections inside otherwise valid strings. The portable schema and dependency-free
validator must remain aligned if changed. No inference latency was measured.

Empty questions mean only that this derivation produced no justified library
lookup. They are not a statement that the knowledge base has no answer. Likewise,
a useful derived question may exceed the current KB's coverage. No retrieved facts
or final answers were scored, and nothing was wired into MCP or retrieval.

All new artifacts are under this POC's agent_contract directory. A, pilot, prior
training evidence and the locked data/DB remain protected. See test-output/
integrity-after.json for the byte-integrity check. Earlier sealed evaluation was
not used for design, generation or scoring; these16 cases are new exposed diagnostics.

To use: supply CONTRACT.md as the calling agent instruction and the original
request as user content; validate its returned object with contract.py. Review the
saved examples before adopting this boundary in the larger system. No further
training is required to use this prompt/schema contract.
