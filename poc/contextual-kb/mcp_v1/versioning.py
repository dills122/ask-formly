"""Resolve a small release catalog without touching the knowledge database."""
import json
import re
from pathlib import Path

from semantic_version import NpmSpec, Version


def normalize_version(value):
    """Accept stable major, minor or exact versions; preserve input precision."""
    if not isinstance(value, str) or len(value) > 64:
        raise ValueError('formly_version must be a string such as v6, 6.3 or 6.3.12')
    normalized = value.strip().removeprefix('v')
    if not re.fullmatch(r'(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*)){0,2}', normalized):
        raise ValueError('Use a stable Formly major, minor or exact version; ranges and prereleases are not supported')
    NpmSpec(normalized)
    return normalized


class VersionResolver:
    def __init__(self, catalog=None):
        if catalog is None:
            catalog = json.loads(Path(__file__).with_name('versions.json').read_text())
        self.versions = tuple(Version(v) for v in catalog['releases'])
        self.default = Version(catalog['default'])
        self.baselines = {int(k): Version(v) for k, v in catalog['major_baselines'].items()}
        if self.default not in self.versions or any(v.prerelease for v in self.versions):
            raise ValueError('Catalog must contain its stable default release')
        for major, version in self.baselines.items():
            if version not in self.versions or version.major != major:
                raise ValueError('Major baseline must name a stored release of the same major')

    def resolve(self, requested=None):
        normalized = normalize_version(requested) if requested is not None else None
        selected = self.default if normalized is None else NpmSpec(normalized).select(self.versions)
        match = 'default' if normalized is None else 'matching_release'
        if selected is None:
            selected = self.baselines.get(int(normalized.split('.')[0]))
            match = 'major_baseline'
        result = {'requested': requested, 'normalized': normalized,
                  'selected': str(selected) if selected is not None else None,
                  'match': match if selected is not None else None,
                  'available_releases': [str(v) for v in sorted(self.versions)]}
        if selected is None:
            return dict(result, status='unsupported_version',
                        message=f'No accepted knowledge coverage for Formly {requested}.',
                        recommended_action='Use web lookup against official Formly documentation and source for the requested version.')
        return dict(result, status='resolved',
                    coverage='Selected source release only; matching does not establish coverage of every release in the requested major or minor.')
