"""Small behavioral checks for the isolated question-path pilot."""

from __future__ import annotations

import sqlite3
import unittest

from kbcompiler.question_pilot import (
    explicit_other_version,
    fts_matches,
    merge_obligations,
    reciprocal_rank_fusion,
    valid_fact_ids,
)


class QuestionPilotTest(unittest.TestCase):
    def test_fts_query_handles_dotted_api_identifiers_without_sql_syntax_error(self) -> None:
        with sqlite3.connect(":memory:") as db:
            db.execute("CREATE VIRTUAL TABLE facts_fts USING fts5(body, tokenize='unicode61')")
            db.execute("INSERT INTO facts_fts VALUES (?)", ("Use props.disabled for a disabled expression",))
            matches = fts_matches(db, "props.disabled?", limit=5)
        self.assertEqual(matches, [1])

    def test_rank_fusion_rewards_a_fact_found_by_both_retrievers(self) -> None:
        ranked = reciprocal_rank_fusion([["a", "shared"], ["shared", "b"]])
        self.assertEqual(ranked[0], "shared")

    def test_packet_budget_gives_each_obligation_a_chance(self) -> None:
        result = merge_obligations([["a", "b", "c"], ["d", "e"]], limit=3)
        self.assertEqual(result, ["a", "d", "b"])

    def test_selector_cannot_invent_ids_or_exceed_budget(self) -> None:
        ids = valid_fact_ids(["known", "made-up", "known", "other"], {"known", "other"}, 1)
        self.assertEqual(ids, ["known"])

    def test_explicit_other_major_version_is_not_served_as_v6(self) -> None:
        self.assertTrue(explicit_other_version("How does Formly v7 use signals?", "6.3.12"))
        self.assertFalse(explicit_other_version("How does Formly v6 handle props?", "6.3.12"))
        self.assertFalse(explicit_other_version("How do I disable a field?", "6.3.12"))


if __name__ == "__main__":
    unittest.main()
