import copy
import unittest
from pathlib import Path
from test_contract import example
from pilot_tools import agreement, check_access, HERE


class AnalysisTests(unittest.TestCase):
    def test_agreement_counts_attachment_and_extra_spans(self):
        a=example(); b=copy.deepcopy(a)
        self.assertEqual(agreement([a],[b])['span_attachment_f1'],1)
        b['aspects'][0]['negative_constraints']=[]
        result=agreement([a],[b])
        self.assertLess(result['span_attachment_f1'],1)
        self.assertEqual(result['aspect_count_agreement'],1)
        self.assertEqual(result['ambiguity_agreement'],1)

    def test_repeated_occurrence_is_not_same_span(self):
        a=example(); b=copy.deepcopy(a)
        b['aspects'][1]['targets']=b['aspects'][0]['targets']
        self.assertLess(agreement([a],[b])['span_attachment_f1'],1)

    def test_misaligned_cases_rejected(self):
        a=example(); b=copy.deepcopy(a);b['id']='wrong'
        with self.assertRaises(ValueError):agreement([a],[b])

    def test_guard_denies_locked_and_sealed_reads_and_external_writes(self):
        for path in [HERE.parents[3]/'planner_cases/sealed.json',
                     HERE.parents[3]/'authored/facts.json',HERE/'test.sqlite']:
            with self.assertRaises(PermissionError):check_access('open',(str(path),'r',0))
        with self.assertRaises(PermissionError):check_access('open',('/tmp/pilot-leak','w',0))
        check_access('open',(str(HERE/'questions.json'),'r',0))
        check_access('open',(str(HERE/'evidence/example.json'),'w',0))

    def test_guard_denies_network_db_and_spawn(self):
        for event in ['socket.connect','socket.getaddrinfo','sqlite3.connect','subprocess.Popen']:
            with self.assertRaises(PermissionError):check_access(event,())


if __name__=='__main__':unittest.main()
