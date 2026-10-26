"""One embedding per fact; immutable request-scoped eligibility before top-k."""
import json
import os
from pathlib import Path
import numpy as np
from kbcompiler.question_pilot import PilotIndex, _terms, _match_expression, EMBED_MODEL
from mcp_v1.backend import citations_for
from versioned_knowledge_v1.compiler import release

class ScopeError(ValueError):
    """No provisioned facts, or a consumer attempted to escape request scope."""

class Index:
    def __init__(self,db,embedder=None):
        self.db=db
        try:version=db.execute('SELECT schema_version FROM build_info').fetchall()
        except Exception as exc:raise ValueError('Missing candidate schema') from exc
        if version!=[(2,)]:raise ValueError('Unsupported candidate schema')
        self.facts={}
        for fid,claim,context,conditions,limits,title,source_version,adapter in db.execute('''
            SELECT f.id,f.claim,f.context,f.conditions_json,f.limits_json,d.title,d.formly_version,d.adapter
            FROM facts f JOIN documents d ON d.id=f.doc_id ORDER BY f.id'''):
            self.facts[fid]=dict(id=fid,claim=claim,context=context,conditions=json.loads(conditions),limits=json.loads(limits),title=title,version=source_version,adapter=adapter)
        self.ids=list(self.facts)
        if not self.ids:raise ValueError('Empty candidate')
        if embedder is None:
            from fastembed import TextEmbedding
            embedder=TextEmbedding(model_name=EMBED_MODEL,cache_dir=os.environ.get('FORMLY_PILOT_EMBED_CACHE',str(Path.home()/'.cache/fastembed')),local_files_only=True)
        self.embedder=embedder
        vectors=np.stack(list(embedder.embed([PilotIndex._embedding_text(self.facts[f]) for f in self.ids]))).astype('float32')
        self.vectors=vectors/np.maximum(np.linalg.norm(vectors,axis=1,keepdims=True),1e-12)

    def for_scope(self,version,adapter=None):
        release(version)
        if adapter not in (None,'core','material'):raise ScopeError('Unsupported adapter')
        adapters=('core','material') if adapter in (None,'material') else ('core',)
        apps={}
        for fid,kind,value,basis,reason in self.db.execute('''
            SELECT a.fact_id,a.kind,a.value,a.basis,a.reason FROM applicability a
            JOIN facts f ON f.id=a.fact_id JOIN documents d ON d.id=f.doc_id
            WHERE ((a.kind='exact' AND a.value=?) OR (a.kind='major' AND a.value=?))
            ORDER BY a.fact_id,a.kind,a.value''',(version,version.split('.')[0])):
            if self.facts[fid]['adapter'] not in adapters:continue
            evidence=[dict(id=eid,release=ev_release) for eid,ev_release in self.db.execute('''
                SELECT ae.evidence_id,er.release FROM applicability_evidence ae
                JOIN evidence_releases er ON er.evidence_id=ae.evidence_id
                WHERE ae.fact_id=? AND ae.kind=? AND ae.value=? ORDER BY ae.evidence_id''',(fid,kind,value))]
            apps.setdefault(fid,[]).append(dict(scope=dict(kind=kind,value=value),basis=basis,reason=reason,evidence=evidence))
        if not apps:raise ScopeError('No accepted applicability for requested scope')
        return ScopedIndex(self,apps,version,adapter)

class ScopedIndex(PilotIndex):
    def __init__(self,parent,apps,version,adapter):
        # Do not call the legacy constructor: it hardcodes 6.3.12 eligibility.
        self.db=parent.db;self.embedder=parent.embedder
        self.applicability=apps;self.version=version;self.adapter=adapter
        self.ids=[fid for fid in parent.ids if fid in apps]
        self.facts={fid:dict(parent.facts[fid],applicability=apps[fid]) for fid in self.ids}
        self.vectors=parent.vectors[[i for i,fid in enumerate(parent.ids) if fid in apps]]

    def lexical(self,text,limit):
        terms=_terms(text)
        if not terms:return []
        marks=','.join('?' for _ in self.ids)
        for operator in ('AND','OR'):
            rows=self.db.execute(f'''SELECT f.id FROM facts_fts JOIN facts f ON f.id=facts_fts.fact_id
                WHERE facts_fts MATCH ? AND f.id IN ({marks})
                ORDER BY bm25(facts_fts),f.id LIMIT ?''',(_match_expression(terms,operator),*self.ids,limit)).fetchall()
            if rows:return [r[0] for r in rows]
        return []

    def require(self,ids):
        if not set(ids)<=self.facts.keys():raise ScopeError('Fact outside request applicability')

    def add_links(self,selected,limit):
        self.require(selected)
        if len(selected)>=limit:return selected[:limit]
        return super().add_links(selected,limit)

    def citations(self,ids):
        self.require(ids)
        result=citations_for(self.db,ids)
        for fid in ids:result[fid]['applicability']=self.applicability[fid]
        return result
