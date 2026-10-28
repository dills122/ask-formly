# Issue 21: caller usability follow-up

This implements the maintenance findings from [Live Project Audit #21](https://github.com/dills122/ask-formly/issues/21).
The model-free runtime identity is `formly-model-free-discovery-8`; knowledge
remains the same 192 facts / 36 documents for Formly 6.3.12 core/Material.

## Delivered changes

- Exact condition-copy requirements and actionable validation errors, required
  question reasons, explicit request/scope semantics, and schema-enforced 1–16
  fact-ID fetch limits.
- `help_formly` with a valid example, workflow, limits, and scoped paginated topic
  and fact-ID inventory.
- Field-weighted lexical ranking, lowercase API recognition, conservative prose
  inflections, and removal of scope-only prefixes from topical scoring. Matching
  diagnostics distinguish recognized identifiers from semantic relevance.
- Fair candidate selection beyond four ranks, under fact-count and byte ceilings.
  A question stops when its next ranked record cannot fit; smaller low-ranked
  records do not fill the remaining space ahead of it.
- Existing scoped `see_also` links, bounded neighbor expansion, global omission
  previews, explicit recovery actions, and discovery over the complete omitted
  list rather than only the preview.
- Shared complete provenance in `compact-v1`, plus an explicit full-fetch format.
- [Design-question guides](knowledge-recipes.md) for hiding, collisions, steppers
  and initialization, separating admitted mechanisms from application proposals.
- Default model-free regression and offline transport suites in source CI.

## Response contract and client migration

The active repair/discovery server returns **one complete JSON text packet** rather
than duplicating it in both text and `structuredContent`. SDK consumers should use
`result.structuredContent` when present, otherwise JSON-decode the first text
content item. Check `isError` and the packet status before using evidence. This
preserves the complete data for ordinary text-based MCP clients.

In `compact-v1`, `citations[id].authored_source_ref` resolves in `sources`, and
each `evidence_refs` entry resolves in `evidence`. Facts retain their conditions,
limits, applicability and eligible related links. Fetch selected IDs with
`get_formly_facts(response_format="full")` when inline provenance is needed.
The full format has a separate 48,000-byte limit and may require fewer IDs.

Successful compact lookup/fetch packets have a 28,000-byte UTF-8 JSON ceiling;
the active serialized MCP result has a 30,000-byte ceiling. Client rendering
policies may impose other limits. Discovery uses its separately documented
24,000-byte candidate page limit. Help and validation errors are separate control
messages, not evidence packets.

`questions[].omitted_indexes` refer to the bounded global `omitted_candidates`
preview. Counts disclose the full omitted population, and discovery pages that
full population. A globally delivered fact is not also an omitted fact. Large
request echoes are explicitly replaced by a fingerprint; plans are summarized.
The caller must retain its original request and plan for recovery.

Restart the server after installing updated code and manifest together. Old
running processes retain their old contract. This source change does not publish
a new archive, change client configuration, or qualify a release on another host.

## What the development replay establishes

Four fixed issue-informed plans were replayed against an isolated DB compiled
from the unchanged canonical inputs. Its SHA-256 is identical to the active
launcher DB pin, `f65802b58ec4f1c2719efd8dc1e391d7e250643a94c96b7a71d446ae67fe1b09`.
The installed DB was not rebuilt or replaced. G1 reproduces the issue's original
37,856-byte baseline response exactly; the other appendix plans were summarized,
so their missing reasons/prefixes were restored and are not claimed as exact
historical transcripts.

| Case | Baseline packet bytes | Updated packet bytes | Issue expected IDs in first packet | Additional known-ID fetches |
| --- | ---: | ---: | ---: | ---: |
| Hide/value/registration | 37,856 | 26,258 | 5/5 | 0 |
| Stepper/model scope | 59,660 | 27,116 | 5/8 | 1 |
| Initialization | 52,061 | 27,801 | 5/12 | 2 |
| Dynamic key collisions | 49,752 | 26,731 | 3/9 | 2 |

The fetch rubric supplies the expected IDs and uses at most four per fetch;
all expected records and their provenance are recoverable within those calls.
This measures known-ID recovery, not an autonomous caller's discovery cost.
The first packet supplies all key hide/value/registration evidence. The other
cases still need additional registration/key-path, default/preset/state, or
shared-validator/key-identity support before a complete answer.

JSON Schema `uniqueItems` and Material `compareWith` positive controls retain
their target fact first. Unsupported v7 returns no facts. An unknown API can still
produce lexical candidates with a no-recognized-identifier warning; it must not be
answered as supported, nor treated as proof of corpus-wide absence.

These are development observations, not a broad relevance or precision score.
The issue's proposed 80% first-pass ID target remains unmet for G2–G4. There was
no blanket topic penalty, unconditional whole-topic inclusion, semantic model,
or change to facts to force the target to pass.

## Remaining boundaries

The existing `see_also` graph is exposed; new semantic edge kinds are not admitted.
Complete Material stepper recipes, generic Angular payload rules, a general
`resetFieldOnHide` configuration guide and duplicate-field outcome matrices need
separately scoped evidence. Guidance documents do not turn those into guarantees.
`candidate_only` is an assessment status, not a per-fact runtime execution flag.
Historical browser failures B06/B13 remain visible and unchanged.

Full local qualification still requires the provisioned compiler, MCP and model
environments. Source-only and model-free transport checks do not qualify the
model-backed path or execute Angular/Material fixtures. New client/platform
qualification and additional library versions remain separate work.

## Verification recorded for this change

The expanded source command passes preservation checks, authored lint and its
274 fixture tests, including 42 model-free contract/ranking/response tests,
29 repair/help/stdio tests and 6 discovery tests. The updated pinned runtime passes its
21-file doctor and a real offline-guarded stdio smoke in an isolated runtime
using the byte-identical verification DB. The smoke covers help, lookup, compact
provenance resolution, discovery and explicit full fetch.

One fresh caller using only server instructions/tool descriptions/help answered
the hide question on its first lookup, with no schema error, repair or follow-up.
Its help example was closely matched to the question, so this is narrow onboarding
evidence. A transport replay of the identical call after removing duplicate
serialization returned the identical evidence in **29,314 SDK-result bytes**,
down from 55,486. That replay is not a second independent caller generation.

Independent review instance 1 found no actionable implementation defect and
recorded the first-pass/recovery limitations. The transport correction received
a separate fresh-context review (instance 2: Ready, no actionable findings). A
31-file local alpha archive also passed manifest verification and its real stdio
self-test using existing dependencies; this was not a fresh dependency installation.
Full local maintenance still stops on missing
worktree environments; these results are not full model-backed qualification.
