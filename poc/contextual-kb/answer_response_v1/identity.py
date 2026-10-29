"""Portable identity over pinned runtime bytes and a checked local import closure."""
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

POC = Path(__file__).resolve().parents[1]
CANDIDATE_FILES = (
    'answer_response_v1/__init__.py', 'answer_response_v1/candidate.py',
    'answer_response_v1/identity.py', 'answer_response_v1/serve.py',
    'answer_response_v1/CALLER.md', 'answer_response_v1/README.md',
)
# Required non-code read at service construction. Other current reads are
# already in the baseline/candidate map or are explicit DB/settings inputs.
RUNTIME_RESOURCES = ('mcp_v1/versions.json',)

# These baseline modules deliberately use bare imports after inserting their
# sibling directory into sys.path. Ambiguous names are resolved explicitly.
LOCAL_ALIASES = {
    'candidate': 'model_free_v1/candidate.py',
    'feedback': 'model_free_repair_v1/feedback.py',
    'serve': 'model_free_repair_v1/serve.py',
    'discovery': 'parity_v1/discovery.py',
    'contract': 'agent_contract/contract.py',
    'project_settings': 'mcp_v1/project_settings.py',
    'versioning': 'mcp_v1/versioning.py',
}
THIRD_PARTY_ROOTS = {'mcp', 'pydantic', 'semantic_version'}
DYNAMIC_IMPORT_CALLS = {'__import__', 'exec', 'eval', 'import_module',
                        'spec_from_file_location', 'SourceFileLoader',
                        'exec_module', 'run_module', 'run_path'}


def _read(root, relative):
    name = PurePosixPath(relative)
    if name.is_absolute() or '..' in name.parts or not name.parts:
        raise ValueError('Unsafe runtime identity path: ' + relative)
    path = root.joinpath(*name.parts)
    if not path.is_file():
        raise ValueError('Missing runtime identity dependency: ' + relative)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Runtime identity dependency escapes its root: ' + relative)
    return path.read_bytes()


def _local_module(root, name):
    if name in LOCAL_ALIASES:
        return LOCAL_ALIASES[name]
    relative = name.replace('.', '/')
    for candidate in (relative + '.py', relative + '/__init__.py'):
        if (root / candidate).is_file():
            return candidate
    # Current external imports are limited and explicit. An unknown/missing
    # first-party import cannot silently disappear from the identity.
    top = name.split('.')[0]
    if top in sys.stdlib_module_names or top in THIRD_PARTY_ROOTS:
        return None
    raise ValueError('Unresolved runtime import: ' + name)


def _closure(root):
    pending = ['answer_response_v1/serve.py']
    found = set()
    while pending:
        relative = pending.pop()
        if relative in found:
            continue
        source = _read(root, relative)
        found.add(relative)
        tree = ast.parse(source, filename=relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = node.func.id if isinstance(node.func, ast.Name) else (
                    node.func.attr if isinstance(node.func, ast.Attribute) else '')
                if name in DYNAMIC_IMPORT_CALLS:
                    raise ValueError('Dynamic runtime loading requires identity review: ' + relative)
            modules = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise ValueError('Relative runtime import requires identity review: ' + relative)
                modules = [node.module] if node.module else []
            for module in modules:
                dependency = _local_module(root, module)
                if dependency is None:
                    continue
                pending.append(dependency)
                # Python executes any package initializers on the route too.
                parts = PurePosixPath(dependency).parts[:-1]
                for count in range(1, len(parts) + 1):
                    init = str(PurePosixPath(*parts[:count], '__init__.py'))
                    if (root / init).is_file():
                        pending.append(init)
    return found


def identity(root=None):
    """Verify pinned first-party bytes and hash all reachable local source files.

    The DB remains a separate Store hash pin. Python/third-party implementations
    are outside this source identity; expected third-party versions are reported.
    No repository-wide scan or imports of the inspected dependency code occur.
    """
    root = Path(root) if root is not None else POC
    manifest_path = 'mcp_runtime/model-free.json'
    manifest_bytes = _read(root, manifest_path)
    manifest = json.loads(manifest_bytes)
    files = {manifest_path: hashlib.sha256(manifest_bytes).hexdigest()}
    for relative, expected in manifest['files'].items():
        if relative == 'build/knowledge.sqlite':
            continue
        actual = hashlib.sha256(_read(root, relative)).hexdigest()
        if actual != expected:
            raise ValueError('Pinned runtime dependency changed: ' + relative)
        files[relative] = actual
    closure = _closure(root)
    for relative in sorted(closure | set(CANDIDATE_FILES) | set(RUNTIME_RESOURCES)):
        files[relative] = hashlib.sha256(_read(root, relative)).hexdigest()
    files = dict(sorted(files.items()))
    digest = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {'build_id': 'answer-response-v1+' + digest[:12], 'runtime_sha256': digest,
            'distribution': 'isolated_experiment', 'files': files,
            'first_party_import_closure': sorted(closure),
            'runtime_resources': list(RUNTIME_RESOURCES),
            'expected_server_packages': manifest['server_packages'],
            'identity_scope': 'Pinned first-party runtime files plus checked static local import closure and explicit runtime resources; excludes Python and third-party implementations. Database verified separately by Store.'}
