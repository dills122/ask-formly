"""The answer diagnostic cannot turn selector output into trusted evidence."""

from __future__ import annotations

import unittest

from kbcompiler.catalog_answer_trial import (
    answer_from_packet, diagnostic_status, validate_answer,
)


PACKET = [{"id": "fact-1", "claim": "A default fills undefined values.",
           "context": "Defaults", "conditions": [], "limits": []}]


class CatalogAnswerTrialTest(unittest.TestCase):
    def test_answer_cannot_cite_a_fact_outside_packet(self) -> None:
        with self.assertRaises(ValueError):
            validate_answer({"claims": [{"text": "Unsupported", "fact_ids": ["other"]}],
                             "unresolved": []}, PACKET)

    def test_empty_packet_avoids_model_call(self) -> None:
        def forbidden(prompt: str) -> object:
            raise AssertionError("model must not be called")

        result = answer_from_packet("What happens?", [], forbidden)
        self.assertEqual(result["claims"], [])
        self.assertEqual(result["unresolved"], ["What happens?"])

    def test_valid_answer_keeps_claim_citations(self) -> None:
        result = validate_answer({
            "claims": [{"text": "A default fills undefined values.",
                        "fact_ids": ["fact-1"]}], "unresolved": [],
        }, PACKET)
        self.assertEqual(result["claims"][0]["fact_ids"], ["fact-1"])

    def test_upstream_selector_error_remains_visible_in_answer_diagnostic(self) -> None:
        self.assertEqual(diagnostic_status("selector_error"),
                         "upstream_selector_error")


if __name__ == "__main__":
    unittest.main()
