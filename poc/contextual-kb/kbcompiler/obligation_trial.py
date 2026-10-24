"""Compare literal obligation planners on one frozen, read-only question set."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
from contextlib import closing
from pathlib import Path

from .evidence_check import ollama_assess
from .obligation_layer import (
    DeterministicObligationPlanner, LOCAL_MODEL, ModelSpanPlanner,
    ObligationQueryLayer, ollama_literal_spans,
)
from .question_layer import LocalReranker, RERANK_MODEL
from .question_pilot import PilotIndex


class TimedPlanner:
    def __init__(self, planner: object) -> None:
        self.planner = planner
        self.seconds = 0.0

    def plan(self, question: str) -> tuple[str, ...]:
        started = time.perf_counter()
        result = self.planner.plan(question)
        self.seconds += time.perf_counter() - started
        return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def complete_case(case: dict, result: object) -> bool:
    required = set(case["required_fact_ids"])
    if not required:
        return result.status == "unresolved"
    return result.status == "candidates_unverified" and required <= set(result.fact_ids)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", choices=("deterministic", "model"), required=True)
    parser.add_argument("--check-evidence", action="store_true")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    fixture = root / "OBLIGATION-TRIAL-CASES.json"
    cases = json.loads(fixture.read_text(encoding="utf-8"))["cases"]
    with closing(sqlite3.connect(f"file:{root / 'build/knowledge.sqlite'}?mode=ro", uri=True)) as db:
        started = time.perf_counter()
        layer = ObligationQueryLayer(
            db, PilotIndex(db), LocalReranker(str(root / "build/model-cache")),
        )
        startup_seconds = time.perf_counter() - started
        planner = (DeterministicObligationPlanner() if args.arm == "deterministic"
                   else ModelSpanPlanner(ollama_literal_spans))
        rows = []
        for case in cases:
            timed = TimedPlanner(planner)
            started = time.perf_counter()
            result = layer.query(case["question"], timed)
            elapsed = time.perf_counter() - started
            assessment = None
            checker_error = None
            check_seconds = 0.0
            if args.check_evidence:
                check_started = time.perf_counter()
                try:
                    assessment = ollama_assess(
                        case["question"], result.obligations, layer.index.facts,
                    )
                except (ValueError, KeyError, TypeError, TimeoutError, OSError) as exc:
                    checker_error = f"{type(exc).__name__}: {exc}"
                    assessment = tuple((False, ()) for _ in result.obligations)
                check_seconds = time.perf_counter() - check_started
            required = set(case["required_fact_ids"])
            missing = sorted(required - set(result.fact_ids))
            rows.append({
                "id": case["id"], "question": case["question"],
                "expected_aspects": case["aspects"],
                "required_fact_ids": case["required_fact_ids"],
                "status": result.status, "fact_ids": result.fact_ids,
                "missing": missing,
                "complete_id_set": complete_case(case, result),
                "planner_fallback": getattr(planner, "used_fallback", False),
                "planner_error": getattr(planner, "last_error", None),
                "planning_seconds": round(timed.seconds, 3),
                "retrieval_seconds": round(elapsed - timed.seconds, 3),
                "evidence_check_seconds": round(check_seconds, 3),
                "checker_error": checker_error,
                "model_assessed_all": (all(supported for supported, _ in assessment)
                                       if assessment is not None else None),
                "assessments": ([{"supported": supported, "fact_ids": ids}
                                 for supported, ids in assessment]
                                if assessment is not None else None),
                "obligations": [
                    {"span": item.span, "status": item.status,
                     "candidate_ids": item.candidate_ids, "pool_size": item.pool_size}
                    for item in result.obligations
                ],
            })
    report = {
        "scope": "obligation-level candidate retrieval trial; no answer claims",
        "arm": args.arm, "model": LOCAL_MODEL if args.arm == "model" else None,
        "evidence_check": args.check_evidence,
        "evidence_check_sha256": sha(root / "kbcompiler/evidence_check.py"),
        "rerank_model": RERANK_MODEL,
        "case_sha256": sha(fixture),
        "obligation_layer_sha256": sha(root / "kbcompiler/obligation_layer.py"),
        "question_layer_sha256": sha(root / "kbcompiler/question_layer.py"),
        "pilot_index_sha256": sha(root / "kbcompiler/question_pilot.py"),
        "database_sha256": sha(root / "build/knowledge.sqlite"),
        "startup_seconds": round(startup_seconds, 3), "cases": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "arm": args.arm,
        "answerable_complete": sum(row["complete_id_set"] for row in rows
                                   if row["required_fact_ids"]),
        "answerable_total": sum(bool(row["required_fact_ids"]) for row in rows),
        "negatives_unresolved": sum(row["status"] == "unresolved" for row in rows
                                    if not row["required_fact_ids"]),
        "model_fallbacks": sum(row["planner_fallback"] for row in rows),
        "model_assessed_complete": sum(
            row["complete_id_set"] and row["model_assessed_all"] for row in rows
            if row["required_fact_ids"]
        ) if args.check_evidence else None,
        "negative_model_abstentions": sum(
            row["model_assessed_all"] is False for row in rows
            if not row["required_fact_ids"]
        ) if args.check_evidence else None,
        "planning_seconds": round(sum(row["planning_seconds"] for row in rows), 3),
        "retrieval_seconds": round(sum(row["retrieval_seconds"] for row in rows), 3),
        "evidence_check_seconds": round(sum(row["evidence_check_seconds"] for row in rows), 3),
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
