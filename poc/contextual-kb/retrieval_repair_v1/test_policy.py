import copy,unittest
from policy import acquire, present, apply_repair, repair
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
class Index:
    facts={str(i):{'id':str(i),'claim':f'claim {i}','context':'context','conditions':[],'limits':[],'version':'6.3.12','adapter':'core','title':'title'} for i in range(30)}
    def lexical(self,q,n):return [str(i) for i in range(n)]
    def dense(self,q,n):return [str(i) for i in range(10,10+n)]
class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.core={'formly_questions':[{'question':'Formly question','reason':'lookup'}],'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[]}
        self.baseline=[str(i) for i in range(8)];self.index=Index()
        self.acquired=acquire(self.index,self.core,self.baseline)
        self.payload,self.mapping=present(self.core,self.baseline,self.acquired['pool'],self.index.facts,lambda f:'source '+f)
        self.reverse={v:k for k,v in self.mapping.items()}
    def decision(self,remove='7',add='19'):
        return {'replacements':[{'remove':self.reverse[remove],'add':self.reverse[add],'question_indexes':[0],'support_quote':'claim '+add,'reason':'Adds missing support; removed fact irrelevant.'}]}
    def test_deeper_channels_preserve_original_and_full_candidate_union(self):
        self.assertEqual(set(self.acquired['pool']),set(str(i) for i in range(30)))
        self.assertEqual([q['text'] for q in self.acquired['queries']],['Formly question','Formly question'])
        self.assertEqual([q['depth'] for q in self.acquired['queries']],[20,20])
    def test_only_explicit_slots_change_no_fact_mutation(self):
        original=copy.deepcopy(self.payload);ids=apply_repair(self.decision(),self.payload,self.mapping)
        self.assertEqual(ids,self.baseline[:7]+['19']);self.assertEqual(self.payload,original)
    def test_invalid_decisions_rejected_atomically(self):
        samples=[]
        x=self.decision();x['replacements'][0]['support_quote']='invented';samples.append(x)
        x=self.decision();x['replacements'][0]['question_indexes']=[True];samples.append(x)
        x=self.decision();x['replacements'][0]['remove']=self.reverse['20'];samples.append(x)
        x=self.decision();x['replacements'][0]['add']=self.reverse['1'];samples.append(x)
        x=self.decision();x['replacements']*=2;samples.append(x)
        x=self.decision();x['replacements']*=3;samples.append(x)
        x=self.decision();x['replacements'][0]['add']='unknown';samples.append(x)
        for sample in samples:
            with self.assertRaises(ValueError):apply_repair(sample,self.payload,self.mapping)
    def test_payload_is_gold_blind_and_has_no_gliner_hints(self):
        self.assertEqual(set(self.payload),{'questions','condition_bindings','library_constraints','baseline','candidates'})
        self.assertNotIn('id',self.payload['candidates'][0]);self.assertNotIn('title',self.payload['candidates'][0])
    def test_failed_or_invalid_selection_preserves_baseline(self):
        def fail(_):raise RuntimeError('unavailable')
        for selector in [fail,lambda _:{'replacements':[{}]}]:
            r=repair(self.index,self.core,self.baseline,lambda f:'source',selector)
            self.assertEqual(r['ids'],self.baseline);self.assertEqual(r['status'],'fallback')
    def test_integrity_failure_is_never_fallback(self):
        def fail(_):raise IntegrityError('changed')
        with self.assertRaises(IntegrityError):repair(self.index,self.core,self.baseline,lambda f:'source',fail)
    def test_empty_questions_do_not_call_selector(self):
        self.core['formly_questions']=[]
        r=repair(self.index,self.core,[],lambda f:self.fail(),lambda p:self.fail())
        self.assertEqual(r['ids'],[]);self.assertEqual(r['status'],'not_needed')
if __name__=='__main__':unittest.main()
