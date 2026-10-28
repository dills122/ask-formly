"""Model-free, read-only evidence retrieval. No inference or semantic completeness claim."""
import copy
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys

POC=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(POC));sys.path.insert(0,str(POC/'mcp_v1'))
from mcp_foundation.capitalization import normalize
from mcp_v1.request_context import ContextLookup
from mcp_v1.project_settings import ProjectSettings, normalize_adapter
from mcp_v1.versioning import normalize_version
from model_free_v1.response import MAX_RESPONSE_BYTES, encoded_size, evidence_packet, fingerprint, fits_packet, measure_packet, omitted_preview
from model_free_v1.ranking import rerank, diagnostics

# Frozen legacy token policy retained ONLY as the comparison arm.
STOPWORDS=set('a an and are as at be by can do does for formly from how i if in is it its my of on or should that the then this to use using what when where which why with'.split())
TOKEN=re.compile(r'[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)*')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def terms(text,basic=False):
    tokens=re.findall(r'[A-Za-z][A-Za-z0-9]*',text) if basic else TOKEN.findall(text)
    result=list(dict.fromkeys(t for t in tokens if (len(t)>=3 if basic else True) and t.casefold() not in STOPWORDS))
    if basic:return result[:8]
    if len(result)>256:raise ValueError('Question exceeds 256 distinct search terms; split it')
    return result


def expression(words,operator):
    return f' {operator} '.join('"'+w.replace('"','""')+'"' for w in words)


