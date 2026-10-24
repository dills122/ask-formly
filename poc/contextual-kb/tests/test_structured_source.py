"""A controlled source record compiles into cited facts without prose splitting."""

import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from kbcompiler.structured_source import build_sources, lint_sources
from kbcompiler.structured_audit import audit
from kbcompiler.db_query_trial import run_trial


class StructuredSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.authored = self.root / "authored"
        self.authored.mkdir()
        source = self.root / "research.md"
        source.write_text(
            "A default applies to undefined values [K05](sources.md#k05).\n"
            "Reset restores a baseline [K05](sources.md#k05), [E07](examples.md#e07).\n",
            encoding="utf-8",
        )
        self.source = source
        self.catalog = self.root / "catalog.json"
        self.catalog.write_text(json.dumps({
            "baseline": "6.3.12",
            "records": [{"id": "K05"}, {"id": "E07"}, {"id": "K99"}],
        }), encoding="utf-8")
        self.document = {
            "schema_version": 1,
            "id": "defaults",
            "title": "Defaults and resets",
            "formly_version": "6.3.12",
            "adapter": "core",
            "summary": "Defaults and reset baselines in Formly core.",
            "derived_from": {
                "path": "research.md",
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            },
            "facts": [
                {
                    "id": "default-when-undefined",
                    "claim": "Formly applies a configured default to an undefined keyed value.",
                    "conditions": ["The field is eligible for defaulting."],
                    "limits": ["An existing value is retained."],
                    "context": "Default value eligibility for a keyed Formly field.",
                    "source_quote": "A default applies to undefined values [K05](sources.md#k05).",
                    "evidence_ids": ["K05"],
                    "related": [],
                },
                {
                    "id": "reset-baseline",
                    "claim": "resetModel restores the saved baseline.",
                    "conditions": [],
                    "limits": [],
                    "context": "Reset behavior after an initial value was recorded.",
                    "source_quote": "Reset restores a baseline [K05](sources.md#k05), [E07](examples.md#e07).",
                    "evidence_ids": ["K05", "E07"],
                    "related": [{"kind": "see_also", "target": "defaults/default-when-undefined"}],
                },
            ],
        }
        self.path = self.authored / "defaults.json"
        self.write_document()
        self.database = self.root / "knowledge.sqlite"

    def write_document(self):
        self.path.write_text(json.dumps(self.document, indent=2) + "\n", encoding="utf-8")

    def test_compiles_claims_conditions_provenance_evidence_and_links(self):
        self.assertEqual([], lint_sources(self.authored, self.root, self.catalog))
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            facts = db.execute("SELECT id, claim, conditions_json, limits_json, context, source_quote, source_start_offset, source_end_offset, status FROM facts ORDER BY id").fetchall()
            evidence = db.execute("SELECT fact_id, evidence_id FROM fact_evidence ORDER BY fact_id, evidence_id").fetchall()
            links = db.execute("SELECT source_fact_id, target_fact_id, kind FROM fact_links").fetchall()
            evidence_rows = db.execute("SELECT id FROM evidence ORDER BY id").fetchall()
            integrity = db.execute("PRAGMA foreign_key_check").fetchall()
        self.assertEqual(2, len(facts))
        self.assertEqual("authored", facts[0][8])
        self.assertEqual(["The field is eligible for defaulting."], json.loads(facts[0][2]))
        self.assertEqual(["An existing value is retained."], json.loads(facts[0][3]))
        source = self.source.read_text(encoding="utf-8")
        for row in facts:
            self.assertEqual(row[5], source[row[6]:row[7]])
        self.assertEqual([
            ("defaults/default-when-undefined", "K05"),
            ("defaults/reset-baseline", "E07"),
            ("defaults/reset-baseline", "K05"),
        ], evidence)
        self.assertEqual([("defaults/reset-baseline", "defaults/default-when-undefined", "see_also")], links)
        self.assertEqual([("E07",), ("K05",)], evidence_rows)
        self.assertEqual([], integrity)

    def test_contextual_fts_candidates_and_packet_joins(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(f"file:{self.database}?mode=ro", uri=True) as db:
            candidates = db.execute("""
                SELECT f.id FROM facts_fts s
                JOIN facts f ON f.id = s.fact_id
                JOIN documents d ON d.id = f.doc_id
                WHERE facts_fts MATCH ? AND d.formly_version = ? AND d.adapter = ?
                ORDER BY bm25(facts_fts), f.id LIMIT 5
            """, ("eligibility", "6.3.12", "core")).fetchall()
            wrong_version = db.execute("""
                SELECT f.id FROM facts_fts s
                JOIN facts f ON f.id = s.fact_id
                JOIN documents d ON d.id = f.doc_id
                WHERE facts_fts MATCH ? AND d.formly_version = ?
            """, ("eligibility", "7.0.0")).fetchall()
            packet = db.execute("""
                SELECT f.claim, f.conditions_json, f.limits_json, d.source_path,
                       fe.evidence_id, fl.target_fact_id
                FROM facts f JOIN documents d ON d.id = f.doc_id
                JOIN fact_evidence fe ON fe.fact_id = f.id
                LEFT JOIN fact_links fl ON fl.source_fact_id = f.id
                WHERE f.id = ?
            """, ("defaults/reset-baseline",)).fetchall()
        self.assertEqual([("defaults/default-when-undefined",)], candidates)
        self.assertEqual([], wrong_version)
        self.assertEqual({"E07", "K05"}, {row[4] for row in packet})
        self.assertEqual({"defaults/default-when-undefined"}, {row[5] for row in packet})

    def test_trial_queries_candidates_then_expands_links_and_reads_packets(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        fixture = {
            "baseline": "6.3.12", "adapters": ["core"], "limit_per_query": 5,
            "cases": [{
                "id": "T1", "matches": ["baseline"],
                "required_fact_ids": ["defaults/default-when-undefined"],
            }],
        }
        result = run_trial(self.database, fixture)
        case = result["cases"][0]
        self.assertEqual(["defaults/reset-baseline"], case["candidate_ids"])
        self.assertIn("defaults/default-when-undefined", case["expanded_ids"])
        self.assertFalse(case["candidate_complete"])
        self.assertTrue(case["expanded_complete"])
        self.assertTrue(case["packets_have_evidence"])

    def test_rejects_stale_source_quote_and_unknown_evidence_without_replacing_db(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        before = self.database.read_bytes()
        self.document["facts"][0]["source_quote"] = "Invented quote [K05](sources.md#k05)."
        self.write_document()
        self.assertTrue(any("source_quote" in error for error in lint_sources(self.authored, self.root, self.catalog)))
        with self.assertRaises(ValueError):
            build_sources(self.authored, self.root, self.catalog, self.database)
        self.assertEqual(before, self.database.read_bytes())
        self.document["facts"][0]["source_quote"] = "A default applies to undefined values [K05](sources.md#k05)."
        self.document["facts"][0]["evidence_ids"] = ["K99"]
        self.write_document()
        self.assertTrue(any("K99" in error for error in lint_sources(self.authored, self.root, self.catalog)))

    def test_rejects_bad_relation_duplicate_id_and_extra_fields(self):
        self.document["facts"][1]["related"][0]["target"] = "defaults/missing"
        self.write_document()
        self.assertTrue(any("missing" in error for error in lint_sources(self.authored, self.root, self.catalog)))
        self.document["facts"][1]["related"][0]["target"] = "defaults/default-when-undefined"
        self.document["facts"][1]["id"] = "default-when-undefined"
        self.write_document()
        self.assertTrue(any("duplicate" in error for error in lint_sources(self.authored, self.root, self.catalog)))
        self.document["facts"][1]["id"] = "reset-baseline"
        self.document["facts"][1]["confidence"] = 0.99
        self.write_document()
        self.assertTrue(any("unknown" in error for error in lint_sources(self.authored, self.root, self.catalog)))

    def test_rebuild_is_logically_identical(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            first = (db.execute("SELECT * FROM facts ORDER BY id").fetchall(),
                     db.execute("SELECT * FROM fact_links ORDER BY source_fact_id").fetchall(),
                     db.execute("SELECT * FROM build_info").fetchall())
        self.database.unlink()
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            second = (db.execute("SELECT * FROM facts ORDER BY id").fetchall(),
                      db.execute("SELECT * FROM fact_links ORDER BY source_fact_id").fetchall(),
                      db.execute("SELECT * FROM build_info").fetchall())
        self.assertEqual(first, second)

    def test_duplicate_document_id_fails_lint_before_seeding(self):
        (self.authored / "copy.json").write_text(self.path.read_text(encoding="utf-8"), encoding="utf-8")
        self.assertTrue(any("duplicate document id" in error for error in lint_sources(self.authored, self.root, self.catalog)))
        with self.assertRaises(ValueError):
            build_sources(self.authored, self.root, self.catalog, self.database)

    def test_audit_checks_seeded_fact_against_authored_source(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        result = audit(self.authored, self.root, self.catalog, self.database)
        self.assertEqual((1, 2, 3, 1), (
            result["documents"], result["facts"],
            result["fact_evidence_links"], result["fact_links"],
        ))
        with sqlite3.connect(self.database) as db:
            db.execute("UPDATE facts SET claim='invented' WHERE id='defaults/reset-baseline'")
        with self.assertRaisesRegex(ValueError, "seeded facts differ"):
            audit(self.authored, self.root, self.catalog, self.database)

    def test_audit_detects_changed_evidence_record(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            db.execute("UPDATE evidence SET record_json='{}' WHERE id='K05'")
        with self.assertRaisesRegex(ValueError, "seeded evidence catalog differs"):
            audit(self.authored, self.root, self.catalog, self.database)

    def test_audit_detects_missing_contextual_search_row(self):
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            db.execute("DELETE FROM facts_fts WHERE fact_id=?", ("defaults/reset-baseline",))
        with self.assertRaisesRegex(ValueError, "search index differs"):
            audit(self.authored, self.root, self.catalog, self.database)

    def test_duplicate_json_key_is_rejected_before_facts_can_be_lost(self):
        raw = self.path.read_text(encoding="utf-8")
        self.path.write_text(raw.replace('"facts": [', '"facts": [],\n  "facts": [', 1), encoding="utf-8")
        errors = lint_sources(self.authored, self.root, self.catalog)
        self.assertTrue(any("duplicate JSON key facts" in error for error in errors))
        with self.assertRaises(ValueError):
            build_sources(self.authored, self.root, self.catalog, self.database)

    def test_non_utf8_source_is_reported_as_lint_error(self):
        self.source.write_bytes(b"\xff")
        self.document["derived_from"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.write_document()
        errors = lint_sources(self.authored, self.root, self.catalog)
        self.assertTrue(any("research.md" in error and "UTF-8" in error for error in errors))

    def test_evidence_link_target_is_valid_with_descriptive_label(self):
        source = self.source.read_text(encoding="utf-8").replace(
            "[K05](sources.md#k05)", "[Core defaults](sources.md#k05)", 1,
        )
        self.source.write_text(source, encoding="utf-8")
        self.document["derived_from"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.document["facts"][0]["source_quote"] = source.splitlines()[0]
        self.write_document()
        self.assertEqual([], lint_sources(self.authored, self.root, self.catalog))
        build_sources(self.authored, self.root, self.catalog, self.database)
        with sqlite3.connect(self.database) as db:
            self.assertEqual(
                [("defaults/default-when-undefined", "K05")],
                db.execute(
                    "SELECT fact_id, evidence_id FROM fact_evidence WHERE fact_id=?",
                    ("defaults/default-when-undefined",),
                ).fetchall(),
            )

        source = source.replace("[Core defaults](sources.md#k05)", "[Core defaults](sources.md#k99)", 1)
        self.source.write_text(source, encoding="utf-8")
        self.document["derived_from"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.document["facts"][0]["source_quote"] = source.splitlines()[0]
        self.write_document()
        self.assertTrue(any("K05 is not cited" in error for error in lint_sources(self.authored, self.root, self.catalog)))


if __name__ == "__main__":
    unittest.main()
