"""Read-only audit of the controlled source database against authored inputs."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from .structured_source import lint_sources, load_json_strict


def audit(source_dir: Path, repo_root: Path, catalog_path: Path, database: Path) -> dict:
    errors = lint_sources(source_dir, repo_root, catalog_path)
    if errors:
        raise ValueError("\n".join(errors))
    docs = [load_json_strict(path) for path in sorted(source_dir.glob("*.json"))]
    expected_documents = []
    expected_facts = []
    expected_search = []
    expected_evidence = set()
    expected_links = []
    input_bytes = [catalog_path.read_bytes()]
    input_bytes.extend(path.read_bytes() for path in sorted(source_dir.glob("*.json")))
    for doc in docs:
        origin = doc["derived_from"]
        source_bytes = (repo_root / origin["path"]).read_bytes()
        source = source_bytes.decode("utf-8")
        input_bytes.append(source_bytes)
        expected_documents.append((
            doc["id"], doc["title"], doc["formly_version"], doc["adapter"],
            doc["summary"], origin["path"], origin["sha256"],
        ))
        for fact in doc["facts"]:
            fact_id = f"{doc['id']}/{fact['id']}"
            start = source.index(fact["source_quote"])
            expected_facts.append((
                fact_id, doc["id"], fact["claim"], json.dumps(fact["conditions"]),
                json.dumps(fact["limits"]), fact["context"], fact["source_quote"],
                start, start + len(fact["source_quote"]), "authored",
            ))
            expected_search.append((
                fact_id, fact["claim"], fact["context"],
                "\n".join(fact["conditions"]), "\n".join(fact["limits"]),
                doc["title"], doc["summary"],
            ))
            expected_evidence.update((fact_id, item) for item in fact["evidence_ids"])
            expected_links.extend((fact_id, link["target"], link["kind"]) for link in fact["related"])

    with closing(sqlite3.connect(f"file:{database}?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("database integrity check failed")
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("database contains broken references")
        actual_documents = db.execute("SELECT * FROM documents ORDER BY id").fetchall()
        if actual_documents != sorted(expected_documents):
            raise ValueError("seeded documents differ from authored source")
        actual_facts = db.execute("SELECT * FROM facts ORDER BY id").fetchall()
        if actual_facts != sorted(expected_facts):
            raise ValueError("seeded facts differ from authored source")
        actual_search = db.execute("""
            SELECT fact_id, claim, context, conditions, limits,
                   document_title, document_summary
            FROM facts_fts ORDER BY fact_id
        """).fetchall()
        if actual_search != sorted(expected_search):
            raise ValueError("search index differs from authored source")
        actual_evidence = db.execute("SELECT * FROM fact_evidence ORDER BY fact_id, evidence_id").fetchall()
        if actual_evidence != sorted(expected_evidence):
            raise ValueError("seeded evidence links differ from authored source")
        actual_links = db.execute("SELECT * FROM fact_links ORDER BY source_fact_id, target_fact_id, kind").fetchall()
        if actual_links != sorted(expected_links):
            raise ValueError("seeded fact links differ from authored source")
        used_ids = {evidence_id for _, evidence_id in expected_evidence}
        catalog = load_json_strict(catalog_path)
        expected_records = sorted(
            (record["id"], json.dumps(record, sort_keys=True))
            for record in catalog["records"] if record["id"] in used_ids
        )
        actual_records = db.execute("SELECT id, record_json FROM evidence ORDER BY id").fetchall()
        if actual_records != expected_records:
            raise ValueError("seeded evidence catalog differs from cited records")
        build_info = db.execute("SELECT schema_version, input_sha256 FROM build_info").fetchall()
        expected_hash = hashlib.sha256(b"".join(input_bytes)).hexdigest()
        if build_info != [(1, expected_hash)]:
            raise ValueError("build input digest differs from authored source")
    return {
        "schema_version": 1,
        "documents": len(expected_documents),
        "facts": len(expected_facts),
        "verified_source_spans": len(expected_facts),
        "indexed_facts": len(expected_search),
        "evidence_catalog_records": len(used_ids),
        "fact_evidence_links": len(expected_evidence),
        "fact_links": len(expected_links),
        "integrity": "ok",
        "semantic_entailment_verified": False,
    }


def main() -> None:
    poc = Path(__file__).resolve().parents[1]
    report = audit(
        poc / "authored", poc.parents[1], poc / "corpus/evidence-catalog.json",
        poc / "build/knowledge.sqlite",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
