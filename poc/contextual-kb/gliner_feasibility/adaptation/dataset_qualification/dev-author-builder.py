"""Independent development annotations; source-only manual labels, no model use."""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pilot.contract import FIELDS, ENTITY_TYPES, validate_annotation

questions = json.loads((HERE / 'questions.json').read_text())['dev']
rows = []


def annotate(n, specs, entities=None, relations=(), rationale=''):
    source = questions[n - 1]
    q = source['question']
    def span(selector):
        # Bare strings must be unique; repeated strings require explicit occurrence.
        if isinstance(selector, tuple):
            text, occurrence = selector
        else:
            text, occurrence = selector, None
        matches = [m.start() for m in re.finditer(re.escape(text), q)]
        if occurrence is None:
            if len(matches) != 1:
                raise ValueError((source['id'], 'ambiguous/missing substring', text, matches))
            occurrence = 0
        if not 0 <= occurrence < len(matches):
            raise ValueError((source['id'], 'missing occurrence', selector))
        start = matches[occurrence]
        end = start + len(text)
        # Reject a partial word, including Unicode words and identifier underscores.
        if (start and (q[start-1].isalnum() or q[start-1] == '_') and
                (text[0].isalnum() or text[0] == '_')):
            raise ValueError(('partial token start', selector))
        if (end < len(q) and (q[end].isalnum() or q[end] == '_') and
                (text[-1].isalnum() or text[-1] == '_')):
            raise ValueError(('partial token end', selector))
        return dict(text=text, start=start, end=end)
    aspects = []
    for i, spec in enumerate(specs, 1):
        item = {field: [span(s) for s in spec.get(field, [])] for field in FIELDS}
        item.update(id=f'a{i}', target_anchor=min(item['targets'], key=lambda s:s['start']))
        aspects.append(item)
    row = dict(id=source['id'], question=q,
               status='needs_clarification' if any(a['unresolved_references'] for a in aspects) else 'clear',
               aspects=aspects,
               entities={kind:[span(s) for s in (entities or {}).get(kind, [])] for kind in ENTITY_TYPES},
               relations=[dict(kind=kind, head=span(head), tail=span(tail)) for kind, head, tail in relations],
               rationale=rationale)
    rows.append(validate_annotation(row))


def a(targets, cues, **kwargs):
    return dict(targets=targets, request_cues=cues, **kwargs)

