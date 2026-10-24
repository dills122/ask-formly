"""Run the bounded read-only question-layer trial against frozen pilot cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
from contextlib import closing
from pathlib import Path

from .question_layer import LocalReranker, QuestionLayer, RERANK_MODEL
from .question_pilot import PilotIndex


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--cases", type=Path,
                        help="Frozen case JSON; defaults to QUESTION-PILOT-CASES.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    fixture = args.cases or root / "QUESTION-PILOT-CASES.json"
    cases = json.loads(fixture.read_text(encoding="utf-8"))["cases"]
    with closing(sqlite3.connect(f"file:{root / 'build/knowledge.sqlite'}?mode=ro", uri=True)) as db:
        startup = time.perf_counter()
        layer = QuestionLayer(db, PilotIndex(db),
                              reranker=LocalReranker(str(root / "build/model-cache")))
        startup_seconds = time.perf_counter() - startup
        rows = []
        for case in cases:
            started = time.perf_counter()
            result = layer.query(case["question"])
            seconds = time.perf_counter() - started
            missing = sorted(set(case["required_fact_ids"]) - set(result.fact_ids))
            rows.append({
                "id": case["id"], "question": case["question"],
                "required_fact_ids": case["required_fact_ids"],
                "fact_ids": result.fact_ids, "missing": missing,
                "complete_id_set": not missing if case["required_fact_ids"] else not result.fact_ids,
                "status": result.status, "seconds": round(seconds, 3),
                "queries": [probe.match for probe in result.plan.probes],
            })
    report = {
        "scope": "read-only question-layer candidate trial; no final answers",
        "case_file": str(fixture),
        "case_sha256": hashlib.sha256(fixture.read_bytes()).hexdigest(),
        "question_layer_sha256": hashlib.sha256(
            (root / "kbcompiler/question_layer.py").read_bytes()).hexdigest(),
        "pilot_index_sha256": hashlib.sha256(
            (root / "kbcompiler/question_pilot.py").read_bytes()).hexdigest(),
        "database_sha256": hashlib.sha256(
            (root / "build/knowledge.sqlite").read_bytes()).hexdigest(),
        "rerank_model": RERANK_MODEL,
        "startup_seconds": round(startup_seconds, 3), "cases": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "answerable_complete": sum(row["complete_id_set"] for row in rows
                                   if row["required_fact_ids"]),
        "answerable_total": sum(bool(row["required_fact_ids"]) for row in rows),
        "negatives_empty": sum(not row["fact_ids"] for row in rows
                               if not row["required_fact_ids"]),
        "seconds_total": round(sum(row["seconds"] for row in rows), 3),
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
