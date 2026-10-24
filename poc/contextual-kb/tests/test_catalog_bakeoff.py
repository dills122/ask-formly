"""Contracts for the side-by-side catalog selection experiment."""

from __future__ import annotations

import unittest

from kbcompiler.catalog_bakeoff import (
    BroadPool, FactSelectionError, FullPool, select_facts, render_packet,
)
from kbcompiler.catalog_bakeoff_trial import row_for


FACTS = {
    "a": {"id": "a", "claim": "The model supplies the initial value.",
          "context": "Initial values.", "conditions": [], "limits": [],
          "version": "6.3.12", "adapter": "core"},
    "b": {"id": "b", "claim": "A default fills an undefined value.",
          "context": "Fallbacks.", "conditions": ["Only when eligible."],
          "limits": [], "version": "6.3.12", "adapter": "core"},
    "other": {"id": "other", "claim": "Another version behaves differently.",
              "context": "Other versions.", "conditions": [], "limits": [],
              "version": "7.0.0", "adapter": "core"},
}


class FakeIndex:
    ids = ["a", "b"]
    facts = FACTS

    def hybrid(self, question: str, limit: int) -> list[str]:
        return ["a", "other"][:limit]

    def add_links(self, selected: list[str], limit: int) -> list[str]:
        return [*selected, "other"][:limit]


class FakeProbe:
    fact_ids = ("b", "other")


class FakePlan:
    probes = (FakeProbe(),)


class FakePlanner:
    def plan(self, question: str) -> FakePlan:
        return FakePlan()


class CatalogBakeoffTest(unittest.TestCase):
    def test_full_pool_contains_every_scoped_fact(self) -> None:
        self.assertEqual(FullPool(FakeIndex()).candidates("How?"), ("a", "b"))

    def test_broad_pool_preserves_probe_only_fact_and_scope(self) -> None:
        ids = BroadPool(FakeIndex(), FakePlanner()).candidates("How?")
        self.assertEqual(ids, ("a", "b"))
        self.assertNotIn("other", ids)

    def test_selector_rejects_invented_id_instead_of_silently_dropping_it(self) -> None:
        with self.assertRaises(FactSelectionError):
            select_facts("How?", ("a", "b"), FACTS,
                         lambda prompt: {"ids": ["not-in-catalog"], "unresolved": []})

    def test_selector_rejects_more_than_packet_limit(self) -> None:
        ids = tuple(str(number) for number in range(9))
        facts = {fid: dict(FACTS["a"], id=fid) for fid in ids}
        with self.assertRaises(FactSelectionError):
            select_facts("How?", ids, facts,
                         lambda prompt: {"ids": list(ids), "unresolved": []})

    def test_selector_returns_only_fact_ids_and_unresolved_asks(self) -> None:
        result = select_facts("How?", ("a", "b"), FACTS,
                              lambda prompt: {"ids": ["b", "a"],
                                              "unresolved": ["Missing timing detail"]})
        self.assertEqual(result.fact_ids, ("b", "a"))
        self.assertEqual(result.unresolved, ("Missing timing detail",))
        self.assertNotIn("answer", result.__dict__)

    def test_packet_copies_database_claim_and_qualifications(self) -> None:
        packet = render_packet(("b",), FACTS)
        self.assertEqual(packet[0]["claim"], FACTS["b"]["claim"])
        self.assertEqual(packet[0]["conditions"], ["Only when eligible."])
        self.assertEqual(packet[0]["id"], "b")

    def test_scoring_keeps_coverage_separate_from_negative_support(self) -> None:
        positive = row_for({"id": "P", "required_fact_ids": ["a", "b"]},
                           "full_catalog", "selected_unverified", ("a",), FACTS)
        negative = row_for({"id": "N", "required_fact_ids": []},
                           "full_catalog", "selected_unverified", ("a",), FACTS,
                           unresolved=("No persistence evidence",))
        self.assertEqual(positive["missing_fact_ids"], ["b"])
        self.assertFalse(positive["complete_required_set"])
        self.assertFalse(negative["negative_empty"])
        self.assertTrue(negative["negative_flagged"])

    def test_selector_error_is_not_a_successful_negative_abstention(self) -> None:
        failed = row_for({"id": "N", "required_fact_ids": []},
                         "broad_24", "selector_error", (), FACTS)
        self.assertTrue(failed["negative_empty"])
        self.assertFalse(failed["negative_successful_abstention"])


if __name__ == "__main__":
    unittest.main()
