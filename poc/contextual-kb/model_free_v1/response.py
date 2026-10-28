"""Lossless provenance interning and bounded model-free response packets."""
import copy
import hashlib
import json

MAX_RESPONSE_BYTES = 28000
MAX_TRANSPORT_BYTES = 30000


def encoded_size(value):
    """Measure the JSON text emitted by the MCP wrapper, excluding its envelope."""
    return len(json.dumps(value, ensure_ascii=False).encode('utf-8'))


def fingerprint(text):
    return dict(sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(), characters=len(text))


def evidence_packet(facts, citations, response_format='compact'):
    if response_format == 'full':
        return dict(response_format='full-v1', facts=facts, citations=citations)
    if response_format != 'compact':
        raise ValueError('response_format must be compact or full')
    sources = {}
    evidence = {}
    refs = {}

    def intern(record, pool, prefix):
        key = prefix + hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        pool.setdefault(key, copy.deepcopy(record))
        return key

    for fid, citation in citations.items():
        refs[fid] = dict(
            authored_source_ref=intern(citation['authored_source'], sources, 's:'),
            evidence_refs=[intern(record, evidence, 'e:') for record in citation['evidence']])
    return dict(response_format='compact-v1', facts=facts, citations=refs,
                sources=sources, evidence=evidence)


def make_tool_result(packet, error=False):
    """One complete JSON text representation, without a duplicate structured copy."""
    from mcp.types import CallToolResult, TextContent
    return CallToolResult(content=[TextContent(type='text', text=json.dumps(packet, ensure_ascii=False))],
                          isError=error)


def transport_size(packet, error=False):
    """Size of the SDK CallToolResult, including escaping inside the text block."""
    return encoded_size(make_tool_result(packet, error).model_dump(mode='json'))


def measure_packet(packet, error=False):
    """Include both size fields in the measured packet and SDK result budgets."""
    packet.setdefault('response', {}).update(max_bytes=MAX_RESPONSE_BYTES,
        max_transport_bytes=MAX_TRANSPORT_BYTES,
        measurement='UTF-8 JSON packet and SDK CallToolResult.model_dump(mode=json); JSON-RPC envelope excluded')
    packet['response'].update(bytes=0, transport_bytes=0)
    while True:
        size = encoded_size(packet)
        transport = transport_size(packet, error)
        if packet['response']['bytes'] == size and packet['response']['transport_bytes'] == transport:
            return size
        packet['response'].update(bytes=size, transport_bytes=transport)


def fits_packet(packet, error=False):
    measure_packet(packet, error)
    return (packet['response']['bytes'] <= MAX_RESPONSE_BYTES and
            packet['response']['transport_bytes'] <= MAX_TRANSPORT_BYTES)


def omitted_preview(ranked, chosen, limit=16):
    """Deduplicate the preview while preserving every question's omission count."""
    chosen = set(chosen)
    groups = [[fid for fid in ids if fid not in chosen] for ids in ranked]
    order = []
    for rank in range(max(map(len, groups), default=0)):
        for ids in groups:
            if rank < len(ids) and ids[rank] not in order:
                order.append(ids[rank])
    preview = [dict(id=fid, question_indexes=[i for i, ids in enumerate(groups) if fid in ids])
               for fid in order[:limit]]
    return groups, preview, len(order)
