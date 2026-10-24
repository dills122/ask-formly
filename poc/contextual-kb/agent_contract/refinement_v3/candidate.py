"""Condition-audited question plan; hints never enter the text-only projection."""
import copy
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from contract import validate as validate_base, exact_keys, nonempty, parse_json
ROLES={'api_reference','registration_name','model_key','value','version','ui_adapter'}
def build_messages(request):
 if not nonempty(request):raise ValueError('Request must be a nonempty string')
 return [{'role':'system','content':Path(__file__).with_name('CONTRACT.md').read_text()}, {'role':'user','content':request}]
def validate(request,value):
 if not nonempty(request):raise ValueError('Request must be nonempty')
 exact_keys(value,('formly_questions','library_constraints','condition_bindings'),'candidate')
 validate_base({k:value[k] for k in ('formly_questions','library_constraints')})
 bindings=value['condition_bindings'];seen=set()
 if not isinstance(bindings,list):raise ValueError('condition bindings must be array')
 for b in bindings:
  exact_keys(b,('condition','question_indexes'),'binding');condition=b['condition'];ids=b['question_indexes']
  if not nonempty(condition) or condition not in request:raise ValueError('condition not grounded in source')
  if condition in seen:raise ValueError('duplicate condition binding')
  seen.add(condition)
  if not isinstance(ids,list) or not ids or any(type(i) is not int or not 0<=i<len(value['formly_questions']) for i in ids) or len(ids)!=len(set(ids)):raise ValueError('invalid question indices')
  for i in ids:
   if condition not in value['formly_questions'][i]['question']:raise ValueError(f'missing condition in question {i}')
 return value

def parse_output(request,text):return validate(request,parse_json(text))

def optional_hints(questions,hints):
 if hints is None:return [],[]
 if not isinstance(hints,list):return [],['ignored_non_array_hints']
 valid=[];warnings=[]
 for i,h in enumerate(hints):
  try:
   exact_keys(h,('question_index','start','end','text','role'),'hint')
   q,a,b=h['question_index'],h['start'],h['end']
   if type(q) is not int or not 0<=q<len(questions):raise ValueError('question index')
   text=questions[q]['question']
   if type(a) is not int or type(b) is not int or not 0<=a<b<=len(text) or text[a:b]!=h['text'] or not isinstance(h['role'],str) or h['role'] not in ROLES:raise ValueError('invalid span/role')
   valid.append((i,copy.deepcopy(h)))
  except (ValueError,TypeError,KeyError):warnings.append(f'ignored_invalid_hint:{i}')
 blocked=set()
 for i,a in valid:
  for j,b in valid:
   if i<j and a['question_index']==b['question_index'] and a['start']<b['end'] and b['start']<a['end']:blocked.update((i,j))
 warnings.extend(f'ignored_overlapping_hint:{i}' for i in sorted(blocked))
 return [dict(h,usable_as_filter=False) for i,h in valid if i not in blocked],warnings

def build_plan(request,value,hints=None):
 """Validate core plan first; invalid or missing advisory hints never block it."""
 validate(request,value)
 questions=value['formly_questions']
 role_hints,warnings=optional_hints(questions,hints)
 return dict(question_plan=copy.deepcopy(value),search_requests=[{'query':q['question']} for q in questions],hint_policy='advisory_only',role_hints=role_hints,hint_warnings=warnings)
