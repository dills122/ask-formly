"""Optional local-only trial of generated routing headmatter; never changes the corpus."""

from __future__ import annotations

import json
import sqlite3
import urllib.request
from pathlib import Path

from .__main__ import DATABASE, POC_ROOT


MODEL = "qwen2.5-coder:3b-instruct"
SAMPLE_IDS = (
    "formly.config-and-model.defaults-and-resets",
    "formly.expressions-and-lifecycle.callback-contracts",
    "formly.expressions-and-lifecycle.hiding-is-more-than-styling",
    "formly.customization.types-and-registration",
)


def trial() -> Path:
    output = POC_ROOT.parents[1] / "test-output" / "contextual-kb-headmatter-trial.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    with sqlite3.connect(f"file:{DATABASE}?mode=ro", uri=True) as connection:
        for unit_id in SAMPLE_IDS:
            row = connection.execute(
                "SELECT u.id, d.title, u.heading_path, u.body_md, u.about "
                "FROM units u JOIN documents d ON d.id=u.doc_id WHERE u.id=?", (unit_id,)
            ).fetchone()
            if row is None:
                raise ValueError(f"missing sample unit {unit_id}")
            prompt = (
                "Write a short routing description that helps a search system decide when to retrieve "
                "the passage below. Describe its subject and important conditions in 25 to 45 words. "
                "Use only facts explicitly stated in the passage. Do not add advice, infer compatibility, "
                "or answer a user question. Return JSON with one key: summary.\n\n"
                f"Document: {row[1]}\nHeading: {row[2]}\nPassage:\n{row[3]}"
            )
            payload = json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "format": {
                    "type": "object", "properties": {"summary": {"type": "string"}},
                    "required": ["summary"], "additionalProperties": False,
                },
                "options": {"temperature": 0},
            }).encode("utf-8")
            request = urllib.request.Request(
                "http://127.0.0.1:11434/api/generate", payload,
                {"Content-Type": "application/json"}, method="POST",
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.load(response)
            summary = json.loads(result["response"])["summary"]
            results.append({
                "unit_id": row[0], "extractive_about": row[4], "local_model_summary": summary,
                "model": MODEL, "total_duration_ns": result.get("total_duration"),
            })
    output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return output


if __name__ == "__main__":
    print(trial())
