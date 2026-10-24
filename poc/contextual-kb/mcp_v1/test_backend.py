import json,sqlite3,unittest
from backend import citations_for
class CitationTests(unittest.TestCase):
    def test_only_selected_ids_keep_original_provenance(self):
        db=sqlite3.connect(':memory:')
        db.executescript('''create table facts(id text,doc_id text,source_quote text,source_start_offset int,source_end_offset int,status text);
create table documents(id text,source_path text,source_sha256 text);
create table fact_evidence(fact_id text,evidence_id text);
create table evidence(id text,record_json text);
insert into facts values('f1','d','quote',1,6,'reviewed');
insert into facts values('f2','d','other',7,12,'reviewed');
insert into documents values('d','path','hash');
insert into fact_evidence values('f1','e');
''')
        record={'id':'e','source_path':'pinned.ts','source_start_line':9,'source_end_line':12,'source_sha256':'sourcehash'}
        db.execute('insert into evidence values(?,?)',('e',json.dumps(record)))
        value=citations_for(db,['f1'])
        self.assertEqual(set(value),{'f1'});self.assertEqual(value['f1']['evidence'],[record])
        self.assertEqual(value['f1']['authored_source']['quote'],'quote')
        self.assertEqual(citations_for(db,[]),{})
if __name__=='__main__':unittest.main()
