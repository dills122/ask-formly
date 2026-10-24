"""A fixed, gold-blind six-slot reservation around existing POC policies."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from kbcompiler.question_pilot import reciprocal_rank_fusion,merge_obligations

def combine(full_lists,extra_lists):
    if len(full_lists)!=len(extra_lists):raise ValueError('question list count mismatch')
    foundation=merge_obligations(full_lists,8)
    fused=[reciprocal_rank_fusion([full,extra])[:8] if extra is not None else full for full,extra in zip(full_lists,extra_lists)]
    current=merge_obligations(fused,8)
    if all(extra is None for extra in extra_lists):protected=list(foundation)
    else:
        protected=foundation[:6]
        for fact in current+foundation:
            if len(protected)==8:break
            if fact not in protected:protected.append(fact)
    return dict(foundation=foundation,current=current,protected=protected)
