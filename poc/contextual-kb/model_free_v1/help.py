"""Small scoped onboarding and topic inventory, not additional library knowledge."""
import copy
from typing import Annotated
from pydantic import Field, StrictInt


HELP_PAGE_MAX = 32
HELP_TOPIC_MAX = 300
HelpOffset = Annotated[StrictInt, Field(ge=0, description="Nonnegative page offset. Use the returned next_offset with the same topic and resolved scope.")]
HelpLimit = Annotated[StrictInt, Field(ge=1, le=HELP_PAGE_MAX, description="1..32 topics or fact IDs per help page; default 16. Page using next_offset rather than increasing beyond 32.")]
HelpTopic = Annotated[str | None, Field(min_length=1, max_length=HELP_TOPIC_MAX, description="Exact topic prefix returned by help_formly, 1..300 characters; omit to list topics. A topic is not a fact ID.")]


EXAMPLE = {
    'request': 'For Formly 6.3.12 with Material, hide a field without losing its model value. Does its control stay registered?',
    'plan': {
        'formly_questions': [
            {'question': 'For Formly 6.3.12 with Material, how does resetOnHide let me hide a field without losing its model value?',
             'reason': 'Find the value-retention setting and its limits.'},
            {'question': 'For Formly 6.3.12 with Material, when I hide a field without losing its model value, does its control stay registered?',
             'reason': 'Distinguish model retention from control registration.'},
        ],
        'library_constraints': {'formly_version': '6.3.12', 'ui_adapter': 'Material'},
        'condition_bindings': [
            {'condition': 'For Formly 6.3.12 with Material', 'question_indexes': [0, 1]},
            {'condition': 'hide a field without losing its model value', 'question_indexes': [0, 1]},
        ],
    },
}


