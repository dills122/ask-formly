"""Replay only the standalone library decoder. No model loading or inference."""
import json
from pathlib import Path
from gliner2.inference.overlap import resolve_overlaps

HERE = Path(__file__).resolve().parent


def verify():
    for name,key in [('decoder-control.json','score'),('decoder-observed-union.json','confidence')]:
        data=json.loads((HERE/'evidence'/name).read_text())
        results={str(t):resolve_overlaps([x for x in data['candidates'] if x[key]>=t],
                    policy='flat',score=lambda x:x[key],start=lambda x:x['start'],end=lambda x:x['end'])
                 for t in [.5,.2]}
        assert results==data['results'], name
        if 'matches_observed' in data:
            samples=[json.loads(s) for s in (HERE/'evidence/phase1-raw.jsonl').read_text().splitlines()]
            selected=[r for r in samples if r['case_id']=='D02' and r['variant'] in ['E0','E3']]
            matches={r['variant']:results[str(.5 if r['variant']=='E0' else .2)]==
                     r['native']['entities']['requested_outcome'] for r in selected}
            assert matches==data['matches_observed'] and all(matches.values())
    return 'Both decoder artifacts reproduced; no model inference'


if __name__=='__main__':
    print(verify())
