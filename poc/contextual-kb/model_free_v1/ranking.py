"""Deterministic lexical reranking; never a relevance or support certificate.

Only the supplied, already scoped candidate IDs may be reordered. Direct claims
and context receive more weight than incidental mentions in conditions/limits.
The latter remain searchable and are always returned intact by the caller.
"""
from collections import Counter
import math
import re


TOKEN = re.compile(r'[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)*')
STOPWORDS = frozenset('a an and are as at be by can do does for formly from how i if in is it its my of on or should that the then this to use using what when where which why with would could please explain'.split())
# These ordinary lowercase words are public field/configuration names too. They
# cannot be recognized by the legacy camel-case/dotted-identifier heuristic.
LOWERCASE_IDENTIFIERS = frozenset('hide key model type props validators hooks expressions wrappers presets parsers template options focus name id fields form'.split())
SCOPE_PREFIX = re.compile(r'^\s*(?:For|In|Use)\s+Formly\s+v?\d+(?:\.\d+){0,2}'
                          r'(?:\s+(?:with\s+)?(?:Material|core))?\s*[,.:]\s*', re.I)

# Explicit spellings of the same public member, grounded in the field/options
# contracts. This is deliberately not a general dotted-name suffix heuristic:
# props.disabled and templateOptions.disabled, for example, remain distinct.
IDENTIFIER_ALIASES = {
    'options.formState': 'formState',
    'field.options.formState': 'formState',
    'hooks.onInit': 'onInit',
    'field.hooks.onInit': 'onInit',
}


def canonical_identifiers(text):
    return TOKEN.sub(lambda match: IDENTIFIER_ALIASES.get(match.group(), match.group()), text)


def lexical_expansions(text):
    """Bounded search hints, not synonyms or assertions about requested behavior."""
    focused = canonical_identifiers(SCOPE_PREFIX.sub('', text, count=1))
    words = {word.casefold() for word in TOKEN.findall(focused)}
    expansions = []
    collision = bool(re.search(r'\b(?:collid(?:e|es|ed|ing)|collisions?|namespac(?:e|es|ed|ing))\b', focused, re.I))
    if collision and words & {'model', 'value', 'values'}:
        expansions.extend(('key', 'model', 'path', 'fieldGroup'))
    # Registration and unregistration are contrasting lifecycle evidence. Offer
    # both only for explicit control questions; never strip arbitrary prefixes
    # or conflate registerField/unregisterField APIs or named type registration.
    # Mixed custom-control registry wording needs an explicit lifetime action.
    lifecycle = {'register', 'registers', 'registered', 'registering', 'registration',
                 'unregister', 'unregisters', 'unregistered', 'unregistering', 'unregistration'}
    named_registry = bool(words & {'type', 'types', 'component', 'components',
                                   'provider', 'providers', 'wrapper', 'wrappers'})
    lifecycle_action = bool(words & {'hide', 'hidden', 'hiding', 'show', 'shown', 'showing',
                                    'unregister', 'unregisters', 'unregistered', 'unregistering'})
    if (words & {'control', 'controls', 'formcontrol', 'field.formcontrol'} and words & lifecycle
            and (not named_registry or lifecycle_action)):
        expansions.extend(('register', 'registered', 'registration',
                           'unregister', 'unregistered', 'unregistration'))
    return expansions


def query_text(text):
    """Normalize a search view only; preserve original request and fact polarity."""
    focused = canonical_identifiers(SCOPE_PREFIX.sub('', text, count=1))
    expansions = lexical_expansions(text)
    return focused + (' ' + ' '.join(expansions) if expansions else '')


def _lexeme(token):
    # Inflect prose only. Preserve exact camel-case/dotted API spelling for the
    # identifier route; do not split names or collapse negation such as unregister.
    if '.' in token or '$' in token or re.search(r'[a-z][A-Z]', token):
        return token.casefold()
    word = token.casefold()
    word = {'hidden': 'hide', 'shown': 'show', 'built': 'build',
            'kept': 'keep', 'written': 'write'}.get(word, word)
    if len(word) > 4 and word.endswith('s') and not word.endswith(('ss', 'is')):
        word = word[:-1]
    for suffix in ('ing', 'ed'):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            word = word[:-len(suffix)]
            if len(word) > 2 and word[-1] == word[-2] and word[-1] not in 'lsz':
                word = word[:-1]
            break
    if len(word) > 3 and word.endswith('e'):
        word = word[:-1]
    return word


