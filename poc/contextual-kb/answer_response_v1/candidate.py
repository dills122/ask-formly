"""Project complete facts for answers; fetch original provenance separately."""
import copy
from pathlib import Path
import sys

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
sys.path.insert(0, str(POC / 'model_free_v1'))
from model_free_v1.candidate import Service, Store
from model_free_v1.response import fits_packet


from answer_response_v1.identity import identity


def stored_text_status(value):
    """Only a nonblank stored string is an available quote/excerpt."""
    return 'available' if isinstance(value, str) and value.strip() else 'absent'


def excerpt_availability(citations):
    """Metadata is separate so original citation dictionaries stay lossless."""
    return {fid: {
        'authored_summary_quote': stored_text_status(citation['authored_source'].get('quote')),
        'evidence': [dict(id=record['id'], kind=record.get('kind'),
                          stored_excerpt=stored_text_status(record.get('excerpt')))
                     for record in citation['evidence']]}
            for fid, citation in citations.items()}


def validate_ids(fact_ids):
    if (not isinstance(fact_ids, list) or not 1 <= len(fact_ids) <= 16 or
            any(not isinstance(fid, str) or not fid or len(fid) > 300 for fid in fact_ids)):
        raise ValueError('Supply 1..16 fact IDs')


def answer_packet(packet, citations):
    """Leave every fact and selection field intact; replace only provenance."""
    result = copy.deepcopy(packet)
    for key in ('sources', 'evidence', 'citations', 'response'):
        result.pop(key, None)
    result.update(record_kind='answer_facts', response_format='answer-v1',
                  evidence_status='candidate_only')
    result['citations'] = {
        fid: [dict({key: copy.deepcopy(value) for key, value in record.items()
                    if key in ('id', 'kind', 'title', 'status', 'url', 'path', 'lines')},
                   stored_excerpt=stored_text_status(record.get('excerpt')))
              for record in citation['evidence']]
        for fid, citation in citations.items()}
    ids = [fact['id'] for fact in result['facts']]
    result['detailed_provenance'] = {
        'status': 'deferred', 'facts_complete': True,
        'message': 'Claims, conditions, limits and scope are complete. Returned citations support ordinary answers. Fetch detailed provenance only for source quotations, hashes, authored offsets or a requested provenance audit; it is not required merely to answer from these facts.',
        'excerpt_note': 'stored_excerpt describes an evidence record, not the separate authored summary quotation. Absent means no nonblank excerpt is stored in this snapshot; changing formats or fetching the same fact IDs cannot add one.',
        'tool': 'get_formly_provenance',
        'arguments': {'fact_ids': ids, 'formly_version': result['version_context']['selected'],
                      'ui_adapter': result['ui_adapter']}}
    if 'next_action' in result:
        result['next_action']['message'] = ('Assess returned facts with conditions, limits and citations. '
            'Discover/fetch only for unmet claims; detailed provenance is optional unless the task requests it.')
    return result


def bounded_packet(ids, context, factory, tool, extra_args=None):
    """Return all requested records or measured disjoint retries, never a prefix."""
    ids = list(dict.fromkeys(ids))
    packet = factory(ids, context)
    if fits_packet(packet):
        return packet
    batches, selected, oversized = [], [], []

    def append(batch):
        value = factory(batch, context)
        if not fits_packet(value):
            raise ValueError('Internal batch sizing mismatch')
        args = dict(fact_ids=list(batch), formly_version=context['version_context']['selected'],
                    ui_adapter=context['ui_adapter'], **(extra_args or {}))
        batches.append(dict(tool=tool, arguments=args, response_bytes=value['response']['bytes'],
                            transport_bytes=value['response']['transport_bytes']))

    for fid in ids:
        if fits_packet(factory(selected + [fid], context)):
            selected.append(fid)
        else:
            if selected:
                append(selected)
            selected = []
            if fits_packet(factory([fid], context)):
                selected = [fid]
            else:
                oversized.append(fid)
    if selected:
        append(selected)
    result = dict(status='response_too_large' if oversized else 'batch_required',
                  record_kind='batch_instructions', evidence_status='not_delivered', facts=[],
                  message='No requested records were delivered. Use retry_batches exact tool/arguments; do not rediscover IDs. Do not retry unbatchable IDs unchanged.',
                  retry_batches=batches, unbatchable_fact_ids=oversized)
    if not fits_packet(result):
        raise ValueError('Batch instructions exceed budget; request fewer IDs')
    return result


class AnswerService(Service):
    async def lookup(self, *args, **kwargs):
        packet = await super().lookup(*args, **kwargs)
        if not packet.get('facts'):
            return packet
        _, citations = self.store.records([f['id'] for f in packet['facts']],
            packet['version_context']['selected'], packet['ui_adapter'])
        result = answer_packet(packet, citations)
        if not fits_packet(result):
            # No fact dropping or changed retrieval selection to fit the new view.
            raise ValueError('Answer view exceeds response budget; split the request')
        return result

    async def get_facts(self, fact_ids, formly_version=None, ui_adapter=None, response_format='answer'):
        if response_format in ('compact', 'full'):
            return await super().get_facts(fact_ids, formly_version, ui_adapter, response_format)
        if response_format != 'answer':
            raise ValueError('response_format must be answer, compact or full')
        validate_ids(fact_ids)
        context = await self.gate.lookup('Fetch requested evidence', formly_version=formly_version,
                                         ui_adapter=ui_adapter)
        if 'status' in context:
            return context
        facts, citations = self.store.records(fact_ids, context['version_context']['selected'], context['ui_adapter'])
        by_id = {fact['id']: fact for fact in facts}
        # Explicit retry scope must have identical metadata to actual next calls.
        context = await self.gate.lookup('Fetch requested evidence',
            formly_version=context['version_context']['selected'], ui_adapter=context['ui_adapter'])
        def factory(ids, ctx):
            return answer_packet(dict(facts=[by_id[fid] for fid in ids], **ctx),
                                 {fid: citations[fid] for fid in ids})
        return bounded_packet(list(by_id), context, factory, 'get_formly_facts', {'response_format': 'answer'})

    async def get_provenance(self, fact_ids, formly_version, ui_adapter):
        validate_ids(fact_ids)
        if not isinstance(formly_version, str) or (ui_adapter is not None and not isinstance(ui_adapter, str)):
            raise ValueError('Repeat the exact resolved version and adapter from the answer')
        context = await self.gate.lookup('Fetch requested evidence', formly_version=formly_version,
                                         ui_adapter=ui_adapter)
        if 'status' in context:
            return context
        if formly_version != context['version_context']['selected'] or ui_adapter != context['ui_adapter']:
            raise ValueError('Repeat the exact resolved version and adapter from the answer')
        _, citations = self.store.records(fact_ids, context['version_context']['selected'], context['ui_adapter'])
        def factory(ids, ctx):
            return dict(record_kind='detailed_provenance', response_format='provenance-v1',
                        evidence_status='provenance_only', fact_ids=list(ids),
                        citations={fid: copy.deepcopy(citations[fid]) for fid in ids},
                        details_complete=True,
                        excerpt_availability=excerpt_availability({fid: citations[fid] for fid in ids}),
                        excerpt_guidance='An absent stored evidence excerpt is absent from this snapshot, not proof that source text does not exist. Switching answer/compact/full formats or fetching these same IDs cannot add a missing excerpt. Authored quotations are summaries, not substitutes for implementation excerpts. Fetch different relevant facts or inspect pinned external sources when legitimately needed; available stored excerpts are already in these citation records.', **ctx)
        return bounded_packet(list(citations), context, factory, 'get_formly_provenance')
