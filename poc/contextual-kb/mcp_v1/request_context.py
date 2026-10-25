"""Settings and coverage gate around the unchanged accepted lookup service."""
from project_settings import ProjectSettings, normalize_adapter
from versioning import VersionResolver, normalize_version


class ContextLookup:
    def __init__(self, service, settings=None, resolver=None):
        self.service = service
        self.settings = settings if settings is not None else ProjectSettings()
        self.resolver = resolver if resolver is not None else VersionResolver()

    async def lookup(self, request, project_id=None, worktree_id=None,
                     formly_version=None, ui_adapter=None):
        if not isinstance(request, str) or not request.strip() or len(request) > 12000:
            raise ValueError('request must be a nonempty string of at most 12000 characters')
        if worktree_id is not None and project_id is None:
            raise ValueError('worktree_id requires project_id')
        if formly_version is not None:
            normalize_version(formly_version)
        if ui_adapter is not None:
            ui_adapter = normalize_adapter(ui_adapter)
        source = 'argument' if formly_version is not None else 'default'
        settings = None
        if project_id is not None:
            if formly_version is not None or ui_adapter is not None:
                settings = self.settings.set(project_id, worktree_id, formly_version, ui_adapter)
            else:
                settings = self.settings.get(project_id, worktree_id)
            if formly_version is None:
                source = settings['sources'].get('formly_version', 'default')
            formly_version = settings['formly_version']
            ui_adapter = settings['ui_adapter']
        version = dict(self.resolver.resolve(formly_version), source=source)
        context = {'version_context': version, 'ui_adapter': ui_adapter,
                   'project_settings': settings}
        if version['status'] != 'resolved':
            return dict(context, status=version['status'], message=version['message'],
                        recommended_action=version['recommended_action'])
        if ui_adapter is not None and ui_adapter not in ('core', 'material'):
            return dict(context, status='unsupported_adapter',
                        message=f'No accepted knowledge coverage for UI adapter {ui_adapter}.',
                        recommended_action='Use web lookup against official Formly documentation for the requested adapter and version.')
        # Catalog expansion alone must never route a new release into the old DB.
        if version['selected'] != '6.3.12':
            return dict(context, status='unavailable_knowledge',
                        message='The current retrieval backend only serves the installed 6.3.12 knowledge.',
                        recommended_action='Use web lookup for the requested version until its retrieval backend is available.')
        result = await self.service.lookup(request)
        return dict(result, **context)
