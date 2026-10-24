# Findings

- Best configurations recorded before experiment in POC BEST-QUESTION-CONFIGURATIONS.md; evidence panels remain distinct.
- Fixed public NLI revision:8e7e5af5983a0ddb1a5b45a38b129ab69e2258e8. Downloaded seven files into local model directory; existing environment unchanged.
- Installed Transformers5.20.2, torch2.14.1, huggingface_hub2.2.0. sentencepiece distribution absent, but AutoTokenizer successfully loads the supplied tokenizer and tokenizes sentence pairs. Binary label map0=entailment,1=not_entailment verified from config. No forward inference during preparation.
- NLI model card documents direct AutoModelForSequenceClassification and binary entailment; Transformers main documentation was available during research. Attempt to fetch version-specific5.20.2 pipeline URL failed in browser; direct installed API is the compatibility source, not a claimed successful versioned-doc fetch.
- Graph index_status/search_graph/check_index_coverage all returned Transport closed. Direct source fallback used for POC dependencies.
- Fresh24 self-authored questions form12 paired cases. No normalized duplicates against302 exposed training/shadow/adjudicated rows. Thematic overlap is intentional, not independent unseen traffic.
- All30 existing beta1 requests yield60 library questions; the complete panel is included to avoid selecting favorable v2 outputs. This is cached v2 generation with newly executed extraction, not a new agent robustness evaluation.
