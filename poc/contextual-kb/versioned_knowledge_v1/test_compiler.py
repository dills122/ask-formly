import sys
from pathlib import Path
POC=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(POC),str(POC/'mcp_v1')]
"""Synthetic provenance, applicability and migration contracts."""
import copy
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from versioned_knowledge_v1.compiler import migrate, build


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.old = self.root/'old'; self.old.mkdir()
        self.new = self.root/'new'
        self.catalog = self.root/'catalog.json'
        self.catalog.write_text(json.dumps({'baseline':'6.3.12','records':[{'id':'K01'}]}))
        quote = 'A scoped claim [K01](sources.md#k01).'
        (self.root/'source.md').write_text(quote)
        self.doc = dict(schema_version=1,id='sample',title='Sample',formly_version='6.3.12',adapter='core',summary='Example',derived_from={'path':'source.md','sha256':hashlib.sha256(quote.encode()).hexdigest()},facts=[dict(id='one',claim='A scoped claim',conditions=['Only when enabled'],limits=['No app guarantee'],context='Example scope',source_quote=quote,evidence_ids=['K01'],related=[])])
        (self.old/'sample.json').write_text(json.dumps(self.doc))
        migrate(self.old,self.root,self.catalog,self.new)
        self.path=self.new/'authored/sample.json'
        self.cat=self.new/'catalog.json'
        self.db=self.root/'candidate.sqlite'

    def edit(self, fn):
        doc=json.loads(self.path.read_text()); fn(doc); self.path.write_text(json.dumps(doc))

    def compile(self):
        build(self.new/'authored',self.root,self.cat,self.db)

    def test_exact_migration_preserves_content_and_rejects_repeat(self):
        doc=json.loads(self.path.read_text())
        fact=doc['facts'][0]; old=self.doc['facts'][0]
        self.assertEqual(old,{k:fact[k] for k in old})
        self.assertEqual([{'scope':{'kind':'exact','value':'6.3.12'},'basis':'direct','evidence_ids':['K01']}],fact['applicability'])
        with self.assertRaises((ValueError,FileExistsError)):
            migrate(self.old,self.root,self.catalog,self.new)
        with self.assertRaises(ValueError):
            migrate(self.new/'authored',self.root,self.cat,self.root/'again')

    def test_build_preserves_provenance_and_indexes_shared_fact_once(self):
        self.edit(lambda d:d['facts'][0].update(applicability=[{'scope':{'kind':'major','value':'6'},'basis':'direct','evidence_ids':['K01']},{'scope':{'kind':'major','value':'7'},'basis':'inferred','reason':'Synthetic reviewed comparison','evidence_ids':['K01']}]))
        self.compile()
        with sqlite3.connect(self.db) as db:
            self.assertEqual(2,db.execute('select schema_version from build_info').fetchone()[0])
            self.assertEqual(1,db.execute('select count(*) from facts_fts').fetchone()[0])
            self.assertEqual(2,db.execute('select count(*) from applicability').fetchone()[0])
            self.assertEqual([('K01','6.3.12')],db.execute('select * from evidence_releases').fetchall())
            self.assertEqual([],db.execute('pragma foreign_key_check').fetchall())

    def test_validation_rejects_bad_scopes_support_and_links(self):
        original=self.path.read_text()
        invalid=[
            lambda d:d.update(schema_version=99),
            lambda d:d['facts'][0].update(applicability=[]),
            lambda d:d['facts'][0]['applicability'][0]['scope'].update(kind='range'),
            lambda d:d['facts'][0]['applicability'][0]['scope'].update(value='6.03.12'),
            lambda d:d['facts'][0]['applicability'][0].update(basis='guess'),
            lambda d:d['facts'][0]['applicability'][0].update(basis='inferred'),
            lambda d:d['facts'][0]['applicability'][0].update(evidence_ids=['K99']),
            lambda d:d['facts'][0]['applicability'][0].update(evidence_ids=[]),
            lambda d:d['facts'][0]['applicability'][0]['scope'].update(value='7.0.0'),
            lambda d:d['facts'][0]['applicability'].append(copy.deepcopy(d['facts'][0]['applicability'][0])),
            lambda d:d['facts'][0].update(related=[{'kind':'replaces','target':'sample/one'}]),
            lambda d:d['facts'][0].update(source_quote='Invented quote'),
            lambda d:d['facts'][0]['applicability'][0].update(typo='ignored'),
        ]
        for change in invalid:
            with self.subTest(change=invalid.index(change)):
                self.path.write_text(original); self.edit(change)
                with self.assertRaises(ValueError):self.compile()
                self.assertFalse(self.db.exists())

    def test_replacements_validate_cycles_and_overlapping_scope(self):
        def add(d):
            second=copy.deepcopy(d['facts'][0]);second['id']='two'
            second['applicability']=[{'scope':{'kind':'exact','value':'7.0.0'},'basis':'inferred','reason':'Synthetic difference','evidence_ids':['K01']}]
            second['related']=[{'kind':'replaces','target':'sample/one'}]
            d['facts'].append(second)
        self.edit(add);self.compile()
        self.db.unlink()
        self.edit(lambda d:d['facts'][0].update(related=[{'kind':'replaces','target':'sample/two'}]))
        with self.assertRaises(ValueError):self.compile()
        self.edit(lambda d:d['facts'][0].update(related=[]))
        self.edit(lambda d:d['facts'][1].update(applicability=d['facts'][0]['applicability']))
        with self.assertRaises(ValueError):self.compile()

    def test_replacement_chains_reject_overlapping_ancestors(self):
        def chain(d):
            old=d['facts'][0]
            middle=copy.deepcopy(old);middle['id']='two'
            middle['applicability']=[{'scope':{'kind':'major','value':'7'},'basis':'inferred','reason':'Synthetic changed behavior','evidence_ids':['K01']}]
            middle['related']=[{'kind':'replaces','target':'sample/one'}]
            latest=copy.deepcopy(old);latest['id']='three'
            latest['applicability']=[{'scope':{'kind':'major','value':'6'},'basis':'direct','evidence_ids':['K01']}]
            latest['related']=[{'kind':'replaces','target':'sample/two'}]
            d['facts'] += [middle,latest]
        self.edit(chain)
        with self.assertRaisesRegex(ValueError,'overlap'):self.compile()
        self.assertFalse(self.db.exists())

    def test_build_is_deterministic_and_never_overwrites(self):
        self.compile(); before=self.db.read_bytes()
        with self.assertRaises(FileExistsError):self.compile()
        self.assertEqual(before,self.db.read_bytes())
        other=self.root/'other.sqlite';build(self.new/'authored',self.root,self.cat,other)
        self.assertEqual(before,other.read_bytes())

    def test_catalog_preserves_source_input_provenance(self):
        c=json.loads(self.cat.read_text())
        c['source_inputs']={'upstream_path':'source.md','upstream_sha256':self.doc['derived_from']['sha256'],'examples_path':'source.md','examples_sha256':self.doc['derived_from']['sha256']}
        self.cat.write_text(json.dumps(c));self.compile()
        self.db.unlink()
        c['source_inputs']['upstream_sha256']='0'*64
        self.cat.write_text(json.dumps(c))
        with self.assertRaises(ValueError):self.compile()

    def test_catalog_release_metadata_is_required_and_validated(self):
        c=json.loads(self.cat.read_text()); c['evidence_releases']['K01']='latest'
        self.cat.write_text(json.dumps(c))
        with self.assertRaises(ValueError):self.compile()


if __name__=='__main__':unittest.main()
