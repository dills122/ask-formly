import asyncio
import copy
import json
import unittest
from discovery import catalog_page


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.packet = dict(status='ok', facts=[dict(id='a')], questions=[
            dict(fact_ids=['a'], omitted_ids=['b', 'c']),
            dict(fact_ids=['a'], omitted_ids=['d', 'b'])])
        self.facts = {k: dict(id=k, claim='claim ' + k, context='context',
            conditions=['only when enabled'], limits=['not universal'], title=k,
            version='6.3.12', adapter='core', applicability=[{'scope': 'exact'}])
            for k in 'abcd'}
        self.reads = []

    def records(self, ids):
        self.reads.extend(ids)
        return [copy.deepcopy(self.facts[k]) for k in ids]

    def test_pages_are_fair_unique_and_exclude_already_delivered(self):
        first = catalog_page(self.packet, self.records, limit=2)
        second = catalog_page(self.packet, self.records, offset=first['next_offset'], limit=2)
        self.assertEqual([f['id'] for f in first['candidates']], ['b', 'd'])
        self.assertEqual([f['id'] for f in second['candidates']], ['c'])
        self.assertIsNone(second['next_offset'])

    def test_preserves_full_conditions_limits_and_scope_without_mutation(self):
        before = copy.deepcopy(self.packet)
        page = catalog_page(self.packet, self.records)
        self.assertEqual(page['candidates'][0], self.facts['b'])
        self.assertEqual(self.packet, before)
        self.assertEqual(page['evidence_status'], 'discovery_only_fetch_full_citations')

    def test_byte_boundary_does_not_skip_the_next_candidate(self):
        size = len(json.dumps([self.facts['b']], ensure_ascii=False).encode())
        page = catalog_page(self.packet, self.records, byte_budget=size)
        self.assertEqual([f['id'] for f in page['candidates']], ['b'])
        self.assertEqual(page['next_offset'], 1)
        self.assertLessEqual(page['candidate_bytes'], size)

    def test_oversized_single_record_fails_instead_of_clipping_or_looping(self):
        with self.assertRaisesRegex(ValueError, 'complete candidate'):
            catalog_page(self.packet, self.records, byte_budget=2)

    def test_invalid_pagination_rejected(self):
        for kwargs in [dict(offset=-1), dict(offset=True), dict(limit=0), dict(limit=33), dict(byte_budget=24001)]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                catalog_page(self.packet, self.records, **kwargs)

    def test_scope_or_repair_feedback_does_not_read_records(self):
        packet = dict(status='unsupported_scope', next_action={'type':'stop'})
        self.assertEqual(catalog_page(packet, self.records), packet)
        self.assertEqual(self.reads, [])


if __name__ == '__main__': unittest.main()
