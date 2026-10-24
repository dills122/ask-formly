"""Local answer diagnostic for frozen catalog-bakeoff fact packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Callable

from .catalog_bakeoff_trial import LocalSelector, MODEL


def validate_answer(raw: object, packet: list[dict]) -> dict:
    allowed = {fact["id"] for fact in packet}
    if not isinstance(raw, dict) or set(raw) != {"claims", "unresolved"}:
        raise ValueError("answer must contain claims and unresolved only")
    claims, unresolved = raw["claims"], raw["unresolved"]
    if not isinstance(claims, list) or len(claims) > 8:
        raise ValueError("invalid claim list")
    for claim in claims:
        if (not isinstance(claim, dict) or set(claim) != {"text", "fact_ids"} or
                not isinstance(claim["text"], str) or not claim["text"].strip() or
                len(claim["text"]) > 500 or
                not isinstance(claim["fact_ids"], list) or
                not claim["fact_ids"] or
                any(not isinstance(fid, str) or fid not in allowed
                    for fid in claim["fact_ids"])):
            raise ValueError("claim is malformed or cites outside the packet")
    if (not isinstance(unresolved, list) or len(unresolved) > 8 or
            any(not isinstance(ask, str) or not ask.strip() or len(ask) > 300
                for ask in unresolved)):
        raise ValueError("invalid unresolved list")
    return {"claims": claims, "unresolved": unresolved}


def answer_from_packet(question: str, packet: list[dict],
                       generate: Callable[[str], object]) -> dict:
    if not packet:
        return {"claims": [], "unresolved": [question]}
    prompt = (
        "Answer the developer question concisely using ONLY the supplied "
        "Formly facts and source quotes. Every factual claim must cite supporting "
        "fact IDs from the packet. If a requested part lacks direct support, put "
        "it in unresolved and do not guess. A citation alone does not make a "
        "claim supported. Return JSON only: "
        '{"claims":[{"text":"one concise factual claim","fact_ids":["exact ID"]}],'
        '"unresolved":["unanswered part"]}. '
        "Question: " + json.dumps(question) + "\nPacket: "
        + json.dumps(packet, ensure_ascii=False, separators=(",", ":"))
    )
    return validate_answer(generate(prompt), packet)


def diagnostic_status(upstream_status: str) -> str:
    if upstream_status in ("selector_error", "no_candidates"):
        return f"upstream_{upstream_status}"
    return "diagnostic_answer"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    questions = {case["id"]: case["question"] for case in source["cases"]}
    results = []
    for row in source["rows"]:
        question = questions[row["case_id"]]
        generator = LocalSelector()
        started = time.perf_counter()
        try:
            answer = answer_from_packet(question, row["packet"], generator)
            status = diagnostic_status(row["status"])
            error = None
        except (ValueError, KeyError, TimeoutError, OSError) as exc:
            answer = {"claims": [], "unresolved": [question]}
            status = "answer_error"
            error = str(exc)
        seconds = round(time.perf_counter() - started, 3)
        cited = {fid for claim in answer["claims"] for fid in claim["fact_ids"]}
        result = {
            "case_id": row["case_id"], "arm": row["arm"], "status": status,
            "answer": answer, "answer_seconds": seconds,
            "retrieval_and_selection_seconds": row["total_seconds"],
            "local_total_seconds": round(row["total_seconds"] + seconds, 3),
            "answer_chars": sum(len(claim["text"]) for claim in answer["claims"]),
            "required_ids_not_cited": sorted(set(row["required_fact_ids"]) - cited),
            "error": error, "model_metrics": generator.metrics,
        }
        results.append(result)
        print(json.dumps({"case": row["case_id"], "arm": row["arm"],
                          "status": status, "claims": len(answer["claims"]),
                          "unresolved": len(answer["unresolved"]),
                          "seconds": result["local_total_seconds"]}), flush=True)
    report = {
        "scope": "local Qwen3 Coder 30B answer diagnostic; not an agent/MCP latency measurement",
        "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "database_sha256": source["database_sha256"], "case_sha256": source["case_sha256"],
        "model": MODEL, "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({"output": str(args.output), "rows": len(results)}), flush=True)


if __name__ == "__main__":
    main()
