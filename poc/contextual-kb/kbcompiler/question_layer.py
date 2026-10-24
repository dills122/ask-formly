"""Read-only, bounded question-to-query path for the contextual KB POC.

The authored facts and SQLite schema belong to the data layer. This module
derives FTS5 probes from question wording and combines their results with the
existing full-question hybrid retriever. It never treats a hit as a verified
answer.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass

from .question_pilot import ADAPTERS, BASELINE, PACKET_LIMIT, STOPWORDS


MAX_PROBES = 12
RERANK_MODEL = "Xenova/ms-marco-MiniLM-L-6-v2"
QUESTION_FILLERS = STOPWORDS | {
    "after", "around", "both", "form", "happens", "instead", "need", "stay", "will",
}
_WORD = re.compile(r"[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z][A-Za-z0-9]*)*")
_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_FORMLY_VERSION = re.compile(
    r"\b(?:ngx-)?formly\s*(?:version\s*|v\s*)?(\d+(?:\.\d+)*)\b", re.I,
)
_OTHER_UI = r"(?:bootstrap|ionic|primeng|kendo|nativescript|ng[- ]zorro[- ]antd)"
_OTHER_UI_NATURAL = re.compile(
    rf"\b(?:{_OTHER_UI}\s+(?:ngx[- ]?)?formly|"
    rf"(?:ngx[- ]?)?formly\s+(?:(?:with|using|for)\s+)?{_OTHER_UI})\b",
    re.I,
)
_OTHER_UI_PACKAGE = re.compile(rf"@ngx-formly/{_OTHER_UI}\b", re.I)


def _explicit_version_conflict(question: str) -> bool:
    baseline = tuple(int(part) for part in BASELINE.split("."))
    for match in _FORMLY_VERSION.finditer(question):
        requested = tuple(int(part) for part in match.group(1).split("."))
        if requested != baseline[:len(requested)]:
            return True
    return False


def _explicit_adapter_conflict(question: str) -> bool:
    return bool(_OTHER_UI_NATURAL.search(question) or _OTHER_UI_PACKAGE.search(question))


@dataclass(frozen=True)
class QueryProbe:
    match: str
    fact_ids: tuple[str, ...]
    terms: tuple[str, ...]


@dataclass(frozen=True)
class QueryPlan:
    semantic_query: str
    identifiers: tuple[str, ...]
    probes: tuple[QueryProbe, ...]


@dataclass(frozen=True)
class QueryResult:
    status: str
    fact_ids: tuple[str, ...]
    plan: QueryPlan


def _question_terms(question: str) -> tuple[list[str], tuple[str, ...]]:
    terms: list[str] = []
    identifiers: list[str] = []
    for token in _WORD.findall(question):
        parts = _CAMEL.sub(" ", token.replace(".", " ")).split()
        if len(parts) > 1:
            identifiers.append(token)
        for part in parts:
            word = part.casefold()
            if len(word) >= 4 and word not in QUESTION_FILLERS:
                terms.append(word)
    return terms[:32], tuple(dict.fromkeys(identifiers))


def _prefix(word: str) -> str:
    # An inflection-tolerant prefix. The original API spelling is separately
    # retained in the full semantic query and identifier list.
    if word.endswith("ally") and len(word) >= 9:
        word = word[:-4]
    elif word.endswith("ly") and len(word) >= 7:
        word = word[:-2]
    return word


def _fts_term(word: str) -> str:
    # _question_terms accepts only ASCII letters/digits. Quoting makes every
    # probe data rather than user-controlled FTS syntax.
    prefix = _prefix(word)
    return f'"{prefix}"*' if len(prefix) >= 5 else f'"{prefix}"'


class QueryPlanner:
    """Build selective lexical probes without a model call or DB mutation."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def _hits(self, match: str) -> tuple[str, ...]:
        rows = self.db.execute(
            "SELECT f.id FROM facts_fts "
            "JOIN facts f ON f.id=facts_fts.fact_id "
            "JOIN documents d ON d.id=f.doc_id "
            "WHERE facts_fts MATCH ? AND d.formly_version=? "
            "AND d.adapter IN (?, ?) "
            "ORDER BY bm25(facts_fts), f.id LIMIT 16",
            (match, BASELINE, *ADAPTERS),
        ).fetchall()
        return tuple(row[0] for row in rows)

    def plan(self, question: str) -> QueryPlan:
        terms, identifiers = _question_terms(question)
        pairs: list[tuple[int, QueryProbe]] = []
        singles: list[tuple[int, QueryProbe]] = []
        seen: set[str] = set()

        # Adjacent and one-gap pairs preserve focused aspects of a compound
        # question, such as "conditionally hide or disable".
        for start, left in enumerate(terms):
            for end in (start + 1, start + 2):
                if end >= len(terms):
                    continue
                right = terms[end]
                if _prefix(left) == _prefix(right):
                    continue
                match = f"{_fts_term(left)} AND {_fts_term(right)}"
                if match in seen:
                    continue
                seen.add(match)
                hits = self._hits(match)
                if hits:
                    pairs.append((start, QueryProbe(match, hits, (left, right))))

        exact_identifiers = [identifier.replace(".", "").casefold() for identifier in identifiers]
        for position, word in enumerate([*terms, *exact_identifiers]):
            match = _fts_term(word)
            if match in seen:
                continue
            seen.add(match)
            hits = self._hits(match)
            if hits:
                singles.append((position, QueryProbe(match, hits, (word,))))

        # Selective pairs carry more context; singles ensure API components and
        # separately named concepts have a chance when no pair matches.
        pairs.sort(key=lambda item: (len(item[1].fact_ids), item[0]))
        singles.sort(key=lambda item: (len(item[1].fact_ids), item[0]))
        terminal_terms = [
            _CAMEL.sub(" ", identifier.replace(".", " ")).split()[-1].casefold()
            for identifier in reversed(identifiers)
        ]
        probes: list[QueryProbe] = []
        used_matches: set[str] = set()

        def append(probe: QueryProbe) -> None:
            if probe.match not in used_matches and len(probes) < MAX_PROBES:
                probes.append(probe)
                used_matches.add(probe.match)

        for term in terminal_terms:
            for _, probe in singles:
                if probe.terms == (term,):
                    append(probe)
                    break
        for _, probe in pairs[:MAX_PROBES - 3]:
            append(probe)
        for _, probe in singles:
            append(probe)
        return QueryPlan(question, identifiers, tuple(probes))


