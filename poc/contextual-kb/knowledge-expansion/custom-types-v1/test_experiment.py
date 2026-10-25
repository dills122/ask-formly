import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from experiment import checked_database, parse_agent_output, ReplayPlanner

class ExperimentTests(unittest.TestCase):
    def test_rejects_unknown_arm(self):
        with self.assertRaises(ValueError): checked_database('other')
    def test_rejects_missing_or_unpinned_candidate(self):
        with patch('experiment.HERE',Path('/nonexistent')):
            with self.assertRaises(FileNotFoundError): checked_database('candidate')
    def test_answer_requires_completed_turn(self):
        with self.assertRaises(ValueError): parse_agent_output([],['Q1'])
    def test_answer_requires_exact_ids_once(self):
        import json
        events=[{'type':'item.completed','item':{'type':'agent_message','text':json.dumps({'answers':[{'id':'wrong','answer':'x','citations':[],'gaps':[]}]})}},{'type':'turn.completed'}]
        with self.assertRaises(ValueError): parse_agent_output(events,['Q1'])
    def test_replay_rejects_request_change(self):
        planner=ReplayPlanner({'original':{'core':{},'generation':{}}})
        with self.assertRaises(ValueError): planner('paraphrase')
    def test_replay_detaches_plan(self):
        planner=ReplayPlanner({'original':{'core':{'x':[]},'generation':{}}})
        first,_=planner('original');first['x'].append(1)
        second,_=planner('original');self.assertEqual(second,{'x':[]})
if __name__=='__main__':unittest.main()

class ReplayCollectionTests(unittest.TestCase):
    def test_failed_source_call_is_missing_not_an_empty_success(self):
        import json
        from replay import collect
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);p=root/'r1-b1-baseline/mcp/audit';p.mkdir(parents=True)
            (p/'a.json').write_text(json.dumps({'request':'q','error':{'type':'ValueError'}}))
            records,source,missing=collect(root,[{'id':'Q1','request':'q'}],'baseline',1)
            self.assertEqual(records,{});self.assertEqual(missing,['Q1'])
    def test_duplicate_source_calls_are_not_cherry_picked(self):
        import json
        from replay import collect
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);p=root/'r1-b1-baseline/mcp/audit';p.mkdir(parents=True)
            for name in ['a','b']:(p/(name+'.json')).write_text(json.dumps({'request':'q','result':{}}))
            self.assertEqual(collect(root,[{'id':'Q1','request':'q'}],'baseline',1)[2],['Q1'])
