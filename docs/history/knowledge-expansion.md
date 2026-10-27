# Knowledge expansion through 192 facts

The bounded retained-source milestone is complete at **192 facts / 36 documents**, exact Formly 6.3.12 core/Material. This is curated library evidence, not whole-library coverage or application investigation.

The complete pre-cleanup source, batch fixtures, runners, review handoffs and reports are retained at [Git checkpoint 5dc8a89](https://github.com/dills122/ask-formly/tree/5dc8a89f34c2deb77895db72d8e5e4abaa3b3ca6/poc/contextual-kb/knowledge-expansion). Retrieve historical work in a separate checkout; old promotion commands intentionally encode obsolete installed-state preconditions and must not be rerun against today's DB.

## What was tried and learned

| Stage | Result and lesson |
| --- | --- |
| Original library POC | 46 authored facts established the bounded question/retrieval workflow. Handwritten decomposition and later GLiNER training experiments did not justify replacing full-question retrieval. The accepted model-backed runtime retains GLiNER as advisory; the model-free runtime delegates reasoning to its caller. Earlier experiments are summarized in [experiments.md](experiments.md). |
| Custom types, model scope, expressions, extensions | 46 → 70 facts. Targeted comparisons improved support; the mixed-adapter extension candidate was rejected and corrected. Source eligibility must be checked before inference. |
| Validation, arrays and select | 70 → 93 facts. Validation reached45/45 targeted answers; the final arrays setup scored15/15,14/15,15/15, retaining a caller-display refusal. Select scored44/45 versus15/45 baseline. Planner premise-handling and wording fixes were qualified separately from knowledge. |
| Version applicability and common controls | Explicit exact-release applicability was introduced without adding release coverage. JSON Schema conversion, datepicker, checkbox/multicheckbox/toggle, input/textarea and radio/native-select brought the set to124 facts. Both runtime modes share these facts. |
| N2–N7 completion | Material presentation, value events, configuration/lifetime, validation messages and JSON Schema scalars/structures brought the candidate to176 facts. Q1 supported160/160 positive requests after recovery and16/16 controls in three fixed-plan repeats; initial lookup supported121/160. These source-informed tests did not establish independent caller accuracy. |
| External question bank | On the176-fact candidate, the260-question diagnostic produced79 full,113 partial,15 unsupported and53 context-dependent answers per repeat. Library-only full support was66/102 (64.71%):36 library-focused misses required diagnosis. This failed broad-coverage signal remains visible; it is not a score for the final192-fact DB. |
| Public API/configuration follow-up | Twelve additions produced188 facts. Independent review corrected a grading ambiguity:20/24 positives, below the22/24 gate, plus8/8 preservation and8/8 controls. The original21/24 result and correction are retained at the checkpoint. The candidate was not promoted alone. |
| Four missing API contracts | Accessor relationships, optional updateInitialValue arguments, wrapper lookup and absent presets produced192 facts. Fresh targeted support was24/24 versus5/24 baseline, with8/8 preservation and8/8 controls in three identical-plan repeats;399 actual MCP calls. See [results](../../poc/contextual-kb/knowledge-expansion/api-contracts-v1/RESULTS.md). |
| Installed promotion | Canonical inputs reproduced the192-fact DB exactly. Model-free smoke:44/44 packet matches; model-backed smoke:10/10 supported answers across two seeds. Advisory extraction degraded on one case in both seeds without losing answer support. Independent review passed. See [installed checkpoint](../../poc/contextual-kb/knowledge-expansion/promotion-v13/RESULTS.md). |

Scores use their recorded cohorts and baselines. Do not pool them, turn repeated fixed packets into independent generations, or claim the final DB rescored the entire external bank. Historical browser failures B06/B13 remain failures. Evaluation remains sealed.

## Retention policy

Keep canonical authored records, original source paths/bytes, pinned evidence, source-disposition ledgers, runtime dependencies, compiler/seeding code and active regression suites. Some version-named modules remain because current checks import their tested helpers; their presence does not make an old batch an active roadmap item.

Retire completed per-run scaffolding, duplicate review handoffs and one-off runners that are not required by those checks. Keep concise conclusions here and at the latest accepted checkpoint. Store raw runs and scratch review packets under ignored test-output; do not continually add them to the public source tree.

Uncommitted experiment files removed in this cleanup have a verified private archive under `local/archives/cleanup-2026-10-27/`, with original paths, modes and SHA-256 hashes. That archive is local recovery material, not a public repository dependency. Installed assets and sealed evaluation were not swept into it.

## Cleanup checkpoint — 2026-10-27

Retired637 tracked scaffolding files and archived191 uncommitted POC experiment files. Eleven dependencies identified during testing/reference inspection were retained or restored from verified bytes. The private archive contains839 original files; all members and hashes were independently verified. Both runtime implementations/manifests, models, installed192-fact DB and required provenance remain unchanged (247 preservation paths verified); evaluation stayed sealed.

Full local maintenance and both doctors passed, as did source-only checks on an export of the retained public files using the existing environments. Both live MCP connections returned the newly admitted API contract after cleanup. Independent review: **Ready, no actionable findings**. This checks cleanup integrity, not new answer accuracy or fresh-machine provisioning. Review packets and command logs are local under `.planning/cleanup-192/` and `test-output/cleanup-192/`; the private recovery archive remains local and must be preserved.
