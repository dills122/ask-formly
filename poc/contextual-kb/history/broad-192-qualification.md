# Broader 192-fact caller qualification

Run started 2026-10-27 against merged baseline `025bb08`, using the installed 192-fact / 36-document Formly 6.3.12 core/Material knowledge base. This measures the default model-free MCP with native calling agents. The model-backed runtime received maintenance and preservation checks, not an accuracy comparison.

## Method and frozen criteria

Sixty fresh, hand-authored development requests: 48 library questions across 16 topic groups and 12 scope/application/unsupported-guarantee controls. Cases, rubric, protocol, budgets and preservation hashes were frozen before execution. Three fresh-context agents independently generated plans and answers; they shared the same configured model and questions, and were instructed not to read the rubric, source, previous runs or one another's answers. This was an instruction boundary, not a filesystem isolation boundary; saved artifacts do not provide a complete access transcript. No tuning occurred during qualification. All 56 tool-using cases had three distinct initial plans. Separate contexts, separate outputs and distinct plans support independent generation, but do not prove total information isolation.

Each case allowed an initial lookup plus at most two plan repairs, six total MCP calls, two discovery pages and one fact fetch. The per-pass target was 44/48 fully usable positives; 43/48 was the predeclared tolerance. All 12 controls and zero critical unsupported claims were also required. Missing cases stayed in the denominator. Grading considered meaning and actual delivered evidence, not matching fact IDs or retrieval hits alone.

## Results

| Independent pass | Conservative frozen-rubric positives | Correct controls | Critical claims | Actual MCP calls |
| --- | --- | --- | --- | --- |
| 1 | 47/48 (97.92%) | 12/12 | 0 | 67 |
| 2 | 47/48 (97.92%) | 12/12 | 0 | 66 |
| 3 | 47/48 (97.92%) | 12/12 | 0 | 67 |

Every pass scored 3/3 in each of these topic groups: custom types, wrappers, expressions, visibility, defaults/reset, model scope, events/parsing, validation, select, datepicker, choice/input controls, configuration/presentation, JSON scalars, JSON structures and public API. Arrays scored a conservative 2/3 per pass solely because of the rubric defect below.

All 180 answers and 200 tool traces were retained. Each pass used 56 lookups; supplementary fact fetches numbered 11, 10 and 11. Four application-only controls per pass correctly declined without calling the library MCP. No discovery pagination, transport failures or plan-validation rejections were reported. Automated audit found no missing answers, call-budget violations or citations lacking delivered source evidence.

Callers reported initial evidence sufficient for 37/48, 38/48 and 37/48 positives respectively. These are caller judgments, not independently measured first-packet recall. Final scores include permitted fact-fetch recovery and must not be presented as initial eight-slot performance.

## Exceptions retained in the record

**P092 rubric defect:** The frozen rubric incorrectly expected `FieldArrayType.add` to preserve falsy initial values. Delivered pinned evidence (`array-operations/falsy-initial-model`) establishes that false and zero take the undefined insertion branch because the implementation tests truthiness. All three answers followed the evidence correctly. The frozen rubric and answers remain unchanged; conservative scores above charge this discrepancy as one failure per pass. Independent review confirmed the evidence-based corrected tally of 48/48 per pass. This is a disclosed rubric correction, not a rerun or replacement of the frozen score.

**Pass 3, C09 planning deviation:** The caller omitted explicit version/adapter metadata despite a request naming Formly 6.3.12 and Material. The full question retained that scope, the service defaulted to release 6.3.12 with adapter null, and the final answer correctly refused a universal accessibility guarantee. The control answer passes; plan compliance is imperfect. Scanning every submitted plan found this single scope-metadata deviation. Passing answer scores do not erase it.

## Verification and preservation

