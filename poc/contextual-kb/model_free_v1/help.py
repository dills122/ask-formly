"""Small scoped onboarding and topic inventory, not additional library knowledge."""
import copy


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
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 1 <= limit <= 32:
        raise ValueError('Use a nonnegative offset and a limit from 1..32')
    if topic is not None and (not isinstance(topic, str) or not topic or len(topic) > 300):
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
            status='help',
            workflow=[
                'Send the unchanged user request and a focused plan to lookup_formly; every question needs a reason.',
                'Copy each condition exactly from request into every bound question. Include known relevant API/config names; do not invent APIs or add unrelated terms.',
                'Assess claims together with conditions, limits, applicability and provenance. ok and candidate_only do not certify answer completeness or execution.',
                'Follow next_action. get_formly_facts accepts 1..16 complete known IDs; discover_formly_candidates pages omitted candidates when more discovery is needed.',
                'Repeat resolved version and adapter for fetch/discovery. Related links suggest candidates, not automatic support.',
            ],
            response=dict(
                compact='citations[id].authored_source_ref resolves in sources; evidence_refs resolve in evidence. Full provenance is shared, not discarded.',
                full='get_formly_facts(response_format="full") expands citations inline when needed.',
                request='Compact lookup summarizes the plan; a large request may be represented by request_ref and request_echo instead of echoed text. Keep the unchanged original request for recovery.',
                omissions='omitted_candidates is a bounded global preview; question omitted_indexes reference it and omitted_count reports all omissions. Discovery pages the complete candidate list. Check global facts before refetching.',
                transport='The default repair/discovery server emits one complete JSON text packet. SDK clients use structuredContent when present, otherwise JSON-decode content[0].text; there is no duplicate structured payload.',
                sizes='Successful compact lookup/fetch is bounded to 28000 UTF-8 packet bytes and 30000 UTF-8 serialized MCP-result bytes. Explicit full fetch has a larger limit. Client-specific rendering and file-spill policies may differ.',
            ),
            limits=dict(questions=6, fetch_ids=16, discovery_records=32, discovery_candidate_bytes=24000),
            project_settings='project_id saves explicit version/UI settings separately from knowledge. Reuse stable IDs and the same server settings file across agents; there is no conversation memory. worktree_id overrides inherit missing project fields. Same-field writes use the last commit. Omit explicit scope only when saved/default scope is intended; fetch/discovery must repeat resolved scope.',
            example=copy.deepcopy(EXAMPLE),
            topics=[dict(topic=name, fact_count=len(ids)) for name, ids in topics.items()][offset:offset + limit],
            total_topics=len(topics),
        )
        total = len(topics)
        count = len(packet['topics'])
    else:
        ids = topics.get(topic, [])
        packet = dict(status='topic' if ids else 'unknown_topic', topic=topic,
                      facts=[dict(id=fid, title=base.store.facts[fid]['title']) for fid in ids[offset:offset + limit]],
                      total_facts=len(ids),
                      next_action='Fetch selected complete IDs with get_formly_facts, preserving this resolved scope. A topic prefix alone is not a fact ID.')
        total = len(ids)
        count = len(packet['facts'])
    packet.update(offset=offset, next_offset=offset + count if offset + count < total else None, **context)
    base.store.verify()
    return packet
