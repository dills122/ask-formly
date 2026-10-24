"""Question-to-query contracts, independent of the seeded POC database."""

from __future__ import annotations

import sqlite3
import unittest
from contextlib import contextmanager
from collections.abc import Iterator

from kbcompiler.question_layer import QuestionLayer, QueryPlan, QueryPlanner, QueryProbe


@contextmanager
def fixture_db() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE documents(id TEXT PRIMARY KEY, formly_version TEXT, adapter TEXT)")
    db.execute("CREATE TABLE facts(id TEXT PRIMARY KEY, doc_id TEXT NOT NULL)")
    db.execute("CREATE VIRTUAL TABLE facts_fts USING fts5(fact_id UNINDEXED, body)")
    db.execute("INSERT INTO documents VALUES ('v6-core', '6.3.12', 'core')")
    rows = [
        ("conditional-hide", "Conditional visibility using a hide expression."),
        ("conditional-disabled", "Conditional disabled state using props.disabled expression."),
        ("hidden-control", "A hidden field unregisters its control."),
        ("hide-value", "A hidden field may clear its model value."),
        ("reset-false", "resetOnHide false keeps the saved model value."),
        ("wrapper-insertion", "A wrapper inserts the wrapped field component."),
    ]
    db.executemany("INSERT INTO facts VALUES (?, 'v6-core')", [(fact_id,) for fact_id, _ in rows])
    db.executemany("INSERT INTO facts_fts(fact_id, body) VALUES (?, ?)", rows)
    try:
        yield db
    finally:
        db.close()


class FakeIndex:
    ids = [
        "hide-value", "reset-false", "hidden-control", "wrapper-insertion",
        "conditional-hide", "conditional-disabled", "required-model",
        "shared-key", "unrelated", "extra-1", "extra-2",
        *[f"direct-{number}" for number in range(8)],
        *[f"base-{number}" for number in range(1, 9)],
        "side-value", "side-form", "side-stays", "side-around",
    ]

    def hybrid(self, question: str, limit: int) -> list[str]:
        return ["hide-value", "reset-false"][:limit]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        return selected[:limit]


class OverexpandingIndex(FakeIndex):
    def hybrid(self, question: str, limit: int) -> list[str]:
        return [f"direct-{number}" for number in range(limit)]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        return [*selected, "extra-1", "extra-2"]


class CrowdedIndex(FakeIndex):
    def hybrid(self, question: str, limit: int) -> list[str]:
        return ["base-1", "base-2", "base-3", "base-4", "base-5", "required-model", "base-7", "base-8"][:limit]


class RerankIndex(CrowdedIndex):
    facts = {
        "base-1": {"claim": "The field value can be retained.", "context": "Hidden value."},
        "shared-key": {"claim": "Fields may share a key.", "context": "Control reuse."},
        "hidden-control": {"claim": "Hiding a field unregisters its control.", "context": "Hidden control."},
        "wrapper-insertion": {"claim": "A wrapper inserts its field component.", "context": "Wrapper template."},
        "unrelated": {"claim": "A custom type has defaults.", "context": "Type settings."},
    }


class LeakyIndex(FakeIndex):
    ids = ["hide-value", "reset-false", "hidden-control"]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        return [*selected, "other-version-fact"]


class PreferAnswerReranker:
    def rerank(self, query: str, documents: list[str]) -> list[float]:
        return [10.0 if "unregisters" in doc or "inserts" in doc else 0.0
                for doc in documents]


class StubPlanner:
    def __init__(self, plan: QueryPlan) -> None:
        self.result = plan

    def plan(self, question: str) -> QueryPlan:
        return self.result


class CrowdedPlanner(QueryPlanner):
    def _hits(self, match: str) -> tuple[str, ...]:
        return (match,)


