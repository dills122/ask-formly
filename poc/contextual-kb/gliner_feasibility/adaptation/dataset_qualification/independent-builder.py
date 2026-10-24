"""Independent manual annotations; helpers only locate explicitly chosen spans.

Inputs are questions.json and the annotation contract. No other annotations,
models, corpus, or evaluators are consulted. Raw output is created exclusively.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pilot.contract import FIELDS, ENTITY_TYPES, validate_annotation

source = json.loads((HERE / 'questions.json').read_text())
selected = [q for q in source['train'] if q['id'] in source['double_annotate_training_ids']] + source['dev']
questions = {q['id']: q['question'] for q in selected}
rows = []


def locate(q, choice):
    """A tuple selects a specified 1-based occurrence; bare text must be unique."""
    text, occurrence = choice if isinstance(choice, tuple) else (choice, None)
    matches = [m.start() for m in re.finditer(re.escape(text), q)]
    if occurrence is None:
        assert len(matches) == 1, (q, choice, matches)
        start = matches[0]
    else:
        assert 1 <= occurrence <= len(matches), (q, choice, matches)
        start = matches[occurrence - 1]
    return {'text': text, 'start': start, 'end': start + len(text)}


def aspect(targets, cues, **kwargs):
    return {'targets': targets, 'request_cues': cues, **kwargs}


def row(id, aspects, *, api=(), custom=(), literal=(), version=(), adapter=(), relations=(), rationale='The explicit wording identifies the requested aspect and its scope.'):
    q = questions[id]
    result = {'id': id, 'question': q, 'status': 'clear', 'aspects': [],
              'entities': {}, 'relations': [], 'rationale': rationale}
    for n, raw in enumerate(aspects, 1):
        a = {'id': f'a{n}'}
        for field in FIELDS:
            a[field] = [locate(q, text) for text in raw.get(field, [])]
        a['target_anchor'] = min(a['targets'], key=lambda s: s['start'])
        if a['unresolved_references']:
            result['status'] = 'needs_clarification'
        result['aspects'].append(a)
    for field, choices in zip(ENTITY_TYPES, [api, custom, literal, version, adapter]):
        result['entities'][field] = [locate(q, text) for text in choices]
    for kind, head, tail in relations:
        result['relations'].append({'kind': kind, 'head': locate(q, head), 'tail': locate(q, tail)})
    rows.append(validate_annotation(result))


row('T001', [
    aspect(['the new row'], ['where is', 'placed'], conditions=['When an address row is inserted']),
    aspect(['which field'], ['receives focus'], conditions=['When an address row is inserted']),
], rationale='Row placement and the recipient of focus require distinct answers under the same insertion condition.')
row('T005', [
    aspect(["the section's model entries"], ['what happens to'], conditions=['When a repeated section is removed']),
    aspect(['validation messages'], ['what happens to'], conditions=['When a repeated section is removed']),
], rationale='Model entries and validation messages are independent consequences of section removal.')
row('T009', [
    aspect(['a loading indicator'], ['how do I show'], conditions=['While options are loading']),
    aspect(['selection of stale options'], ['how do I', 'prevent'], conditions=['While options are loading'], negative_constraints=['prevent selection of stale options']),
], rationale='Showing progress and preventing stale selection are separate asks; prevention attaches only to selection.')
row('T013', [
    aspect(['the group'], ['how is', 'rendered'], conditions=['When a field group becomes visible']),
    aspect(['its child labels'], ['how are', 'displayed'], conditions=['When a field group becomes visible'], references=['its'], resolved_antecedents=['a field group']),
], relations=[('refers_to', 'its', 'a field group')], rationale='Group rendering and child-label display are separate asks; its denotes the newly visible field group.')
row('T017', [aspect(['a field label'], ['How can I update'], negative_constraints=['without changing its key'], references=['its'], resolved_antecedents=['a field'])], relations=[('refers_to', 'its', 'a field')])
row('T021', [aspect(['an error message'], ['How can I hide'], negative_constraints=['without disabling the validator'])])
row('T025', [aspect(['one section'], ['How do I reset'], negative_constraints=['without resetting the sibling section'])])
row('T029', [aspect(['a description'], ['How do I compute'], negative_constraints=['without mutating the source model'])])
row('T033', [aspect(['FormlyFieldConfig<ContactProps>'], ['Where do I declare'], conditions=['when ContactProps has a field named résumé'], identifiers=['FormlyFieldConfig<ContactProps>', ('ContactProps', 1), ('ContactProps', 2), 'résumé'])],
    api=['FormlyFieldConfig<ContactProps>'], custom=[('ContactProps', 1), ('ContactProps', 2), 'résumé'], rationale='The generic API expression and both supplied custom type-name occurrences are preserved, as is the Unicode field name.')
row('T037', [aspect(["key 'address.zip'", "key ['address', 'zip']"], ['How does', 'differ from'], identifiers=[('key', 1), ('key', 2)], literals=["'address.zip'", "['address', 'zip']"])],
    api=[('key', 1), ('key', 2)], literal=["'address.zip'", "['address', 'zip']"], relations=[('has_value', ('key', 1), "'address.zip'"), ('has_value', ('key', 2), "['address', 'zip']")], rationale='One comparison retains both complete keyed alternatives and their individual identifier/value pairings; the supplied array is one literal.')
row('T041', [aspect(['an expression'], ['How do I attach'], identifiers=["expressions['props.description']"], literals=["'props.description'"])],
    api=["expressions['props.description']"], literal=["'props.description'"], rationale='Attaching the expression is one ask. The whole API expression is retained; its quoted lookup string is preserved without inventing an assignment relation.')
row('T045', [
    aspect(["className: 'col-6'"], ['Where should', 'be placed'], identifiers=['className'], literals=["'col-6'"]),
    aspect(["fieldGroupClassName: 'grid'"], ['Where should', 'be placed'], identifiers=['fieldGroupClassName'], literals=["'grid'"]),
], api=['className', 'fieldGroupClassName'], literal=["'col-6'", "'grid'"], relations=[('has_value', 'className', "'col-6'"), ('has_value', 'fieldGroupClassName', "'grid'")], rationale='The placement question is independently answerable for each of two differently named configuration properties.')
row('T049', [aspect(['prefix text'], ['where is', 'configured'], versions=['Formly 6.3.12'], ui_adapters=['Material'])], version=['Formly 6.3.12'], adapter=['Material'])
row('T053', [aspect(['select options'], ['how are', 'supplied'], versions=['Formly 6'], ui_adapters=['PrimeNG'])], version=['Formly 6'], adapter=['PrimeNG'])
row('T057', [aspect(['description placement'], ['how does', 'differ'], versions=['Formly 6.3.12'], ui_adapters=['Material', 'Bootstrap'])], version=['Formly 6.3.12'], adapter=['Material', 'Bootstrap'], rationale='The comparison has one behavior target and two adapter scopes.')
row('T061', [
    aspect(['an input'], [('how do I configure', 1)], versions=['Formly 6'], ui_adapters=['Material']),
    aspect(['a textarea'], [('how do I configure', 2)], versions=['Formly 7'], ui_adapters=['Bootstrap']),
], version=['Formly 6', 'Formly 7'], adapter=['Material', 'Bootstrap'], rationale='Each configuration request retains only its own explicitly local version and adapter.')
row('T065', [aspect(['that group'], ['How do I reset'], references=['that group'], unresolved_references=['that group'])], rationale='That group could denote either the billing group or the shipping group.')
row('T069', [aspect(['Which one'], ['does', 'use'], references=['this'], unresolved_references=['this'])], rationale='The choice between initial and current values is the question itself, but this has no specified consuming setting or operation.')
row('T073', [aspect(['it'], ['How do I remove'], references=['it'], unresolved_references=['it'])], rationale='It could refer to the expression controlling the label or the expression controlling the description.')
row('T077', [aspect(['that behavior'], ['How do I stop'], negative_constraints=['stop that behavior'], references=['that behavior', 'this field'], unresolved_references=['that behavior', 'this field'])], rationale='Neither the behavior to stop nor the indicated field is identified in the question.')
row('T081', [aspect(['custom validation functions'], ['Where are', 'configured'])])
row('T085', [aspect(['a label', 'a description'], ['How does', 'differ from'])], rationale='A single comparison asks for the distinction between label and description.')
row('T089', [aspect(['related fields'], ['How do I group', 'visually'])])
row('T093', [aspect(['logic'], ['Where can I run'], conditions=['when a field is initialized'])])

row('D001', [
    aspect(['the city choices'], ['how do I refresh'], conditions=['When a country selection invalidates a city choice']),
    aspect(['the old choice'], ['how do I', 'explain why', 'disappeared'], conditions=['When a country selection invalidates a city choice']),
], rationale='Refreshing dependent choices and explaining disappearance are independent asks under a shared invalidation condition.')
row('D002', [
    aspect(['progress'], ['how can I display'], conditions=['During submission']),
    aspect(['a second submission'], ['how can I', 'prevent'], conditions=['During submission'], negative_constraints=['prevent a second submission']),
], rationale='Progress display and preventing duplicate submission are distinct; prevention applies only to the second ask.')
row('D003', [
    aspect(['the moved row'], ['how can I identify'], conditions=['After dragging a row to a new position']),
    aspect(['its expanded state'], ['how can I', 'retain'], conditions=['After dragging a row to a new position'], references=['its'], resolved_antecedents=['the moved row']),
], relations=[('refers_to', 'its', 'the moved row')], rationale='Identity and expanded-state retention are separate asks; its uniquely denotes the moved row.')
row('D004', [
    aspect(['each error'], ['where can I attach'], conditions=['When a server returns errors for two fields']),
    aspect(['those server errors'], ['how can I clear', 'later'], conditions=['When a server returns errors for two fields'], references=['those server errors'], resolved_antecedents=['errors for two fields']),
], relations=[('refers_to', 'those server errors', 'errors for two fields')], rationale='Attachment and later clearing are separate operations. Those server errors refers to the errors returned for the two fields.')
row('D005', [
    aspect(['a computed summary'], ['explain formatting']),
    aspect(['a computed summary'], ['explain', 'recomputation'], conditions=['when an input changes']),
], rationale='Formatting and recomputation are separate operations on the same summary target. The trailing input-change condition directly qualifies recomputation.')
row('D006', [aspect(['whether submission is allowed'], ['How can I check'], negative_constraints=['without marking every field touched'])])
row('D007', [aspect(['a server-side error'], ['Can I report'], negative_constraints=['without running the server check again'])])
row('D008', [aspect(['a read-only preview'], ['How can I show'], negative_constraints=['without copying the model into another object'])])
row('D009', [aspect(['one cell'], ['How do I prevent editing'], negative_constraints=['prevent editing one cell', 'without disabling the entire row'])], rationale='Preventing cell editing is the requested negative outcome, constrained against disabling the parent row.')
row('D010', [aspect(['a configuration'], ['Can I reuse'], negative_constraints=['without assuming that Material is installed'], ui_adapters=['Material'])], adapter=['Material'], rationale='Material is explicitly mentioned as an adapter inside a negated assumption; the full constraint prevents treating installation as given.')
row('D011', [aspect(['the model'], ['when is', 'updated'], conditions=["With modelOptions.updateOn set to 'blur'"], identifiers=['modelOptions.updateOn'], literals=["'blur'"])],
    api=['modelOptions.updateOn'], literal=["'blur'"], relations=[('has_value', 'modelOptions.updateOn', "'blur'")])
row('D012', [aspect(['focus'], ['How do I set'], conditions=["on the field whose key is 'search'"], identifiers=['focus', 'key', "'search'"], literals=['true', "'search'"])],
    api=['focus', 'key'], custom=["'search'"], literal=['true', "'search'"], relations=[('has_value', 'focus', 'true'), ('has_value', 'key', "'search'")], rationale='Setting focus is the ask; the key clause selects the field. The supplied property name search is retained as custom identifier and literal.')
row('D013', [
    aspect(['options.fieldChanges'], ['Where do I subscribe to'], conditions=["to inspect an event whose type is 'expressionChanges'"], identifiers=['options.fieldChanges', 'type'], literals=["'expressionChanges'"]),
], api=['options.fieldChanges', 'type'], literal=["'expressionChanges'"], relations=[('has_value', 'type', "'expressionChanges'")], rationale='The requested subscription location is one ask; inspecting the specified event expresses the purpose and preserves its exact type discriminator.')
row('D014', [aspect(["field.parent.model['region']"], ['How do I read'], conditions=['inside an expression'], identifiers=["field.parent.model['region']", "'region'"], literals=["'region'"])],
    api=["field.parent.model['region']"], custom=["'region'"], literal=["'region'"], rationale='The entire member access is the API target; region is the explicitly supplied model-property name. A lookup key is not an assigned value of the member access.')
row('D015', [aspect(['which type'], ['describes the container'], conditions=["For type: 'repeat-block' and fieldArray: { type: 'input' }"], identifiers=[('type', 1), 'fieldArray', ('type', 2), "'repeat-block'"], literals=["'repeat-block'", "{ type: 'input' }", "'input'"])],
    api=[('type', 1), 'fieldArray', ('type', 2)], custom=["'repeat-block'"], literal=["'repeat-block'", "{ type: 'input' }", "'input'"],
    relations=[('has_value', ('type', 1), "'repeat-block'"), ('has_value', 'fieldArray', "{ type: 'input' }"), ('has_value', ('type', 2), "'input'")], rationale='The configuration is a setup assumption. Distinct type occurrences and the nested fieldArray object preserve their exact value links; repeat-block is a supplied custom registration name.')
row('D016', [aspect(['a radio group'], ['how do I configure'], versions=['Formly 6'], ui_adapters=['Ionic'])], version=['Formly 6'], adapter=['Ionic'])
row('D017', [aspect(['a character counter'], ['where can I add'], conditions=['to a textarea'], versions=['Formly 6.3.12'], ui_adapters=['Material'])], version=['Formly 6.3.12'], adapter=['Material'], rationale='The textarea destination scopes where to add the counter; the opening Material/Formly phrase is adapter/version scope rather than a duplicate condition.')
row('D018', [aspect(['expression changes'], ['how do I observe'], versions=['Formly 7'])], version=['Formly 7'])
row('D019', [aspect(['a blur-triggered update'], ['when does', 'reach the model'], versions=['Angular 20', 'Formly 6'])], version=['Angular 20', 'Formly 6'])
row('D020', [aspect(['date-input configuration'], ['Compare'], versions=['Formly 6.3.12'], ui_adapters=['Bootstrap', 'PrimeNG'])], version=['Formly 6.3.12'], adapter=['Bootstrap', 'PrimeNG'])
row('D021', [aspect(['it'], ['How do I hide'], references=['it'], unresolved_references=['it'])], rationale='It could denote the save button or cancel button.')
row('D022', [aspect(['that button'], ['How do I hide'], conditions=['while submission is pending'], references=['that button'], resolved_antecedents=['The save button'])], relations=[('refers_to', 'that button', 'The save button')], rationale='Only the save button is introduced, so the reference is resolved; pending submission constrains the hiding request.')
row('D023', [aspect(['that container'], ['How do I collapse'], references=['that container'], unresolved_references=['that container'])], rationale='Either the tab or the nested panel could be the container to collapse.')
row('D024', [aspect(['that panel'], ['How do I collapse'], identifiers=["'totals'"], literals=["'totals'"], references=['that panel'], resolved_antecedents=["The panel named 'totals'"])], custom=["'totals'"], literal=["'totals'"], relations=[('refers_to', 'that panel', "The panel named 'totals'")], rationale='The uniquely named panel resolves that panel; its supplied name remains attached to the request.')
row('D025', [aspect(['the same rule'], ['Should I apply', 'instead'], references=['the same rule', 'here'], unresolved_references=['the same rule', 'here'])], rationale='Neither the rule being reused nor the location here is supplied; instead also presupposes an unspecified alternative.')
row('D026', [aspect(['Which component'], ["should handle the form's submit event"])], rationale='The component responsible for handling the specified submit event is the requested target; the event is part of the requested handling operation, not a setup assumption.')
row('D027', [aspect(['a form-level error banner'], ['Where can I display'])])
row('D028', [aspect(['an array of field configurations'], ['How do I supply'], conditions=['to a form'])])
row('D029', [aspect(['a pristine control', 'an untouched control'], ['What is the difference between'])], rationale='One comparison retains both control-state descriptions.')
row('D030', [aspect(['observing a field change', 'defining an expression'], ['How does', 'differ from'])], rationale='The two named operations are the targets of one comparison, not independent procedural asks.')

assert len(rows) == 54
assert [r['id'] for r in rows] == [q['id'] for q in selected]
for r in rows:
    validate_annotation(r)
with (HERE / 'independent-raw.json').open('x') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(f'Validated and wrote {len(rows)} independent annotations.')
