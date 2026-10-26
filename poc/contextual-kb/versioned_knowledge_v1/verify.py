"""Read-only preservation/rollback check plus disposable post-fix rebuild."""
import json
import os
import tempfile
from pathlib import Path
from versioned_knowledge_v1.qualify import POC,ROOT,connect,rows,TABLES,QUERIES,preserved
from versioned_knowledge_v1.compiler import build
from kbcompiler.question_pilot import PilotIndex


def run(output):
    baseline=json.loads((output/'baseline.json').read_text())
    result={'preservation':preserved(baseline)}
    with tempfile.TemporaryDirectory(dir=output) as tmp:
        rebuilt=Path(tmp)/'candidate.sqlite'
        build(output/'migrated/authored',ROOT,output/'migrated/catalog.json',rebuilt)
        result['post_fix_rebuild_identical']=rebuilt.read_bytes()==(output/'candidate.sqlite').read_bytes()
        assert result['post_fix_rebuild_identical']
        # Rehearse old-reader compatibility on an isolated restored snapshot.
        restored=Path(tmp)/'restored.sqlite';restored.write_bytes((output/'rollback.sqlite').read_bytes())
        old=connect(POC/'build/knowledge.sqlite');rollback=connect(restored)
        try:
            assert all(rows(old,t)==rows(rollback,t) for t in TABLES)
            os.environ.update(FORMLY_PILOT_EMBED_CACHE=str(POC/'agent_contract/advisory_lookup_v1/test-output/embed-cache'),HF_HUB_OFFLINE='1')
            index=PilotIndex(rollback)
            comparisons=json.loads((output/'comparison.json').read_text())['comparisons']
            for case in comparisons[:len(QUERIES)]:
                assert index.hybrid(case['query'],8)==case['rankings']['hybrid_8']
            result['rollback_legacy_reader_queries']=len(QUERIES)
        finally:old.close();rollback.close()
    result['preservation']=preserved(baseline)
    (output/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run(Path(__file__).resolve().parent/'test-output')
