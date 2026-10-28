"""Bounded fact discovery for the caller; no inference or relevance certification."""
import json


def catalog_page(packet, records, *, offset=0, limit=16, byte_budget=24000):
    """Page existing omitted candidates, retaining complete fact constraints.

    records must resolve IDs in the packet's already-resolved version/adapter.
    Candidate bytes exclude the envelope; discover also checks the complete
    single-text SDK tool result before returning a page.
    Pagination is stable only for the same request, plan and frozen knowledge.
    """
    if (type(offset) is not int or offset < 0 or type(limit) is not int
            or not 1 <= limit <= 32 or type(byte_budget) is not int
            or not 2 <= byte_budget <= 24000):
        raise ValueError('Invalid discovery pagination or byte budget')
    if packet.get('status') not in ('ok', 'no_evidence'):
        return packet
    seen = {fact['id'] for fact in packet['facts']}
    groups = [q['omitted_ids'] for q in packet['questions']]
    ordered = []
    for rank in range(max(map(len, groups), default=0)):
        for group in groups:
            if rank < len(group) and group[rank] not in seen:
                seen.add(group[rank])
                ordered.append(group[rank])
    selected = []
    for fid in ordered[offset:offset + limit]:
        record = records([fid])[0]
        prospective = selected + [record]
        if len(json.dumps(prospective, ensure_ascii=False).encode()) > byte_budget:
            if not selected:
                raise ValueError('Budget cannot fit one complete candidate; increase budget or fetch its full fact separately')
            break
        selected = prospective
    next_offset = offset + len(selected)
    return dict(status='candidates' if selected else 'exhausted', candidates=selected,
                offset=offset, next_offset=next_offset if next_offset < len(ordered) else None,
                total_omitted_candidates=len(ordered),
                candidate_bytes=len(json.dumps(selected, ensure_ascii=False).encode()),
                max_candidate_bytes=byte_budget,
                evidence_status='discovery_only_fetch_full_citations')


async def discover(service, request, plan=None, *, offset=0, limit=16, **scope):
    """Reuse the frozen repair/scope gate before exposing any candidate summary."""
    packet, error = await service.lookup(request, plan=plan, **scope)
    if packet.get('status') not in ('ok', 'no_evidence'):
        return packet, error
    version = packet['version_context']['selected']
    adapter = packet['ui_adapter']
    # Lookup exposes only a bounded, deduplicated preview. Recompute the full
    # deterministic candidate order after the same validated scope/plan gate.
    # Never page the preview itself: doing so silently loses later candidates.
    from model_free_v1.candidate import normalize
    questions = normalize(request, plan)[0]['formly_questions'] if plan is not None else [dict(question=request)]
    search = getattr(service.store, 'candidates', service.store.search)
    delivered = {fact['id'] for fact in packet['facts']}
    catalog = dict(status=packet['status'], facts=packet['facts'], questions=[
        dict(omitted_ids=[fid for fid in search(q['question'], version, adapter) if fid not in delivered])
        for q in questions])
    def records(ids):
        # Full claims, conditions, limits and applicability; omit only heavy quotes.
        return service.store.records(ids, version, adapter)[0]
    from model_free_v1.response import fits_packet
    while True:
        page = catalog_page(catalog, records, offset=offset, limit=limit)
        page.update(version_context=packet['version_context'], ui_adapter=adapter,
                    next_action=dict(type='assess_candidates_then_fetch', tool='get_formly_facts',
                                     message='Select relevant IDs; fetch full citations in this exact scope before answering. More pages are discovery, not proof of support.'))
        if fits_packet(page):return page, False
        count=len(page['candidates'])
        if count<=1:
            raise ValueError('Tool-result budget cannot fit one complete candidate; fetch its full fact separately')
        limit=count-1
