import copy
import json
from pathlib import Path
import tempfile
import sqlite3
import unittest

from ledger import inventory, validate, render


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'guide.md').write_text('Intro\n# Guide\n\nText.\n```md\n## Not a section\n```\n## Other\nOther fact.\n')
        self.manifest = self.root/'manifest.json'
        self.manifest.write_text(json.dumps({'schema_version':1,'documents':[{'id':'guide','source':'guide.md'}]}))
        self.authored = self.root/'authored'; self.authored.mkdir()
        (self.authored/'facts.json').write_text(json.dumps({'id':'doc','facts':[{'id':'fact'}]}))
        self.ledger = inventory(self.root, self.manifest)

    def decide(self):
        for section in self.ledger['documents'][0]['sections']:
            section.update(status='existing_support', rationale='Entire section reviewed; no additional claims.', fact_ids=['doc/fact'], review='Reviewer unit fixture')
            section['decisions'] = [dict(id='claim', scope='Whole section', quote=section['heading'] if section['heading'] != '(preamble)' else 'Intro', status='existing_support', rationale='Supported by existing record.', fact_ids=['doc/fact'], review='Reviewer unit fixture')]

    def check(self, **kw):
        return validate(self.ledger, self.root, self.manifest, [self.authored], **kw)

    def test_inventory_accounts_preamble_and_ignores_fenced_headings(self):
        sections=self.ledger['documents'][0]['sections']
        self.assertEqual([s['heading'] for s in sections], ['(preamble)','Guide','Other'])
        self.assertEqual([s['start_line'] for s in sections], [1,2,8])
        self.assertEqual(self.check(), [])
        self.assertIn('pending', '\n'.join(self.check(require_complete=True)))

    def test_decided_ledger_completes_and_report_has_claim_dispositions(self):
        self.decide()
        self.assertEqual(self.check(require_complete=True), [])
        report=render(self.ledger)
        self.assertIn('doc/fact',report)
        self.assertIn('Whole section',report)
        self.assertIn('3',report)

    def test_source_drift_rejected(self):
        (self.root/'guide.md').write_text('Changed source')
        self.assertIn('source', '\n'.join(self.check()).lower())

    def test_missing_duplicate_or_forged_section_rejected(self):
        sections=self.ledger['documents'][0]['sections']
        original=copy.deepcopy(sections)
        sections.pop()
        self.assertTrue(self.check())
        sections[:]=original+[copy.deepcopy(original[0])]
        self.assertTrue(self.check())
        sections[:]=copy.deepcopy(original)
        sections[1]['end_offset']-=1
        self.assertTrue(self.check())

    def test_missing_fact_and_no_fact_for_supported_decision_rejected(self):
        self.decide()
        decision=self.ledger['documents'][0]['sections'][0]['decisions'][0]
        decision['fact_ids']=['missing/fact']
        self.assertIn('unknown fact', '\n'.join(self.check()))
        decision['fact_ids']=[]
        self.assertIn('fact_ids', '\n'.join(self.check()))

    def test_quote_outside_section_rejected(self):
        self.decide()
        self.ledger['documents'][0]['sections'][0]['decisions'][0]['quote']='Other fact.'
        self.assertIn('quote', '\n'.join(self.check()))

    def test_review_required_and_partial_section_cannot_be_complete(self):
        self.decide()
        section=self.ledger['documents'][0]['sections'][0]
        section['review']=''
        self.assertIn('review', '\n'.join(self.check()))
        section['review']='Reviewed'
        section['decisions'][0]['status']='pending'
        self.assertIn('aggregate', '\n'.join(self.check()))

    def test_source_escape_and_manifest_drift_rejected(self):
        self.ledger['documents'][0]['source']='../outside.md'
        self.assertTrue(self.check())
        self.ledger=inventory(self.root,self.manifest)
        self.manifest.write_text(self.manifest.read_text()+'\n')
        self.assertIn('manifest', '\n'.join(self.check()))

    def test_duplicate_fact_ids_across_inputs_rejected(self):
        (self.authored/'duplicate.json').write_text((self.authored/'facts.json').read_text())
        self.assertIn('duplicate fact', '\n'.join(self.check()))

    def test_duplicate_decisions_are_rejected(self):
        self.decide()
        decisions=self.ledger['documents'][0]['sections'][0]['decisions']
        decisions.append(copy.deepcopy(decisions[0]))
        self.assertIn('duplicate decision', '\n'.join(self.check()))

    def test_partial_section_stays_pending_while_other_decisions_are_excluded(self):
        self.decide()
        section=self.ledger['documents'][0]['sections'][0]
        decision=section['decisions'][0]
        decision.update(status='excluded',fact_ids=[],rationale='Non-library guidance.')
        section['decisions'].append(dict(id='unresolved',scope='Unresolved part',quote='Intro',status='pending',fact_ids=[],review='',rationale='Needs source review.'))
        section.update(status='pending',fact_ids=[])
        self.assertEqual(self.check(), [])
        self.assertIn('pending','\n'.join(self.check(require_complete=True)))

    def test_seeded_fact_check_is_read_only_and_rejects_missing_ids(self):
        self.decide()
        database=self.root/'candidate.sqlite'
        with sqlite3.connect(database) as db:
            db.execute('CREATE TABLE facts (id TEXT PRIMARY KEY)')
            db.execute("INSERT INTO facts VALUES ('doc/fact')")
        before=database.read_bytes()
        self.assertEqual(self.check(database=database), [])
        self.assertEqual(database.read_bytes(), before)
        with sqlite3.connect(database) as db:
            db.execute('DELETE FROM facts')
        self.assertIn('not seeded','\n'.join(self.check(database=database)))

    def test_excluded_decision_requires_reason_and_no_fact(self):
        self.decide()
        section=self.ledger['documents'][0]['sections'][0]
        decision=section['decisions'][0]
        decision.update(status='excluded',rationale='',fact_ids=[])
        section.update(status='excluded',fact_ids=[])
        self.assertIn('rationale','\n'.join(self.check()))

if __name__=='__main__': unittest.main()
