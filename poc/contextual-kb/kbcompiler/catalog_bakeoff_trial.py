"""Compare current, broad-pool and whole-catalog fact packets read-only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
import urllib.request
from contextlib import closing
from pathlib import Path

from .catalog_bakeoff import (
    BroadPool, FactSelectionError, FullPool, render_packet, scope_status,
    select_facts,
)
from .question_layer import LocalReranker, QueryPlanner, QuestionLayer
from .question_pilot import PilotIndex


MODEL = "qwen3-coder:30b"
OLLAMA = "http://127.0.0.1:11434/api/generate"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_facts(db: sqlite3.Connection, index: PilotIndex) -> dict[str, dict]:
    facts = {fid: dict(index.facts[fid]) for fid in index.ids}
    for fid, source_path, quote in db.execute("""
        SELECT f.id, d.source_path, f.source_quote FROM facts f
        JOIN documents d ON d.id=f.doc_id
        WHERE d.formly_version='6.3.12' AND d.adapter IN ('core', 'material')
    """):
        if fid in facts:
            facts[fid]["source_path"] = source_path
            facts[fid]["source_quote"] = quote
    return facts


class LocalSelector:
    def __init__(self) -> None:
        self.metrics: dict = {}

    def __call__(self, prompt: str) -> object:
        request = urllib.request.Request(
            OLLAMA,
            data=json.dumps({
                "model": MODEL, "prompt": prompt, "format": "json",
                "stream": False, "keep_alive": "10m",
                "options": {"temperature": 0, "num_predict": 500},
            }).encode(),
            headers={"Content-Type": "application/json"},
        )
        started = time.perf_counter()
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
        self.metrics = {
            "seconds": round(time.perf_counter() - started, 3),
            "prompt_eval_count": payload.get("prompt_eval_count"),
            "eval_count": payload.get("eval_count"),
            "prompt_bytes": len(prompt.encode("utf-8")),
        }
        return json.loads(payload["response"])


def row_for(case: dict, arm: str, status: str, ids: tuple[str, ...],
            facts: dict[str, dict], unresolved: tuple[str, ...] = (),
            **timing: object) -> dict:
    required = set(case["required_fact_ids"])
    packet = render_packet(ids, facts)
    return {
        "case_id": case["id"], "arm": arm, "status": status,
        "fact_ids": ids, "unresolved": unresolved,
        "required_fact_ids": case["required_fact_ids"],
        "missing_fact_ids": sorted(required - set(ids)),
        "complete_required_set": bool(required) and required <= set(ids),
        "negative_empty": not required and not ids,
        "negative_successful_abstention": not required and not ids and status in (
            "selected_unverified", "version_unverified", "adapter_unverified",
            "no_lexical_anchor",
        ),
        "negative_flagged": not required and (bool(unresolved) or status in (
            "version_unverified", "adapter_unverified")),
        "packet_bytes": len(json.dumps(packet, ensure_ascii=False).encode("utf-8")),
        "packet": packet,
        **timing,
    }


def run_case(case: dict, layer: QuestionLayer, broad: BroadPool,
             full: FullPool, facts: dict[str, dict]) -> list[dict]:
    question = case["question"]
    started = time.perf_counter()
    baseline = layer.query(question)
    elapsed = round(time.perf_counter() - started, 3)
    rows = [row_for(case, "current_eight", baseline.status, baseline.fact_ids,
                    facts, retrieval_seconds=elapsed, total_seconds=elapsed,
                    candidate_count=len(baseline.fact_ids))]
    for arm, pool in (("broad_24", broad), ("full_catalog", full)):
        scope = scope_status(question)
        if scope:
            rows.append(row_for(case, arm, scope, (), facts,
                                retrieval_seconds=0.0, selector_seconds=0.0,
                                total_seconds=0.0, candidate_count=0))
            continue
        started = time.perf_counter()
        candidates = pool.candidates(question)
        retrieval_seconds = round(time.perf_counter() - started, 3)
        if not candidates:
            rows.append(row_for(case, arm, "no_candidates", (), facts,
                                retrieval_seconds=retrieval_seconds,
                                selector_seconds=0.0,
                                total_seconds=retrieval_seconds,
                                candidate_count=0))
            continue
        selector = LocalSelector()
        try:
            selected = select_facts(question, candidates, facts, selector)
            rows.append(row_for(
                case, arm, "selected_unverified", selected.fact_ids, facts,
                unresolved=selected.unresolved,
                retrieval_seconds=retrieval_seconds,
                selector_seconds=selector.metrics["seconds"],
                total_seconds=round(retrieval_seconds + selector.metrics["seconds"], 3),
                candidate_count=len(candidates), **{
                    key: value for key, value in selector.metrics.items()
                    if key != "seconds"
                },
            ))
        except (FactSelectionError, ValueError, KeyError, TimeoutError, OSError) as exc:
            rows.append(row_for(
                case, arm, "selector_error", (), facts,
                retrieval_seconds=retrieval_seconds,
                selector_seconds=selector.metrics.get("seconds"),
                total_seconds=round(time.perf_counter() - started, 3),
                candidate_count=len(candidates), error=str(exc),
            ))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cases", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    fixture = args.cases or root / "CATALOG-BAKEOFF-CASES.json"
    cases = json.loads(fixture.read_text(encoding="utf-8"))["cases"]
    db_path = root / "build/knowledge.sqlite"
    with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)) as db:
        db.execute("PRAGMA query_only=ON")
        started = time.perf_counter()
        index = PilotIndex(db)
        facts = load_facts(db, index)
        layer = QuestionLayer(db, index,
                              reranker=LocalReranker(str(root / "build/model-cache")))
        broad = BroadPool(index, QueryPlanner(db))
        full = FullPool(index)
        startup_seconds = round(time.perf_counter() - started, 3)
        rows = []
        for case in cases:
            current = run_case(case, layer, broad, full, facts)
            rows.extend(current)
            print(json.dumps({
                "case": case["id"],
                "arms": [{"arm": row["arm"], "status": row["status"],
                          "missing": row["missing_fact_ids"],
                          "ids": len(row["fact_ids"]),
                          "seconds": row["total_seconds"]}
                         for row in current],
            }), flush=True)
    report = {
        "scope": "read-only candidate and fact-packet bake-off; no final agent answers",
        "database_sha256": sha(db_path), "case_sha256": sha(fixture),
        "selector_code_sha256": sha(root / "kbcompiler/catalog_bakeoff.py"),
        "model": MODEL, "startup_seconds": startup_seconds,
        "cases": cases, "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({"output": str(args.output), "startup_seconds": startup_seconds,
                      "rows": len(rows)}), flush=True)


if __name__ == "__main__":
    main()
