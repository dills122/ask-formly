import copy,unittest
from unittest.mock import patch
from integration import Backend
from mcp_v1.backend import Backend as Original
from agent_contract.advisory_lookup_v1.runtime import IntegrityError
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.base={'plan':{'question_plan':{'unchanged':True},'search_requests':[{'query':'full question'}],'role_hints':[{'text':'api'}]},'retrieval':{'ids':['old'],'queries':[{'text':'full question','ids':['old']}],'query_count':1,'questions':[['old']]},'facts':[{'id':'old'}],'citations':{'old':{}},'advisory':{'status':'available'},'runtime':{'db_unchanged':True},'evidence_status':'candidate_only'}
        self.obj=Backend.__new__(Backend);self.obj.selector=lambda _:None;self.obj.dbpath='unused';self.obj.dbhash='hash';self.obj.db=object();self.obj.index=type('I',(),{'facts':{'new':{'id':'new','claim':'original'}}})()
    def test_selection_changes_only_packet_not_core_queries_or_hints(self):
        original=copy.deepcopy(self.base)
        with patch.object(Original,'lookup',return_value=self.base),patch('integration.repair',return_value={'ids':['new'],'status':'repaired','queries':[]}),patch('integration.citations_for',return_value={'new':{'stored':True}}),patch('integration.digest',return_value='hash'):
            result=self.obj.lookup('original',{'plan':'core'})
        self.assertEqual(result['plan'],original['plan']);self.assertEqual(result['retrieval']['queries'],original['retrieval']['queries'])
        self.assertEqual(result['retrieval']['foundation_ids'],['old']);self.assertEqual(result['retrieval']['ids'],['new'])
        self.assertEqual(result['facts'],[{'id':'new','claim':'original'}]);self.assertEqual(result['citations'],{'new':{'stored':True}})
        self.assertEqual(self.base,original)
    def test_known_db_change_after_selection_is_fatal(self):
        with patch.object(Original,'lookup',return_value=self.base),patch('integration.repair',return_value={'ids':['old'],'status':'unchanged'}),patch('integration.digest',return_value='changed'):
            with self.assertRaises(IntegrityError):self.obj.lookup('request',{})
if __name__=='__main__':unittest.main()
