import asyncio
import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

from candidate import Service, Store, digest
from model_free_v1.response import MAX_RESPONSE_BYTES, MAX_TRANSPORT_BYTES, encoded_size, evidence_packet, make_tool_result, fits_packet
from test_candidate import fixture, plan


class FakeStore:
    """Synthetic retrieval order; no installed knowledge or database."""
    def __init__(self, count=40):
        self.facts = {str(i): dict(id=str(i), claim='claim '+str(i), context='fixture',
            conditions=['Only under the stated fixture condition.'],
            limits=['No universal behavior is established.'], related=[],
            applicability=[dict(scope=dict(kind='exact', value='6.3.12'))]) for i in range(count)}
        self.order = list(self.facts)
        self.quote = 'Shared complete source paragraph.'

    def verify(self):
        pass

    def search(self, question, *args):
        return self.order if question != 'beta' else self.order[::-1]

    def records(self, ids, *args):
        return ([copy.deepcopy(self.facts[fid]) for fid in ids],
            {fid: dict(authored_source=dict(path='fixture.md',sha256='abc',quote=self.quote,
                start_offset=0,end_offset=len(self.quote),status='authored'),
                evidence=[dict(id='K1', path='fixture.ts', quote='complete evidence')],
                applicability=self.facts[fid]['applicability']) for fid in ids})