class LocalReranker:
    """FastEmbed's local cross-encoder over a small retrieved candidate set."""

    def __init__(self, cache_dir: str) -> None:
        from fastembed.rerank.cross_encoder import TextCrossEncoder

        self.model = TextCrossEncoder(
            model_name=RERANK_MODEL, cache_dir=cache_dir, local_files_only=True,
        )

    def rerank(self, query: str, documents: list[str]) -> list[float]:
        return list(self.model.rerank(query, documents))


class QuestionLayer:
    """Construct queries and return candidate IDs, without answer assertions."""

    def __init__(self, db: sqlite3.Connection, index: object,
                 reranker: object | None = None) -> None:
        self.planner = QueryPlanner(db)
        self.index = index
        self.reranker = reranker
        # The existing index exposes only baseline/core/Material IDs here.
        # Apply that scope again after expansion because see-also links may
        # point at otherwise valid facts in another version or adapter.
        self.allowed_ids = set(index.ids)

    def query(self, question: str) -> QueryResult:
        if _explicit_version_conflict(question):
            return QueryResult("version_unverified", (), QueryPlan(question, (), ()))
        if _explicit_adapter_conflict(question):
            return QueryResult("adapter_unverified", (), QueryPlan(question, (), ()))
        plan = self.planner.plan(question)
        if not plan.probes:
            return QueryResult("no_lexical_anchor", (), plan)

        direct = self.index.hybrid(question, PACKET_LIMIT - 2)
        selected = [fact_id for fact_id in dict.fromkeys(direct)
                    if fact_id in self.allowed_ids][:PACKET_LIMIT - 2]
        linked = [fact_id for fact_id in self.index.add_links(selected, PACKET_LIMIT)
                  if fact_id in self.allowed_ids][:PACKET_LIMIT]
        terminal_terms = [
            _CAMEL.sub(" ", identifier.replace(".", " ")).split()[-1].casefold()
            for identifier in reversed(plan.identifiers)
        ]
        focus = [probe for term in terminal_terms for probe in plan.probes
                 if probe.terms == (term,)]
        needles = [probe for probe in plan.probes
                   if len(probe.terms) == 2 and len(probe.fact_ids) <= 2]
        singles = [probe for probe in plan.probes if len(probe.terms) == 1]

        def add_probe(probe: QueryProbe, focused: bool = False) -> bool:
            ranked = [fact_id for fact_id in probe.fact_ids
                      if fact_id in self.allowed_ids][:2]
            if focused and self.reranker is not None:
                facts = getattr(self.index, "facts", {})
                candidates = [fact_id for fact_id in probe.fact_ids
                              if fact_id in facts and fact_id in self.allowed_ids]
                if candidates:
                    documents = [" ".join((facts[fact_id]["claim"],
                                           facts[fact_id]["context"]))
                                 for fact_id in candidates]
                    scores = self.reranker.rerank(" ".join(probe.terms), documents)
                    ranked = [fact_id for _, fact_id in sorted(
                        zip(scores, candidates), key=lambda item: (-item[0], item[1]),
                    )]
            for fact_id in ranked:
                if fact_id not in selected:
                    selected.append(fact_id)
                    return True
            return False

        for probe in focus:
            if len(selected) == PACKET_LIMIT:
                break
            add_probe(probe, focused=True)
        for probe in needles:
            if len(selected) == PACKET_LIMIT:
                break
            add_probe(probe)
        if len(selected) < PACKET_LIMIT:
            for probe in singles:
                if probe not in focus and add_probe(probe, focused=True):
                    break
        for fact_id in linked:
            if len(selected) == PACKET_LIMIT:
                break
            if fact_id not in selected:
                selected.append(fact_id)
        fact_ids = selected[:PACKET_LIMIT]
        return QueryResult("candidates_unverified", tuple(fact_ids[:PACKET_LIMIT]), plan)