async def help_packet(service, topic=None, formly_version=None, ui_adapter=None, offset=0, limit=16):
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= HELP_PAGE_MAX:
        raise ValueError('Use a nonnegative offset and a limit from 1..32')
    if topic is not None and (not isinstance(topic, str) or not topic or len(topic) > HELP_TOPIC_MAX):
        raise ValueError('topic must be a nonempty topic prefix of at most 300 characters')
    base = getattr(service, 'base', service)
    context = await base.gate.lookup('Read Formly tool help', formly_version=formly_version, ui_adapter=ui_adapter)
    if 'status' in context:
        return context
    base.store.verify()
    eligible = base.store.scopes(context['version_context']['selected'], context['ui_adapter'])
    topics = {}
    for fid in sorted(eligible):
        prefix = fid.split('/', 1)[0]
        topics.setdefault(prefix, []).append(fid)
    if topic is None:
        packet = dict(
            status='help', record_kind='workflow_and_topic_inventory',
            workflow=[
                'Send the unchanged user request and a focused plan to lookup_formly; every question needs a reason. Copy each condition exactly into every bound question; preserve scope and all requested decisions.',
                'Maintain a working evidence ledger per requested decision: supported claims/fact IDs, missing distinction, next evidence needed. Track IDs already listed and complete records/provenance already delivered. Assess claims with conditions, limits and scope; candidate_only is not completeness or execution.',
                'Check lookup facts and omitted previews first. Prioritize unmet decisions; if all are supported, answer without exhausting omissions. For hiding, separately obtain control-registration and value-retention support. Shared words, titles and new IDs do not establish the missing claim.',
                'discover_formly_candidates(question_index=i) selects omissions for an original question; omit the selector for the global stream. Optional focus (1..500 nonblank characters) reranks only original omissions, adding no candidates and relaxing no conditions. It excludes lookup-delivered facts, not later fetches.',
                'Changing focus or question_index restarts offset zero: a reranked first page is not a later page. To inspect later candidates use next_offset with unchanged request, plan, scope, question_index and focus.',
                'Identify the evidence owner before recovery: Formly, a versioned dependency, or application code. Fetch relevant already-listed IDs when full records could settle the decision; seek mechanisms, not a whole recipe. Retain relevant Formly integration branches. For dependency-only gaps, establish the actual dependency version and use matching primary sources with available authorized tools; do not infer it from Formly or use latest by default. If version/access is unavailable, state the exact handoff. Request custom implementation/runtime evidence for project-owned gaps; repeated Formly refocus cannot establish unseen code. Keep useful supported advice and labeled proposals; handoff is not corpus exhaustion.',
                'Before another discovery, name the missing distinction and what a new result could establish. Update the ledger after recovery. Do not repeat equivalent first-page searches with synonyms merely to spend a budget. Continue only for a concrete next step: a relevant unfetched candidate, unseen page, or genuinely different distinction.',
                'When successive refocuses add no relevant support and no concrete next step remains, stop that branch and disclose the exact gap while addressing other unmet decisions. This is not a fixed call cap. Overlap, page limits and no useful match prove neither corpus exhaustion nor library nonexistence; never mark an unresolved decision complete.',
                'Batch independent already-selected IDs (1..16) instead of one fetch per decision; read earlier when conditions determine the next search. ID count does not guarantee byte size. batch_required delivers no facts: use retry_batches exact arguments, without rediscovery or guessed splits. response_too_large identifies unbatchable IDs; do not repeat them unchanged. Batch instructions are not evidence. Keep optional answer elaboration from creating unnecessary searches.',
                'Repeat resolved version/adapter for fetch/discovery. Related links are candidates, not automatic support. Use exact returned help topics and limit 1..32 with next_offset; do not guess topic names.',
            ],
            response=dict(
                record_kinds='complete_evidence: reuse full returned facts; claims_without_provenance: fetch selected IDs; topic_inventory: IDs/titles only; batch_instructions: no facts delivered. candidate_only is relevance assessment; truncated is omitted candidates, not clipped facts.',
                compact='citations[id].authored_source_ref resolves in sources; evidence_refs resolve in evidence. Full provenance is shared, not discarded.',
                full='get_formly_facts(response_format="full") expands citations inline when needed.',
                request='Compact lookup summarizes the plan; a large request may be represented by request_ref and request_echo instead of echoed text. Keep the unchanged original request for recovery.',
                omissions='omitted_candidates is a bounded global preview; question omitted_indexes reference it and omitted_count reports all omissions. Discovery pages the complete candidate list or one original question_index. Targeted pages exclude globally delivered facts. Optional focus reorders those omissions only. Keep request, plan, scope, selector and focus unchanged between pages; a question_ref identifies the selected question, not a semantic completeness certificate.',
                transport='The default repair/discovery server emits one complete JSON text packet. SDK clients use structuredContent when present, otherwise JSON-decode content[0].text; there is no duplicate structured payload.',
                sizes='Successful compact lookup/fetch is bounded to 28000 UTF-8 packet bytes and 30000 UTF-8 serialized MCP-result bytes. Explicit full fetch has a larger limit. Client-specific rendering and file-spill policies may differ.',
            ),
            limits=dict(help_records=HELP_PAGE_MAX, help_topic_characters=HELP_TOPIC_MAX, questions=6, fetch_ids=16, discovery_records=32, discovery_candidate_bytes=24000, discovery_focus_characters=500),
            project_settings='project_id saves explicit version/UI settings separately from knowledge. Reuse stable IDs and the same server settings file across agents; there is no conversation memory. worktree_id overrides inherit missing project fields. Same-field writes use the last commit. Omit explicit scope only when saved/default scope is intended; fetch/discovery must repeat resolved scope.',
            example=copy.deepcopy(EXAMPLE),
            topics=[dict(topic=name, fact_count=len(ids)) for name, ids in topics.items()][offset:offset + limit],
            total_topics=len(topics),
        )
        total = len(topics)
        count = len(packet['topics'])
    else:
        ids = topics.get(topic, [])
        packet = dict(status='topic' if ids else 'unknown_topic', record_kind='topic_inventory', topic=topic,
                      facts=[dict(id=fid, title=base.store.facts[fid]['title']) for fid in ids[offset:offset + limit]],
                      total_facts=len(ids),
                      next_action='Fetch selected complete IDs with get_formly_facts, preserving this resolved scope. A topic prefix alone is not a fact ID.')
        total = len(ids)
        count = len(packet['facts'])
    packet.update(offset=offset, next_offset=offset + count if offset + count < total else None, **context)
    base.store.verify()
    return packet
