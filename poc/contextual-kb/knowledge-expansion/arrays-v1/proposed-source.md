# Arrays source mappings for independent review

Six proposed core facts in two documents extend the installed 79 facts / 17 documents to an isolated 85 facts / 19 documents if the review/build gates pass. All ledger decisions remain pending. No candidate has been built or qualified by this source-authoring step.

All six required upstream files were fetched at commit `5f099fddea6426b46a453866adf0fede5be0bcd7`; their full-file SHA256 values match the frozen catalog. URLs, hashes and ignored local copies are recorded in [source-verification.json](source-verification.json). Actual implementation and example files and K27 lines 500–584 were read. No upstream tests or Angular application were executed.

| Source paragraph | Draft support / disposition | Verified scope |
| --- | --- | --- |
| Version/test scope | Exclude execution claims | 6.3.12 source inspection only |
| Template/children | `array-operations/template-and-children` | K12: keyed field registers existing control or new FormArray; array-model length; cloned template/function; `key === null` exception |
| Repeater registration | `array-repeat-example/registered-repeat-renderer` | E01a/b/c and K03: official string alias and component together. Direct component-class type does not universally require alias registration. Reuse existing general registration facts. |
| Add/remove coordination | `array-operations/add-coordination`, `array-operations/remove-coordination` | K12: independent operations with model/control/rebuild/notification coordination; omitted options mark dirty, false suppresses explicit marking; valid initialized usage. Empty options also provide no truthy flag. |
| Falsy initialModel | `array-operations/falsy-initial-model` | K12: falsy values insert undefined before build; final defaulted result not guaranteed |
| Defaults/hide/insertion | `array-operations/default-insertion-test-scope`; existing `hiding-and-visibility/hide-can-clear-array-children` | K27 exact test assertions and setup only; hide cleanup not duplicated; exclude earlier patch equivalence and universal default/reset ordering |
| Material adaptation | Limits on `array-repeat-example/registered-repeat-renderer` | E01b/c Bootstrap import/classes confirmed; no turnkey Material recipe, tested renderer or app-specific guarantee |

The five operation facts use exact frozen arrays.md paragraphs, retaining K12/K27 public anchors. The example fact uses exact E01 prose from examples.md retaining E01a/b/c anchors. Existing evidence IDs are reused; source-evidence.json is empty. No source, catalog, compiler, installed DB or model changes are needed. Supplemental examples provenance covers E01 only, not every examples.md section.

Granularity follows independently useful operation contracts, one construction fact, one falsy-argument boundary, one explicitly source-inspected regression scenario group, and one example mechanism. It does not target ten facts for ten qualification questions. Combined canonical-plus-draft compiler lint passed for 19 documents using a temporary directory, without compiling a database.

Review must assess these exact draft facts, exclusions and case coverage before any isolated build. Qualification remains separate from source verification; none of these checks establish whole-library or Material runtime compatibility.
