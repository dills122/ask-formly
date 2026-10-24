"""Compile controlled authored knowledge records into one SQLite database.

The compiler verifies structure and provenance. It cannot certify that a
natural-language claim is semantically entailed by the cited source.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path


DOC_KEYS = {"schema_version", "id", "title", "formly_version", "adapter", "summary", "derived_from", "facts"}
FACT_KEYS = {"id", "claim", "conditions", "limits", "context", "source_quote", "evidence_ids", "related"}
SLUG = re.compile(r"^[a-z][a-z0-9-]*$")
EVIDENCE_ID = re.compile(r"^(?:K|E)\d+[a-z]?$", re.IGNORECASE)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json_strict(path: Path) -> dict:
    """Parse JSON without silently accepting repeated object keys."""
    def unique_pairs(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)


def _keys(value: object, expected: set[str], where: str, errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{where}: expected an object")
        return False
    missing = expected - value.keys()
    unknown = value.keys() - expected
    if missing:
        errors.append(f"{where}: missing fields {sorted(missing)}")
    if unknown:
        errors.append(f"{where}: unknown fields {sorted(unknown)}")
    return not missing and not unknown


def _string(value: object, where: str, errors: list[str]) -> bool:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        errors.append(f"{where}: expected a nonempty, trimmed string")
        return False
    return True


def _strings(value: object, where: str, errors: list[str]) -> bool:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() or item != item.strip() for item in value):
        errors.append(f"{where}: expected a list of nonempty, trimmed strings")
        return False
    return True


def _read_sources(source_dir: Path, repo_root: Path, catalog_path: Path) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    try:
        catalog = load_json_strict(catalog_path)
        catalog_ids = {item["id"] for item in catalog["records"]}
        baseline = catalog["baseline"]
    except (OSError, ValueError, UnicodeError, KeyError, TypeError) as exc:
        return [], [f"evidence catalog: {exc}"]
    paths = sorted(source_dir.glob("*.json"))
    if not paths:
        return [], [f"{source_dir}: no authored source files"]
    documents: list[dict] = []
    document_ids: set[str] = set()
    all_ids: set[str] = set()
    all_links: list[tuple[str, str]] = []
    root = repo_root.resolve()
    for path in paths:
        where = path.name
        try:
            doc = load_json_strict(path)
        except (OSError, ValueError, UnicodeError) as exc:
            errors.append(f"{where}: invalid JSON: {exc}")
            continue
        if not _keys(doc, DOC_KEYS, where, errors):
            continue
        if doc["schema_version"] != 1 or type(doc["schema_version"]) is not int:
            errors.append(f"{where}: unsupported schema_version")
        for key in ("id", "title", "formly_version", "adapter", "summary"):
            _string(doc[key], f"{where}.{key}", errors)
        if not isinstance(doc["id"], str) or not SLUG.fullmatch(doc["id"]):
            errors.append(f"{where}: id must be a lowercase slug")
        if isinstance(doc["id"], str):
            if doc["id"] in document_ids:
                errors.append(f"{where}: duplicate document id {doc['id']}")
            document_ids.add(doc["id"])
        if doc["formly_version"] != baseline:
            errors.append(f"{where}: formly_version differs from evidence catalog baseline")
        origin = doc["derived_from"]
        source_text = None
        if _keys(origin, {"path", "sha256"}, f"{where}.derived_from", errors):
            if _string(origin["path"], f"{where}.derived_from.path", errors) and _string(origin["sha256"], f"{where}.derived_from.sha256", errors):
                source_path = (root / origin["path"]).resolve()
                if not source_path.is_relative_to(root):
                    errors.append(f"{where}: derived_from path leaves repository")
                elif not source_path.is_file():
                    errors.append(f"{where}: derived_from file does not exist")
                else:
                    data = source_path.read_bytes()
                    if _sha(data) != origin["sha256"]:
                        errors.append(f"{where}: derived_from sha256 differs from source")
                    try:
                        source_text = data.decode("utf-8")
                    except UnicodeDecodeError:
                        errors.append(f"{where}: derived_from {origin['path']} is not UTF-8")
        facts = doc["facts"]
        if not isinstance(facts, list) or not facts:
            errors.append(f"{where}: facts must be a nonempty list")
            continue
        for index, fact in enumerate(facts):
            label = f"{where}.facts[{index}]"
            if not _keys(fact, FACT_KEYS, label, errors):
                continue
            for key in ("id", "claim", "context", "source_quote"):
                _string(fact[key], f"{label}.{key}", errors)
            if not isinstance(fact["id"], str) or not SLUG.fullmatch(fact["id"]):
                errors.append(f"{label}: id must be a lowercase slug")
            _strings(fact["conditions"], f"{label}.conditions", errors)
            _strings(fact["limits"], f"{label}.limits", errors)
            if source_text is not None and isinstance(fact["source_quote"], str):
                if source_text.count(fact["source_quote"]) != 1:
                    errors.append(f"{label}: source_quote must occur exactly once in derived_from")
            full_id = f"{doc['id']}/{fact['id']}"
            if full_id in all_ids:
                errors.append(f"{label}: duplicate fact id {full_id}")
            all_ids.add(full_id)
            citations = fact["evidence_ids"]
            if not isinstance(citations, list) or not citations:
                errors.append(f"{label}: evidence_ids must be a nonempty list")
            else:
                if len(citations) != len(set(map(str, citations))):
                    errors.append(f"{label}: duplicate evidence id")
                for evidence_id in citations:
                    if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
                        errors.append(f"{label}: invalid evidence id {evidence_id}")
                    elif evidence_id not in catalog_ids:
                        errors.append(f"{label}: unknown evidence id {evidence_id}")
                    elif isinstance(fact["source_quote"], str) and not re.search(
                        rf"\[[^\]\n]+\]\((?:sources|examples)\.md#{re.escape(evidence_id.lower())}\)",
                        fact["source_quote"], re.IGNORECASE,
                    ):
                        errors.append(f"{label}: {evidence_id} is not cited in source_quote")
            links = fact["related"]
            if not isinstance(links, list):
                errors.append(f"{label}: related must be a list")
            else:
                for link in links:
                    if _keys(link, {"kind", "target"}, f"{label}.related", errors):
                        if link["kind"] != "see_also" or not isinstance(link["target"], str):
                            errors.append(f"{label}: unsupported related link")
                        else:
                            all_links.append((full_id, link["target"]))
        documents.append(doc)
    for source, target in all_links:
        if target not in all_ids:
            errors.append(f"{source}: related target {target} is missing")
        if source == target:
            errors.append(f"{source}: self relation is not useful")
    return documents, errors


def lint_sources(source_dir: Path, repo_root: Path, catalog_path: Path) -> list[str]:
    """Return all deterministic structure, provenance, and link errors."""
    _, errors = _read_sources(source_dir, repo_root, catalog_path)
    return errors


def build_sources(source_dir: Path, repo_root: Path, catalog_path: Path, database: Path) -> None:
    """Validate and atomically seed authored facts into a standalone database."""
    documents, errors = _read_sources(source_dir, repo_root, catalog_path)
    if errors:
        raise ValueError("\n".join(errors))
    catalog = load_json_strict(catalog_path)
    input_bytes = [catalog_path.read_bytes()]
    for path in sorted(source_dir.glob("*.json")):
        input_bytes.append(path.read_bytes())
    for doc in documents:
        input_bytes.append((repo_root / doc["derived_from"]["path"]).read_bytes())
    database.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".knowledge-", suffix=".sqlite", dir=database.parent)
    os.close(descriptor)
    try:
        with closing(sqlite3.connect(temporary)) as db:
            db.execute("PRAGMA foreign_keys=ON")
            db.executescript("""
                CREATE TABLE build_info (schema_version INTEGER NOT NULL, input_sha256 TEXT NOT NULL);
                CREATE TABLE documents (
                    id TEXT PRIMARY KEY, title TEXT NOT NULL, formly_version TEXT NOT NULL,
                    adapter TEXT NOT NULL, summary TEXT NOT NULL, source_path TEXT NOT NULL,
                    source_sha256 TEXT NOT NULL
                );
                CREATE TABLE facts (
                    id TEXT PRIMARY KEY, doc_id TEXT NOT NULL REFERENCES documents(id),
                    claim TEXT NOT NULL, conditions_json TEXT NOT NULL, limits_json TEXT NOT NULL,
                    context TEXT NOT NULL, source_quote TEXT NOT NULL,
                    source_start_offset INTEGER NOT NULL, source_end_offset INTEGER NOT NULL,
                    status TEXT NOT NULL CHECK (status='authored')
                );
                CREATE TABLE evidence (id TEXT PRIMARY KEY, record_json TEXT NOT NULL);
                CREATE TABLE fact_evidence (
                    fact_id TEXT NOT NULL REFERENCES facts(id),
                    evidence_id TEXT NOT NULL REFERENCES evidence(id),
                    PRIMARY KEY (fact_id, evidence_id)
                );
                CREATE TABLE fact_links (
                    source_fact_id TEXT NOT NULL REFERENCES facts(id),
                    target_fact_id TEXT NOT NULL REFERENCES facts(id),
                    kind TEXT NOT NULL CHECK (kind='see_also'),
                    PRIMARY KEY (source_fact_id, target_fact_id, kind)
                );
                CREATE VIRTUAL TABLE facts_fts USING fts5(
                    fact_id UNINDEXED, claim, context, conditions, limits,
                    document_title, document_summary, tokenize='unicode61'
                );
            """)
            used_evidence = {
                evidence_id
                for doc in documents for fact in doc["facts"]
                for evidence_id in fact["evidence_ids"]
            }
            for record in sorted(catalog["records"], key=lambda item: item["id"]):
                if record["id"] not in used_evidence:
                    continue
                db.execute("INSERT INTO evidence VALUES (?, ?)", (record["id"], json.dumps(record, sort_keys=True)))
            links = []
            for doc in documents:
                origin = doc["derived_from"]
                source_text = (repo_root / origin["path"]).read_text(encoding="utf-8")
                db.execute("INSERT INTO documents VALUES (?, ?, ?, ?, ?, ?, ?)", (
                    doc["id"], doc["title"], doc["formly_version"], doc["adapter"],
                    doc["summary"], origin["path"], origin["sha256"],
                ))
                for fact in doc["facts"]:
                    fact_id = f"{doc['id']}/{fact['id']}"
                    start = source_text.index(fact["source_quote"])
                    end = start + len(fact["source_quote"])
                    db.execute("INSERT INTO facts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        fact_id, doc["id"], fact["claim"], json.dumps(fact["conditions"]),
                        json.dumps(fact["limits"]), fact["context"], fact["source_quote"],
                        start, end, "authored",
                    ))
                    db.execute("INSERT INTO facts_fts VALUES (?, ?, ?, ?, ?, ?, ?)", (
                        fact_id, fact["claim"], fact["context"],
                        "\n".join(fact["conditions"]), "\n".join(fact["limits"]),
                        doc["title"], doc["summary"],
                    ))
                    for evidence_id in fact["evidence_ids"]:
                        db.execute("INSERT INTO fact_evidence VALUES (?, ?)", (fact_id, evidence_id))
                    links.extend((fact_id, link["target"], link["kind"]) for link in fact["related"])
            for link in links:
                db.execute("INSERT INTO fact_links VALUES (?, ?, ?)", link)
            if db.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("compiled knowledge contains broken references")
            db.execute("INSERT INTO build_info VALUES (?, ?)", (1, _sha(b"".join(input_bytes))))
            db.commit()
        os.replace(temporary, database)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