class Store:
    def __init__(self,path,expected_sha):
        self.path=Path(path).resolve();self.expected_sha=expected_sha
        self.verify()
        self.db=sqlite3.connect(self.path.as_uri()+'?mode=ro',uri=True)
        self.db.execute('PRAGMA query_only=ON')
        try:
            if self.db.execute('SELECT schema_version FROM build_info').fetchall()!=[(2,)]:raise ValueError('Expected schema2')
            self.facts={};self.document_ids={};self.api_identifiers={}
            for fid,claim,context,conditions,limits,title,version,adapter,doc_id in self.db.execute('''SELECT f.id,f.claim,f.context,f.conditions_json,f.limits_json,d.title,d.formly_version,d.adapter,f.doc_id FROM facts f JOIN documents d ON d.id=f.doc_id ORDER BY f.id'''):
                self.document_ids[fid]=doc_id
                self.api_identifiers[fid]=set(TOKEN.findall(claim+' '+context))
                self.facts[fid]=dict(id=fid,claim=claim,context=context,conditions=json.loads(conditions),limits=json.loads(limits),title=title,version=version,adapter=adapter)
            self.links = {fid: [] for fid in self.facts}
            if self.db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='fact_links'").fetchone():
                for source, target, kind in self.db.execute('SELECT source_fact_id,target_fact_id,kind FROM fact_links ORDER BY source_fact_id,target_fact_id,kind'):
                    if source not in self.facts or target not in self.facts:
                        raise ValueError('Broken stored fact link')
                    self.links[source].append(dict(kind=kind,target=target))
            self.symbols={fid:set(t for t in TOKEN.findall(' '.join([f['claim'],f['context'],*f['conditions'],*f['limits']])) if '.' in t or '$' in t or re.search(r'[a-z][A-Z]',t)) for fid,f in self.facts.items()}
        except BaseException:
            self.db.close();raise
    def close(self):self.db.close()
    def verify(self):
        if digest(self.path)!=self.expected_sha:raise ValueError('Knowledge DB hash differs from pinned baseline')
    def scopes(self,version,adapter):
        if adapter not in (None,'core','material'):raise ValueError('Unsupported adapter')
        result={}
        for fid,kind,value,basis,reason in self.db.execute('SELECT fact_id,kind,value,basis,reason FROM applicability WHERE (kind=? AND value=?) OR (kind=? AND value=?) ORDER BY fact_id,kind,value',('exact',version,'major',version.split('.')[0])):
            if adapter=='core' and self.facts[fid]['adapter']!='core':continue
            if self.facts[fid]['adapter'] not in ('core','material'):continue
            evidence=[dict(id=eid,release=release) for eid,release in self.db.execute('''SELECT ae.evidence_id,er.release FROM applicability_evidence ae JOIN evidence_releases er ON er.evidence_id=ae.evidence_id WHERE ae.fact_id=? AND ae.kind=? AND ae.value=? ORDER BY ae.evidence_id''',(fid,kind,value))]
            result.setdefault(fid,[]).append(dict(scope=dict(kind=kind,value=value),basis=basis,reason=reason,evidence=evidence))
        return result
    def search(self,text,version,adapter,strategy='improved'):
        eligible=self.scopes(version,adapter)
        if not eligible:return []
        words=terms(text,strategy=='basic')
        if not words:return []
        marks=','.join('?' for _ in eligible)
        def route(operator):
            weight='' if strategy=='basic' else ',0,5,2,3,3,2,1'
            return [r[0] for r in self.db.execute(f'''SELECT f.id FROM facts_fts JOIN facts f ON f.id=facts_fts.fact_id WHERE facts_fts MATCH ? AND f.id IN ({marks}) ORDER BY bm25(facts_fts{weight}),f.id''',(expression(words,operator),*eligible))]
        precise=route('AND')
        if strategy=='basic':return precise or route('OR')
        if strategy!='improved':raise ValueError('Unknown retrieval strategy')
        broad=route('OR');mentioned=set(TOKEN.findall(text))
        symbols=sorted((fid for fid in eligible if self.symbols[fid]&mentioned),key=lambda fid:(-len(self.symbols[fid]&mentioned),fid))
        scores={}
        for weight,ranked in [(3,symbols),(2,precise),(1,broad)]:
            for rank,fid in enumerate(ranked,1):scores[fid]=scores.get(fid,0)+weight/(60+rank)
        ranked=rerank(text,self.facts,sorted(scores,key=lambda fid:(-scores[fid],fid)))
        # A class-qualified API can be written as separate class/method names in
        # evidence. Offer bounded document context without displacing any hits.
        qualified=[t.split('.') for t in TOKEN.findall(text)
                   if t.count('.')==1 and t[0].isupper()]
        documents=[]
        for fid in sorted(eligible):
            if any(set(parts)<=self.api_identifiers[fid] for parts in qualified):
                doc=self.document_ids[fid]
                if doc not in documents:documents.append(doc)
                if len(documents)==4:break
        supplemental=[fid for fid in sorted(eligible)
                      if self.document_ids[fid] in documents and fid not in scores][:16]
        return ranked+supplemental
    def candidates(self,text,version,adapter,strategy='improved'):
        """Two direct seeds may introduce at most two scoped see_also neighbors."""
        ranked=self.search(text,version,adapter,strategy)
        if strategy=='basic':return ranked
        eligible=self.scopes(version,adapter)
        neighbors=[]
        for fid in ranked[:2]:
            for link in self.links[fid]:
                target=link['target']
                if link['kind']=='see_also' and target in eligible and target not in ranked[:2] and target not in neighbors:
                    neighbors.append(target)
                    break
        return list(dict.fromkeys(ranked[:2]+neighbors+ranked[2:]))

    def records(self,ids,version,adapter):
        self.verify();apps=self.scopes(version,adapter)
        if not set(ids)<=apps.keys():raise ValueError('Unknown fact or fact outside requested scope')
        facts=[];citations={}
        for fid in dict.fromkeys(ids):
            facts.append(dict(copy.deepcopy(self.facts[fid]),applicability=apps[fid],
                              related=[copy.deepcopy(link) for link in self.links[fid] if link['target'] in apps]))
            row=self.db.execute('''SELECT d.source_path,d.source_sha256,f.source_quote,f.source_start_offset,f.source_end_offset,f.status FROM facts f JOIN documents d ON d.id=f.doc_id WHERE f.id=?''',(fid,)).fetchone()
            path,sha,quote,start,end,status=row
            evidence=[json.loads(r[0]) for r in self.db.execute('SELECT e.record_json FROM fact_evidence fe JOIN evidence e ON e.id=fe.evidence_id WHERE fe.fact_id=? ORDER BY e.id',(fid,))]
            citations[fid]=dict(authored_source=dict(path=path,sha256=sha,quote=quote,start_offset=start,end_offset=end,status=status),evidence=evidence,applicability=apps[fid])
        return facts,citations


