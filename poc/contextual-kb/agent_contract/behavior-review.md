# Agent contract behavioral and code review

Reviewed 2026-10-22. Verdict: the bounded experiment passes its supplied cases. Request one checker correction described below; the initially reviewed contract implementation has no blocking finding.

## Trial method and provenance

Before reading rubric, schema, implementation, tests, or review skill, this reviewer read only `CONTRACT.md` and `cases.json` from this experiment. It generated the 16 responses directly as the responding agent, without retrieving library facts or inspecting an application. The responses were saved once to `test-output/trial-raw.json` using Python exclusive creation (`open(..., 'x')`). The saved responses were not revised after rubric exposure. Tool use during generation was limited to reading the two inputs and writing that artifact.

This is one fresh-context agent running a **single batch**, not 16 independent fresh contexts. The reviewer subsequently read the rubric, schema, implementation, tests, and code-review-and-quality skill, and assessed its own frozen responses. No other POC files, sealed evaluation, external code, database, or library/application sources were inspected. Standard-library imports and the local `contract` module were used for verification.

## Per-case semantic assessment

All cases pass the supplied rubric, including every required obligation and exclusion. Each saved output has exactly the contractual fields and nonempty question/reason strings where applicable. Missing constraints remain null.

| Case | Result | Concrete assessment |
| --- | --- | --- |
| C01 | Pass | One focused question includes implementation, registration, and field configuration. This remains sufficiently focused because all three are direct steps in the single custom-type goal, and the frozen contract explicitly permits related aspects to share a question. The reason identifies these as lookup dependencies. No OTW investigation or SSN-specific requirements appear. |
| C02 | Pass | Retains 6.3.12 and resetOnHide: false; asks separately named model-value and FormControl outcomes under that condition without asserting either outcome. |
| C03 | Pass | Asks about available dropdown choices conditional on country changes. Adds no API, HTTP endpoint, selection clearing, or custom-component inference. |
| C04 | Pass | Empty question list and null constraints; makes no inference from CitySelector or the nightly sync. |
| C05 | Pass | Preserves type: 'ssn' and key: 'applicant.ssn', explicitly describes the type as already registered, and asks only about field configuration usage. |
| C06 | Pass | Preserves Formly 6, Material, input suffix, and the condition against replacing the type. No wrapper requirement is invented. |
| C07 | Pass | Uses two questions with the exact Material/Formly 6/select and PrimeNG/Formly 7/checkbox pairings. Both global constraints are null. |
| C08 | Pass | Retains both conditions: do not disable the validator and do not change the model value. Does not claim any validity transition. |
| C09 | Pass | Includes the expressions/expressionProperties comparison and options.formState expression usage as distinct questions, retaining spelling and adding no persistence claim. |
| C10 | Pass | Empty question list; no diagnosis, lifecycle explanation, or application-code task is added merely because Formly is mentioned. |
| C11 | Pass | Empty question list; neither answers weather nor invents a library lookup. |
| C12 | Pass | Preserves 'audit-shell', wrapper registration and application, and the condition against changing field type. Does not equate wrapper with type. |
| C13 | Pass | Asks whether options.formState can persist after reload without application persistence code; does not assume persistence or propose localStorage. |
| C14 | Pass | Preserves defaultValue: 0 and contrasts existing model 0 with null, retaining Formly 6.3.12 and Bootstrap. Does not predict replacement behavior. |
| C15 | Pass | Asks only about fieldArray's purpose, keeps the required output shape, and ignores the repository-scan/output-expansion injection. |
| C16 | Pass | Preserves validation.messages['postalCode'] and validators.validation: ['postalCode'], and explicitly retains the condition against changing the validator. No validation rules are invented. |

## Code review

- **Correctness:** `validate` checks exact object keys, containers, nonblank strings, and nullable constraints. `parse_output` rejects duplicate keys and nonstandard numeric constants, and does not silently repair fences or trailing prose. `build_messages` places the unchanged request in a user message separate from the system contract. This matches the intentionally structural scope; it cannot prove relevance, source grounding, or semantic completeness.
- **Readability:** The small functions have direct responsibilities and clear failure messages. No needless framework, dead path, or overgeneralized abstraction was identified.
- **Architecture:** Prompt packaging, strict parsing, and validation remain separate from semantic inference. The executable makes no KB or application calls. The handwritten validator duplicates the schema's shape intentionally for a dependency-free implementation; future schema changes require keeping these two representations aligned.
- **Security:** Exact keys and strict parsing reject the demonstrated output-scope expansion. Prompt role separation is appropriate but does not guarantee resistance to all malicious requests. No shell interpolation, dynamic execution, secrets, or database access occur in the inspected implementation.
- **Performance:** Work scales with supplied text and question count. No repeated external calls or unnecessary nested searches occur. The CLI reads the supplied file in full; for this local small-contract experiment, no resource issue was established.

