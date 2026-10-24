import copy
import json
from pathlib import Path
import unittest
from revision import export_example, load_pilot, check_access, HERE, PILOT


class RevisionTests(unittest.TestCase):
    def test_gold_is_unmodified_and_anchor_is_not_identity(self):
        row=load_pilot()[3]; original=copy.deepcopy(row)
        out=export_example(row)
        self.assertEqual(out['output']['record_metadata'],{'request':{'mode':'anchorless'}})
        records=out['output']['json_structures']
        self.assertEqual(len(records),2)
        self.assertEqual(records[0]['request']['target_anchor'],records[1]['request']['target_anchor'])
        self.assertNotEqual(records[0]['request']['request_cues'],records[1]['request']['request_cues'])
        self.assertEqual(row,original)

    def test_all_fields_and_occurrences_preserved(self):
        for row in load_pilot():
            out=export_example(row)
            self.assertEqual(out['input'],row['question'])
            for source,dest in zip(row['aspects'],out['output']['json_structures']):
                self.assertEqual(dest['request'],{k:v for k,v in source.items() if k!='id'})
            self.assertEqual(out['output']['entities'],row['entities'])

    def test_negative_relation_tasks_are_explicit(self):
        row=load_pilot()[3]
        self.assertEqual(row['relations'],[])
        out=export_example(row)
        self.assertEqual(out['output']['relations'],[
            {'has_value':{'head':[],'tail':[]}}, {'refers_to':{'head':[],'tail':[]}}])

    def test_positive_relation_pairs_untouched(self):
        row=load_pilot()[1];out=export_example(row)
        for r in row['relations']:
            self.assertIn({r['kind']:{'head':r['head'],'tail':r['tail']}},out['output']['relations'])

    def test_invalid_offsets_rejected_without_repair(self):
        row=load_pilot()[0];row['aspects'][0]['targets'][0]['end']+=1
        with self.assertRaises(ValueError):export_example(row)

    def test_only_frozen_pilot_can_be_loaded(self):
        with self.assertRaises(ValueError):load_pilot(PILOT/'questions.json')
        self.assertEqual(len(load_pilot()),24)

    def test_access_limits(self):
        for path in [HERE.parents[2]/'planner_cases/sealed.json',HERE/'data.db']:
            with self.assertRaises(PermissionError):check_access('open',(str(path),'r',0))
        with self.assertRaises(PermissionError):check_access('open',(str(PILOT/'adjudicated-v2.json'),'w',0))
        check_access('open',(str(PILOT/'adjudicated-v2.json'),'r',0))
        check_access('open',(str(HERE/'evidence/out.json'),'w',0))
        for event in ['socket.connect','sqlite3.connect','subprocess.Popen']:
            with self.assertRaises(PermissionError):check_access(event,())


if __name__=='__main__':unittest.main()
