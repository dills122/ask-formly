"""Arm A: dependency-tree coordination projection, with no Formly vocabulary.

Rules: separate top-level coordinated predicates/objects; retain common parse
context; keep comparison/disjunction groups intact; flag unresolved deixis.
This is deliberately a small general grammar, not a semantic guarantee.
"""
from time import perf_counter
from .contract import make_plan, failed, validate_question


def _render(doc, keep):
    """Copy original token runs; preserve code punctuation inside each run."""
    runs = []
    for token in doc:
        if token.i not in keep:
            continue
        if runs and token.i == runs[-1][1] + 1:
            runs[-1][1] = token.i
        else:
            runs.append([token.i, token.i])
    result = ''
    for start, end in runs:
        chunk = doc.text[doc[start].idx:doc[end].idx + len(doc[end])]
        if result and not doc[start].is_punct:
            result += ' '
        result += chunk
    return result.strip()


def _groups(doc):
    for head in doc:
        conjuncts = list(head.conjuncts)
        if head.dep_ == 'conj' or not conjuncts:
            continue
        members = [head, *conjuncts]
        if any(t.lower_ in {'or', 'nor', 'but'} for m in members for t in m.children if t.dep_ == 'cc'):
            continue
        if any(t.dep_ in {'advcl', 'relcl', 'ccomp'} or t.lower_ in {'between', 'versus'}
               for t in [head, *head.ancestors]):
            continue
        if head.pos_ in {'VERB', 'AUX'} and head.dep_ == 'ROOT':
            yield members
        elif head.pos_ in {'NOUN', 'PROPN'} and head.dep_ in {'dobj', 'pobj', 'attr'}:
            yield members


def _parts(members):
    """Disjoint coordinated branches; subjects, auxiliaries and conditions shared."""
    branches = []
    shared_roles = {'nsubj', 'nsubjpass', 'csubj', 'aux', 'auxpass', 'neg', 'advmod', 'advcl', 'punct'}
    for member in members:
        branch = {member.i}
        for child in member.children:
            if child.dep_ in {'conj', 'cc'}:
                continue
            if member == members[0] and member.pos_ in {'VERB', 'AUX'}:
                if child.dep_ in shared_roles or (child.dep_ == 'prep' and child.i < member.i):
                    continue
            branch.update(t.i for t in child.subtree)
        branches.append(branch)
    separators = {t.i for member in members for t in member.children if t.dep_ == 'cc'}
    return branches, separators


class SyntaxPlanner:
    def __init__(self, nlp=None):
        if nlp is None:
            import spacy
            nlp = spacy.load('en_core_web_sm', exclude=['ner'])
        if 'parser' not in nlp.pipe_names:
            raise ValueError('Arm A requires a trained dependency parser')
        self.nlp = nlp

    def plan(self, question):
        trace = {'dependencies': []}
        try:
            validate_question(question)
        except ValueError as exc:
            return failed(question, 'invalid_input', str(exc)), trace
        start = perf_counter()
        try:
            doc = self.nlp(question)
            trace['dependencies'] = [[t.text, t.idx, t.dep_, t.head.i] for t in doc]
            # A demonstrative with no preceding nominal referent is unresolved.
            deictic = [t for t in doc if t.lower_ in {'this', 'that', 'these', 'those'}
                       and t.dep_ == 'det' and not any(
                           p.pos_ in {'NOUN', 'PROPN'} for p in doc[:t.i])]
            if deictic:
                result = make_plan(question, [], ['The demonstrative reference is unspecified: '
                                                  + ', '.join(t.text for t in deictic)])
            else:
                variants = [set(range(len(doc)))]
                for members in _groups(doc):
                    branches, separators = _parts(members)
                    group = set.union(*branches) | separators
                    expanded = []
                    for keep in variants:
                        if not group & keep:
                            expanded.append(keep)
                        else:
                            expanded.extend((keep - group) | (branch & keep) for branch in branches)
                    variants = expanded
                    if len(variants) > 8:
                        raise OverflowError('More than eight syntactic requests')
                queries = list(dict.fromkeys(_render(doc, keep) for keep in variants))
                result = make_plan(question, queries)
        except OverflowError as exc:
            result = failed(question, 'capacity_exceeded', str(exc))
        except ValueError as exc:
            result = failed(question, 'invalid_output', str(exc))
        except Exception as exc:
            result = failed(question, 'backend_error', str(exc))
        trace['native_seconds'] = perf_counter() - start
        return result, trace
