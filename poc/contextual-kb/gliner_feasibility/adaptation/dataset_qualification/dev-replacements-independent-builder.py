"""Manual independent labels for seven replacement development questions.

Only questions-v2.json and the annotation contract are read. Explicit chosen
strings are resolved uniquely; output creation is exclusive to preserve raw data.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pilot.contract import FIELDS, ENTITY_TYPES, validate_annotation

IDS = ['D013', 'D014', 'D018', 'D021', 'D022', 'D025', 'D030']
source = json.loads((HERE / 'questions-v2.json').read_text())
questions = {q['id']: q['question'] for q in source['dev'] if q['id'] in IDS}
rows = []


def span(question, text):
    offsets = [m.start() for m in re.finditer(re.escape(text), question)]
    assert len(offsets) == 1, (question, text, offsets)
    return {'text': text, 'start': offsets[0], 'end': offsets[0] + len(text)}


def annotate(id, fields, *, api=(), custom=(), literals=(), versions=(), adapters=(), relations=(), rationale):
    q = questions[id]
    a = {'id': 'a1', **{field: [span(q, text) for text in fields.get(field, [])] for field in FIELDS}}
    a['target_anchor'] = min(a['targets'], key=lambda s: s['start'])
    row = {
        'id': id,
        'question': q,
        'status': 'needs_clarification' if a['unresolved_references'] else 'clear',
        'aspects': [a],
        'entities': {key: [span(q, text) for text in texts]
                     for key, texts in zip(ENTITY_TYPES, [api, custom, literals, versions, adapters])},
        'relations': [{'kind': kind, 'head': span(q, head), 'tail': span(q, tail)}
                      for kind, head, tail in relations],
        'rationale': rationale,
    }
    rows.append(validate_annotation(row))


annotate('D013', {
    'targets': ["props.attributes['data-testid']"],
    'request_cues': ['How do I set'],
    'identifiers': ["props.attributes['data-testid']", "'data-testid'", "'customer-input'"],
    'literals': ["'data-testid'", "'customer-input'"],
}, api=["props.attributes['data-testid']"],
   custom=["'data-testid'", "'customer-input'"],
   literals=["'data-testid'", "'customer-input'"],
   relations=[('has_value', "props.attributes['data-testid']", "'customer-input'")],
   rationale='One assignment request preserves the complete API lookup. The custom data-attribute name and supplied test identifier are retained as quoted custom names and literals; the assigned value belongs to the full lookup, not to props.attributes as a whole.')

annotate('D014', {
    'targets': ["parsers that transform '  Ada  ' into 'Ada'"],
    'request_cues': ['Where do I attach'],
    'identifiers': ['parsers'],
    'literals': ["'  Ada  '", "'Ada'"],
}, api=['parsers'], literals=["'  Ada  '", "'Ada'"],
   rationale='One parser-attachment location is requested. The complete parser noun phrase retains the specified transformation direction, and both quoted strings preserve their exact whitespace. These are example input/output strings, not values assigned to the parsers API, so no has_value relation is invented.')

annotate('D018', {
    'targets': ['an accessible name'],
    'request_cues': ['how do I supply'],
    'conditions': ['for a custom widget'],
    'versions': ['Formly 7'],
}, versions=['Formly 7'],
   rationale='The accessible name is the requested target, scoped to the custom widget and Formly 7. No actual custom widget identifier or accessibility API is supplied.')

annotate('D021', {
    'targets': ['the label', 'the placeholder', 'the description'],
    'request_cues': ['should', 'follow'],
    'conditions': ['If it changes'],
    'references': ['it'],
    'unresolved_references': ['it'],
}, rationale='This is one choice about the label following one of two alternatives. The forward reference it could refer to the placeholder, description, or label; the question does not identify which change is the triggering condition.')

annotate('D022', {
    'targets': ['the custom validator'],
    'request_cues': ['how do I configure'],
    'conditions': ['Before it runs'],
    'references': ['it'],
    'resolved_antecedents': ['the custom validator'],
}, relations=[('refers_to', 'it', 'the custom validator')],
   rationale='The custom validator is the only available referent for it, even though it is named later in the sentence. The configuration request retains the before-execution condition without inventing a validator registration name.')

annotate('D025', {
    'targets': ['properties of the former'],
    'request_cues': ['Which', 'can depend on'],
    'references': ['the former', 'the latter'],
    'resolved_antecedents': ['the schema', 'the model'],
}, relations=[('refers_to', 'the former', 'the schema'), ('refers_to', 'the latter', 'the model')],
   rationale='Former and latter resolve to the ordered pair schema and model, respectively. The question asks which schema properties may depend on the model; it does not ask two separate questions or imply any allowed dependency.')

annotate('D030', {
    'targets': ["an upload field's accepted file-format list"],
    'request_cues': ['Where is', 'configured'],
}, rationale='The complete noun phrase identifies the accepted-format list for the upload field, with one configuration-location ask. No exact property, MIME type, or file extension is supplied.')

assert [row['id'] for row in rows] == IDS
for row in rows:
    validate_annotation(row)
with (HERE / 'dev-replacements-independent.json').open('x') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'Validated and wrote {len(rows)} independent replacement annotations.')
