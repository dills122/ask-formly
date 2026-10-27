# Source-independent case preparation

The initial 40-case draft was authored from PLAN.md's bounded topic list and library-miss-diagnosis-v1/RESULTS.md's public failure summary. The case author did not inspect candidate/installed knowledge inventories, source-author outputs, runtime databases, models, or sealed evaluation. Two completion-v1 cases and their call objects were read only to establish the JSON contract, not to derive target answers. No historical artifact was changed.

This is a fresh source-independent diagnostic, not a sealed test or a sample of production traffic. Freshness means newly written requests in this batch; it is not a claim of semantic novelty against every historic question.

## Cohorts

| Package | Kind | Count | Scope |
| --- | --- | ---: | --- |
| API | target | 12 | Field/control lookup; key/id/name; CSS targets; typed scalar/array surfaces; populated type accessors; formState; exposed build/check/update hooks |
| CONFIG | target | 12 | Wrapper nesting and defaults; duplicate type/wrapper/validator registrations; missing lookup behavior; partial preset overrides including explicit false |
| REGRESSION | regression | 8 | Hide retention; array add/remove; custom wrappers; validation; Material select/input/radio; bounded JSON Schema conversion |
| CONTROL | control | 8 | Version, adapter, application diagnosis, Angular policy, universal CSS propagation, lookup equivalence, reorder preservation, universal lifecycle ordering |

The default is explicit Formly 6.3.12 and Material, including core questions asked in that environment. Only CONTROL-01 uses 7.0.0 and only CONTROL-02 uses Bootstrap. Their unsupported requested scope is the point of the control, not new admission coverage.

The positive requests are deliberately finite. They ask about API behavior without assuming a favorable answer. `required_points` specify which parts must be resolved; they do not encode source-derived expected results or fact IDs. The source review must establish the appropriate bounded answer before scoring. Unsupported broad guarantees are confined to controls. Existing-model overwrite, universal runtime availability, and arbitrary lifecycle guarantees are not hidden requirements of positive cases.

## Caller plans

Every call repeats the exact original request unchanged and supplies matching top-level and plan version/adapter constraints. Focused questions retain one useful question; seven requests with separable obligations have two. There are 47 questions total, with no case exceeding six. Comparisons such as type/wrapper/validator resolution are intentionally kept together so retrieval must support the requested comparison rather than unrelated fragments.

`condition_bindings` is the exact-excerpt ledger. Each condition is a literal excerpt of the original request and is repeated verbatim in every bound question. Single-question plans bind the full request. Decomposed plans bind the exact scope phrase plus relevant caller conditions; their question prose preserves the remaining semantic obligations. The original request remains authoritative, and the fixed required points expose omissions. No lookup plan contains fact IDs, source filenames, catalog keys, or source-derived answers.

Freeze the same plans for baseline and candidate. The caller must use delivered evidence and observed discovery IDs for any recovery. Neither answer grading nor recovery may consult an inventory oracle. Use the prospective GRADING.md rules for supported composition and bounded scope.

## Draft validation

JSON shape, cohort counts, unique IDs, exact request preservation, scope alignment, question budget, and literal condition repetition were checked locally. This validates preparation consistency only; it does not certify runtime compatibility or answerability. Independent review, source adjudication, and the parent batch's freeze manifest remain required before scored execution.
