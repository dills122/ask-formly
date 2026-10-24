# Quality gates

Run python3 tools/project.py check (or npm run check) for local source/compiler and accepted MCP checks. Source-only CI uses python3 tools/project.py source and cannot qualify model inference or the installed service. Missing local assets must fail local qualification. Compiler tests use temporary fixtures; never rebuild the locked installed DB or open sealed evaluation during cleanup. Preserve known historical B06/B13 failures without presenting them as current test failures or new passes.
