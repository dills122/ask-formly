# Fresh correction review bootstrap

Review instance2of3 of the user-authorized isolated reliability fix. Read this first, record preliminary findings before REVIEW-2-AUTHOR.md. Use independent-review reviewer mode, read-only; no source edits, hosted calls, DB builds, sealed evaluation, extra agents or new workstreams.

Repo /Users/dsteele/repos/ask-formly; branch codex/readme-verified-branches HEAD881afd2; changes untracked under poc/contextual-kb/knowledge-expansion/reliability-v1. Preserve all existing candidates/setup/models/DB.

Review current capitalization.py, test_capitalization.py, PLAN.md, run.py/CALLER.md/transport.py/server.py as necessary. Main target: quoted-region protection and retained API/literal/source/binding checks. Review1 found a literal rewrite and blocked live regression. Now16 tests pass; raw red/green evidence under test-output/quote-red.txt and quote-green.txt. Confirm correction, assess boundaries and qualification plan; verdict is readiness for frozen repeated inference, not adoption.

Run poc/contextual-kb/mcp_v1/.venv/bin/python -B -m unittest discover -s poc/contextual-kb/knowledge-expansion/reliability-v1 -p 'test_*.py'. Prior accepted project check passed under test-output/accepted-regressions.txt. Old raw qualification remains under custom-types-v1/test-output/qualification-1; not sealed evaluation. New fresh-cases.json is visible and not yet used. Freeze all behavior-bearing dependencies before inference. Reserve final review3 for completed results.
