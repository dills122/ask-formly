"""Small persistent project/worktree settings store, separate from knowledge."""
from contextlib import closing
import os
from pathlib import Path
import sqlite3

from versioning import normalize_version


def default_store_path():
    configured = os.environ.get('FORMLY_SETTINGS_PATH')
    if configured:
        return Path(configured).expanduser()
    base = Path(os.environ.get('XDG_STATE_HOME', str(Path.home() / '.local/state')))
    return base / 'ask-formly/project-settings.sqlite'


def validate_identity(project_id, worktree_id=None):
    for name, value in [('project_id', project_id), ('worktree_id', worktree_id)]:
        if name == 'worktree_id' and value is None:
            continue
        if not isinstance(value, str) or not value.strip() or len(value) > 4096:
            raise ValueError(f'{name} must be a nonempty identifier of at most 4096 characters')
    # IDs are opaque caller-owned keys; never resolve paths or inspect repositories.
    return project_id, worktree_id or ''


def normalize_adapter(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 100:
        raise ValueError('ui_adapter must be a nonempty string of at most 100 characters')
    return value.strip().lower()


class ProjectSettings:
    def __init__(self, path=None):
        self.path = (Path(path) if path is not None else default_store_path()).expanduser().absolute()

    def _read(self, db, project_id, worktree_id):
        result = {'project_id': project_id, 'worktree_id': worktree_id or None,
                  'formly_version': None, 'ui_adapter': None, 'sources': {}}
        if not db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='project_settings'").fetchone():
            return result
        for scope, key in [('project', ''), ('worktree', worktree_id)]:
            if scope == 'worktree' and not key:
                continue
            row = db.execute('SELECT formly_version, ui_adapter FROM project_settings '
                             'WHERE project_id=? AND worktree_id=?', (project_id, key)).fetchone()
            if row:
                for field, value in zip(('formly_version', 'ui_adapter'), row):
                    if value is not None:
                        result[field] = value
                        result['sources'][field] = scope
        return result

    def get(self, project_id, worktree_id=None):
        project_id, worktree_id = validate_identity(project_id, worktree_id)
        if not self.path.exists():
            return {'project_id': project_id, 'worktree_id': worktree_id or None,
                    'formly_version': None, 'ui_adapter': None, 'sources': {}}
        with closing(sqlite3.connect(self.path.as_uri() + '?mode=ro', uri=True, timeout=10)) as db:
            # One snapshot for project defaults and worktree settings.
            with db:
                db.execute('BEGIN')
                return self._read(db, project_id, worktree_id)

    def set(self, project_id, worktree_id=None, formly_version=None, ui_adapter=None):
        project_id, worktree_id = validate_identity(project_id, worktree_id)
        if formly_version is None and ui_adapter is None:
            raise ValueError('Supply formly_version or ui_adapter to save settings')
        if formly_version is not None:
            normalize_version(formly_version)
            formly_version = formly_version.strip()
        if ui_adapter is not None:
            ui_adapter = normalize_adapter(ui_adapter)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.path, timeout=10)) as db:
            with db:
                db.execute('BEGIN IMMEDIATE')
                db.execute('CREATE TABLE IF NOT EXISTS project_settings ('
                           'project_id TEXT NOT NULL, worktree_id TEXT NOT NULL, '
                           'formly_version TEXT, ui_adapter TEXT, PRIMARY KEY(project_id,worktree_id))')
                db.execute('INSERT INTO project_settings VALUES (?,?,?,?) '
                           'ON CONFLICT(project_id,worktree_id) DO UPDATE SET '
                           'formly_version=COALESCE(excluded.formly_version,project_settings.formly_version), '
                           'ui_adapter=COALESCE(excluded.ui_adapter,project_settings.ui_adapter)',
                           (project_id, worktree_id, formly_version, ui_adapter))
                return self._read(db, project_id, worktree_id)
