"""Optional exact-span hints around the unchanged foundation plan."""
import copy
import math
from pathlib import Path
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agent_contract.qualification_v3.candidate import build_plan


def map_hints(raw, question_index):
    if not isinstance(raw, dict) or set(raw) != {'entities'} or not isinstance(raw['entities'], dict):
        raise ValueError('malformed native envelope')
    hints = []
    for role, mentions in raw['entities'].items():
        if not isinstance(mentions, list):
            raise ValueError('malformed native mentions')
        for mention in mentions:
            if not isinstance(mention, dict) or not {'start', 'end', 'text'} <= set(mention):
                raise ValueError('malformed native mention')
            hints.append(dict(question_index=question_index, start=mention['start'],
                              end=mention['end'], text=mention['text'], role=role))
    return hints


def integrate(request, value, extract=None):
    """Fail open for optional extraction, never for an invalid core plan."""
    before = copy.deepcopy(value)
    started = time.perf_counter()
    baseline = build_plan(request, value)
    baseline_seconds = time.perf_counter() - started
    hints, extractions = [], []
    if extract is not None:
        for index, question in enumerate(value['formly_questions']):
            row = dict(question_index=index, text=question['question'], raw=None, error=None)
            started = time.perf_counter()
            try:
                row['raw'] = extract(question['question'])
            except Exception as error:
                row['error'] = type(error).__name__ + ': ' + str(error)
            row['seconds'] = time.perf_counter() - started
            if row['error'] is None:
                try:
                    hints.extend(map_hints(row['raw'], index))
                except (TypeError, ValueError, KeyError) as error:
                    row['error'] = type(error).__name__ + ': ' + str(error)
            extractions.append(row)
    started = time.perf_counter()
    plan = build_plan(request, value, hints) if extract is not None else baseline
    projection_seconds = time.perf_counter() - started if extract is not None else baseline_seconds
    if value != before or plan['question_plan'] != baseline['question_plan'] or plan['search_requests'] != baseline['search_requests']:
        raise AssertionError('core plan or input changed')
    return dict(plan=plan, extractions=extractions, projection_seconds=projection_seconds,
                extraction_seconds=sum(r['seconds'] for r in extractions))


def score_sets(gold, predicted):
    tp, fp, fn = len(gold & predicted), len(predicted - gold), len(gold - predicted)
    return dict(tp=tp, fp=fp, fn=fn,
                precision=tp / (tp + fp) if tp + fp else None,
                recall=tp / (tp + fn) if tp + fn else None,
                f1=2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None)


def summarize_times(values):
    ordered = sorted(values)
    if not ordered:
        return dict(count=0, total=0, p50=None, p95=None, maximum=None)
    return dict(count=len(values), total=sum(values), p50=ordered[math.ceil(len(values)*.5)-1],
                p95=ordered[math.ceil(len(values)*.95)-1], maximum=ordered[-1])