annotate(1, [
    a(['the city choices'], ['how do I refresh'], conditions=['When a country selection invalidates a city choice']),
    a(['the old choice'], ['how do I', 'explain why', 'disappeared'], conditions=['When a country selection invalidates a city choice'])
], rationale='Refreshing available choices and explaining the disappearance are separately requested outcomes. The old choice is a descriptive target, not a pronominal reference.')
annotate(2, [
    a(['progress'], ['how can I display'], conditions=['During submission']),
    a(['a second submission'], ['how can I', 'prevent'], conditions=['During submission'], negative_constraints=['prevent a second submission'])
], rationale='The prohibition applies to the second submission, while the progress request is positive.')
annotate(3, [
    a(['the moved row'], ['how can I identify'], conditions=['After dragging a row to a new position']),
    a(['its expanded state'], ['how can I', 'retain'], conditions=['After dragging a row to a new position'], references=['its'], resolved_antecedents=['the moved row'])
], relations=[('refers_to','its','the moved row')], rationale='Identification and retention are distinct asks; its refers to the moved row.')
annotate(4, [
    a(['each error'], ['where can I attach'], conditions=['When a server returns errors for two fields'], references=['each error'], resolved_antecedents=['errors for two fields']),
    a(['those server errors'], ['how can I clear'], conditions=['When a server returns errors for two fields', 'later'], references=['those server errors'], resolved_antecedents=['errors for two fields'])
], relations=[('refers_to','each error','errors for two fields'), ('refers_to','those server errors','errors for two fields')], rationale='Attachment location and later clearing are separate asks referring to the returned errors. Later preserves the explicitly requested timing.')
annotate(5, [
    a(['formatting'], ['explain']),
    a(['recomputation'], ['explain'], conditions=['when an input changes'])
], rationale='The topical computed summary is shared semantic context. The adjacent when-clause qualifies recomputation; no separate formatting-on-change request is asserted.')
annotate(6, [a(['submission'], ['How can I check whether', 'is allowed'], negative_constraints=['without marking every field touched'])])
annotate(7, [a(['a server-side error'], ['Can I report'], negative_constraints=['without running the server check again'])])
annotate(8, [a(['a read-only preview'], ['How can I show'], negative_constraints=['without copying the model into another object'])])
annotate(9, [a(['one cell'], ['How do I prevent editing'], negative_constraints=['prevent editing one cell', 'without disabling the entire row'])], rationale='Prevention of editing is the requested operation; the row-level constraint qualifies that operation.')
annotate(10, [a(['a configuration'], ['Can I reuse'], negative_constraints=['without assuming that Material is installed'], ui_adapters=['Material'])], entities={'ui_adapter':['Material']}, rationale='Material is explicitly mentioned inside a negative assumption, not asserted as the installed adapter.')
annotate(11, [a(['the model'], ['when is', 'updated'], conditions=["With modelOptions.updateOn set to 'blur'"], identifiers=['modelOptions.updateOn'], literals=["'blur'"])], entities={'api':['modelOptions.updateOn'], 'literal':["'blur'"]}, relations=[('has_value','modelOptions.updateOn',"'blur'")])
annotate(12, [a(['focus'], ['How do I set'], conditions=["on the field whose key is 'search'"], identifiers=['focus','key',"'search'"], literals=['true',"'search'"])], entities={'api':['focus','key'], 'custom_identifier':["'search'"], 'literal':['true',"'search'"]}, relations=[('has_value','focus','true'),('has_value','key',"'search'")], rationale='The field selector limits the focus-setting request; search is a supplied model-key identifier.')
annotate(13, [a(['options.fieldChanges'], ['Where do I subscribe to'], conditions=["to inspect an event whose type is 'expressionChanges'"], identifiers=['options.fieldChanges','type'], literals=["'expressionChanges'"])], entities={'api':['options.fieldChanges','type'], 'literal':["'expressionChanges'"]}, relations=[('has_value','type',"'expressionChanges'")], rationale='Inspection specifies the purpose of the subscription-location ask, rather than independently requesting a second operation.')
annotate(14, [a(["field.parent.model['region']"], ['How do I read'], conditions=['inside an expression'], identifiers=["field.parent.model['region']", "'region'"], literals=["'region'"])], entities={'api':["field.parent.model['region']"], 'custom_identifier':["'region'"], 'literal':["'region'"]}, rationale='The full access path is preserved. Region is an explicit supplied property key; indexing does not assert a has_value assignment.')
annotate(15, [a([('type',2)], ['which', 'describes the container'], conditions=["For type: 'repeat-block' and fieldArray: { type: 'input' }"], identifiers=[('type',0),'fieldArray',('type',1),"'repeat-block'","'input'"], literals=["'repeat-block'","'input'"])], entities={'api':[('type',0),'fieldArray',('type',1)], 'custom_identifier':["'repeat-block'","'input'"], 'literal':["'repeat-block'","'input'"]}, relations=[('has_value',('type',0),"'repeat-block'"),('has_value',('type',1),"'input'")], rationale='The supplied configuration is a setup assumption. The question asks which type denotes the container; both quoted type names are supplied registration identifiers. The final unquoted type is a descriptive noun, not an additional API occurrence.')
annotate(16, [a(['a radio group'], ['how do I configure'], versions=['Formly 6'], ui_adapters=['Ionic'])], entities={'version':['Formly 6'],'ui_adapter':['Ionic']})
annotate(17, [a(['a character counter'], ['where can I add'], conditions=['to a textarea'], versions=['Formly 6.3.12'], ui_adapters=['Material'])], entities={'version':['Formly 6.3.12'],'ui_adapter':['Material']})
annotate(18, [a(['expression changes'], ['how do I observe'], versions=['Formly 7'])], entities={'version':['Formly 7']})
annotate(19, [a(['a blur-triggered update'], ['when does', 'reach the model'], versions=['Angular 20','Formly 6'])], entities={'version':['Angular 20','Formly 6']}, rationale='The requested timing concerns a blur-triggered update reaching the model; blur-triggered is part of the specified update target.')
annotate(20, [a(['date-input configuration'], ['Compare'], versions=['Formly 6.3.12'], ui_adapters=['Bootstrap','PrimeNG'])], entities={'version':['Formly 6.3.12'],'ui_adapter':['Bootstrap','PrimeNG']}, rationale='One comparison of configuration across two adapters; adapters are scope rather than separate target asks.')
annotate(21, [a(['it'], ['How do I hide'], references=['it'], unresolved_references=['it'])], rationale='It could refer to the save button or the cancel button; the source does not choose one.')
annotate(22, [a(['that button'], ['How do I hide'], conditions=['while submission is pending'], references=['that button'], resolved_antecedents=['The save button'])], relations=[('refers_to','that button','The save button')], rationale='The source names only one button, so the demonstrative resolves uniquely.')
annotate(23, [a(['that container'], ['How do I collapse'], references=['that container'], unresolved_references=['that container'])], rationale='Both the tab and the panel can be the referenced container; no explicit choice resolves the requested target.')
annotate(24, [a(['that panel'], ['How do I collapse'], identifiers=["'totals'"], literals=["'totals'"], references=['that panel'], resolved_antecedents=["The panel named 'totals'"])], entities={'custom_identifier':["'totals'"], 'literal':["'totals'"]}, relations=[('refers_to','that panel',"The panel named 'totals'")], rationale='The named panel uniquely resolves the demonstrative. The summary is contained content, not another panel.')
annotate(25, [a(['the same rule'], ['Should I apply'], references=['the same rule','here','instead'], unresolved_references=['the same rule','here','instead'])], rationale='The rule, destination, and alternative to be replaced are absent from the question; no antecedents can be supplied.')
annotate(26, [a(["the form's submit event"], ['Which component should handle'])], rationale='The event is the target of the responsibility question; the cue asks which component handles it.')
annotate(27, [a(['a form-level error banner'], ['Where can I display'])])
annotate(28, [a(['an array of field configurations'], ['How do I supply'], conditions=['to a form'])])
annotate(29, [a(['a pristine control','an untouched control'], ['What is the difference between'])], rationale='One comparison includes both control-state targets.')
annotate(30, [a(['observing a field change','defining an expression'], ['How does','differ from'])], rationale='One comparison between two operations, with no explicit API identifiers supplied.')

assert len(rows) == len(questions) == 30
assert [row['id'] for row in rows] == [q['id'] for q in questions]
(HERE / 'dev-author.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
print(f'Validated {len(rows)} independent development annotations.')
