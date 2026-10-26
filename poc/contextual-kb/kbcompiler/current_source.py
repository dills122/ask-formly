"""Active schema2 authoring interface; legacy compiler stays available for history."""
import tempfile
from pathlib import Path
from versioned_knowledge_v1.compiler import build as build_sources


def lint_sources(source_dir,repo_root,catalog_path):
    """Validate complete structure/provenance using a disposable candidate only."""
    try:
        with tempfile.TemporaryDirectory() as tmp:
            build_sources(source_dir,repo_root,catalog_path,Path(tmp)/'lint.sqlite')
    except (ValueError,OSError) as exc:
        return [str(exc)]
    return []
