# Extensions and presets v2: adapter classification repair

Status: metadata repair for independent review before build/inference. The original extensions-v1 inputs and failed run are retained unchanged.

## Reason for a separate candidate

The first candidate grouped core mechanisms and a Material example into one `mixed` document. The frozen retrieval contract accepts only `core` and `material`, so the new facts were not eligible for lookup. This is an authored-document classification defect; the retrieval policy and models are not being widened to conceal it.

Split the six unchanged fact objects into five `core` facts under the existing `extensions-presets` document ID, and one `material` fact under `extension-addons-material`. The only moved qualified ID is `extension-addons-material/guarded-addons-example`. Exact claims, conditions, limits, quotations, evidence IDs and relationships remain unchanged. Both documents retain the same original customization-guide hash. Expected isolated candidate: **70 facts / 15 documents**, preserving every installed 64-fact baseline row.

## Source classification

Core extension lifecycle and priority come from the core builder/configuration and core module registrations. Named preset module/setup/provider/substitution belongs to `@ngx-formly/core/preset`. The guarded addons fact is explicitly the Material prefix/suffix example and remains a bounded example, not a universal wrapper or arbitrary rerun-safety guarantee. Preset recursion, async-provider handling and arbitrary null/empty merge semantics remain unqualified.

No catalog, source, compiler, schema, runtime, model or installed DB edits by this source repair. Existing evidence verification is retained; source-read checks are not Angular runtime execution.

## Qualification repair/regression protocol

Reuse the exact 15 requests and answer checks from v1, changing only the moved Material fact's required-support ID. These are **exposed repair/regression questions**, not fresh or unseen evidence. Preserve v1 outcomes separately; do not overwrite or remove failures from historical denominators.

After review, freeze v2 inputs and run three repeats against the installed 64-fact baseline and isolated 70-fact candidate: 90 calls, seeds 1701/1702/1701, alternating arms, same planner/selector/caller/extractors, no tuning/retries or denominator exclusions. Gate unchanged: at least 14/15 usable and 9/10 target in each repeat, all five controls, zero critical or delivery failures. Accept semantically equivalent baseline quotations; fact-ID coverage is diagnostic only.

Forty-five paired replays preserve normalized plans: baseline-to-candidate repeats 1/3, candidate-to-baseline repeat 2. Recheck original rows, frozen model/runtime hashes and DB preservation. The broader combined qualification also needs a separately named repaired protocol; do not describe previously attempted questions as fresh or alter the original combined cases.

A pre-inference guard must reject draft adapters outside the frozen retrievable allow-list so this classification defect cannot recur unnoticed. The parent owns that mechanism and its red/green tests, candidate build and runtime runs.
