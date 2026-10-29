# Isolated linked examples candidate

This server adds candidate examples to the existing fact workflow. It does not
promote examples into the installed knowledge database or establish new facts.
Use facts with their conditions, limits and provenance before selecting code.

Lookup and compact fact fetch may include `example_references`. These references
are optional under the unchanged fact byte budget: even when absent, call
`get_formly_examples(fact_ids=[...])` with relevant returned fact IDs to list
examples. Repeat the resolved Formly version and adapter. List results contain
summaries, links and verification; they do not contain code. Follow `next_offset`
until sufficient or exhausted. An empty result means no linked example in this
candidate catalog, not that the behavior is impossible.

Fetch chosen IDs with `get_formly_examples(example_ids=[...])`. Full examples
contain complete files and hashes, prerequisites, assertions, provenance, limits
and per-fact support. For large examples use `file_paths` to request complete
individual files. Never present a subset as a complete runnable project. A file
that exceeds the response budget is rejected rather than silently truncated.

Verification states distinguish illustrations, source review, and actual recorded
execution. Source review is not execution. Execution describes only its pinned
environment and assertions; it is not universal compatibility. Example code can
contain application decisions beyond the linked facts. Disclose those limits.
These examples support only Formly 6.3.12 with Material. Unsupported scope stops;
do not silently substitute the candidate scope or rewrite the original question.
