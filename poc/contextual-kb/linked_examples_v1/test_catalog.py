import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
from linked_examples_v1.catalog import Catalog, ExecutionEnvironment, authored_fact_ids
from model_free_v1.response import fits_packet, transport_size


def example(eid='demo', facts=None):
    return dict(schema_version=1, id=eid, title='Demo', summary='Bounded illustration',
        scope=dict(formly_version='6.3.12', ui_adapter='Material'),
        fact_links=[dict(fact_id=fid, support='Demonstrates this mechanism') for fid in (facts or ['a/one'])],
        conditions=[], limits=['Not universal compatibility'], prerequisites=['Pinned environment'],
        files=[dict(path='demo.ts', language='typescript')], assertions=['Check state'],
        provenance=[dict(kind='authored_fact', reference='a/one')],
        verification=dict(status='illustrative', details='Not executed'))


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write(example())

    def write(self, record, content='export const x = 1;'):
        folder = self.root / record['id']
        folder.mkdir(exist_ok=True)
        (folder / 'manifest.json').write_text(json.dumps(record))
        (folder / 'demo.ts').write_text(content)

    def catalog(self):
        return Catalog(self.root, {'a/one', 'a/two'})

    def test_many_to_many_listing_deduplicates_and_does_not_include_code(self):
        self.write(example('other', ['a/one', 'a/two']))
        page = self.catalog().retrieve(fact_ids=['a/one', 'a/two'])
        self.assertEqual(['demo', 'other'], [r['id'] for r in page['examples']])
        self.assertNotIn('files', page['examples'][0])

    def test_complete_fetch_preserves_code_and_constraints(self):
        record = self.catalog().retrieve(example_ids=['demo'])['examples'][0]
        self.assertEqual('export const x = 1;', record['files'][0]['content'])
        self.assertEqual(64, len(record['files'][0]['sha256']))
        self.assertTrue(record['limits'])
        self.assertEqual('illustrative', record['verification']['status'])

    def test_pagination_and_exhaustion(self):
        self.write(example('other'))
        catalog = self.catalog()
        self.assertEqual(1, catalog.retrieve(fact_ids=['a/one'], limit=1)['next_offset'])
        self.assertEqual('other', catalog.retrieve(fact_ids=['a/one'], offset=1)['examples'][0]['id'])
        self.assertEqual('exhausted', catalog.retrieve(fact_ids=['a/one'], offset=2)['status'])

    def test_validation_is_atomic(self):
        for kwargs in ({}, {'fact_ids': []}, {'fact_ids': ['a/one'], 'example_ids': ['demo']},
                {'fact_ids': ['a/one', 'unknown']}, {'example_ids': ['demo', 'unknown']},
                {'fact_ids': ['a/one'], 'offset': True}, {'fact_ids': ['a/one'], 'limit': 0},
                {'example_ids': ['demo'], 'file_paths': ['no.ts']}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.catalog().retrieve(**kwargs)

    def test_unsupported_scope_and_no_link_are_explicit(self):
        catalog = self.catalog()
        self.assertEqual('unsupported_scope', catalog.retrieve(fact_ids=['a/one'], formly_version='7')['status'])
        self.assertEqual('unsupported_scope', catalog.retrieve(fact_ids=['a/one'], ui_adapter='core')['status'])
        self.assertEqual('exhausted', catalog.retrieve(fact_ids=['a/two'])['status'])

    def test_unknown_links_and_extra_fields_reject(self):
        for update in ({'fact_links': [dict(fact_id='unknown', support='No')]}, {'unknown': 1}):
            record = example(); record.update(update); self.write(record)
            with self.assertRaises(ValueError): self.catalog()

    def test_duplicate_links_reject(self):
        self.write(example(facts=['a/one', 'a/one']))
        with self.assertRaises(ValueError): self.catalog()

    def test_unsafe_files_reject(self):
        for name in ('../demo.ts', '/demo.ts', 'a\\b.ts', 'C:demo.ts', './demo.ts'):
            record = example(); record['files'][0]['path'] = name; self.write(record)
            with self.subTest(name=name), self.assertRaises(ValueError): self.catalog()

    def test_symlink_file_rejects(self):
        target = self.root / 'demo/demo.ts'
        target.unlink(); target.symlink_to(self.root / 'demo/manifest.json')
        with self.assertRaises(ValueError): self.catalog()

    def test_executed_without_hashes_rejects(self):
        record = example(); record['verification'].update(status='executed', command='test', environment={'x':'1'}, result_path='result.json')
        self.write(record)
        with self.assertRaises(ValueError): self.catalog()

    def test_execution_environment_has_typed_fixture_hashes_and_assertions(self):
        env = {key: '1' for key in ('@angular/core', '@angular/material', '@ngx-formly/core',
            '@ngx-formly/material', 'rxjs', 'zone.js', 'playwright', 'esbuild', 'node',
            'platform', 'arch', 'browser')}
        env.update(fixture_sha256={'fixture.ts': 'a' * 64}, assertions_passed=['model.retained'])
        self.assertEqual(env, ExecutionEnvironment.model_validate(env).model_dump(by_alias=True))
        for update in ({'fixture_sha256': {'fixture.ts': 'not-a-digest'}},
                       {'assertions_passed': []}, {'assertions_passed': [2]},
                       {'unknown': 'field'}, {'node': {'nested': 'unexpected'}}):
            with self.subTest(update=update), self.assertRaises(ValueError):
                ExecutionEnvironment.model_validate(dict(env, **update))

    def test_code_over_budget_rejects_instead_of_truncating(self):
        self.write(example(), content='x' * 30000)
        with self.assertRaisesRegex(ValueError, 'never truncated'):
            self.catalog().retrieve(example_ids=['demo'])

    def test_file_selection_has_manifest_and_complete_file(self):
        result = self.catalog().retrieve(example_ids=['demo'], file_paths=['demo.ts'])['examples'][0]
        self.assertEqual('export const x = 1;', result['files'][0]['content'])
        self.assertNotIn('content', result['available_files'][0])

    def test_enrichment_preserves_fact_payload_and_size(self):
        catalog = self.catalog()
        packet = dict(status='ok', ui_adapter='material', facts=[dict(id='a/one', claim='Test')])
        result = catalog.enrich(packet)
        self.assertEqual(packet['facts'], result['facts'])
        self.assertEqual(['a/one'], result['example_references'][0]['matched_fact_ids'])
        self.assertNotIn('files', result['example_references'][0])
        self.assertLessEqual(transport_size(result), 30000)

    def test_full_budget_never_loses_facts(self):
        packet = dict(status='ok', ui_adapter='material', facts=[dict(id='a/one', claim='x' * 27000)])
        while fits_packet(packet): packet['facts'][0]['claim'] += 'x'
        packet['facts'][0]['claim'] = packet['facts'][0]['claim'][:-1]
        self.assertTrue(fits_packet(packet))
        original = copy.deepcopy(packet)
        result = self.catalog().enrich(packet)
        self.assertEqual(original['facts'], result['facts'])
        self.assertTrue(fits_packet(result))

    def test_real_catalog_links_resolve_to_authored_facts(self):
        root = POC / 'linked_examples_v1/examples'
        if not root.exists(): self.skipTest('Example authoring still in progress')
        catalog = Catalog(root, authored_fact_ids(POC / 'authored'))
        self.assertEqual(3, len(catalog.records))


if __name__ == '__main__': unittest.main()
