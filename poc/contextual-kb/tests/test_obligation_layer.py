"""Contracts for the bounded, read-only obligation-planning experiment."""

from __future__ import annotations

import sqlite3
import unittest
from contextlib import contextmanager
from collections.abc import Iterator
from types import SimpleNamespace

from kbcompiler.obligation_layer import (
    DeterministicObligationPlanner, ModelSpanPlanner, ObligationQueryLayer,
    validate_spans,
)
from kbcompiler.obligation_trial import complete_case
from kbcompiler.evidence_check import validate_assessments


@contextmanager
def fixture_db() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE documents(id TEXT PRIMARY KEY, formly_version TEXT, adapter TEXT)")
    db.execute("CREATE TABLE facts(id TEXT PRIMARY KEY, doc_id TEXT NOT NULL)")
    db.execute("CREATE VIRTUAL TABLE facts_fts USING fts5(fact_id UNINDEXED, body)")
    db.execute("INSERT INTO documents VALUES ('v6-core', '6.3.12', 'core')")
    rows = [
        ("hide-target", "Conditionally hide a field with an expression."),
        ("disable-target", "Conditionally disable a field with props disabled."),
        ("value-effect", "Hiding can clear a model value."),
        ("control-effect", "A hidden field unregisters its control."),
    ]
    db.executemany("INSERT INTO facts VALUES (?, 'v6-core')", [(key,) for key, _ in rows])
    db.executemany("INSERT INTO facts_fts(fact_id,body) VALUES (?,?)", rows)
    try:
        yield db
    finally:
        db.close()


class FakeIndex:
    ids = ["hide-target", "disable-target", "value-effect", "control-effect"]
    facts = {
        "hide-target": {"claim": "Conditionally hide a field with an expression.", "context": "visibility"},
        "disable-target": {"claim": "Conditionally disable a field with props.disabled.", "context": "state"},
        "value-effect": {"claim": "Hiding can clear a model value.", "context": "hidden value"},
        "control-effect": {"claim": "A hidden field unregisters its control.", "context": "hidden control"},
    }

    def hybrid(self, text: str, limit: int) -> list[str]:
        return ["value-effect", "hide-target", "disable-target", "control-effect"][:limit]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        return selected[:limit]


class StubPlanner:
    def __init__(self, spans: tuple[str, ...]) -> None:
        self.spans = spans

    def plan(self, question: str) -> tuple[str, ...]:
        return self.spans


class TermReranker:
    def rerank(self, query: str, documents: list[str]) -> list[float]:
        words = {word.lower() for word in query.split()}
        return [sum(word in doc.lower() for word in words) for doc in documents]


class ObligationLayerTest(unittest.TestCase):
    def test_evidence_check_rejects_unlisted_and_uncited_support(self) -> None:
        obligations = (
            SimpleNamespace(candidate_ids=("hide-target",)),
            SimpleNamespace(candidate_ids=()),
        )
        valid = {"assessments": [
            {"index": 0, "supported": True, "fact_ids": ["hide-target"]},
            {"index": 1, "supported": False, "fact_ids": []},
        ]}
        self.assertEqual(validate_assessments(valid, obligations),
                         ((True, ("hide-target",)), (False, ())))
        with self.assertRaises(ValueError):
            validate_assessments({"assessments": [
                {"index": 0, "supported": True, "fact_ids": ["invented"]},
                {"index": 1, "supported": False, "fact_ids": []},
            ]}, obligations)
        with self.assertRaises(ValueError):
            validate_assessments({"assessments": [
                {"index": 0, "supported": True, "fact_ids": []},
                {"index": 1, "supported": False, "fact_ids": []},
            ]}, obligations)

    def test_complete_case_requires_every_ask_to_have_candidates(self) -> None:
        case = {"required_fact_ids": ["control-effect"]}
        result = SimpleNamespace(status="unresolved", fact_ids=("control-effect",))
        self.assertFalse(complete_case(case, result))

    def test_deterministic_planner_separates_compound_asks(self) -> None:
        question = "Should I conditionally hide or disable a field, and what happens to its model value and control when hidden?"
        spans = DeterministicObligationPlanner().plan(question)
        self.assertTrue(any("hide" in span and "disable" not in span for span in spans))
        self.assertTrue(any("disable" in span and "hide" not in span for span in spans))
        self.assertTrue(any("value" in span and "control" not in span for span in spans))
        self.assertTrue(any("control" in span and "value" not in span for span in spans))

    def test_model_spans_must_be_literal_and_preserve_api_identifiers(self) -> None:
        question = "Does resetOnHide affect the model value and FormControl?"
        self.assertEqual(validate_spans(question, ["resetOnHide", "model value", "FormControl"]),
                         ("resetOnHide", "model value", "FormControl"))
        with self.assertRaises(ValueError):
            validate_spans(question, ["hidden control"])
        with self.assertRaises(ValueError):
            validate_spans(question, ["model value", "FormControl"])

    def test_model_planner_falls_back_if_output_is_not_lossless(self) -> None:
        question = "Does resetOnHide affect the model value and FormControl?"
        planner = ModelSpanPlanner(lambda _: {"spans": ["model value"]})
        spans = planner.plan(question)
        self.assertIn("resetOnHide", " ".join(spans))
        self.assertTrue(planner.used_fallback)

    def test_model_planner_falls_back_if_local_daemon_is_unavailable(self) -> None:
        def unavailable(_: str) -> object:
            raise OSError("local daemon unavailable")

        planner = ModelSpanPlanner(unavailable)
        spans = planner.plan("Should I hide or disable a field?")
        self.assertTrue(planner.used_fallback)
        self.assertGreaterEqual(len(spans), 2)

    def test_each_obligation_retrieves_before_global_budget(self) -> None:
        question = "Should I hide or disable a field, and what happens to its value and control?"
        planner = StubPlanner(("hide", "disable", "value", "control"))
        with fixture_db() as db:
            result = ObligationQueryLayer(db, FakeIndex(), TermReranker()).query(question, planner)
        self.assertEqual(len(result.obligations), 4)
        self.assertTrue(all(item.candidate_ids for item in result.obligations))
        self.assertIn("control-effect", result.fact_ids)
        self.assertIn("disable-target", result.fact_ids)

    def test_unknown_technical_ask_is_unresolved_not_dense_only_support(self) -> None:
        question = "Which PostgreSQL persistence pattern should I use?"
        with fixture_db() as db:
            result = ObligationQueryLayer(db, FakeIndex(), TermReranker()).query(
                question, StubPlanner(("PostgreSQL persistence",)),
            )
        self.assertEqual(result.status, "unresolved")
        self.assertEqual(result.fact_ids, ())

    def test_one_unresolved_ask_blocks_the_merged_fact_packet(self) -> None:
        with fixture_db() as db:
            result = ObligationQueryLayer(db, FakeIndex(), TermReranker()).query(
                "How do I hide a field using PostgreSQL?",
                StubPlanner(("hide a field", "PostgreSQL")),
            )
        self.assertEqual(result.status, "unresolved")
        self.assertTrue(result.obligations[0].candidate_ids)
        self.assertEqual(result.fact_ids, ())

    def test_scope_gate_precedes_planning_and_retrieval(self) -> None:
        with fixture_db() as db:
            layer = ObligationQueryLayer(db, FakeIndex(), TermReranker())
            self.assertEqual(layer.query("In Formly v7, hide a field?", StubPlanner(("hide",))).status,
                             "version_unverified")
            self.assertEqual(layer.query("Formly with Bootstrap hide?", StubPlanner(("hide",))).status,
                             "adapter_unverified")


if __name__ == "__main__":
    unittest.main()
