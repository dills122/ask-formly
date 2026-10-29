# Isolated answer/provenance candidate

Use ask-formly for pinned Formly library evidence, not application inspection.
Preserve the user's unchanged request, version, adapter and conditions in your
focused question plan. Call help_formly for the valid plan example when needed.

Default lookup_formly/get_formly_facts returns answer_facts: every delivered fact
has its complete claim, context, conditions, limits, applicability and related
links. Source citation IDs, URLs and locations support ordinary cited answers.
Assess relevance and compose the answer; candidate_only does not certify the
answer. detailed_provenance.status=deferred means quotations, hashes and authored
offsets were not delivered, not that claims or qualifications were clipped.

Fetch get_formly_provenance only when a requested source audit, quotation, hash or
offset requires those details. Use the returned exact resolved scope and selected
fact IDs. It returns complete original citation records without repeating facts.
Do not claim to have inspected detailed provenance without receiving it.

Discovery lists claims without usable citations. Before another page or refocus,
map each unmet decision to the already-listed claims, conditions and limits.
Batch-fetch suitable selected IDs with get_formly_facts, then reassess remaining
gaps. Retain partial support from a worked example without treating it as a full
API contract. Continue paging/refocus only for facets with no suitable current
candidate; do not fetch irrelevant IDs or mark unresolved facets complete. Reuse
complete delivered facts. Stop unsupported branches with an explicit gap, not
invented evidence or repeated synonym searches. Related links are not additional
delivered support. Dependency and application gaps need evidence from
those owners; this library service cannot inspect custom code or establish an
unknown dependency version.

batch_required contains no records. Use retry_batches exact tool and arguments.
response_too_large identifies unsplittable IDs; do not retry them unchanged.
truncated/omitted counts refer to candidates omitted from lookup, never clipped
facts. Explicit compact/full fetch retains the baseline evidence formats.

Each lightweight citation reports stored_excerpt=available or absent for that
specific evidence record. Available means a nonblank excerpt is stored; retrieve
provenance when the requested quotation/audit needs it. Absent means no such
excerpt is stored in this knowledge snapshot, not that source text does not exist.
Changing answer/compact/full format or refetching the same fact IDs cannot add
that missing excerpt. An authored summary quote is not an implementation excerpt.
After detailed provenance arrives, do not repeat the same fetch seeking absent
text. Different relevant facts or authorized inspection of pinned external source
locations remain legitimate recovery when the task needs more evidence.

Discovery requires the complete original lookup plan on every call, even after a
successful lookup. The service stores no conversation plan. Keep the unchanged
request, resolved scope and selected question/focus/paging arguments when repairing
a discovery plan error; correct only the reported issue, without a new lookup or
a smaller replacement plan.

Keep a source-evidence ledger as well as fact IDs. Reuse a previously received
source record only when evidence ID, release and source URL/path/lines agree, and
its hash agrees when provided. Do not repeat a source fetch merely because another
fact cites that same record. However, shared source evidence does not replace a
different fact's authored quotation, offsets, applicability or other evidence.
Fetch those distinct per-fact details when the request needs them. The service
does not keep a global seen-record cache or suppress requested provenance.
