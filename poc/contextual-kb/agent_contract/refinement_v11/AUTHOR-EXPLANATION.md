# Author explanation

V11 addresses v10 unknown-version normalization ambiguity, requested setup history versus local method restriction, and malformed hand-serialized batch. Only new v11 files, existing state frozen, sealed evaluation byte-only, no downstream or training/dependency work.

CHANGE clarifies wholly unknown version null vs tentative concrete/range strings; explicit unknown scope still in text/ledger. Same-field requested starting setup can remain history without imposing method restrictions on a future operation. Explicit independence overrides. No older regrade; diagnostic U22 criterion changes prospectively and cannot establish pure behavioral improvement. Other diagnostic rubrics unchanged.

New delivery.serialize_batch encodes already structured JSON-shaped record lists with standard json.dumps ensure_ascii=False/allow_nan=False. No semantic validation/filtering/repair; wrong-but-encodable plans retained. Reject nonlists/nonencodable data. Native generators construct first Python literal rows and use serializer once, retaining producer files. This enforces experiment transport, not a model-only or deployed API guarantee; future runtime integration outside this task. Reviewer must inspect scripts statically and compare bytes without rerunning them.

8selector+6delivery tests before implementation, red missing modules, green14.8v10 and8scorer regressions pass. Escaping/newlines/unicode roundtrip, nonfinite/unencodable rejection, semantics untouched and old malformed JSON remains rejected. These tests prove delivery properties and transport, not prompt semantics. Prompt22,859bytes vs20,999v10; no latency/cost measure.

24 independently authored policy-informed fresh requests,3x8 repeated3; six diagnostics repeated3,90first outputs. Candidate/input/raw/final freezes; every scheduled slot retained. No generator feedback, semantic validation before save, repair/resample or post-freeze tuning. Malformed packet fails all slots under prospective protocol. Full fresh24/24 anddiagnostic6/6 across3 gates; exactwording not semantic stability. Independent reviewer sees neutral bootstrap and all evidence before this account.

Preservation extends v10 final63files:39 manifests/38,688 overlapping entries. Native modelrevision/temp/seed uncontrolled, correlated synthetic development, no sealed evaluation or causal baseline comparison. Hashes establish bytes, not unseen attempts or independent timing. Risk: normalization/history instruction remains fallible, JSON shaping does not guarantee semantic schema validity, growing prompt costs unmeasured. Do not turn source ambiguity into an unqualified regression claim; retain frozen scores and separate sensitivities if needed.

Fresh review added only V09 expression-change event coverage before generation; original rubric retained. No requests changed. Diagnostic18responses saved with three producer scripts, byte-equivalent to standard encoding.

Execution complete:12packets all valid JSON and byte-equal to serialize_batch(AST literal rows);90/90 structural checks pass. Raw+producer freeze24entries. Independent reviewer has all originals; no author semantic grades supplied. No script reruns for verification: AST literal evaluation only.
