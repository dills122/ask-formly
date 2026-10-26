# Material select source mapping

Eight proposed facts in two authored documents; accepted foundation7 remains85facts/19documents. If admitted unchanged, the isolated candidate will contain93facts/21documents. No installed or candidate DB was built for source preparation.

## Evidence verification

Fetched exact upstream bytes at Formly6.3.12 commit `5f099fddea6426b46a453866adf0fede5be0bcd7` and compared their full-file SHA256 against the unchanged catalog. K14 (Material select renderer), K15 (shared select-options pipe), and K28 (select test source) all match. The web reader could not fetch the raw URLs; direct HTTPS retrieval succeeded and its bytes were retained under ignored test-output/source-cache. Full files were inspected, not merely the catalog line ranges. Upstream Angular tests were not executed.

Catalog ranges cover these implementation claims exactly: K14 lines8–130 includes all select-all logic (state87–93, toggle95–99, cache/filter117–129); K15 lines6–137 includes mapping46–101 and lifecycle/update32–44,103–136. No catalog range adjustment is needed. K28 tests were inspected across the full hash-verified file but are corroboration only; no new fact relies on extending its pinned15–104 excerpt.

No new catalog entries are needed; source-evidence.json is empty. Canonical-plus-draft authored lint passes using21documents. Initial lint caught three quotes missing one of their declared evidence anchors; expanding to the exact adjacent guide paragraphs resolved it. Original guide/catalog bytes are unchanged.

## Proposed facts

| Fact | Verified implementation | Important boundary |
| --- | --- | --- |
| material-select-options/option-mapping | K15 transformSelectProps/transformOption: property name or function, defaults and Boolean disabled coercion | Value mapping does not define selection identity |
| material-select-options/option-groups | K15 transformOption/transformOptions; K14 template | Recursive transformation does not establish arbitrary-depth Material rendering |
| material-select-options/observable-consumption | K15 transform/dispose/ngOnDestroy; K14 template async pipe | Cleanup concerns pipe-owned helper state, not arbitrary application producers/manual/hook subscriptions |
| material-select-options/expression-array-updates | K15 observableOf filter and tap | Exact same field, expressionChanges, options property prefix, current array and existing helper subject required |
| material-select-options/strict-comparison | K14 defaultOptions and compareWith binding; K15 mappings | Equal-looking object instances are not strictly equal; no application identity policy invented |
| material-select-options/multiple-and-change | K14 multiple/select-all template bindings and change method | select-all entry requires multiple and label; selectionChange delegates field/event, not a scalar-only callback contract |
| material-select-all/enabled-values | K14 getSelectAllValue/toggleSelectAll | One-level flatten, disabled filtering, length-based toggle and explicit dirty marking; private helper is not public application API |
| material-select-all/state-and-cache | K14 getSelectAllState/getSelectAllValue | Equal lengths do not establish equal sets; cache keys transformed selectOptions array identity, not necessarily raw props.options identity |

## Ownership and update distinctions

The supplied Observable branch returns the input stream with a map transformation; it does not create a direct subscription. The template consumes the transformed stream with async. The non-Observable branch creates a BehaviorSubject and can subscribe to field.options.fieldChanges. dispose completes that subject and unsubscribes that internal subscription. These observations resolve the previously deferred select path, but do not prove cancellation of an arbitrary producer or replace the separate managed hook-return fact.

The array-event filter compares field identity, type expressionChanges, prefix templateOptions.options or props.options, current field.props.options being an array, and an existing helper subject. It is not an every-mutation refresh promise.

Select-all cache identity is measured after option conversion. The mapper normally constructs new output arrays, so a claim that every raw input mutation leaves the UI stale would overstate this implementation. The bounded claim is only that reusing the same transformed array reference does not invalidate this helper cache.

## Deliberately unadmitted material

Both retained guides are fully inventoried as11sections, but unrelated modules, datepicker/slider, non-select controls, custom Material controls, required-marker/consent behavior, accessibility/panelClass and upgrade/browser compatibility remain pending. The original select paragraph's cascading-demo concern and application-specific retained/cleared child-value policy are excluded from this batch. Native-select is not certified equivalent. K28 corroborates selected test fixtures only; no additional test-outcome fact or execution claim is added.

ledger.json and candidate-ledger.json currently leave draft fact decisions pending independent review. Other Material sections must remain pending even after select claims are admitted to an isolated candidate; `--require-complete` must not falsely close whole Material coverage. The earlier expression ledger is frozen historical evidence; this batch records the new ownership support rather than rewriting it.

## Review gates

Independent source/mapping review precedes building. Verify the precise teardown scope, transformed-array cache identity, same-length toggle behavior, scalar mapping versus equality distinction, and correct private API boundary. Source interpretation is curated; ledger validation and lint provide mechanical identity/provenance checks, not proof of those interpretations.
