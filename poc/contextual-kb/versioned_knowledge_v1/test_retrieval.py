import sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(POC),str(POC/'mcp_v1')]
import copy
import sqlite3
import unittest
import numpy as np
import test_compiler
from versioned_knowledge_v1.index import Index, ScopeError

class Embeddings:
    def __init__(self):self.texts=[]
    def embed(self,texts):
        self.texts.extend(texts)
        return iter(np.array([1.,0.],dtype='float32') for _ in texts)
    def query_embed(self,text):return iter([np.array([1.,0.],dtype='float32')])

class RetrievalTests(unittest.TestCase):
    edit = test_compiler.CompilerTests.edit
    compile = test_compiler.CompilerTests.compile
    # Inherit fixture only, not compiler test cases.
    def setUp(self):
        test_compiler.CompilerTests.setUp(self)
        def add(d):
            old=d['facts'][0];old['id']='a-old'
            new=copy.deepcopy(old);new['id']='z-new';new['claim']='A scoped claim newer'
            new['applicability']=[{'scope':{'kind':'major','value':'7'},'basis':'inferred','reason':'Synthetic','evidence_ids':['K01']}]
            old['related']=[{'kind':'see_also','target':'sample/z-new'}]
            d['facts'].append(new)
        self.edit(add);self.compile()
        self.connection=sqlite3.connect(f'file:{self.db}?mode=ro',uri=True)
        self.addCleanup(self.connection.close)
        self.embedder=Embeddings();self.index=Index(self.connection,self.embedder)

    def test_filter_before_limits_and_reject_cross_scope_citations(self):
        seven=self.index.for_scope('7.0.0','material')
        self.assertEqual(['sample/z-new'],seven.lexical('scoped claim',1))
        self.assertEqual(['sample/z-new'],seven.dense('scoped claim',1))
        self.assertEqual(['sample/z-new'],seven.hybrid('scoped claim',1))
        with self.assertRaises(ScopeError):seven.citations(['sample/a-old'])
        with self.assertRaises(ScopeError):seven.add_links(['sample/a-old'],8)
        six=self.index.for_scope('6.3.12','material')
        self.assertEqual(['sample/a-old'],six.add_links(['sample/a-old'],8))
        citation=seven.citations(['sample/z-new'])['sample/z-new']
        self.assertEqual('6.3.12',citation['applicability'][0]['evidence'][0]['release'])
        self.assertEqual('inferred',citation['applicability'][0]['basis'])

    def test_shared_index_no_duplicate_embeddings_and_fail_closed(self):
        self.assertEqual(2,len(self.embedder.texts))
        self.index.for_scope('6.3.12','core');self.index.for_scope('7.0.0','material')
        self.assertEqual(2,len(self.embedder.texts))
        for version,adapter in [('8.0.0','core'),('7','core'),('7.0.0','bootstrap')]:
            with self.assertRaises((ValueError,ScopeError)):self.index.for_scope(version,adapter)

    def test_selector_pool_and_fallback_cannot_escape_scope(self):
        from retrieval_repair_v1.policy import repair
        six=self.index.for_scope('6.3.12','core')
        core={'formly_questions':[{'question':'scoped claim'}],'condition_bindings':[],'library_constraints':[]}
        presented=[]
        def malicious_selector(payload):
            presented.extend(payload['candidates'])
            return {'replacements':[{'remove':payload['baseline'][0],'add':'c999','question_indexes':[0],'support_quote':'A scoped claim','reason':'Bad handle'}]}
        result=repair(six,core,['sample/a-old'],lambda fid:six.facts[fid]['claim'],malicious_selector)
        self.assertEqual('fallback',result['status'])
        self.assertEqual(['sample/a-old'],result['ids'])
        self.assertEqual(1,len(presented))
        self.assertEqual('6.3.12',presented[0]['version'])
        self.assertTrue(all('sample/z-new' not in q['ids'] for q in result['queries']))

    def test_schema_is_explicit(self):
        memory=sqlite3.connect(':memory:');self.addCleanup(memory.close)
        with self.assertRaises(ValueError):Index(memory,self.embedder)

if __name__=='__main__':unittest.main()