def _terms(text):
    return [_lexeme(token) for token in TOKEN.findall(text)
            if token.casefold() not in STOPWORDS]


def _fields(fact):
    return tuple(canonical_identifiers(field) for field in (fact.get('claim', ''), fact.get('context', ''),
            fact.get('title', ''),
            ' '.join([*fact.get('conditions', []), *fact.get('limits', [])])))


def _recognized(text, facts, ids):
    vocabulary = {token for fid in ids for field in _fields(facts[fid])
                  for token in TOKEN.findall(field)}
    return sorted({token for token in TOKEN.findall(canonical_identifiers(text))
                   if token in vocabulary and
                   (token in LOWERCASE_IDENTIFIERS or '.' in token or '$' in token
                    or re.search(r'[a-z][A-Z]', token))})


def rerank(text, facts, candidate_ids):
    """Return the same candidate set, with field-weighted BM25 ordering.

    Corpus statistics use only candidates, so excluded versions/adapters cannot
    contribute documents. Ties preserve the incoming fused-route ranking.
    Repeating a query term or a claim token cannot yield an unbounded boost.
    """
    ids = list(dict.fromkeys(candidate_ids))
    if not ids:
        return ids
    # A scope prefix selects eligibility in Store; it is not topical evidence.
    focused = query_text(text)
    query = set(_terms(focused))
    if not query:
        return ids
    fields = {fid: tuple(Counter(_terms(field)) for field in _fields(facts[fid]))
              for fid in ids}
    document_frequency = Counter(term for fid in ids
                                 for term in set().union(*fields[fid]))
    averages = [max(1, sum(sum(fields[fid][i].values()) for fid in ids) / len(ids))
                for i in range(4)]
    weights = (3.0, 2.0, 4.0, 0.2)
    identifiers = {_lexeme(token): 1.5 if token in LOWERCASE_IDENTIFIERS else 3.0
                   for token in _recognized(focused, facts, ids)}

    def score(fid):
        total = 0.0
        for i, counts in enumerate(fields[fid]):
            length = sum(counts.values())
            for term in query & counts.keys():
                frequency = counts[term]
                inverse = math.log1p((len(ids) - document_frequency[term] + 0.5)
                                    / (document_frequency[term] + 0.5))
                normalization = frequency + 1.2 * (0.25 + 0.75 * length / averages[i])
                total += (weights[i] * identifiers.get(term, 1.0) * inverse
                          * frequency * 2.2 / normalization)
        return total

    return sorted(ids, key=lambda fid: -score(fid))


def diagnostics(text, facts, candidate_ids):
    """Expose bounded observable matching signals, never inferred topic support."""
    ids = list(dict.fromkeys(candidate_ids))
    recognized = _recognized(text, facts, ids)
    primary = {term for fid in ids for field in _fields(facts[fid])[:2]
               for term in _terms(field)}
    focused = canonical_identifiers(SCOPE_PREFIX.sub('', text, count=1))
    query = set(_terms(focused))
    unmatched = sorted(query - primary)
    return {
        'recognized_identifiers': recognized[:16],
        'recognized_identifier_count': len(recognized),
        'identifier_aliases': [dict(supplied=token, canonical=IDENTIFIER_ALIASES[token])
                               for token in sorted(set(TOKEN.findall(text)) & IDENTIFIER_ALIASES.keys())],
        'lexical_expansions': lexical_expansions(text),
        'unmatched_primary_terms': unmatched[:16],
        'unmatched_primary_term_count': len(unmatched),
        'signal': 'no_recognized_identifier' if not recognized else 'identifier_match',
        'hint': ('No recognized identifier matched these candidates. Use relevant '
                 'known API names or inspect help_formly/discovery; do not invent APIs.'
                 if not recognized else
                 'Identifier matches are lexical signals, not proof of relevance or complete support.'),
        'semantic_relevance': 'not_assessed',
    }
