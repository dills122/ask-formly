# Model scope registration and key path audit

**2026-10-28 — read-only audit of the discovery10 source runtime.** The targeted
model-scope, registration and key-path distinctions have existing library
support. Focused questions retrieve that support; the broad historical wizard
plan still loses conditional details through ranking, packet limits and caller
selection. No facts, installed DB, runtime code or frozen prior rubrics changed.

This follows the [four-slice direction](knowledge-direction.md): library facts
support design decisions, while a custom wizard remains a proposed application
composition. Examples, standards/patterns and repository knowledge stay deferred.

## What the original question requires

The original G2 request asks how to split a form across stepper views while model
binding works. Its historical plan introduced a custom FieldType, wrapper,
registration, lazy rendering and per-step validation. Those can be useful design
choices, but they were not all requirements supplied by the user.

| Support | Disposition |
| --- | --- |
| Keyless groups share parent scope; keyed groups provide nested scope | Essential distinctions for the proposed group-based design |
| A leaf's field.model is its enclosing object | Essential when explaining that accessor; conditional in a general wizard answer |
| Numeric, dotted, bracket and literal array key paths | Required when making those syntax claims, not for every wizard proposal |
| FieldType accessors and scalar/group control typing | Conditional on implementing a custom field component; typing does not create controls |
| String aliases versus direct component references | Distinct supported routes; named aliases require registration, direct class references still require Angular setup and are not JSON values |
| Hiding and control registration | Conditional on using Formly hide for navigation; visual navigation does not intrinsically require hide |
| Wizard navigation, stepControl wiring and per-step validity | Application composition and fixture work; no complete recipe established by these facts |
| Behavior of repository-defined components or methods | Requires inspection of that repository by the calling agent |

The older `component-needs-registration` claim explicitly concerns a type name.
Reading it as a requirement for every direct component reference would overstate
it. The existing `component-reference-or-alias` fact supplies the distinction and
JSON limitation. This is a qualification/readability hazard, not an identified
contradiction or a reason to add a duplicate fact. Likewise a fact listing key
shapes is not equivalent to the detailed path-parser contract.

## Frozen measurement

Revision 1 froze eight supplemental cases, their support rubric and recovery
policies before diagnostic execution. They cover everyday group wording, leaf
scope, registration routes/JSON, FieldType surfaces/control typing, key parsing,
an unfamiliar custom method, the unknown-string-type contract and unsupported v7.
The original G2 plan and its eight expected IDs remain a separate diagnostic.

The audit ran 57 real MCP case executions: three repeats of the eight cases under
two policies, plus G2 under three policies. All repeats were stable; there were no
tool errors or fetches of undiscovered IDs. Unsupported v7 returned no evidence.
Maximum serialized SDK response was 29,819 bytes, within the unchanged ceilings.

All eight supplemental essential facets were delivered on the first lookup.
G2 also delivered both essential group-scope facets initially. The scripted
policies nevertheless attempted their bounded recovery rounds; their call counts
are not minimum autonomous recovery effort. The unfamiliar-method control has
no positive fact requirement: generic lexical candidates cannot certify the
method's behavior, and absence of a useful match cannot prove API nonexistence.

| Historical G2 diagnostic | Initial expected IDs | After up to four follow-ups |
| --- | ---: | ---: |
| Historical paging/selection policy on current source | 4/8 | 4/8 |
| Previous question-directed policy on current source | 4/8 | 4/8 |
| Guided focused recovery on current source | 4/8 | 6/8 |

The previously recorded 5/8 result remains historical evidence; it is not the
current score. Selected-ID counts measure delivery of that particular checklist,
not complete answer correctness. Passing the smaller essential rubric does not
erase the lost conditional evidence.

## Where broad retrieval loses support

A read-only snapshot comparison reproduces 5/8 and 29,167 SDK bytes on RC8,
versus 4/8 and 29,819 bytes on both source9 and source10. The lost fact is
`hiding-and-visibility/hide-unregisters-control`. This predates focused discovery.
It moved from fifth to sixth in the hiding question's candidates. Current
selection stops that question at a preceding lazy-render fact whose trial costs
30,380 SDK bytes even with no omission preview. Preview-space reclamation also
admits an Angular setup fact that previously did not fit, leaving less room for
the hiding branch.