class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.store=FakeStore()
        self.service=Service(self.store,Path(self.temp.name)/'settings.sqlite')

    def tearDown(self):
        self.temp.cleanup()

    def lookup(self, *args, **kwargs):
        return asyncio.run(self.service.lookup(*args,**kwargs))

    def test_selection_considers_more_than_four_candidates(self):
        result=self.lookup('alpha',max_facts=8)
        self.assertEqual(8,len(result['facts']))
        self.assertEqual(1,len(result['sources']))
        self.assertEqual(1,len(result['evidence']))
        self.assertLessEqual(encoded_size(result),MAX_RESPONSE_BYTES)
        self.assertEqual(encoded_size(result),result['response']['bytes'])
        sdk=make_tool_result(result)
        self.assertIsNone(sdk.structuredContent)
        self.assertEqual(result,json.loads(sdk.content[0].text))
        self.assertLessEqual(encoded_size(sdk.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
        self.assertEqual(encoded_size(sdk.model_dump(mode='json')),result['response']['transport_bytes'])

    def test_compact_provenance_round_trips_without_losing_constraints(self):
        facts,citations=self.store.records(['1','2'])
        packet=evidence_packet(facts,citations)
        for fact in packet['facts']:
            ref=packet['citations'][fact['id']]
            self.assertEqual(citations[fact['id']]['authored_source'],packet['sources'][ref['authored_source_ref']])
            self.assertEqual(citations[fact['id']]['evidence'],[packet['evidence'][r] for r in ref['evidence_refs']])
            self.assertEqual(citations[fact['id']]['applicability'],fact['applicability'])
            self.assertEqual(self.store.facts[fact['id']]['conditions'],fact['conditions'])
            self.assertEqual(self.store.facts[fact['id']]['limits'],fact['limits'])

    def test_full_fetch_remains_explicitly_available(self):
        result=asyncio.run(self.service.get_facts(['1'],response_format='full'))
        self.assertEqual('full-v1',result['response_format'])
        self.assertEqual(self.store.quote,result['citations']['1']['authored_source']['quote'])
        with self.assertRaisesRegex(ValueError,'response_format'):
            asyncio.run(self.service.get_facts(['1'],response_format='invented'))

    def test_fairness_and_packet_relative_omissions(self):
        p=plan('alpha');p['formly_questions'].append(dict(question='beta',reason='Independent question'))
        result=self.lookup('Compare alpha and beta',plan=p,max_facts=2)
        self.assertEqual(['0','39'],[f['id'] for f in result['facts']])
        omitted=[row['id'] for row in result['omitted_candidates']]
        self.assertEqual(len(omitted),len(set(omitted)))
        self.assertFalse(set(omitted)&{'0','39'})
        for question in result['questions']:
            self.assertEqual(38,question['omitted_count'])
            self.assertEqual({'0','39'},set(question['fact_ids']))
            self.assertTrue(question['omitted_indexes'])
        self.assertTrue(result['omitted_preview_truncated'])
        self.assertEqual('get_formly_facts',result['next_action']['tool'])
        self.assertEqual('complete_evidence',result['record_kind'])
        self.assertTrue(result['truncated'])
        self.assertEqual({f['id'] for f in result['facts']},set(result['citations']))

    def test_large_unicode_request_does_not_exhaust_packet_budget(self):
        request='界'*10000
        result=self.lookup(request,plan=plan('alpha'))
        self.assertEqual('omitted_for_budget',result['request_echo'])
        self.assertEqual(10000,result['request_ref']['characters'])
        self.assertNotIn('request',result)
        self.assertLessEqual(encoded_size(result),MAX_RESPONSE_BYTES)
        self.assertTrue(result['facts'])

    def test_oversized_evidence_is_recoverable_not_clipped(self):
        self.store.quote='界'*15000
        result=self.lookup('alpha')
        self.assertEqual([],result['facts'])
        self.assertEqual('no_evidence',result['status'])
        self.assertTrue(result['omitted_candidates'])
        self.assertLessEqual(encoded_size(result),MAX_RESPONSE_BYTES)
        oversized=asyncio.run(self.service.get_facts(['0']))
        self.assertEqual('response_too_large',oversized['status'])
        self.assertEqual(['0'],oversized['unbatchable_fact_ids'])
        self.assertEqual([],oversized['retry_batches'])
        self.assertEqual([],oversized['facts'])

    def test_compact_oversize_returns_measured_retry_batches_without_partial_evidence(self):
        for i in range(6):
            self.store.facts[str(i)]['claim'] = ('quoted " \\ 界 '*600) + str(i)
        ids = ['0', '1', '2', '3', '4', '5']
        result = asyncio.run(self.service.get_facts(ids, '6.3.12', 'material'))
        self.assertEqual('batch_required', result['status'])
        self.assertEqual('batch_instructions', result['record_kind'])
        self.assertEqual('not_delivered', result['evidence_status'])
        self.assertEqual([], result['facts'])
        self.assertEqual([], result['unbatchable_fact_ids'])
        self.assertGreater(len(result['retry_batches']), 1)
        self.assertTrue(fits_packet(result))
        delivered = []
        for batch in result['retry_batches']:
            args = batch['arguments']
            self.assertEqual(('6.3.12', 'material', 'compact'),
                (args['formly_version'], args['ui_adapter'], args['response_format']))
            packet = asyncio.run(self.service.get_facts(**args))
            self.assertNotIn('status', packet)
            self.assertEqual('complete_evidence', packet['record_kind'])
            self.assertEqual(batch['response_bytes'], encoded_size(packet))
            self.assertEqual(batch['transport_bytes'], encoded_size(make_tool_result(packet).model_dump(mode='json')))
            for fact in packet['facts']:
                delivered.append(fact['id'])
                self.assertEqual(self.store.facts[fact['id']]['claim'], fact['claim'])
                self.assertEqual(self.store.facts[fact['id']]['limits'], fact['limits'])
                citation = packet['citations'][fact['id']]
                self.assertEqual(self.store.quote, packet['sources'][citation['authored_source_ref']]['quote'])
        self.assertEqual(ids, delivered)
        self.assertEqual(result, asyncio.run(self.service.get_facts(ids, '6.3.12', 'material')))

    def test_retry_sizes_use_resolved_arguments_not_original_default_context(self):
        for i in range(4):self.store.facts[str(i)]['claim']='large '*2400
        for scope in ({}, {'formly_version':'6', 'ui_adapter':'Material'}):
            result=asyncio.run(self.service.get_facts(['0','1','2','3'],**scope))
            self.assertEqual('batch_required',result['status'])
            for batch in result['retry_batches']:
                packet=asyncio.run(self.service.get_facts(**batch['arguments']))
                self.assertEqual(batch['response_bytes'],encoded_size(packet))
                self.assertEqual(batch['transport_bytes'],encoded_size(make_tool_result(packet).model_dump(mode='json')))

    def test_batch_retries_deduplicate_ids_and_preserve_order(self):
        self.store.facts['1']['claim'] = 'large '*2400
        self.store.facts['2']['claim'] = 'large '*2400
        self.store.facts['3']['claim'] = 'large '*2400
        result=asyncio.run(self.service.get_facts(['3','1','3','2','1']))
        self.assertEqual('batch_required',result['status'])
        self.assertEqual(['3','1','2'],[fid for b in result['retry_batches'] for fid in b['arguments']['fact_ids']])

    def test_unbatchable_fact_does_not_hide_other_retryable_ids(self):
        self.store.facts['1']['claim']='界'*15000
        result=asyncio.run(self.service.get_facts(['0','1','2']))
        self.assertEqual('response_too_large',result['status'])
        self.assertEqual(['1'],result['unbatchable_fact_ids'])
        self.assertEqual(['0','2'],[fid for b in result['retry_batches'] for fid in b['arguments']['fact_ids']])
        self.assertEqual([],result['facts'])
        self.assertTrue(fits_packet(result))

    def test_explicit_full_format_still_has_separate_nonlooping_limit(self):
        self.store.quote='x'*50000
        with self.assertRaisesRegex(ValueError,'single-record failure cannot be split'):
            asyncio.run(self.service.get_facts(['0'],response_format='full'))

    def test_does_not_fill_budget_with_smaller_lower_ranked_facts(self):
        self.store.facts['1']['claim']='large important claim '*3000
        result=self.lookup('alpha')
        self.assertEqual(['0'],[fact['id'] for fact in result['facts']])
        self.assertEqual('1',result['omitted_candidates'][0]['id'])
        self.assertLess(result['response']['bytes'],MAX_RESPONSE_BYTES)

    def test_complete_ranked_evidence_takes_space_before_omission_preview(self):
        self.store.quote='x'*22000
        result=self.lookup('alpha',max_facts=8)
        # Shared provenance remains complete; optional omitted-ID previews may
        # shrink so the next ranked evidence can fit. Discovery retains the tail.
        self.assertGreater(len(result['facts']),5)
        self.assertEqual([str(i) for i in range(len(result['facts']))],
                         [fact['id'] for fact in result['facts']])
        self.assertLess(len(result['omitted_candidates']),16)
        self.assertEqual(40-len(result['facts']),result['omitted_count'])
        self.assertEqual(self.store.quote,next(iter(result['sources'].values()))['quote'])
        self.assertTrue(result['omitted_preview_truncated'])
        self.assertLessEqual(result['response']['transport_bytes'],MAX_TRANSPORT_BYTES)

    def test_escaped_text_is_budgeted_against_actual_sdk_result(self):
        # This fits the inner packet but grows significantly when JSON text is
        # escaped inside CallToolResult. Do not mistake inner bytes for wire size.
        probe={'claim':'"\\'*4000}
        self.assertFalse(fits_packet(probe))
        self.assertLess(probe['response']['bytes'],MAX_RESPONSE_BYTES)
        self.assertGreater(probe['response']['transport_bytes'],MAX_TRANSPORT_BYTES)
        self.store.facts['0']['claim']='"\\'*4000
        packet=self.lookup('alpha')
        self.assertEqual([],packet['facts'])
        sdk=make_tool_result(packet)
        self.assertLessEqual(encoded_size(sdk.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
        self.assertEqual(packet,json.loads(sdk.content[0].text))

    def test_discovery_pages_full_order_not_lookup_preview(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'model_free_repair_v1'))
        from feedback import RepairService
        from parity_v1.discovery import discover
        p=plan('alpha')
        lookup=self.lookup('alpha',plan=p)
        self.assertGreater(lookup['omitted_count'],len(lookup['omitted_candidates']))
        first,error=asyncio.run(discover(RepairService(self.service),'alpha',p,limit=16))
        second,error=asyncio.run(discover(RepairService(self.service),'alpha',p,offset=first['next_offset'],limit=16))
        ids=[f['id'] for f in first['candidates']+second['candidates']]
        self.assertEqual([str(i) for i in range(16,40)],ids)
        self.assertIsNone(second['next_offset'])

    def test_discovery_shrinks_for_escaped_transport_without_skipping(self):
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'model_free_repair_v1'))
        from feedback import RepairService
        from parity_v1.discovery import discover
        for i in range(16,40):self.store.facts[str(i)]['claim']='"\\'*1600
        p=plan('alpha')
        first,_=asyncio.run(discover(RepairService(self.service),'alpha',p,limit=16))
        second,_=asyncio.run(discover(RepairService(self.service),'alpha',p,offset=first['next_offset'],limit=16))
        self.assertEqual(['16','17'],[f['id'] for f in first['candidates']])
        self.assertEqual('18',second['candidates'][0]['id'])
        for packet in (first,second):
            sdk=make_tool_result(packet)
            self.assertLessEqual(encoded_size(sdk.model_dump(mode='json')),MAX_TRANSPORT_BYTES)
            self.assertEqual(self.store.facts[packet['candidates'][0]['id']]['claim'],packet['candidates'][0]['claim'])


class StoredLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.path=Path(self.temp.name)/'fixture.sqlite'
        fixture(self.path)
        db=sqlite3.connect(self.path)
        db.executescript('CREATE TABLE fact_links(source_fact_id TEXT,target_fact_id TEXT,kind TEXT);')
        db.executemany('INSERT INTO fact_links VALUES(?,?,?)',[
            ('target','generic','see_also'),('target','material','see_also')])
        db.commit();db.close()
        self.store=Store(self.path,digest(self.path))

    def tearDown(self):
        self.store.close();self.temp.cleanup()

    def test_fetch_validates_all_ids_before_oversize_guidance(self):
        service=Service(self.store,Path(self.temp.name)/'settings.sqlite')
        self.store.facts['target']['claim']='large '*10000
        for ids in (['target','missing'], ['target','material']):
            with self.subTest(ids=ids), self.assertRaisesRegex(ValueError,'Unknown fact or fact outside requested scope'):
                asyncio.run(service.get_facts(ids,'6.3.12','core'))

    def test_links_and_expansion_are_scope_filtered(self):
        facts,_=self.store.records(['target'],'6.3.12','core')
        self.assertEqual([dict(kind='see_also',target='generic')],facts[0]['related'])
        self.assertIn('generic',self.store.candidates('resetOnHide','6.3.12','core'))
        self.assertNotIn('material',self.store.candidates('resetOnHide','6.3.12','core'))
        self.assertNotIn('generic',self.store.search('resetOnHide','6.3.12','core'))


if __name__=='__main__':unittest.main()
