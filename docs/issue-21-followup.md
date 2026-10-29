# Issue 21: delivered behavior and remaining gaps

The [original audit](https://github.com/dills122/ask-formly/issues/21) led to the
demo RC and subsequent retrieval refinements. See [current status](current-status.md)
for the distinction between the published RC, current source and isolated candidate.
Knowledge remains 192 facts / 36 documents for Formly 6.3.12 core/Material.

## Delivered changes

The demo repair added actionable plan errors, help/topic inventory, exact-symbol
and field-weighted ranking, fair bounded selection, scoped related-fact recovery,
and compact single-text responses. Subsequent source changes refine identifier
matching, model/registration/key-path recovery, conditional-control warnings,
help limits, response batching and build identity. Facts and the installed DB
were not changed by these retrieval fixes.

The isolated answer candidate adds lightweight citations, separately fetched
detailed provenance, excerpt availability, required discovery plans and selection
of suitable listed evidence before further searches. It is not selected by the
installed launcher or published RC. Its [latest comparison](selection-first-followup.md)
reports both improved costs and remaining selection gaps.

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

## Remaining work

- Avoid near-equivalent discovery refocuses that add no relevant support; retain
  limited example evidence without turning it into a universal contract.
- Reuse identical authored provenance where safe while retaining distinct
  evidence for other facts. Mixed batches may still contain useful new evidence.
- Keep callback inputs, sibling revalidation and deeper initialization/collision
  outcomes explicit gaps until supported. The latest historical callback case
  did not establish that the earlier selection miss was fixed.
- Review isolated Material/reset fact proposals separately before any admission.
  Examples, recipe storage, standards and repository-specific slices stay deferred.
- Qualify any future package separately. Kiro IDE behavior, other machines and
  platforms, broad browser behavior and model-backed inference are not established
  by source checks or these Codex caller trials.

Core facts may apply to Material requests. `candidate_only` is an assessment
status, not a per-fact runtime execution flag. Existing `see_also` links are
available; new relationship semantics and complete application recipes remain
outside this change. Historical browser failures B06/B13 remain failures.

## Evidence and verification

The [audit history](history/caller-retrieval-audits.md) retains all earlier
measurements, frozen rubric changes and failed revisions. Current source checks
pass 348 tests; the isolated answer candidate passes 27. Full local maintenance
still requires the missing provisioned worktree compiler environment. These
source results do not qualify the installed DB, models or hosted generation.
