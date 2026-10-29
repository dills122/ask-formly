# Isolated answer response v1

This candidate projects the existing lookup's selected complete facts into a
smaller answer view. It changes neither ranking nor lookup capacity. Default
fact fetch returns the same fact objects with lightweight evidence citations.
`get_formly_provenance` returns the exact original citation records when detailed
quotes, hashes or authored offsets are needed. Both paths validate every ID and
scope before delivery and use measured bounded retries instead of partial data.

It is not connected to the installed launcher or release manifest. Run explicitly:

```sh
python poc/contextual-kb/answer_response_v1/serve.py \
  --database /absolute/path/to/knowledge.sqlite \
  --sha256 ACTUAL_PINNED_DATABASE_SHA256 \
  --settings /absolute/path/to/disposable/settings.sqlite
```

Use the existing MCP Python environment. The DB opens through the unchanged
read-only verified Store. Settings are separate from knowledge. Initialize and
help report an `answer-response-v1+…` identity hashing this candidate and its
baseline runtime dependencies. Facts, installed DB and recipe storage are not
modified. See the investigation's current docs for comparison results.

## Excerpts and dependency identity

Lightweight citations explicitly mark whether a nonblank evidence excerpt is
stored. Detailed provenance keeps exact original citation records and adds
availability/stopping guidance separately. Missing stored excerpts are not
claims of globally missing source text; authored summary quotes remain distinct
from implementation evidence. Switching formats or repeatedly fetching the same
IDs cannot add missing stored text. Other facts or pinned external sources may
still be useful for a legitimate unresolved request.

The identity verifies actual bytes for every non-DB file pinned by the baseline
runtime manifest, then includes explicit candidate files, required non-code resources (including
`mcp_v1/versions.json`) and a checked static
local import closure rooted at this server. It includes previously omitted
`mcp_foundation/capitalization.py` and checks reachable helpers rather than
assuming every historical refinement directory is active. Unresolved local
imports, missing dependencies, changed baseline pins and recognized dynamic
loading fail closed. Bare-import aliases are explicit for the baseline's path
setup. New import styles need review. Staging exactly `identity()['files']` under
a new POC root produces the same identity without copying unrelated plan/history
documents. Runtime dependency verification occurs when the server is created;
it is not continuous monitoring of source edits after startup.

The source identity excludes Python and third-party implementation bytes; it
reports the baseline's expected third-party versions rather than asserting the
installed versions match them. The DB is verified separately by the unchanged
Store using the explicit hash supplied on launch. The source identity alone does
not qualify the environment or prove database identity.

The minimal staging contract includes the version catalog read by VersionResolver
at service construction. Resource coverage is explicitly reviewed alongside the
static import closure; static imports alone do not discover data-file reads.
A real stdio startup/help/lookup/fetch/provenance smoke verifies the staged runtime.

## Recovery guidance

Discovery's schema requires the original non-null plan on every call. Valid-shaped
plan repair feedback names discovery and preserves its selectors instead of
sending callers back to lookup. No plan is reconstructed from session history.
Caller guidance distinguishes reuse of an identical scoped source-evidence record
from fetching distinct per-fact authored provenance. Requested details remain
available even when another fact cited the same evidence. No ranking, metadata
format or provenance deduplication changes are made in this recovery follow-up.

The selection-first follow-up changes caller guidance only: map unmet facets to
current candidate claims/conditions/limits and fetch suitable selected IDs before
more paging. Examples can provide limited support without proving a full
contract. Discovery replaces its existing next-action prose with a shorter
message, recomputes byte measurements, and preserves every candidate and paging
field. Empty/exhausted results and error behavior remain unchanged.