class GateOnly:
    async def lookup(self,request):return {}


class Service:
    def __init__(self,store,settings_path):
        self.store=store;self.gate=ContextLookup(GateOnly(),settings=ProjectSettings(settings_path))
    async def lookup(self,request,plan=None,project_id=None,worktree_id=None,formly_version=None,ui_adapter=None,*,strategy='improved',max_facts=16,byte_budget=48000):
        if not isinstance(request,str) or not request.strip() or len(request)>12000:raise ValueError('request must contain 1..12000 characters')
        if type(max_facts) is not int or not 1<=max_facts<=16 or type(byte_budget) is not int or not 1<=byte_budget<=48000:raise ValueError('Invalid evidence budget')
        audit=None
        if plan is None:
            questions=[dict(question=request,reason='Raw request; not decomposed')];status='not_decomposed';core=None
        else:
            if len(json.dumps(plan))>32000:raise ValueError('Plan too large')
            core,audit=normalize(request,plan)
            questions=core['formly_questions'];status='caller_plan'
            if len(questions)>6 or len(core['condition_bindings'])>48 or any(len(q['question'])>2000 or len(q['reason'])>1000 for q in questions):raise ValueError('Plan exceeds bounded question/condition limits')
            for key,explicit,normalizer in [('formly_version',formly_version,normalize_version),('ui_adapter',ui_adapter,normalize_adapter)]:
                planned=core['library_constraints'][key]
                if planned is not None and explicit is not None and normalizer(planned)!=normalizer(explicit):raise ValueError('Conflicting plan and explicit '+key)
            formly_version=formly_version or core['library_constraints']['formly_version']
            ui_adapter=ui_adapter or core['library_constraints']['ui_adapter']
        context=await self.gate.lookup(request,project_id,worktree_id,formly_version,ui_adapter)
        if 'status' in context:return context
        version=context['version_context']['selected'];adapter=context['ui_adapter']
        self.store.verify()
        candidate_search=getattr(self.store,'candidates',self.store.search)
        ranked=[candidate_search(q['question'],version,adapter,strategy) for q in questions]
        signals=[diagnostics(q['question'],self.store.facts,ids)
                 for q,ids in zip(questions,ranked)]
        cache={}
        def records(ids):
            missing=[fid for fid in ids if fid not in cache]
            if missing:
                fs,cs=self.store.records(missing,version,adapter)
                cache.update({f['id']:(f,cs[f['id']]) for f in fs})
            return [cache[fid][0] for fid in ids],{fid:cache[fid][1] for fid in ids}
        planning=dict(status=status,structural_validity='checked' if core is not None else 'not_applicable',
            semantic_completeness='not_assessed',question_count=len(questions),
            condition_binding_count=len(core['condition_bindings']) if core else 0,
            normalization=dict(policy=audit.get('policy') if audit else None,
                               rewrite_count=len(audit.get('rewrites',[])) if audit else 0))
        def packet(ids,preview_limit=16):
            facts,citations=records(ids)
            evidence=evidence_packet(facts,citations)
            omitted,preview,total=omitted_preview(ranked,ids,preview_limit)
            grouped=[]
            for i,(q,candidates) in enumerate(zip(questions,ranked)):
                grouped.append(dict(question_index=i,question_ref=fingerprint(q['question']),
                    fact_ids=[fid for fid in candidates if fid in ids],
                    omitted_indexes=[j for j,row in enumerate(preview) if i in row['question_indexes']],
                    omitted_count=len(omitted[i]),candidate_count=len(candidates),
                    matching=signals[i],
                    status='candidates' if candidates else 'no_matches',truncated=bool(omitted[i])))
            if total:
                action=dict(type='assess_candidates_then_fetch',tool='get_formly_facts' if preview else 'discover_formly_candidates',
                    suggested_fact_ids=[row['id'] for row in preview[:8]],
                    formly_version=version,ui_adapter=adapter,
                    discovery=dict(tool='discover_formly_candidates',offset=0,repeat_original_request_and_plan=True),
                    message='These are omitted candidates, not relevance judgments. Fetch selected IDs in this scope, or page discovery for complete claims and limits.')
            else:
                action=dict(type='assess_evidence' if facts else 'assess_gap',
                    message='Check relevance, conditions, limits and provenance; candidate evidence does not certify answer completeness or API nonexistence.')
            result=dict(status='ok' if facts else 'no_evidence',planning=planning,questions=grouped,
                omitted_candidates=preview,omitted_count=total,omitted_preview_truncated=total>len(preview),
                evidence_status='candidate_only',truncated=bool(total),next_action=action,
                retrieval=dict(strategy=strategy,policy='Scoped lexical/API candidates and bounded see_also neighbors; no semantic relevance certification',
                               evidence_bytes=encoded_size(evidence),max_evidence_bytes=byte_budget),
                **evidence,**context)
            if len(request.encode('utf-8'))<=4096:result['request']=request
            else:result.update(request_ref=fingerprint(request),request_echo='omitted_for_budget')
            return result
        chosen=[]
        # Fairly consider candidate ranks beyond four. Stop a question at its first
        # budget failure rather than backfilling with smaller, lower-ranked facts.
        # Its omitted candidates remain available through fetch/discovery.
        preview_limit=16
        current=packet(chosen,preview_limit)
        while not fits_packet(current) and preview_limit:
            preview_limit//=2;current=packet(chosen,preview_limit)
        if not fits_packet(current):
            raise ValueError('Response metadata exceeds budget; split the request')
        budget_stopped=set()
        for rank in range(max(map(len,ranked),default=0)):
            for qi,candidates in enumerate(ranked):
                if len(chosen)>=max_facts:break
                if qi in budget_stopped:continue
                if rank>=len(candidates) or candidates[rank] in chosen:continue
                proposed=chosen+[candidates[rank]]
                trial=packet(proposed,preview_limit)
                if trial['retrieval']['evidence_bytes']<=byte_budget and fits_packet(trial):
                    chosen=proposed;current=trial
                else:
                    budget_stopped.add(qi)
            if len(chosen)>=max_facts:break
        self.store.verify()
        measure_packet(current)
        return current

    async def get_facts(self,fact_ids,formly_version=None,ui_adapter=None,response_format='compact'):
        if not isinstance(fact_ids,list) or not 1<=len(fact_ids)<=16 or any(not isinstance(x,str) or not x or len(x)>300 for x in fact_ids):raise ValueError('Supply 1..16 fact IDs')
        if response_format not in ('compact','full'):raise ValueError('response_format must be compact or full')
        context=await self.gate.lookup('Fetch requested evidence',formly_version=formly_version,ui_adapter=ui_adapter)
        if 'status' in context:return context
        facts,citations=self.store.records(fact_ids,context['version_context']['selected'],context['ui_adapter'])
        packet=dict(evidence_status='candidate_only',**evidence_packet(facts,citations,response_format),**context)
        if response_format=='full':
            if encoded_size(packet)>48000:raise ValueError('Evidence exceeds budget; request fewer fact IDs')
        elif not fits_packet(packet):
            raise ValueError('Response exceeds 28000-byte packet or 30000-byte tool-result budget; request fewer fact IDs')
        return packet
