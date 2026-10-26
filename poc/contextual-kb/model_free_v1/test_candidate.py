import asyncio
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from candidate import Store, Service, digest


def fixture(path):
    db=sqlite3.connect(path)
    db.executescript('''
    CREATE TABLE build_info(schema_version INTEGER);
    INSERT INTO build_info VALUES(2);
    CREATE TABLE documents(id TEXT PRIMARY KEY,title TEXT,formly_version TEXT,adapter TEXT,source_path TEXT,source_sha256 TEXT);
    CREATE TABLE facts(id TEXT PRIMARY KEY,doc_id TEXT,claim TEXT,context TEXT,conditions_json TEXT,limits_json TEXT,source_quote TEXT,source_start_offset INT,source_end_offset INT,status TEXT);
    CREATE TABLE applicability(fact_id TEXT,kind TEXT,value TEXT,basis TEXT,reason TEXT);
    CREATE TABLE applicability_evidence(fact_id TEXT,kind TEXT,value TEXT,evidence_id TEXT);
    CREATE TABLE evidence_releases(evidence_id TEXT,release TEXT);
    CREATE TABLE evidence(id TEXT,record_json TEXT);
    CREATE TABLE fact_evidence(fact_id TEXT,evidence_id TEXT);
    CREATE VIRTUAL TABLE facts_fts USING fts5(fact_id UNINDEXED,claim,context,conditions,limits,document_title,document_summary);
    ''')
    rows=[('generic','Explain hidden field preserves model value control registration','core'),
          ('target','resetOnHide false preserves model data','core'),
          ('and','alpha beta','core'),('broader','alpha gamma','core'),
          ('material','specialMaterial only','material')]
    for fid,claim,adapter in rows:
        db.execute('INSERT INTO documents VALUES(?,?,?,?,?,?)',(fid,'Topic','6.3.12',adapter,'fixture.md','testhash'))
        db.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?,?,?,?)',(fid,fid,claim,'',json.dumps(['Only in fixture']),json.dumps(['Does not prove compatibility']),claim,0,len(claim),'authored'))
        db.execute('INSERT INTO applicability VALUES(?,?,?,?,?)',(fid,'exact','6.3.12','direct',None))
        db.execute('INSERT INTO facts_fts VALUES(?,?,?,?,?,?,?)',(fid,claim,'','','','Topic',''))
    db.commit();db.close()


def plan(question,condition=None):
    return dict(formly_questions=[dict(question=question,reason='Library behavior')],library_constraints=dict(formly_version=None,ui_adapter=None),condition_bindings=[] if condition is None else [dict(condition=condition,question_indexes=[0])])


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.path=self.root/'db.sqlite';fixture(self.path)
        self.sha=digest(self.path);self.store=Store(self.path,self.sha)
        self.service=Service(self.store,self.root/'settings.sqlite')
    def tearDown(self):
        self.store.close();self.temp.cleanup()
    def lookup(self,*args,**kwargs):return asyncio.run(self.service.lookup(*args,**kwargs))
    def test_late_identifier_survives(self):
        q='Explain how a hidden field preserves its model value and control registration with resetOnHide: false.'
        self.assertNotIn('target',self.store.search(q,'6.3.12',None,'basic'))
        self.assertIn('target',self.store.search(q,'6.3.12',None,'improved'))
    def test_or_candidates_not_suppressed(self):
        self.assertEqual(['and'],self.store.search('alpha beta','6.3.12',None,'basic'))
        self.assertIn('broader',self.store.search('alpha beta','6.3.12',None,'improved'))
    def test_scope_applied_before_selection_and_followup(self):
        self.assertEqual([],self.store.search('specialMaterial','6.3.12','core'))
        with self.assertRaises(ValueError):self.store.records(['material'],'6.3.12','core')
        self.assertEqual('unsupported_version',self.lookup('alpha',formly_version='7')['status'])
    def test_raw_fallback_disclosed_and_readonly(self):
        result=self.lookup('alpha beta')
        self.assertEqual('not_decomposed',result['planning']['status'])
        self.assertEqual('candidate_only',result['evidence_status'])
        with self.assertRaises(sqlite3.OperationalError):self.store.db.execute('DELETE FROM facts')
        self.assertEqual(self.sha,digest(self.path))
    def test_conditions_and_scope_cannot_be_silently_dropped(self):
        p=plan('How does alpha behave without beta?','without beta')
        self.lookup('Explain alpha without beta',plan=p)
        p['formly_questions'][0]['question']='How does alpha behave?'
        with self.assertRaises(ValueError):self.lookup('Explain alpha without beta',plan=p)
        p=plan('alpha');p['library_constraints']['formly_version']='7'
        with self.assertRaises(ValueError):self.lookup('alpha',plan=p,formly_version='6.3.12')
    def test_budget_and_complete_records(self):
        result=self.lookup('alpha',max_facts=1)
        self.assertTrue(result['truncated']);self.assertTrue(result['questions'][0]['omitted_ids'])
        self.assertEqual(1,len(result['facts']))
        self.assertEqual(['Does not prove compatibility'],result['facts'][0]['limits'])
        self.assertEqual(set(result['citations']),{f['id'] for f in result['facts']})
        result=self.lookup('alpha',byte_budget=1)
        self.assertEqual([],result['facts']);self.assertTrue(result['truncated'])
    def test_sql_like_input_never_executes(self):
        self.lookup('" OR 1=1; DROP TABLE facts; -- alpha')
        self.assertEqual(5,self.store.db.execute('SELECT count(*) FROM facts').fetchone()[0])
    def test_empty_plan_is_explicit_no_library_questions(self):
        p=plan('alpha');p['formly_questions']=[]
        result=self.lookup('Find my private widget',plan=p)
        self.assertEqual([],result['facts']);self.assertEqual('caller_plan',result['planning']['status'])
    def test_bounded_inputs_and_integrity(self):
        p=plan('alpha');p['formly_questions']*=7
        with self.assertRaises(ValueError):self.lookup('alpha',plan=p)
        with self.assertRaises(ValueError):Store(self.path,'wrong')

if __name__=='__main__':unittest.main()
