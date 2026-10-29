"""Exercise search normalization at the FTS boundary using disposable data."""
from pathlib import Path
import sqlite3
import tempfile
import unittest

from candidate import Store, digest
from test_candidate import fixture


class SearchMatchingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'knowledge.sqlite'
        fixture(self.path)
        claims = {
            'generic': 'options.formState carries shared form context.',
            'target': 'formState changes trigger expression updates.',
            'and': 'A keyed fieldGroup gives child values a nested model path.',
            'broader': 'Material appearance selects a visual style.',
            'material': 'compareWith compares Material select options.',
        }
        with sqlite3.connect(self.path) as db:
            for fid, claim in claims.items():
                db.execute('UPDATE facts SET claim=?,source_quote=? WHERE id=?', (claim, claim, fid))
                db.execute('UPDATE facts_fts SET claim=? WHERE fact_id=?', (claim, fid))
        self.sha = digest(self.path)
        self.store = Store(self.path, self.sha)

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_qualified_and_bare_members_use_identical_routes(self):
        bare = self.store.search('How does formState trigger expression updates?', '6.3.12', 'material')
        qualified = self.store.search('How does options.formState trigger expression updates?', '6.3.12', 'material')
        self.assertEqual(bare, qualified)
        self.assertEqual('target', bare[0])
        self.assertEqual(self.sha, digest(self.path))

    def test_unknown_namespace_is_not_an_alias(self):
        self.assertEqual([], self.store.search('application.formState', '6.3.12', 'material'))

    def test_scope_prose_cannot_seed_a_material_candidate(self):
        results = self.store.search('For Formly 6.3.12 with Material, formState', '6.3.12', 'material')
        self.assertNotIn('broader', results)
        self.assertIn('target', results)
        self.assertEqual([], self.store.search('compareWith', '6.3.12', 'core'))
        self.assertEqual(['material'], self.store.search('compareWith', '6.3.12', 'material'))

    def test_model_collision_hint_changes_candidates_without_fabricating_facts(self):
        results = self.store.search('Two sections have name fields; their values collide.', '6.3.12', 'material')
        self.assertEqual('and', results[0])
        self.assertEqual('A keyed fieldGroup gives child values a nested model path.', self.store.facts['and']['claim'])
        self.assertEqual([], self.store.search('DOM name collision', '6.3.12', 'material'))


if __name__ == '__main__':
    unittest.main()
