"""A bounded grammatical rewrite, followed by the unchanged strict validator."""
import copy
import re
import sys
from pathlib import Path

POC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(POC))
from agent_contract.qualification_v3.candidate import build_plan

# Whole-question grammar, not a substring/token-similarity matcher. Identifiers
# remain case-sensitive and cannot contain operators, values, or extra clauses.
PATH = r'[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+'
CONFIGURATION = re.compile(
    rf'In Formly, how can (?P<target>{PATH}) be configured to track (?P<controller>{PATH})\?'
)


def normalize(request, core):
    """Return a detached strict-valid plan and provenance, or reject atomically.

    The grammar changes voice only. It neither infers missing ledger entries nor
    repairs arbitrary paraphrases. All remaining invariants use frozen code.
    """
    canonical = copy.deepcopy(core)
    audit = {'policy': 'configuration-voice-v1', 'original_plan': copy.deepcopy(core), 'rewrites': []}
    try:
        build_plan(request, canonical)
        return canonical, audit
    except ValueError:
        pass

    # Defensive traversal only; frozen validation below owns schema errors.
    if isinstance(canonical, dict):
        questions = canonical.get('formly_questions')
        bindings = canonical.get('condition_bindings')
        if isinstance(questions, list) and isinstance(bindings, list):
            for index, question in enumerate(questions):
                if not isinstance(question, dict) or not isinstance(question.get('question'), str):
                    continue
                before = question['question']
                match = CONFIGURATION.fullmatch(before)
                if match is None:
                    continue
                condition = f"{match['target']} to track {match['controller']}"
                applicable = any(
                    isinstance(binding, dict)
                    and binding.get('condition') == condition
                    and isinstance(binding.get('question_indexes'), list)
                    and index in binding['question_indexes']
                    for binding in bindings
                )
                if not applicable or not isinstance(request, str) or condition not in request:
                    continue
                after = f'In Formly, how can I configure {condition}?'
                question['question'] = after
                audit['rewrites'].append({'rule': 'configuration-voice-v1', 'question_index': index,
                                          'condition': condition, 'before': before, 'after': after})
    # Never accept a plan solely because the rewrite matched. This also rejects
    # other missing conditions on this or any other question, malformed bindings,
    # invalid indices, ungrounded excerpts, duplicate entries, and extra fields.
    build_plan(request, canonical)
    return canonical, audit


class NormalizingPlanner:
    """Opt-in adapter; original planner persists its raw output as usual."""
    def __init__(self, planner):
        self.planner = planner

    def __call__(self, request):
        core, generation = self.planner(request)
        canonical, audit = normalize(request, core)
        return canonical, dict(generation, wording_normalization=audit)
