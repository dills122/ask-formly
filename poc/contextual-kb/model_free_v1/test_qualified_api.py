"""Qualified API discovery supplements must not replace ranked evidence."""
import sqlite3
import unittest
from test_candidate import fixture
from candidate import Store, digest

class QualifiedApiTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'db.sqlite';fixture(self.path)
        db=sqlite3.connect(self.path)
        rows=[('api','topic','ExampleSchema exposes toFieldConfig(schema).','core'),
              ('detail','topic','A map callback returns the converted result.','core'),
              ('other','elsewhere','Unrelated callback ordering.','core'),
              ('material-detail','topic','Renderer configuration.','material')]
        for fid,doc,claim,adapter in rows:
            # Separate documents for adapter filtering; doc siblings below share topic.
            if fid in ('api','other'):
                db.execute('INSERT INTO documents VALUES(?,?,?,?,?,?)',(doc,doc,'6.3.12',adapter,'fixture','hash'))
            db.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?,?,?,?)',(fid,doc,claim,'','[]','[]',claim,0,len(claim),'authored'))
            db.execute('INSERT INTO applicability VALUES(?,?,?,?,?)',(fid,'exact','6.3.12','direct',None))
            db.execute('INSERT INTO facts_fts VALUES(?,?,?,?,?,?,?)',(fid,claim,'','','',doc,''))
        # A different release in the same document must never leak through expansion.
        db.execute("UPDATE applicability SET value='7.0.0' WHERE fact_id='material-detail'")
        db.commit();db.close()
        self.store=Store(self.path,digest(self.path));self.addCleanup(self.store.close)
    def test_qualified_api_exposes_eligible_document_context(self):
        ids=self.store.search('ExampleSchema.toFieldConfig','6.3.12','core')
        self.assertIn('api',ids);self.assertIn('detail',ids)
        self.assertNotIn('other',ids);self.assertNotIn('material-detail',ids)
    def test_unknown_owner_and_lowercase_property_do_not_expand(self):
        for query in ('UnknownSchema.toFieldConfig','exampleSchema.toFieldConfig','props.label'):
            self.assertNotIn('detail',self.store.search(query,'6.3.12',None))
    def test_existing_ranking_prefix_is_preserved(self):
        baseline=self.store.search('alpha','6.3.12',None)
        expanded=self.store.search('alpha ExampleSchema.toFieldConfig','6.3.12',None)
        self.assertEqual(baseline,expanded[:len(baseline)])
        self.assertIn('detail',expanded)
    def test_supplement_is_capped_without_modifying_database(self):
        self.store.close()
        db=sqlite3.connect(self.path)
        for i in range(30):
            fid=f'extra{i:02}'
            db.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?,?,?,?)',(fid,'topic','Additional context','','[]','[]','quote',0,5,'authored'))
            db.execute('INSERT INTO applicability VALUES(?,?,?,?,?)',(fid,'exact','6.3.12','direct',None))
        db.commit();db.close()
        before=digest(self.path)
        self.store=Store(self.path,before);self.addCleanup(self.store.close)
        ids=self.store.search('ExampleSchema.toFieldConfig','6.3.12','core')
        self.assertEqual(16,len(ids));self.assertEqual(before,digest(self.path))

    def test_document_limit_and_adapter_filter_apply_to_anchors(self):
        self.store.close()
        db=sqlite3.connect(self.path)
        for i in range(6):
            doc=f'doc{i}';fid=f'anchor{i}';adapter='material' if i==0 else 'core'
            db.execute('INSERT INTO documents VALUES(?,?,?,?,?,?)',(doc,doc,'6.3.12',adapter,'fixture','hash'))
            claim='ExampleSchema exposes toFieldConfig.'
            db.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?,?,?,?)',(fid,doc,claim,'','[]','[]',claim,0,len(claim),'authored'))
            db.execute('INSERT INTO applicability VALUES(?,?,?,?,?)',(fid,'exact','6.3.12','direct',None))
            db.execute('INSERT INTO facts_fts VALUES(?,?,?,?,?,?,?)',(fid,claim,'','','',doc,''))
        db.commit();db.close()
        self.store=Store(self.path,digest(self.path));self.addCleanup(self.store.close)
        ids=self.store.search('ExampleSchema.toFieldConfig','6.3.12','core')
        self.assertNotIn('anchor0',ids)
        self.assertEqual(4,len({self.store.document_ids[fid] for fid in ids}))

    def test_basic_comparison_route_remains_unexpanded(self):
        self.assertNotIn('detail',self.store.search('ExampleSchema.toFieldConfig','6.3.12',None,'basic'))

if __name__=='__main__':unittest.main()
