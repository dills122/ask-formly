import copy,unittest
from lookup import AdvisoryLookup

Q='In Formly, what happens to hide with resetOnHide: false?'
CORE={'formly_questions':[{'question':Q,'reason':'Requested behavior'}], 'library_constraints':{'formly_version':None,'ui_adapter':None},'condition_bindings':[{'condition':'resetOnHide: false','question_indexes':[0]}]}
class Index:
    def __init__(self):
        self.calls=[];self.facts={f'f{i}':{'id':f'f{i}','claim':f'Claim{i}','conditions':['condition'],'limits':['limit']} for i in range(8)}
    def hybrid(self,text,limit):self.calls.append((text,limit));return list(self.facts)
def native(role='api_reference',text='hide',start=None):
    a=Q.index(text) if start is None else start
    return {'entities':{role:[{'start':a,'end':a+len(text),'text':text,'confidence':.9}]}}

class LookupTests(unittest.TestCase):
    def test_hints_present_but_queries_and_packet_identical(self):
        index=Index();plain=AdvisoryLookup(index).lookup(Q,CORE)
        calls=[]
        def factory():
            def extract(q):calls.append(q);return native()
            return extract
        value=copy.deepcopy(CORE);r=AdvisoryLookup(index,factory).lookup(Q,value)
        self.assertEqual(value,CORE);self.assertEqual(r['plan']['question_plan'],CORE)
        self.assertEqual(r['plan']['search_requests'],plain['plan']['search_requests'])
        self.assertEqual(r['retrieval']['ids'],plain['retrieval']['ids']);self.assertEqual(r['facts'],plain['facts'])
        self.assertEqual(index.calls,[(Q,8),(Q,8)]);self.assertEqual(calls,[Q])
        self.assertFalse(r['plan']['role_hints'][0]['usable_as_filter']);self.assertEqual(r['advisory']['status'],'available')
    def test_load_failure_does_not_block_retrieval(self):
        def factory():raise RuntimeError('unavailable')
        index=Index();r=AdvisoryLookup(index,factory).lookup(Q,CORE)
        self.assertEqual(r['retrieval']['ids'],list(index.facts));self.assertEqual(r['advisory']['status'],'degraded')
        self.assertIn('unavailable',r['advisory']['diagnostics'][0]);self.assertEqual(r['plan']['role_hints'],[])
    def test_inference_failure_explicit_but_retrieval_survives(self):
        def extract(q):raise RuntimeError('inference failed')
        r=AdvisoryLookup(Index(),lambda:extract).lookup(Q,CORE)
        self.assertEqual(r['advisory']['status'],'degraded');self.assertTrue(r['extractions'][0]['error']);self.assertEqual(len(r['facts']),8)
    def test_malformed_unknown_offset_overlap_no_search_change(self):
        for raw in [None,{},native('alien'),native(start=0),{'entities':dict(api_reference=native()['entities']['api_reference'],value=native()['entities']['api_reference'])}]:
            with self.subTest(raw=raw):
                i=Index();r=AdvisoryLookup(i,lambda:lambda _:raw).lookup(Q,CORE)
                self.assertEqual(i.calls,[(Q,8)]);self.assertEqual(r['plan']['role_hints'],[]);self.assertEqual(r['advisory']['status'],'degraded')
    def test_semantically_wrong_hint_cannot_change_queries(self):
        r=AdvisoryLookup(Index(),lambda:lambda _:native('value')).lookup(Q,CORE)
        self.assertEqual(r['plan']['role_hints'][0]['role'],'value');self.assertEqual(r['retrieval']['queries'][0]['text'],Q)
    def test_invalid_core_fails_before_loading_or_search(self):
        i=Index();v=copy.deepcopy(CORE);v['condition_bindings'][0]['condition']='invented'
        with self.assertRaises(ValueError):AdvisoryLookup(i,lambda:self.fail('loaded')).lookup(Q,v)
        self.assertEqual(i.calls,[])
    def test_empty_plan_does_not_load_extract_or_retrieve(self):
        i=Index();v=copy.deepcopy(CORE);v['formly_questions']=[];v['condition_bindings']=[]
        r=AdvisoryLookup(i,lambda:self.fail('loaded')).lookup('Who wrote our form?',v)
        self.assertEqual(i.calls,[]);self.assertEqual(r['facts'],[]);self.assertEqual(r['advisory']['status'],'not_needed')
    def test_model_loaded_once_across_requests(self):
        loads=[]
        def factory():loads.append(1);return lambda _:native()
        s=AdvisoryLookup(Index(),factory);s.lookup(Q,CORE);s.lookup(Q,CORE)
        self.assertEqual(loads,[1])
    def test_load_failure_not_retried_per_request(self):
        loads=[]
        def factory():loads.append(1);raise RuntimeError('unavailable')
        s=AdvisoryLookup(Index(),factory);s.lookup(Q,CORE);s.lookup(Q,CORE);self.assertEqual(loads,[1])
    def test_multiple_questions_preserve_order_and_complete_text(self):
        i=Index();v=copy.deepcopy(CORE);v['formly_questions'].append({'question':'How is a Formly type registered?','reason':'Second ask'})
        r=AdvisoryLookup(i,lambda:lambda _: {'entities':{}}).lookup(Q+' How is a Formly type registered?',v)
        self.assertEqual(i.calls,[(Q,8),('How is a Formly type registered?',8)]);self.assertEqual(len(r['facts']),8)
    def test_returned_facts_cannot_mutate_index(self):
        i=Index();r=AdvisoryLookup(i).lookup(Q,CORE);r['facts'][0]['limits'].append('edited')
        self.assertEqual(i.facts['f0']['limits'],['limit'])
    def test_real_retrieval_failure_not_hidden(self):
        class Broken(Index):
            def hybrid(self,*args):raise RuntimeError('DB search failed')
        with self.assertRaisesRegex(RuntimeError,'DB search failed'):AdvisoryLookup(Broken(),lambda:lambda _:native()).lookup(Q,CORE)

if __name__=='__main__':unittest.main()
