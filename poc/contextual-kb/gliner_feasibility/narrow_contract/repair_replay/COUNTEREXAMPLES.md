# Independent repair counterexamples

Authored independently before scored execution. The author read only the repair
design PROPOSAL.md, repair design TEST-PLAN.md, and narrow CONTRACT.md. No repair
implementation, pilot prediction, or pilot gold was inspected. The coordinator's
pre-execution clarification of unsupported path handling is recorded below.

These 12 hand-authored candidate sets test the deterministic repair algorithm.
They do not measure GLiNER inference or generalization. Each family contains a
supported case (S) and a superficially similar case where a particular repair
would be unsafe (U). An unsafe repair does not necessarily imply needs_review:
a single unconflicted candidate can remain wrong or incomplete under this design.
Expected envelopes describe the full cumulative repair stage. Missing candidates
are deliberately not synthesized, including property-name API mentions.

| Family | Supported case | Unsafe operation tested |
|---|---|---|
| Quote ownership | A complete defaultValue literal owns and suppresses an interior false key. | Expanding a partial payload candidate to the entire literal. |
| Escape/boundary | Unicode precedes a literal containing an escaped apostrophe and the other quote type. | Treating an unclosed recognized literal as a sound value. |
| Path adjacency | An API-root candidate completes through adjacent bracket and dot members, owning the bracket string. | Completing through an arbitrary computed bracket expression. |
| Assignment versus prose | An equals assignment can relabel a value candidate as a registration name. | Treating the noun phrase “custom type” as a property binding. |
| Same text/different role | Equal spellings at distinct type/key occurrences receive distinct roles. | Executing apparent type/key bindings inside an owned literal payload. |
| Unresolved ambiguity | An explicit key binding resolves competing labels at one occurrence. | Choosing a winner for the same candidates without a supported binding. |

All candidates use one of the six declared roles. Every row supplies an entities
mapping containing all six role keys. Questions are immutable, offsets count
Python Unicode codepoints, ends are exclusive, and raw values are exact source
slices. Generated assertions checked every candidate and expected mention slice,
source ordering, and lack of overlap. This construction validation does not run
the repair implementation and is not a scored result.

## Pre-execution interpretation notes

The proposal forbids extending an API root through unsupported expressions but
does not fully specify the envelope status or issue span for a syntactically
unsupported suffix. Before suite completion, the coordinator supplied this
implementation-spec decision: omit a root immediately followed by a call,
computed bracket, or unmatched bracket, and emit boundary_ambiguous over the
original root candidate span. CX-PA-U adopts that decision. It does not claim the
entire expression is a supported API or invent an issue boundary for it.

The partial candidate in CX-QO-U remains a partial value. The rules forbid quote
expansion of a proper substring and do not define independent semantic rejection
of an unconflicted label. Its ok status deliberately does not assert semantic
completeness. Similarly, CX-AP-U retains the supplied value role after legitimate
quote-boundary expansion; prose does not authorize relabeling it.

The apparent assignments in CX-SR-U occur inside a value whose enclosing
explicit defaultValue binding establishes ownership. Their nested candidate
labels are therefore suppressed, rather than becoming independent mentions or
causing a conflict. In CX-UA-U, the competing complete quoted occurrences have
no independent ownership or role evidence, so the disputed quoted region is
omitted and the sound version/adapter mentions remain.

## Freeze and disclosure

counterexamples-freeze.json records SHA-256 values for this document and the
JSON suite. The coordinator receives only completion and file paths until repair
implementation freeze. Expectations must not be changed after scored execution
to match implementation output. Record any mismatch as a failure or a separately
explained specification disagreement, preserving the frozen evidence.
