"""Application-level repair feedback; never performs inference or retries a call."""
from pathlib import Path
import re
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'model_free_v1'))
from candidate import normalize, normalize_version, normalize_adapter
from model_free_v1.server import QuestionPlan
from pydantic import ValidationError

# A bounded omission check for explicit opening scope clauses, not general intent
# extraction. Require a complete clause so ranges/prereleases are not clipped.
SCOPE_PREFIX = re.compile(
    r'^\s*(?:For|In|Use)\s+Formly\s+(?P<formly_version>[0-9]+\.[0-9]+\.[0-9]+)'
    r'(?:\s+with\s+(?P<ui_adapter>Material|Bootstrap|PrimeNG|core))?'
    r'[,.](?=\s|$)', re.IGNORECASE)


def issue(code,path,message,**detail):
    return dict(code=code,path=path,message=message,**detail)


def refinement(issues):
    return dict(status='needs_refinement',issues=issues[:16],issues_truncated=len(issues)>16,
                next_action=dict(type='revise_plan_and_retry',tool='lookup_formly',preserve_original_request=True,user_input_required=False,max_repair_attempts=2),
                validation_scope='Explicit structure and declared bindings only; semantic completeness is not assessed.')


def plan_issues(request,plan,formly_version=None,ui_adapter=None):
    try:QuestionPlan.model_validate(plan)
    except ValidationError as exc:
        return [issue('INVALID_PLAN_SHAPE','/plan/'+ '/'.join(str(x) for x in e['loc']),e['msg']) for e in exc.errors()]
    issues=[]
    prefix=SCOPE_PREFIX.match(request)
    if prefix:
        for key,value in prefix.groupdict().items():
            if value is not None and plan['library_constraints'][key] is None:
                issues.append(issue('MISSING_SCOPE_METADATA','/plan/library_constraints/'+key,
                    'The opening request clause names scope missing from the plan. Copy the requested scope into library_constraints; do not substitute a supported default.',
                    source_excerpt=prefix.group(0).strip(),scope_value=value))
    for key,explicit,normalizer in [('formly_version',formly_version,normalize_version),('ui_adapter',ui_adapter,normalize_adapter)]:
        supplied=plan['library_constraints'][key]
        valid=True
        for value,path in [(supplied,'/plan/library_constraints/'+key),(explicit,'/'+key)]:
            if value is None:continue
            try:normalizer(value)
            except ValueError as exc:
                valid=False;issues.append(issue('INVALID_SCOPE',path,str(exc)))
        if valid and supplied is not None and explicit is not None and normalizer(supplied)!=normalizer(explicit):
            issues.append(issue('SCOPE_CONFLICT','/plan/library_constraints/'+key,'Plan and explicit scope disagree; resolve from the original request/context.',plan_value=supplied,argument_value=explicit))
    try:normalize(request,plan)
    except ValueError as exc:
        seen=set();questions=plan['formly_questions']
        for bi,binding in enumerate(plan['condition_bindings']):
            condition=binding['condition'];indexes=binding['question_indexes'];path=f'/plan/condition_bindings/{bi}'
            if not condition.strip() or condition not in request:
                issues.append(issue('UNGROUNDED_CONDITION',path+'/condition','Copy a nonempty condition excerpt exactly from the original request.',condition=condition));continue
            if condition in seen:
                issues.append(issue('DUPLICATE_CONDITION',path,'Merge repeated condition bindings without dropping applicable question indexes.',condition=condition))
            seen.add(condition)
            if len(indexes)!=len(set(indexes)) or any(not 0<=i<len(questions) for i in indexes):
                issues.append(issue('INVALID_QUESTION_INDEX',path+'/question_indexes','Use unique zero-based indexes of existing questions.',condition=condition));continue
            for qi in indexes:
                if condition not in questions[qi]['question']:
                    issues.append(issue('MISSING_DECLARED_CONDITION',f'/plan/formly_questions/{qi}/question','This declared condition is assigned to the question but absent from its text. Preserve its meaning and binding.',question_index=qi,condition=condition))
        if not issues:issues.append(issue('INVALID_PLAN','/plan',str(exc)))
    return issues


class RepairService:
    def __init__(self,base):self.base=base;self.store=base.store
    async def lookup(self,request,plan=None,**kwargs):
        if not isinstance(request,str) or not request.strip() or len(request)>12000:
            return refinement([issue('INVALID_REQUEST','/request','Provide the unchanged nonempty original request, at most12000characters.')]),True
        if plan is None:
            return refinement([issue('PLAN_REQUIRED','/plan','Prepare the Formly library question plan from the original request before searching.')]),False
        issues=plan_issues(request,plan,kwargs.get('formly_version'),kwargs.get('ui_adapter'))
        if issues:return refinement(issues),True
        # Do not catch operational/integrity errors as input problems.
        result=await self.base.lookup(request,plan=plan,**kwargs)
        if result.get('status') in ('unsupported_version','unsupported_adapter','unavailable_knowledge'):
            return dict(result,scope_status=result['status'],status='unsupported_scope',next_action=dict(type='stop',reason='Rephrasing cannot supply missing scope coverage.')),False
        if not result['facts']:
            return dict(result,status='no_evidence',next_action=dict(type='assess_gap',message='No records delivered; check truncation/omitted IDs and scope. Absence is not proof that an API or behavior does not exist.')),False
        return dict(result,status='ok',next_action=dict(type='assess_evidence',message='Check relevance, conditions, limitations and truncation before answering.')),False
