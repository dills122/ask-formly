"""Deterministic authoring/offset audit; reads only two explicitly allowed datasets."""
import json,re,hashlib,unicodedata,difflib
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]/'verifier_training_plan'/'test-output'
ROLES=['api_reference','registration_name','model_key','value','version','ui_adapter']
def save(name,d):
 (HERE/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
def add(i,text,group,pair,golds,neg=(),mal=()):
 def span(s):
  assert text.count(s)==1,(i,s,text)
  x=text.index(s);return x,x+len(s)
 gold=sorted([list(span(s))+[r] for s,r in golds])
 probes=[dict(start=a,end=b,expected_role=r,family='gold') for a,b,r in gold]
 probes += [dict(start=span(s)[0],end=span(s)[1],expected_role=None,family='semantic_'+group) for s in neg]
 probes += [dict(start=span(s)[0],end=span(s)[1],expected_role=None,family='malformed_boundary') for s in mal]
 r=dict(id=f'SDEV-{i:03}',text=text,group=group,gold=gold,probes=probes)
 if pair:r['pair_id']=pair
 rows.append(r)
A='api_reference';R='registration_name';K='model_key';V='value';U='ui_adapter';Z='version'
add(1,'For a Formly field, explain what the configuration property type selects.', 'property_prose','PP1',[('type',A)])
add(2,'For a Formly field, explain what makes a reusable type suitable for dates.', 'property_prose','PP1',[],['type'])
add(3,'Does the Formly model property expose the current data object?', 'property_prose','PP2',[('model',A)])
add(4,'When designing a Formly form, should a model mirror the business record?', 'property_prose','PP2',[],['model'])
add(5,'Which Formly documentation explains the property expressions for dynamic presentation?', 'property_literal','PL1',[('expressions',A)])
add(6,"A Formly caption must display 'expressions' verbatim; can a field type support that text?", 'property_literal','PL1',[("'expressions'",V)],['type'],["'expressions"])
add(7,'In Formly, what is the configuration property wrappers used for?', 'property_literal','PL2',[('wrappers',A)])
add(8,'A Formly hint must contain "wrappers" verbatim; does the chosen field type matter?', 'property_literal','PL2',[( '"wrappers"',V)],['type'],['wrappers"'])
add(9,"Where does Formly document registering a field type named 'cedar-calendar'?", 'registration_value','RV1',[("'cedar-calendar'",R)],['type'])
add(10,"For a Formly hint, how can I display the literal 'cedar-calendar' below the control?", 'registration_value','RV1',[("'cedar-calendar'",V)])
add(11,'Can a Formly wrapper registered as "iris-border" decorate a custom field type?', 'registration_value','RV2',[( '"iris-border"',R)],['type'])
add(12,'Can a Formly caption display "iris-border" exactly, including the hyphen?', 'registration_value','RV2',[( '"iris-border"',V)])
add(13,"How does Formly interpret the model key 'shipment.lane' for a field?", 'key_value','KV1',[("'shipment.lane'",K)],['model'])
add(14,"For a Formly example, I need the initial content to be exactly 'shipment.lane'; how is that literal supplied?", 'key_value','KV1',[("'shipment.lane'",V)])
add(15,'Is the model key "résumé.code" supported in a Formly field configuration?', 'key_value','KV2',[( '"résumé.code"',K)],['model'])
add(16,'Is the literal "résumé.code" allowed as display text in a Formly form?', 'key_value','KV2',[( '"résumé.code"',V)])
add(17,'With the Material adapter, how does Formly present a custom field type?', 'adapter_registration','AR1',[('Material',U)],['type'])
add(18,"Where is a Formly field registered under the name 'Material' selected?", 'adapter_registration','AR1',[("'Material'",R)])
add(19,'With the Bootstrap adapter, how does Formly compose wrapper components around a field type?', 'adapter_registration','AR2',[('Bootstrap',U)],['type'])
add(20,'How is a Formly wrapper registered under the name "Bootstrap" referenced?', 'adapter_registration','AR2',[( '"Bootstrap"',R)])
add(21,"In Formly, how is `expressions['props.readonly']` configured for a field?", 'whole_path_opaque','WO1',[("expressions['props.readonly']",A)],mal=['props.readonly'])
add(22,"Can a Formly field type accept the opaque callback `field => field.props.readonly === true`?", 'whole_path_opaque','WO1',[('field => field.props.readonly === true',V)],['type'],['field.props.readonly'])
add(23,'In Formly, where is the API path `field.options.formState.reviewMode` available?', 'whole_path_opaque','WO2',[('field.options.formState.reviewMode',A)],mal=['options.formState'])
add(24,'Can a Formly field type use the supplied opaque callback `field => field.options.formState.reviewMode`?', 'whole_path_opaque','WO2',[('field => field.options.formState.reviewMode',V)],['type'],['field.options.formState'])
add(25,'Which Formly migration notes compare v6.3.10 with v6.3.12?', 'version_control',None,[('v6.3.10',Z),('v6.3.12',Z)])
add(26,'For Formly 6.3.12, is resetOnHide set to false sufficient to retain a hidden field value?', 'version_control',None,[('6.3.12',Z),('resetOnHide',A),('false',V)])
add(27,'In a Formly form, when is hooks.onDestroy called?', 'ordinary_control',None,[('hooks.onDestroy',A)])
add(28,'Could Formly defaultValue be [] for a field that stores a collection?', 'ordinary_control',None,[('defaultValue',A),('[]',V)])
add(29,'How can a Formly form make a long questionnaire easier to navigate?', 'no_mention_control',None,[])
add(30,'What should I consider before grouping related questions in Formly?', 'no_mention_control',None,[])
assert len(rows)==30
for r in rows:
 assert all(0<=a<b<=len(r['text']) and role in ROLES for a,b,role in r['gold'])
 assert all(x[1]<=y[0] for x,y in zip(r['gold'],r['gold'][1:]))
save('development-v1.json',rows)
train=json.loads((BASE/'training-labels.json').read_text());dev=json.loads((BASE/'calibration.json').read_text())
remove_train={'H01/focused/1','H21/focused/1','H13/focused/1','H14/focused/1','H21/focused/3','T37'}
remove_dev={'VCAL-010','VCAL-011','VCAL-012','VCAL-013','VCAL-015','VCAL-017'}
overlay=[]
for split,data,remove in [('train',train,remove_train),('development',dev,remove_dev)]:
 for r in data:
  for o in r['occurrences']:
   if r['id'] in remove and o['text']=='type':
    overlay.append(dict(split=split,id=r['id'],start=o['start'],end=o['end'],text=o['text'],old_targets=o['targets'],proposed_targets=[0]*7,reason='Registered/named component category, not explicit configuration member; registration-name span retained.'))
save('proposed-overlay-v1.json',dict(status='author_proposal_pending_independent_review',source_sha256={f:sha(BASE/f) for f in ['training-labels.json','calibration.json']},corrections=overlay))
# Full original dev inventory after proposed overlay. No source modifications.
reviewed=[];audit=[]
for r in dev:
 corrections={(o['start'],o['end']) for o in overlay if o['split']=='development' and o['id']==r['id']}
 gold=[[o['start'],o['end'],o['source_kind']] for o in r['occurrences'] if o['targets'][0] and (o['start'],o['end']) not in corrections]
 probes=[dict(start=o['start'],end=o['end'],expected_role=(o['source_kind'] if o['targets'][0] and (o['start'],o['end']) not in corrections else None),family=('adjudicated_concept' if (o['start'],o['end']) in corrections else o.get('negative_family','gold'))) for o in r['occurrences']]
 reviewed.append(dict(id=r['id'],text=r['text'],group='original_development_exposed',gold=gold,probes=probes))
 reasons={
 'VCAL-002':'expressions/model are directly coordinated named members with options.formState; keep both APIs.',
 'VCAL-015':'registered type denotes category; bare its key denotes the configuration member.',
 'VCAL-018':'label value is prose about caption content, not explicitly props.label; no inferred API.',
 'VCAL-019':'label text is prose; string and explicit version retain separate roles.',
 'VCAL-025':'custom type registration is category prose; only versions.',
 'VCAL-026':'wrappers denotes wrapper components in adapter comparison; not explicitly wrappers member.'}
 audit.append(dict(id=r['id'],text=r['text'],reviewed_gold=gold,original_positive_count=sum(bool(o['targets'][0]) for o in r['occurrences']),changes=len(corrections),verdict='complete_inventory_reviewed',reason=reasons.get(r['id'],'Remove category type; retain all remaining mentions and exact boundaries.' if corrections else 'All explicit mentions retained; no missing six-role mention found.'),negative_probes_reviewed=sum(not o['targets'][0] for o in r['occurrences'])))
save('original-development-adjudicated-v1.json',reviewed);save('original-development-inventory-audit-v1.json',audit)
# Exhaustive occurrence inventory of ambiguous lexical family, including unsupervised substrings.
amb=[]
for r in train:
 for m in re.finditer(r'\b(?:type|key|model|wrappers|expressions)\b',r['text']):
  a,b=m.span();exact=[o for o in r['occurrences'] if (o['start'],o['end'])==(a,b)]
  enclosing=[o for o in r['occurrences'] if o['targets'][0] and o['start']<=a and b<=o['end'] and (o['start'],o['end'])!=(a,b)]
  changed=r['id'] in remove_train and m.group()=='type' and exact and exact[0]['targets'][0]
  if changed:decision='proposed_supplied_occurrence_negative';reason='Registered component category, not property.'
  elif exact:decision='retain_supplied_'+('positive' if exact[0]['targets'][0] else 'negative');reason='Explicit member reference.' if exact[0]['targets'][0] else 'Nested/clipped boundary, not a complete mention.'
  elif enclosing:decision='unsupervised_nested_fragment';reason='Inside complete quoted name/key/value or maximal path; no standalone mention.'
  else:
   decision='unsupervised_context_only';reason='Generic component/data/address prose; no new negative supervision.'
   if r['id']=='rb-train-048' and m.group()=='key':reason='Bare key denotes configuration property, but no supplied occurrence exists; missing inventory is not a training negative and no supervision is added.'
  amb.append(dict(id=r['id'],text=r['text'],start=a,end=b,raw=m.group(),decision=decision,reason=reason))
save('training-ambiguity-audit-v1.json',dict(scope='Every whole-word type/key/model/wrappers/expressions occurrence in all 242 training rows; supplied positives/negatives and nested/unannotated contexts. Other training vocabulary not fully audited.',rows_scanned=len(train),occurrences=amb))
# No heldout/evaluation access. Report nearest references, do not choose cases by predictions.
def norm(t):return ' '.join(unicodedata.normalize('NFKC',t).casefold().split())
def template(t):
 t=re.sub(r'`[^`]*`|\"[^\"]*\"|\x27[^\x27]*\x27',' TOKEN ',norm(t));t=re.sub(r'\bv?\d+(?:\.\d+)*\b','VERSION',t)
 return ' '.join(re.findall(r'\w+',t))
refs=[(split,r) for split,d in [('train',train),('original_development',dev)] for r in d]
overlap=[]
for r in rows:
 scores=[]
 for split,old in refs:
  score=difflib.SequenceMatcher(None,template(r['text']),template(old['text']),autojunk=False).ratio()
  scores.append(dict(split=split,id=old['id'],text=old['text'],template_similarity=round(score,5),normalized_duplicate=norm(r['text'])==norm(old['text'])))
 overlap.append(dict(id=r['id'],nearest=sorted(scores,key=lambda x:x['template_similarity'],reverse=True)[:3],normalized_duplicates=[x for x in scores if x['normalized_duplicate']]))
save('overlap-audit-v1.json',dict(method='NFKC/casefold/whitespace exact duplicate check; quote/backtick/version-masked word SequenceMatcher, top three per new row; heuristic near-template evidence, no independence claim.',comparisons=len(rows)*len(refs),rows=overlap))
save('author-receipt-v1.json',dict(status='AUTHORED_PENDING_INDEPENDENT_REVIEW_NOT_READY',new_questions=len(rows),pairs=12,paired_questions=24,controls=6,role_counts={role:sum(g[2]==role for r in rows for g in r['gold']) for role in ROLES},gold_count=sum(len(r['gold']) for r in rows),semantic_negative_count=sum(p['family'].startswith('semantic_') for r in rows for p in r['probes']),malformed_count=sum(p['family']=='malformed_boundary' for r in rows for p in r['probes']),original_dev_rows=30,original_dev_gold=sum(len(r['gold']) for r in reviewed),training_ambiguous_occurrences=len(amb),training_proposed_corrections=sum(o['split']=='train' for o in overlay),development_proposed_corrections=sum(o['split']=='development' for o in overlay),normalized_duplicates=sum(len(r['normalized_duplicates']) for r in overlap),maximum_template_similarity=max(r['nearest'][0]['template_similarity'] for r in overlap),no_predictions=True,no_training=True,no_sealed_reads=True,no_encoder_forward=True,source_hashes={f:sha(BASE/f) for f in ['training-labels.json','calibration.json']},artifact_hashes={p.name:sha(p) for p in HERE.glob('*v1.json') if p.name!='author-receipt-v1.json'}))