A diagnostic comparison of old/new candidate lists against old/new selection
shows that either change can independently displace this conditional warning.
This is a tradeoff between complete evidence records under the existing budget,
not a reason to clip provenance or silently increase the ceiling. The synthetic
comparison shares current matching metadata; the snapshot results above provide
the actual historical packet sizes.

| Omitted support in broad G2 | Best candidate rank | Global omission position | Guided recovery result |
| --- | ---: | ---: | --- |
| Type registration options | 9 | 9 | Fetched |
| Named component registration | 14 | 16 | Fetched |
| Direct component versus alias | 30 | 57 | Focus moved it to first; fetched |
| Detailed key paths | 20 | 42 | Focus returned it eighth; caller did not select it |
| Hide unregisters control | 6 | 6 | Neither guided focus targeted the hiding branch |

Key-path support is first in the dedicated path question. In broad recovery it
is already on the returned discovery page, but the scripted novelty/word-overlap
selector chooses tree lookup, leaf events, array templates and JSON Schema
records instead. This is selection loss after successful discovery. Fetching
more overlapping records is not a substitute for assessing the missing claim.

The custom-method control returns generic lexical candidates, with unmatched
custom names and `semantic_relevance: not_assessed`. The real unknown-string
contract is retrieved when asked directly. These results support retaining the
distinction between a library API question and an application implementation
question; `ok` does not certify the unfamiliar method.

## Fresh caller evidence

A caller given only two user questions and live schemas/help produced a wizard
design using supported group scope and custom component mechanisms, explicitly
labelling navigation and validation wiring as application work. It used one
lookup plus discovery/fetch. On a second question containing unfamiliar
`props.autoScopeByStep` and `registerStepField` names, it used one lookup and one
discovery call, withheld unsupported API claims and did not claim exhaustive
absence. These are two inspected answers, not a general answer-quality score.

An independent support review matched all ten citations in the first answer and
three in the second to their delivered provenance, with no unsupported material
claims found. The first answer also recovered the child-render loop from K141
inside a CSS-focused fact's source evidence. That supports its explicitly sourced
rendering example, but also shows why discovery based only on a fact's topic or
claim can miss useful provenance. It does not qualify the complete wizard.

## Next bounded work

1. Protect the inactive-control warning when a proposed design uses Formly hide.
   Add that conditional branch to preservation checks before changing global
   ranking or packet selection. Keep the newly observed historical loss visible.
2. Improve caller selection of discovered evidence: test the exact key-parser
   distinction against distracting model/path overlap, and prioritize unmet
   branches rather than repeatedly covering already-supported scope facts.
3. Keep configuration choice, model scope and control lifetime as independent
   library questions where appropriate. Require support for implementation
   choices the answer actually recommends, without forcing every custom design
   through the same recipe or optimizing directly for the old eight IDs.

No new fact admission is indicated for the eight tested distinctions. Proposed
wording/link improvements and the previously identified changed-model/shared-hide
clarifications remain separate review work. The three future slices stay deferred.

## Preservation and reproducibility

All 86 protected fact/corpus/compiler/schema/DB hashes and 60 captured runtime and
evaluation file hashes matched after execution. Source validation passed for
130 preserved files and authored lint. Full local maintenance still stops on the
missing worktree compiler environment; this audit does not qualify Angular
execution or the model-backed runtime.

Frozen inputs, runner, full transcripts, ranks, packet trials, support review and
fresh answers are retained under ignored `test-output/library-support-audit/`.
The database digest remains
`f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.
The input hashes are:

| Input | SHA-256 |
| --- | --- |
| Cases | `46306b639bea84596750b0d9d296f56d5a8ff96403e55e3bcfaad165c1e8edf2` |
| Rubric | `9379c4b8b5e6d1aab3196e3fd58f3287e08b0906ba9964eb1c78134cba0204a7` |
| Policy | `6e23d984282885faa3b0cef4bf16fada43ad694906a941fbb93e702aae370094` |
