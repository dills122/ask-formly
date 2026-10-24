"""Read-only comparison paths over the frozen contextual knowledge catalog.

The model may select IDs and name unresolved parts. The packet always copies
authored facts from the database; model-generated Formly prose is never sent.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from .question_layer import _explicit_adapter_conflict, _explicit_version_conflict


POOL_LIMIT = 24
PACKET_LIMIT = 8


class FactSelectionError(ValueError):
    """The selector did not honor the evidence packet contract."""


@dataclass(frozen=True)
class FactSelection:
    fact_ids: tuple[str, ...]
    unresolved: tuple[str, ...]


def scope_status(question: str) -> str | None:
    if _explicit_version_conflict(question):
        return "version_unverified"
    if _explicit_adapter_conflict(question):
        return "adapter_unverified"
    return None


class FullPool:
    """The entire in-scope fact catalog, without ranking or query rewriting."""

    def __init__(self, index: object) -> None:
        self.ids = tuple(index.ids)

    def candidates(self, question: str) -> tuple[str, ...]:
        return self.ids


class BroadPool:
    """One frozen, broad hybrid plus contextual-FTS candidate recipe."""

    def __init__(self, index: object, planner: object) -> None:
        self.index = index
        self.planner = planner
        self.allowed = set(index.ids)

    def candidates(self, question: str) -> tuple[str, ...]:
        direct = [fid for fid in self.index.hybrid(question, 16)
                  if fid in self.allowed]
        probe_hits = [fid for probe in self.planner.plan(question).probes
                      for fid in probe.fact_ids[:4] if fid in self.allowed]
        linked = [fid for fid in self.index.add_links(direct[:8], 16)
                  if fid in self.allowed]
        return tuple(dict.fromkeys([
            *direct[:8], *probe_hits, *direct[8:16], *linked,
        ]))[:POOL_LIMIT]


def selection_prompt(question: str, candidate_ids: tuple[str, ...],
                     facts: dict[str, dict]) -> str:
    catalog = [{key: facts[fid][key] for key in
                ("id", "claim", "context", "conditions", "limits")}
               for fid in candidate_ids]
    return (
        "Select only catalog facts that DIRECTLY answer parts of this developer "
        "question. Similar topic words are insufficient. Include all facts needed "
        "for a complete answer, including qualifications, up to eight IDs. "
        "If any requested part is not directly answered, describe that part in "
        "unresolved. For a wholly unsupported question, use ids=[]. "
        "Do not write an answer or any Formly advice. Return JSON only: "
        '{"ids":["exact fact ID"],"unresolved":["unanswered part"]}. '
        "Question: " + json.dumps(question) + "\nCatalog: "
        + json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    )


def select_facts(question: str, candidate_ids: tuple[str, ...],
                 facts: dict[str, dict], generate: Callable[[str], object]
                 ) -> FactSelection:
    if len(candidate_ids) != len(set(candidate_ids)) or any(
        fid not in facts for fid in candidate_ids
    ):
        raise FactSelectionError("candidate pool contains duplicates or unknown IDs")
    raw = generate(selection_prompt(question, candidate_ids, facts))
    if not isinstance(raw, dict) or set(raw) != {"ids", "unresolved"}:
        raise FactSelectionError("selector must return only ids and unresolved")
    ids, unresolved = raw["ids"], raw["unresolved"]
    if (not isinstance(ids, list) or len(ids) > PACKET_LIMIT or
            any(not isinstance(fid, str) for fid in ids) or
            len(ids) != len(set(ids)) or
            any(fid not in candidate_ids for fid in ids)):
        raise FactSelectionError("selector returned invalid fact IDs")
    if (not isinstance(unresolved, list) or len(unresolved) > PACKET_LIMIT or
            any(not isinstance(ask, str) or not ask.strip() or len(ask) > 300
                for ask in unresolved)):
        raise FactSelectionError("selector returned invalid unresolved asks")
    return FactSelection(tuple(ids), tuple(ask.strip() for ask in unresolved))


def render_packet(fact_ids: tuple[str, ...], facts: dict[str, dict]) -> list[dict]:
    """Copy original source-linked records; never use generated answer prose."""
    keys = ("id", "claim", "context", "conditions", "limits", "version",
            "adapter", "source_path", "source_quote")
    return [{key: facts[fid][key] for key in keys if key in facts[fid]}
            for fid in fact_ids]
