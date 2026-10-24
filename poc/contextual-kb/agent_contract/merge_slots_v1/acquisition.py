"""Collect identical query rankings once for the three combination policies."""
import sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent_contract.context_queries_v1.candidate import retrieve
from policy import combine

def acquire(index,core,supplements):
    trace=retrieve(index,core,supplements)
    full=[q['ids'] for q in trace['queries'] if q['kind']=='full']
    extra={q['question_index']:q['ids'] for q in trace['queries'] if q['kind']=='context'}
    started=time.perf_counter();packets=combine(full,[extra.get(i) for i in range(len(full))]);combine_seconds=time.perf_counter()-started
    if packets['current']!=trace['ids']:raise AssertionError('current policy differs from frozen contextual candidate')
    return dict(queries=trace['queries'],query_count=trace['query_count'],query_characters=trace['query_characters'],acquisition_seconds=trace['seconds'],
                combination_seconds=combine_seconds,supplement_error=trace['supplement_error'],packets=packets)
