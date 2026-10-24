import json,unittest
from candidate import acquire,present,validate_selection,account

class Index:
    def __init__(self):self.calls=[]
    def hybrid(self,q,k):
        self.calls.append((q,k))
        return ['late','early','extra'] if k==20 else ['early','tail']

class CandidateTests(unittest.TestCase):
    def core(self):return {'formly_questions':[{'question':'What happens?','reason':'Asked'}],'condition_bindings':[],'library_constraints':{'formly_version':None,'ui_adapter':None}}
    def test_depth_does_not_assume_prefix(self):
        i=Index();r=acquire(i,self.core())
        self.assertEqual(i.calls,[('What happens?',8),('What happens?',20)])
        self.assertEqual(r['foundation'],['early','tail'])
        self.assertEqual(r['wide_pool'],['late','early','extra','tail'])
        self.assertEqual(r['wide_rank'],['late','early','extra','tail'])
    def test_no_questions_no_queries(self):
        c=self.core();c['formly_questions']=[];i=Index();r=acquire(i,c)
        self.assertEqual(r['wide_pool'],[]);self.assertEqual(i.calls,[])
    def test_presentation_opaque_order_rank_independent(self):
        facts={k:dict(id=k,claim=k+' claim',conditions=[],limits=['limit'],version='6.3.12',adapter='core',context='DO NOT SHOW',title='DO NOT SHOW') for k in ['early','tail']}
        a,m=present('R1',self.core(),['tail','early'],facts);b,n=present('R1',self.core(),['early','tail'],facts)
        self.assertEqual(a,b);self.assertEqual(m,n)
        self.assertNotIn('context',a['candidates'][0]);self.assertNotIn('title',a['candidates'][0]);self.assertNotIn('id',a['candidates'][0])
        self.assertEqual(set(m.values()),set(facts))
    def test_selection_translates_and_allows_empty(self):
        self.assertEqual(validate_selection([dict(handle='c001',question_indexes=[0],reason='Direct')],{'c001':'fact'},1),['fact'])
        self.assertEqual(validate_selection([],{},0),[])
    def test_bad_handles_duplicates_and_more_than_eight_rejected(self):
        row=dict(handle='c001',question_indexes=[0],reason='Direct')
        for rows in [[dict(row,handle='absent')],[row,row],[dict(row,handle=f'c{i}') for i in range(9)]]:
            with self.assertRaises(ValueError):validate_selection(rows,{'c001':'fact',**{f'c{i}':f'f{i}' for i in range(9)}},1)
    def test_index_reason_schema_strict(self):
        row=dict(handle='c001',question_indexes=[0],reason='Direct')
        for change in [dict(question_indexes=[True]),dict(question_indexes=[1]),dict(question_indexes=[]),dict(question_indexes=[0,0]),dict(reason=' '),dict(extra=1)]:
            with self.assertRaises(ValueError):validate_selection([dict(row,**change)],{'c001':'fact'},1)
    def test_envelope_failure_accounts_all(self):
        for raw in ['[]','[{"id":"R1","selected":[],"id":"R1"}]','NaN']:
            result=account(raw,[dict(id='R1',questions=[{}]),dict(id='R2',questions=[{}])],{'R1':{},'R2':{}})
            self.assertEqual(len(result),2);self.assertTrue(all(x['error'] for x in result));self.assertTrue(all(not x['ids'] for x in result))
    def test_one_bad_selection_does_not_repair(self):
        raw=json.dumps([dict(id='R1',selected=[dict(handle='wrong',question_indexes=[0],reason='x')]),dict(id='R2',selected=[])])
        r=account(raw,[dict(id='R1',questions=[{}]),dict(id='R2',questions=[{}])],{'R1':{},'R2':{}})
        self.assertTrue(r[0]['error']);self.assertIsNone(r[1]['error'])

if __name__=='__main__':unittest.main()