class QueryPlannerTest(unittest.TestCase):
    def test_conditional_hide_and_disable_get_distinct_db_queries(self) -> None:
        with fixture_db() as db:
            plan = QueryPlanner(db).plan(
                "How should I conditionally hide or disable a field, and what happens "
                "to its model value and control when hidden?"
            )
            hits = {probe.match: set(probe.fact_ids) for probe in plan.probes}
        self.assertTrue(any("conditional-hide" in ids and "conditional-disabled" not in ids
                            for ids in hits.values()))
        self.assertTrue(any("conditional-disabled" in ids and "conditional-hide" not in ids
                            for ids in hits.values()))
        self.assertTrue(any("hidden-control" in ids for ids in hits.values()))

    def test_camel_case_identifier_is_kept_and_component_terms_are_searchable(self) -> None:
        with fixture_db() as db:
            question = "Does resetOnHide: false keep the saved value and FormControl?"
            plan = QueryPlanner(db).plan(question)
        self.assertEqual(plan.semantic_query, question)
        self.assertIn("resetOnHide", plan.identifiers)
        self.assertIn("FormControl", plan.identifiers)
        self.assertTrue(any("reset-false" in probe.fact_ids for probe in plan.probes))
        self.assertTrue(any("hidden-control" in probe.fact_ids for probe in plan.probes))

    def test_unrelated_question_has_no_db_probe_and_no_fact_packet(self) -> None:
        with fixture_db() as db:
            result = QuestionLayer(db, FakeIndex()).query(
                "How does Formly connect to Stripe payment intents?"
            )
        self.assertEqual(result.status, "no_lexical_anchor")
        self.assertEqual(result.fact_ids, ())

    def test_explicit_other_version_stops_before_retrieval(self) -> None:
        with fixture_db() as db:
            result = QuestionLayer(db, FakeIndex()).query(
                "In Formly v7, is there a signals-only replacement for expressions?"
            )
        self.assertEqual(result.status, "version_unverified")
        self.assertEqual(result.fact_ids, ())

    def test_explicit_other_minor_or_patch_stops_before_retrieval(self) -> None:
        with fixture_db() as db:
            for version in ("v6.2", "6.3.11", "v6.4.0"):
                result = QuestionLayer(db, FakeIndex()).query(
                    f"In Formly {version}, does resetOnHide keep the value?"
                )
                self.assertEqual(result.status, "version_unverified", version)
                self.assertEqual(result.fact_ids, (), version)

    def test_explicit_baseline_version_is_accepted(self) -> None:
        with fixture_db() as db:
            for version in ("v6", "6.3", "v6.3.12"):
                result = QuestionLayer(db, FakeIndex()).query(
                    f"In Formly {version}, does resetOnHide keep the value?"
                )
                self.assertNotEqual(result.status, "version_unverified", version)

    def test_explicit_unsupported_ui_adapter_stops_before_retrieval(self) -> None:
        with fixture_db() as db:
            for label in ("Bootstrap Formly", "Formly Ionic", "@ngx-formly/primeng",
                          "Formly with Bootstrap", "Formly using Ionic"):
                result = QuestionLayer(db, FakeIndex()).query(
                    f"In {label}, does resetOnHide keep the value?"
                )
                self.assertEqual(result.status, "adapter_unverified", label)
                self.assertEqual(result.fact_ids, (), label)

    def test_explicit_supported_ui_adapter_is_accepted(self) -> None:
        with fixture_db() as db:
            for label in ("Material Formly", "@ngx-formly/core"):
                result = QuestionLayer(db, FakeIndex()).query(
                    f"In {label}, does resetOnHide keep the value?"
                )
                self.assertNotEqual(result.status, "adapter_unverified", label)

    def test_question_text_cannot_become_fts_syntax(self) -> None:
        with fixture_db() as db:
            plan = QueryPlanner(db).plan('props.disabled" OR * -- resetOnHide')
        self.assertEqual(plan.semantic_query, 'props.disabled" OR * -- resetOnHide')
        self.assertLessEqual(len(plan.probes), 12)

    def test_fts_probes_exclude_other_versions_and_adapters(self) -> None:
        with fixture_db() as db:
            db.executemany("INSERT INTO documents VALUES (?, ?, ?)", [
                ("v7-core", "7.0.0", "core"),
                ("v6-other", "6.3.12", "third-party"),
            ])
            db.executemany("INSERT INTO facts VALUES (?, ?)", [
                ("v7-signal", "v7-core"), ("other-control", "v6-other"),
            ])
            db.executemany("INSERT INTO facts_fts(fact_id, body) VALUES (?, ?)", [
                ("v7-signal", "Signal-only replacement for expressions."),
                ("other-control", "Stripe payment control adapter."),
            ])
            plan = QueryPlanner(db).plan("Can Stripe use a payment control?")
        self.assertFalse({"v7-signal", "other-control"} & {
            fact_id for probe in plan.probes for fact_id in probe.fact_ids
        })

    def test_packet_cap_holds_even_if_link_expander_overfills(self) -> None:
        with fixture_db() as db:
            result = QuestionLayer(db, OverexpandingIndex()).query("How does a wrapper insert a field?")
        self.assertEqual(len(result.fact_ids), 8)
        self.assertNotIn("extra-2", result.fact_ids)

    def test_link_expansion_cannot_add_out_of_scope_fact(self) -> None:
        with fixture_db() as db:
            result = QuestionLayer(db, LeakyIndex()).query(
                "Does resetOnHide false keep the saved value?"
            )
        self.assertNotIn("other-version-fact", result.fact_ids)

    def test_probe_expansion_does_not_discard_a_relevant_direct_candidate(self) -> None:
        question = "When an API value arrives, should I update the model?"
        probes = tuple(QueryProbe(f'"term{n}"', (f"side-{n}",), (f"term{n}",)) for n in range(4))
        with fixture_db() as db:
            layer = QuestionLayer(db, CrowdedIndex())
            layer.planner = StubPlanner(QueryPlan(question, (), probes))
            result = layer.query(question)
        self.assertIn("required-model", result.fact_ids)

    def test_explicit_api_component_has_a_packet_slot_among_generic_probes(self) -> None:
        question = "Does resetOnHide false keep the FormControl?"
        probes = (
            QueryProbe('"hide" AND "false"', ("base-1",), ("hide", "false")),
            QueryProbe('"saved" AND "value"', ("side-value",), ("saved", "value")),
            QueryProbe('"form"', ("side-form",), ("form",)),
            QueryProbe('"stays"', ("side-stays",), ("stays",)),
            QueryProbe('"around"', ("side-around",), ("around",)),
            QueryProbe('"control"', ("hidden-control",), ("control",)),
        )
        with fixture_db() as db:
            layer = QuestionLayer(db, CrowdedIndex())
            layer.planner = StubPlanner(QueryPlan(question, ("resetOnHide", "FormControl"), probes))
            result = layer.query(question)
        self.assertIn("hidden-control", result.fact_ids)

    def test_many_pair_queries_cannot_evict_api_component_probe(self) -> None:
        with fixture_db() as db:
            plan = CrowdedPlanner(db).plan(
                "If I hide a field and set resetOnHide to false, do both its saved "
                "value and FormControl stay around?"
            )
        self.assertTrue(any(probe.match == '"control"*' for probe in plan.probes))

    def test_focused_reranking_reaches_control_fact_below_bm25_neighbors(self) -> None:
        question = "Does hiding a field leave its FormControl registered?"
        probe = QueryProbe('"control"*',
                           ("base-1", "shared-key", "hidden-control"), ("control",))
        with fixture_db() as db:
            layer = QuestionLayer(db, RerankIndex(), reranker=PreferAnswerReranker())
            layer.planner = StubPlanner(QueryPlan(question, ("FormControl",), (probe,)))
            result = layer.query(question)
        self.assertIn("hidden-control", result.fact_ids)

    def test_focused_reranking_reaches_wrapper_fact_below_bm25_neighbors(self) -> None:
        question = "When should I use a wrapper instead of a custom type?"
        probe = QueryProbe('"wrapper"*',
                           ("base-1", "unrelated", "wrapper-insertion"), ("wrapper",))
        with fixture_db() as db:
            layer = QuestionLayer(db, RerankIndex(), reranker=PreferAnswerReranker())
            layer.planner = StubPlanner(QueryPlan(question, (), (probe,)))
            result = layer.query(question)
        self.assertIn("wrapper-insertion", result.fact_ids)


if __name__ == "__main__":
    unittest.main()
