import json
import unittest
from unittest.mock import patch
from candidate import HERE, ORIGINAL, COPIED, checked_database, preserved

class PreservationTests(unittest.TestCase):
    def test_original_grading_and_cases_are_identical(self):
        for name in COPIED:
            self.assertEqual((HERE/name).read_bytes(), (ORIGINAL/name).read_bytes(), name)

    def test_installed_arm_cannot_be_selected(self):
        with self.assertRaises(ValueError):
            checked_database('baseline')

    def test_candidate_is_original_frozen_85_fact_artifact(self):
        path, digest = checked_database('candidate')
        self.assertEqual(path, ORIGINAL/'candidate-build/knowledge.sqlite')
        self.assertEqual(digest, 'bbb55e168cc81e60927a1bf146af767cd8ab6c9999875239ea28a879487531ff')

    def test_changed_pin_aborts_before_database_use(self):
        with patch('candidate.digest', return_value='changed'):
            with self.assertRaisesRegex(ValueError, 'Preservation mismatch'):
                checked_database('candidate')

    def test_original_167_pins_and_freezes_are_preserved(self):
        state = preserved()
        self.assertEqual(state['original_baseline_pin_count'], 167)
        for name in ('input-freeze.json','qualification-freeze.json'):
            self.assertIn(str((ORIGINAL/'test-output'/name).relative_to(HERE.parents[3])),state['files'])

if __name__ == '__main__': unittest.main()
