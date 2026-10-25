"""Promoted source-spelling adapter; strict validator remains unchanged."""
import copy
import re
import sys
from pathlib import Path
POC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(POC))
from wording_candidate_v1.candidate import normalize as accepted_normalize


def normalize(request, core):
    # Preserve the accepted behavior first, including its narrow voice rewrite.
    try:
        return accepted_normalize(request, core)
    except ValueError:
        pass
    canonical = copy.deepcopy(core)
    rewrites = []
    if isinstance(request, str) and isinstance(canonical, dict):
        bindings = canonical.get('condition_bindings')
        questions = canonical.get('formly_questions')
        if isinstance(bindings, list) and isinstance(questions, list):
            for binding in bindings:
                if not isinstance(binding, dict):
                    continue
                old = binding.get('condition')
                indexes = binding.get('question_indexes')
                if not isinstance(old, str) or old in request or not re.match(r'^(?:a|an|the) [A-Za-z]', old):
                    continue
                exact = old[0].upper() + old[1:]
                # Only the opening article of the entire request. Do not search
                # quoted strings, API spellings, or arbitrary case-folded spans.
                if not request.startswith(exact) or request.count(exact) != 1 or not boundary(request, len(exact)):
                    continue
                if not isinstance(indexes, list) or not indexes or any(type(i) is not int or not 0 <= i < len(questions) for i in indexes):
                    continue
                updates = []
                for index in indexes:
                    question = questions[index]
                    if not isinstance(question, dict) or not isinstance(question.get('question'), str):
                        break
                    text = question['question']
                    matches = list(re.finditer(re.escape(old), text))
                    if len(matches) != 1:
                        break
                    match = matches[0]
                    if (match.start() and (text[match.start()-1].isalnum() or text[match.start()-1] in '_.$')) or not boundary(text, match.end()) or inside_literal(text, match.start()):
                        break
                    updates.append((index, text[:match.start()] + exact + text[match.end():]))
                else:
                    binding['condition'] = exact
                    for index, text in updates:
                        questions[index]['question'] = text
                    rewrites.append({'rule': 'source-initial-article-case', 'before': old, 'after': exact,
                                     'source_start': 0, 'source_end': len(exact), 'question_indexes': list(indexes)})
    # All schema, exact-source, binding and missing-condition checks still run.
    fixed, prior = accepted_normalize(request, canonical)
    return fixed, {'policy': 'source-initial-article-case-v1', 'original_plan': copy.deepcopy(core),
                   'rewrites': rewrites + prior['rewrites']}


def boundary(text, end):
    if end == len(text):
        return True
    char = text[end]
    if char.isalnum() or char in '_$':
        return False
    # Do not treat a dotted API path suffix as sentence punctuation.
    return not (char == '.' and end+1 < len(text) and (text[end+1].isalnum() or text[end+1] in '_$'))


def inside_literal(text, position):
    """Plain single-line prose only; reject code/markup rather than parse it."""
    if any(marker in text for marker in ('`', '~~~', '\n', '\r', '<', '>')):
        return True
    pairs = {'"': '"', "'": "'", '“': '”', '‘': '’'}
    closing = None
    escaped = False
    for index, char in enumerate(text[:position]):
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        # Apostrophes in ordinary contractions are not quotation delimiters.
        if char in ("'", '’') and index and index+1 < len(text) and text[index-1].isalnum() and text[index+1].isalnum():
            continue
        if closing is not None:
            if char == closing:
                closing = None
        elif char in pairs:
            closing = pairs[char]
    return closing is not None


class CapitalizingPlanner:
    def __init__(self, planner):
        self.planner = planner

    def __call__(self, request):
        core, generation = self.planner(request)
        fixed, audit = normalize(request, core)
        return fixed, dict(generation, wording_normalization=audit)
