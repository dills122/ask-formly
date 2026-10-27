# Independent prebuild preliminary review

Review instance: 1 of 3. Recorded before opening PREBUILD-AUTHOR.md.

Scope: completion-v1 at HEAD 250f83da2d93aababf27f169078807ff66f183ee. All 74 prebuild-freeze hashes match; tracked working tree is clean. No candidate build, installed mutation or sealed archive access performed.

## Preliminary findings

- N3 and N4 source-decisions.json use dotted document.fact identifiers while authored/compiler IDs use document/fact. Forty disposition references fail exact ID resolution; all resolve after replacing the first dot with a slash. This is a concrete traceability defect, not missing factual coverage. Correct and validate the references before the final source-to-fact checklist.
- No blocking source-truth defect identified in the examined pinned implementations. Claims deliberately distinguish source bindings from browser, adapter, timing and conformance guarantees.
- Experiment guard checks are useful, but semantic judgments and package gates remain caller/reviewer responsibilities; passing audit unit tests is not qualification. The final run must separately check each package threshold, every scope control, critical claims and baseline regressions.

## Checks so far

Twenty focused unit tests pass. Draft lint accepts 52 additions without errors. All 105 requests and required-point rubrics inspected. Entire converter implementation inspected, plus core key/clone/merge, parser/debounce, host emission, validation/message, shared-validator, Material wrapper/select/slider/toggle sources. Graph lookup has no completion-v1 symbols and exact coverage reports not_tracked; direct source reads used.

## Pending before final judgment

Reconcile author claims; finish preservation/source hash checks and compare reused transport/build helpers to N1. No database exists for this prebuild review, so retrieval/answer performance remains unverified by design.
