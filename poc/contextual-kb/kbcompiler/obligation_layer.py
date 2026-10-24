"""Read-only obligation-planning experiment over the existing contextual KB.

This module keeps the old question layer intact. It tests whether independently
retrieving each literal ask preserves facts lost by one broad packet ranking.
Candidate IDs are never assertions that a fact answers an ask.
"""

from __future__ import annotations

import json
import re
import sqlite3
import urllib.request
from dataclasses import dataclass
from typing import Callable

from .question_layer import (
    QueryPlanner, _explicit_adapter_conflict, _explicit_version_conflict,
    _question_terms,
)
from .question_pilot import PACKET_LIMIT


MAX_OBLIGATIONS = 8
MAX_CANDIDATES_PER_ASK = 2
MAX_POOL_PER_ASK = 32
LOCAL_MODEL = "qwen3-coder:30b"
_BREAK = re.compile(r"[?;,]|\.(?=\s|$)|\b(?:and|or|but|also)\b", re.I)


def validate_spans(question: str, raw: object) -> tuple[str, ...]:
    """Reject invented wording and dropped API identifiers in model output."""
    if not isinstance(raw, list) or not 1 <= len(raw) <= MAX_OBLIGATIONS:
        raise ValueError("planner must return 1-8 spans")
    spans: list[str] = []
    for item in raw:
        if not isinstance(item, str) or not item.strip() or item.strip() not in question:
            raise ValueError("planner span must be a literal question substring")
        span = item.strip()
        if span not in spans:
            spans.append(span)
    _, identifiers = _question_terms(question)
    if any(not any(identifier in span for span in spans) for identifier in identifiers):
        raise ValueError("planner dropped an exact API identifier")
    return tuple(spans)


class DeterministicObligationPlanner:
    """A low-cost punctuation/coordinator baseline, intentionally untrained."""

    def plan(self, question: str) -> tuple[str, ...]:
        pieces = [part.strip(" .!?,'\"\t\n") for part in _BREAK.split(question)]
        spans = [part for part in pieces if part and not re.fullmatch(
            r"(?:in|with|for)\s+(?:ngx-)?formly\s+v?\d+(?:\.\d+)*", part, re.I,
        )]
        return tuple(dict.fromkeys(spans)) or (question,)


class ModelSpanPlanner:
    """Validate a local model's literal spans; fall back on malformed output."""

    def __init__(self, generate: Callable[[str], object]) -> None:
        self.generate = generate
        self.used_fallback = False
        self.last_error: str | None = None

    def plan(self, question: str) -> tuple[str, ...]:
        self.used_fallback = False
        self.last_error = None
        try:
            payload = self.generate(question)
            if not isinstance(payload, dict):
                raise ValueError("planner returned a non-object")
            return validate_spans(question, payload.get("spans"))
        except (ValueError, KeyError, TypeError, TimeoutError, OSError) as exc:
            self.used_fallback = True
            self.last_error = str(exc)
            return DeterministicObligationPlanner().plan(question)


def ollama_literal_spans(question: str) -> dict:
    """Local-only constrained planner call. No facts or repository files sent."""
    prompt = (
        "Split the user's question into its separately answerable asks. "
        "Return JSON only: {\"spans\":[\"exact substring of the question\",...]}. "
        "Each span must be copied verbatim from the question, not paraphrased. "
        "Preserve every exact API name. Split coordinated actions and outcomes "
        "when each needs different evidence. Use at most eight spans. "
        "Do not answer and do not add concepts. Example: for 'Can I sort and "
        "export orders?' return {\"spans\":[\"sort\",\"export orders\"]}. "
        "Question: " + json.dumps(question)
    )
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({
            "model": LOCAL_MODEL, "prompt": prompt, "format": "json",
            "stream": False, "keep_alive": "10m",
            "options": {"temperature": 0, "num_predict": 300},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.load(response)
    return json.loads(body["response"])


@dataclass(frozen=True)
class ObligationEvidence:
    span: str
    candidate_ids: tuple[str, ...]
    status: str
    pool_size: int


@dataclass(frozen=True)
class ObligationResult:
    status: str
    obligations: tuple[ObligationEvidence, ...]
    fact_ids: tuple[str, ...]


class ObligationQueryLayer:
    """Search and rerank each ask before merging, without claiming support."""

    def __init__(self, db: sqlite3.Connection, index: object, reranker: object) -> None:
        self.planner = QueryPlanner(db)
        self.index = index
        self.reranker = reranker
        self.allowed_ids = set(index.ids)

    def _candidates(self, span: str) -> ObligationEvidence:
        plan = self.planner.plan(span)
        if not plan.probes:
            return ObligationEvidence(span, (), "unresolved_no_lexical_anchor", 0)
        direct = self.index.hybrid(span, 12)
        probe_ids = [fact_id for probe in plan.probes for fact_id in probe.fact_ids]
        linked = self.index.add_links(direct[:8], 16)
        pool = list(dict.fromkeys(
            fact_id for fact_id in [*direct, *probe_ids, *linked]
            if fact_id in self.allowed_ids
        ))[:MAX_POOL_PER_ASK]
        if not pool:
            return ObligationEvidence(span, (), "unresolved_no_candidates", 0)
        facts = self.index.facts
        documents = [" ".join((facts[fact_id]["claim"], facts[fact_id]["context"]))
                     for fact_id in pool]
        scores = self.reranker.rerank(span, documents)
        if len(scores) != len(pool):
            raise ValueError("reranker returned the wrong number of scores")
        ranked = sorted(range(len(pool)), key=lambda position: (-scores[position], position))
        chosen = tuple(pool[position] for position in ranked[:MAX_CANDIDATES_PER_ASK])
        return ObligationEvidence(span, chosen, "candidates_unverified", len(pool))

    def query(self, question: str, planner: object) -> ObligationResult:
        if _explicit_version_conflict(question):
            return ObligationResult("version_unverified", (), ())
        if _explicit_adapter_conflict(question):
            return ObligationResult("adapter_unverified", (), ())
        spans = planner.plan(question)
        if not spans:
            return ObligationResult("unresolved", (), ())
        obligations = tuple(self._candidates(span) for span in spans)
        ids = tuple(dict.fromkeys(
            fact_id for obligation in obligations for fact_id in obligation.candidate_ids
        ))
        if any(not obligation.candidate_ids for obligation in obligations):
            return ObligationResult("unresolved", obligations, ())
        if len(ids) > PACKET_LIMIT:
            return ObligationResult("over_budget", obligations, ())
        return ObligationResult("candidates_unverified", obligations, ids)
