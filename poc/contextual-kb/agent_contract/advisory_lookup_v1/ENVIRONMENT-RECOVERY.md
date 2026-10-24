# Environment recovery

The first live run used the retrieval environment and retained all outputs in test-output/live. It failed acceptance because torch was absent; zero native inference calls actually ran. Full-question searches continued with explicit extractor_load diagnostics, demonstrating the failure path but not native success.

The POC has separate existing environments: .venv provides fastembed retrieval, while gliner_feasibility/env/.venv provides torch/gliner2/peft but lacks fastembed. No existing environment is modified. A persistent local subprocess will run the frozen extractor in its own established environment, with structured JSON transport, while retrieval stays in its established environment. No network service is introduced.

Original cli.py, verify_live.py and README.md are preserved under test-output/failed-environment-source before correction. Original run-freeze.json and live-freeze.json remain historical evidence; the changed source paths must be checked against these archived copies when auditing that run. A new manifest/output directory binds the corrected run. No model predictions were discarded or tuned; the first native inference is still pending. This is an environment/integration correction, not a new extraction design.