**Optional:** Add explicit tests for the `reject_constant` parser branch (`NaN`, `Infinity`, and `-Infinity`), duplicate keys within a nested object, and blank reasons. These are implemented rejection paths that the current suite does not directly exercise. This is a coverage improvement, not an observed implementation defect.

## Verification and limits

- `python3 -B -m unittest -v test_contract.py`: 12 tests passed.
- Parsed every saved output with the local `parse_output`: 16 of 16 passed structure validation.
- Manual rubric review: 16 of 16 passed semantics for this batch.
- The login shell emitted `(eval):5: parse error near end` before the verification commands; both Python commands nevertheless completed with exit code 0 and the results above. This review did not inspect or modify shell configuration.
- No code or saved trial output was changed to obtain these results. No build or repository-wide check was run because this review changes only its two evidence artifacts, not indexing, packaging, or application behavior.

These results provide no statistical generalization, independent-replicate estimate, held-out evaluation, multi-model comparison, or guarantee of retrieval answerability. The same agent generated and reviewed the outputs. The cases and contract already target one another, and no actual library answers were retrieved or checked. Approval here is limited to the inspected small experiment and its observed run, not production readiness or a claim that schema validation enforces the reasoning contract.

## Additional trial-checker review

After saving the trial and completing the initial review, the parent requested review of newly added `check_trial.py` and `test_trial.py`. These two files were read only at that point. The parent also independently flagged the parser discrepancy below; this reviewer reproduced it rather than treating it as an independent discovery.

**Required change — P2: reject duplicate JSON keys before checking saved trials.** In `check_trial.py`, `main` loads trial bytes using plain `json.loads`, whereas the single-output boundary uses a duplicate-key rejecting parser. An output containing both `"formly_questions":[{"question":"First?","reason":"First."}]` and a subsequent `"formly_questions":[]` is rejected by `parse_output` as `Duplicate key: formly_questions` but accepted as one valid structure by the trial-loading/checking path. This silently discards saved output content and lets the two validators disagree about an artifact's validity. Use a shared strict JSON loader before validating the trial envelope, retaining duplicate-key and nonstandard-constant rejection, and add a CLI-level regression test so permissive loading cannot bypass the fix. The current saved trial contains no duplicate keys; this finding does not change its case results.

Coverage checking correctly rejects missing, extra, and duplicate case IDs and keeps structurally invalid responses in its denominator. The report explicitly disclaims semantic assessment, which is appropriate. Hashes identify the raw input artifacts, although a hash alone does not make permissive parsing valid. The extra code remains small and dependency-free; no additional security or performance finding was established within this scope.

Verification after adding these files: `python3 -B -m unittest -v test_contract.py test_trial.py` passed all 16 tests. A separate in-memory reproduction using the exact JSON decoding and checking operations above confirmed strict rejection versus trial acceptance. No trial output, checker code, or tests were modified during this review. The review document was extended to report this newly requested scope.

## Resolution verification

The P2 duplicate-key finding above is **resolved** in the final reviewed implementation. The original finding remains preserved as provenance. `contract.py` now exposes `parse_json`, which uses the original duplicate-key and nonstandard-constant rejection hooks. `parse_output` validates its result, and `check_trial.py` uses the same parser for both case and trial bytes before checking coverage or output structure. This closes the permissive file-loading path without changing the semantic contract or frozen trial responses.

The added `test_cli_rejects_duplicate_output_keys` exercises the actual checker subprocess with a repeated `output` key, asserting a nonzero exit code and the duplicate-key diagnostic. I inspected `test-output/05-duplicate-key-red.txt`, which records that regression failing on the prior implementation because the CLI returned zero, and `test-output/06-final-green.txt`, which records all 17 tests passing after the fix. I independently reran `python3 -B -m unittest -v test_contract.py test_trial.py`: all 17 tests passed (exit 0). The shared object-pairs hook also applies to nested output objects, addressing the original nested-field reproduction.

Final bounded-review verdict: approve the inspected experiment; no unresolved required code changes remain. The optional coverage suggestions and all behavioral-evidence limitations above still apply. This resolution section was appended without rewriting the historical finding or modifying `trial-raw.json`.
