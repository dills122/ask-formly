"""Independent source-only replacement annotations; no model or answer labels."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pilot.contract import FIELDS, ENTITY_TYPES, validate_annotation

IDS = ['D013', 'D014', 'D018', 'D021', 'D022', 'D025', 'D030']
questions = {r['id']: r['question'] for r in json.loads((HERE / 'questions-v2.json').read_text())['dev'] if r['id'] in IDS}
rows = []


def annotate(identifier, specs, entities=None, relations=(), rationale=''):
    q = questions[identifier]
    def span(selector):
        if isinstance(selector, tuple):
            text, occurrence = selector
        else:
            text, occurrence = selector, None
        starts = [m.start() for m in re.finditer(re.escape(text), q)]
        if occurrence is None:
            if len(starts) != 1:
                raise ValueError((identifier, 'ambiguous or missing substring', selector, starts))
            occurrence = 0
        if not 0 <= occurrence < len(starts):
            raise ValueError((identifier, 'missing occurrence', selector))
        start = starts[occurrence]
        end = start + len(text)
        if start and (q[start - 1].isalnum() or q[start - 1] == '_') and (text[0].isalnum() or text[0] == '_'):
            raise ValueError((identifier, 'partial token start', selector))
        if end < len(q) and (q[end].isalnum() or q[end] == '_') and (text[-1].isalnum() or text[-1] == '_'):
            raise ValueError((identifier, 'partial token end', selector))
        return {'text': text, 'start': start, 'end': end}
    aspects = []
    for i, spec in enumerate(specs, 1):
        aspect = {field: [span(s) for s in spec.get(field, [])] for field in FIELDS}
        aspect.update(id=f'a{i}', target_anchor=min(aspect['targets'], key=lambda s: s['start']))
        aspects.append(aspect)
    row = dict(id=identifier, question=q,
               status='needs_clarification' if any(a['unresolved_references'] for a in aspects) else 'clear',
               aspects=aspects,
               entities={kind: [span(s) for s in (entities or {}).get(kind, [])] for kind in ENTITY_TYPES},
               relations=[dict(kind=k, head=span(h), tail=span(t)) for k, h, t in relations],
               rationale=rationale)
    rows.append(validate_annotation(row))


annotate('D013', [dict(
    targets=["props.attributes['data-testid']"], request_cues=['How do I set'],
    identifiers=["props.attributes['data-testid']", "'data-testid'", "'customer-input'"],
    literals=["'data-testid'", "'customer-input'"]
)], entities={'api':["props.attributes['data-testid']"],
             'custom_identifier':["'data-testid'", "'customer-input'"],
             'literal':["'data-testid'", "'customer-input'"]},
    relations=[('has_value', "props.attributes['data-testid']", "'customer-input'")],
    rationale='The full attribute access path is the API target. The supplied data attribute key and test identifier retain exact quoted spellings; only the complete access path is assigned the supplied value.')

annotate('D014', [dict(
    targets=['parsers'], request_cues=['Where do I attach'],
    conditions=["that transform '  Ada  ' into 'Ada'"],
    identifiers=['parsers'], literals=["'  Ada  '", "'Ada'"]
)], entities={'api':['parsers'], 'literal':["'  Ada  '", "'Ada'"]},
    rationale='One attachment-location request specifies a parser transformation. The padded input and output are distinct literal spans; transformation is not a has_value assignment.')

annotate('D018', [dict(
    targets=['an accessible name'], request_cues=['how do I supply'],
    conditions=['for a custom widget'], versions=['Formly 7']
)], entities={'version':['Formly 7']},
    rationale='The widget identifies the naming context. The explicit version is scope, and no implementation identifier is supplied.')

annotate('D021', [dict(
    targets=['the label', 'the placeholder', 'the description'],
    request_cues=['should', 'follow'], conditions=['If it changes'],
    references=['it'], unresolved_references=['it']
)], rationale='One choice of relationship is requested, retaining the label and both candidate sources. The forward reference it could denote the label, placeholder, or description; the source does not uniquely resolve which changes.')

annotate('D022', [dict(
    targets=['the custom validator'], request_cues=['how do I configure'],
    conditions=['Before it runs'], references=['it'],
    resolved_antecedents=['the custom validator']
)], relations=[('refers_to', 'it', 'the custom validator')],
    rationale='The forward reference resolves to the sole runnable entity explicitly named, the custom validator. Before-running timing qualifies the configuration request.')

annotate('D025', [dict(
    targets=['properties of the former'], request_cues=['Which', 'can depend on'],
    references=['the former', 'the latter'], resolved_antecedents=['the schema', 'the model']
)], relations=[('refers_to', 'the former', 'the schema'), ('refers_to', 'the latter', 'the model')],
    rationale='Former and latter resolve to the ordered coordinated pair schema and model, respectively. The renderer is the subject of the setup sentence, not a member of that pair. This is one property-dependency request.')

annotate('D030', [dict(
    targets=["an upload field's accepted file-format list"],
    request_cues=['Where is', 'configured']
)], rationale='One configuration-location request retains the upload-field owner and accepted-format qualifier in its target.')

assert [row['id'] for row in rows] == IDS
(HERE / 'dev-replacements-author.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
print(f'Validated {len(rows)} independent development replacement annotations.')