`python3 tools/project.py check` passed, including both runtime doctors and 149 active MCP regressions. Eleven qualification scorer/audit unit tests passed. All five frozen-input hashes and 233 protected asset hashes matched after execution. Both runtime implementations/manifests, models, installed DB, authored knowledge and source inputs stayed unchanged; sealed evaluation was not opened.

DB SHA256: `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.
Cases SHA256: `cd1403b382f3c2bab2b9bd37c8548ebe885cefcb3d2cb1bc0ba8c98626d05028`.
Raw inputs, rubric erratum, complete calls/answers, grading, maintenance log and 380-file execution seal remain local and ignored under `poc/contextual-kb/test-output/broad192-20261027/`. No private artifacts are intended for Git.

Independent review (instance 1 of 3): **Ready with non-blocking follow-ups**. The fresh-context reviewer checked all 180 answers against delivered claims, conditions and limits, reproduced all frozen/execution/preservation hashes and passed all 11 qualification tests. The review confirmed the P092 erratum and retained the C09 metadata deviation and information-isolation limitations. Full local review: `.planning/broad192/review.md`.

## Interpretation

This is a strong result on a bounded, coverage-oriented development sample, not an unbiased population estimate or a whole-library guarantee. Each positive represents 2.08 percentage points; this cannot establish consistency within a sub-percentage band. Same-model fresh contexts do not establish Claude/Kiro equivalence, model-backed accuracy, production latency or browser qualification. Historical browser failures B06/B13 remain unresolved by this exercise.

The observed follow-up is caller scope-metadata discipline. This run does not justify another broad tuning cycle or changes to the locked data/models. Keep the qualified foundation and use a separate bounded caller-contract check if addressing that omission.

## Follow-up: bounded scope-metadata safeguard

A subsequent authorized fix adds `MISSING_SCOPE_METADATA` feedback before retrieval when a shaped plan leaves scope null despite a recognized opening declaration. The supported syntax is `For`/`In`/`Use Formly x.y.z`, optionally `with Material`, `Bootstrap`, `PrimeNG` or `core`, followed by a comma or period and whitespace/end. It returns the missing field path and source excerpt; the caller repairs metadata while preserving the original request. It does not auto-fill scope, infer arbitrary prose, or certify supplied values against user intent. Caller instructions and the tool description make this responsibility explicit.

The original omission failed before implementation and passed after it. Six added unit tests cover partial metadata, defaults/unrecognized wording, exact-version boundaries, repair and unsupported-scope stopping. The real stdio transport regression also covers rejection and repair. All 23 repair tests and the full local maintenance check (now 155 active MCP regressions) passed. A new stable-launcher process against the installed DB completed three real calls: rejection, repaired success and unsupported-release stop.

Revalidating the 168 saved qualification lookup plans accepted 167 and flagged only the known pass3 C09 omission. This is a validation replay, not a new answer-quality qualification. Original qualification artifacts were not rewritten. Protection checks found 229 assets unchanged; the only four authorized changes among the pinned assets were repair feedback, caller instructions, tool description and the corresponding model-free manifest. Models, DB and model-backed implementation remain unchanged. Existing MCP processes need a restart to load the new code/instructions; the fresh stable-launcher process was verified.

Independent implementation review (instance 1 of 3): **Ready**, no actionable findings. The reviewer independently reran all 23 repair tests (including fixture stdio), checked the three changed source pins and reviewed the retained full-maintenance, replay, installed-DB transport and preservation evidence. Protected-asset hashes were checked by the implementation run, not independently reread by this reviewer. Raw tests and review evidence are ignored under `poc/contextual-kb/test-output/scope-metadata-fix/`.

After the user restarted both native MCP connections, candidate and discovery each passed three live checks: missing metadata returned `MISSING_SCOPE_METADATA`, corrected metadata returned `ok` with explicit 6.3.12/Material scope, and 7.0.0 returned `unsupported_scope` with a stop action. All six complete responses remain in ignored test output. Source pins and protected assets were rechecked; models and DB remained unchanged.
