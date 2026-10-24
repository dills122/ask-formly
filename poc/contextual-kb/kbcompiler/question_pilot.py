"""One-pass comparison of direct hybrid, planned hybrid, and whole-fact selection.

This is a local diagnostic harness, not the serving MCP. It reads the existing
knowledge.sqlite without changing its schema or authored inputs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import time
import urllib.request
from contextlib import closing
from pathlib import Path


BASELINE = "6.3.12"
ADAPTERS = ("core", "material")
MODEL_NAME = "qwen2.5-coder:3b-instruct"
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
PACKET_LIMIT = 8
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does",
    "for", "formly", "from", "how", "i", "if", "in", "is", "it", "its",
    "my", "of", "on", "or", "should", "that", "the", "then", "this",
    "to", "use", "using", "what", "when", "where", "which", "why", "with",
}


def explicit_other_version(question: str, baseline: str) -> bool:
    """Only reject an explicit major-version conflict; do not guess versions."""
    matches = re.findall(r"\b(?:ngx-)?formly\s*(?:version\s*|v\s*)?(\d+)(?:\.\d+)*\b", question, re.I)
    return bool(matches) and any(major != baseline.split(".")[0] for major in matches)


def _terms(text: str) -> list[str]:
    return list(dict.fromkeys(
        token for token in re.findall(r"[A-Za-z][A-Za-z0-9]*", text)
        if len(token) >= 3 and token.casefold() not in STOPWORDS
    ))[:8]


def _match_expression(terms: list[str], operator: str) -> str:
    return f" {operator} ".join('"' + term.replace('"', '""') + '"' for term in terms)


def fts_matches(db: sqlite3.Connection, text: str, limit: int) -> list[int]:
    """Exercise the production tokenizer/query policy on an arbitrary FTS table."""
    terms = _terms(text)
    if not terms:
        return []
    for operator in ("AND", "OR"):
        rows = db.execute(
            "SELECT rowid FROM facts_fts WHERE facts_fts MATCH ? "
            "ORDER BY bm25(facts_fts), rowid LIMIT ?",
            (_match_expression(terms, operator), limit),
        ).fetchall()
        if rows:
            return [row[0] for row in rows]
    return []


def reciprocal_rank_fusion(lists: list[list[str]]) -> list[str]:
    scores: dict[str, float] = {}
    for ranked in lists:
        for rank, fact_id in enumerate(dict.fromkeys(ranked), 1):
            scores[fact_id] = scores.get(fact_id, 0.0) + 1.0 / (60 + rank)
    return sorted(scores, key=lambda fact_id: (-scores[fact_id], fact_id))


def merge_obligations(lists: list[list[str]], limit: int) -> list[str]:
    """Interleave facets so a broad query cannot consume the whole packet."""
    result: list[str] = []
    for offset in range(max((len(items) for items in lists), default=0)):
        for items in lists:
            if offset < len(items) and items[offset] not in result:
                result.append(items[offset])
                if len(result) == limit:
                    return result
    return result


def valid_fact_ids(raw: object, allowed: set[str], limit: int) -> list[str]:
    if not isinstance(raw, list):
        return []
    result: list[str] = []
    for item in raw:
        if isinstance(item, str) and item in allowed and item not in result:
            result.append(item)
            if len(result) == limit:
                break
    return result


def _ollama_json(prompt: str) -> tuple[dict, float]:
    request = urllib.request.Request(
        os.environ.get("FORMLY_PILOT_OLLAMA", "http://127.0.0.1:11434/api/generate"),
        data=json.dumps({
            "model": MODEL_NAME, "prompt": prompt, "format": "json", "stream": False,
            "keep_alive": "15m", "options": {"temperature": 0, "num_predict": 350},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=45) as response:
        payload = json.load(response)
    elapsed = time.perf_counter() - started
    parsed = json.loads(payload["response"])
    if not isinstance(parsed, dict):
        raise ValueError("model did not return a JSON object")
    return parsed, elapsed


class PilotIndex:
    def __init__(self, db: sqlite3.Connection) -> None:
        import numpy as np
        from fastembed import TextEmbedding

        self.db = db
        self.facts: dict[str, dict] = {}
        for row in db.execute("""
            SELECT f.id, f.claim, f.context, f.conditions_json, f.limits_json,
                   d.title, d.formly_version, d.adapter
            FROM facts f JOIN documents d ON d.id=f.doc_id ORDER BY f.id
        """):
            fact_id, claim, context, conditions, limits, title, version, adapter = row
            self.facts[fact_id] = {
                "id": fact_id, "claim": claim, "context": context,
                "conditions": json.loads(conditions), "limits": json.loads(limits),
                "title": title, "version": version, "adapter": adapter,
            }
        self.ids = [fact_id for fact_id, fact in self.facts.items()
                    if fact["version"] == BASELINE and fact["adapter"] in ADAPTERS]
        cache = os.environ.get("FORMLY_PILOT_EMBED_CACHE", str(Path.home() / ".cache/fastembed"))
        self.embedder = TextEmbedding(model_name=EMBED_MODEL, cache_dir=cache, local_files_only=True)
        texts = [self._embedding_text(self.facts[fact_id]) for fact_id in self.ids]
        vectors = np.stack(list(self.embedder.embed(texts))).astype("float32")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        self.vectors = vectors / np.maximum(norms, 1e-12)

    @staticmethod
    def _embedding_text(fact: dict) -> str:
        return "\n".join((fact["title"], fact["claim"], fact["context"],
                          *fact["conditions"], *fact["limits"]))

    def lexical(self, text: str, limit: int) -> list[str]:
        terms = _terms(text)
        if not terms:
            return []
        for operator in ("AND", "OR"):
            rows = self.db.execute("""
                SELECT f.id FROM facts_fts
                JOIN facts f ON f.id=facts_fts.fact_id
                JOIN documents d ON d.id=f.doc_id
                WHERE facts_fts MATCH ? AND d.formly_version=?
                  AND d.adapter IN (?, ?)
                ORDER BY bm25(facts_fts), f.id LIMIT ?
            """, (_match_expression(terms, operator), BASELINE, *ADAPTERS, limit)).fetchall()
            if rows:
                return [row[0] for row in rows]
        return []

    def dense(self, text: str, limit: int) -> list[str]:
        import numpy as np

        query = next(self.embedder.query_embed(text)).astype("float32")
        query /= max(float(np.linalg.norm(query)), 1e-12)
        scores = self.vectors @ query
        ranked = sorted(range(len(self.ids)), key=lambda i: (-float(scores[i]), self.ids[i]))
        return [self.ids[i] for i in ranked[:limit]]

    def hybrid(self, text: str, limit: int) -> list[str]:
        return reciprocal_rank_fusion([self.lexical(text, limit), self.dense(text, limit)])[:limit]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        result = selected[:limit]
        for fact_id in selected:
            for (target,) in self.db.execute(
                "SELECT target_fact_id FROM fact_links WHERE source_fact_id=? "
                "AND kind='see_also' ORDER BY target_fact_id", (fact_id,),
            ):
                if target in self.facts and target not in result:
                    result.append(target)
                    if len(result) == limit:
                        return result
        return result


def _planned_queries(question: str) -> tuple[list[str], float]:
    prompt = (
        "Return one JSON object with a queries array of 1 to 4 nonempty search "
        "query strings. Split this Formly question into independently answerable "
        "parts. Preserve exact API names. If it asks one thing, use the original "
        "question as the single query. Do not answer, invent facts, or add topics. "
        "Question: "
        + json.dumps(question)
    )
    output, elapsed = _ollama_json(prompt)
    raw = output.get("queries")
    if not isinstance(raw, list) or not 1 <= len(raw) <= 4 or any(
        not isinstance(item, str) or not item.strip() for item in raw
    ):
        raise ValueError("invalid planner queries")
    return [item.strip() for item in raw], elapsed


def _whole_fact_selection(question: str, facts: list[dict], limit: int) -> tuple[list[str], float, object]:
    compact = [{key: fact[key] for key in ("id", "claim", "conditions", "limits", "context")}
               for fact in facts]
    prompt = (
        "You select evidence IDs from a Formly 6.3.12 fact catalog. Return JSON "
        f"only: {{\"ids\":[...]}} with at most {limit} listed IDs. Include every fact "
        "needed to answer all parts, including material caveats. Select only exact "
        "IDs in the catalog. Return [] if the catalog cannot answer the question. "
        "Do not answer the question. Question: " + json.dumps(question) +
        "\nCatalog: " + json.dumps(compact, separators=(",", ":"))
    )
    output, elapsed = _ollama_json(prompt)
    raw = output.get("ids")
    return valid_fact_ids(raw, {fact["id"] for fact in facts}, limit), elapsed, raw


def run_case(index: PilotIndex, case: dict) -> dict:
    question = case["question"]
    required = set(case["required_fact_ids"])
    outcomes: dict[str, dict] = {}
    if explicit_other_version(question, BASELINE):
        for arm in ("A_direct_hybrid", "B_planned_hybrid", "C_whole_fact"):
            outcomes[arm] = {"ids": [], "seconds": 0.0, "scope": "version_unverified"}
    else:
        started = time.perf_counter()
        direct = index.hybrid(question, PACKET_LIMIT - 2)
        outcomes["A_direct_hybrid"] = {
            "ids": index.add_links(direct, PACKET_LIMIT),
            "seconds": round(time.perf_counter() - started, 3),
        }
        started = time.perf_counter()
        try:
            queries, planner_seconds = _planned_queries(question)
            lists = [index.hybrid(query, 3) for query in queries]
            selected = merge_obligations(lists, PACKET_LIMIT - 2)
            outcomes["B_planned_hybrid"] = {
                "ids": index.add_links(selected, PACKET_LIMIT), "queries": queries,
                "planner_seconds": round(planner_seconds, 3),
                "seconds": round(time.perf_counter() - started, 3),
            }
        except (ValueError, OSError, TimeoutError) as exc:
            outcomes["B_planned_hybrid"] = {
                "ids": [], "error": str(exc), "seconds": round(time.perf_counter() - started, 3),
            }
        started = time.perf_counter()
        try:
            selected, model_seconds, raw = _whole_fact_selection(
                question, [index.facts[fact_id] for fact_id in index.ids], PACKET_LIMIT,
            )
            outcomes["C_whole_fact"] = {
                "ids": selected, "model_seconds": round(model_seconds, 3),
                "raw_ids": raw, "seconds": round(time.perf_counter() - started, 3),
            }
        except (ValueError, OSError, TimeoutError) as exc:
            outcomes["C_whole_fact"] = {
                "ids": [], "error": str(exc), "seconds": round(time.perf_counter() - started, 3),
            }
    for outcome in outcomes.values():
        found = set(outcome["ids"])
        outcome["missing"] = sorted(required - found)
        outcome["complete"] = required <= found if required else not found
        outcome["irrelevant_count"] = len(found - required)
    return {"id": case["id"], "question": question,
            "required_fact_ids": case["required_fact_ids"], "arms": outcomes}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    poc = Path(__file__).resolve().parents[1]
    cases = json.loads((poc / "QUESTION-PILOT-CASES.json").read_text(encoding="utf-8"))
    started = time.perf_counter()
    with closing(sqlite3.connect(f"file:{poc / 'build/knowledge.sqlite'}?mode=ro", uri=True)) as db:
        index = PilotIndex(db)
        startup = time.perf_counter() - started
        results = [run_case(index, case) for case in cases["cases"]]
    report = {
        "scope": "one fixed local-model pilot, no tuning, no MCP or final agent answer",
        "corpus_facts": len(index.ids), "model": MODEL_NAME, "embedding_model": EMBED_MODEL,
        "packet_limit": PACKET_LIMIT, "startup_seconds": round(startup, 3),
        "cases": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {arm: {
        "complete": sum(case["arms"][arm]["complete"] for case in results),
        "seconds_total": round(sum(case["arms"][arm]["seconds"] for case in results), 3),
    } for arm in ("A_direct_hybrid", "B_planned_hybrid", "C_whole_fact")}
    print(json.dumps({"cases": len(results), "startup_seconds": report["startup_seconds"],
                      "arms": summary, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
