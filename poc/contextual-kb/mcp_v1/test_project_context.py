"""Asset-free regressions for settings, npm matching and the coverage gate."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tempfile
import unittest

from project_settings import ProjectSettings
from request_context import ContextLookup
from versioning import VersionResolver, normalize_version


class VersionTests(unittest.TestCase):
    def test_current_catalog_matches_without_claiming_major_coverage(self):
        resolver = VersionResolver()
        for value in [None, 'v6', ' 6 ', '6.3', '6.3.12']:
            with self.subTest(value=value):
                result = resolver.resolve(value)
                self.assertEqual(result['selected'], '6.3.12')
                self.assertEqual(result['status'], 'resolved')
                self.assertIn('does not establish', result['coverage'])

    def test_unavailable_minor_patch_and_major_do_not_fall_back_silently(self):
        for value in ['7', '6.1', '6.3.11', '6.3.13']:
            result = VersionResolver().resolve(value)
            self.assertEqual(result['status'], 'unsupported_version')
            self.assertIsNone(result['selected'])
            self.assertIn('web lookup', result['recommended_action'])

    def test_numeric_order_and_partial_matching_with_synthetic_releases(self):
        resolver = VersionResolver({'default':'6.1.5', 'releases':['6.1.5','6.9.0','6.10.0','7.1.0'],
                                    'major_baselines':{}})
        for value, expected in [('v6','6.10.0'),('6.1','6.1.5'),('6.1.5','6.1.5'),('7','7.1.0')]:
            self.assertEqual(resolver.resolve(value)['selected'], expected)

    def test_major_baseline_requires_explicit_catalog_opt_in(self):
        resolver = VersionResolver({'default':'6.3.12','releases':['6.3.12'],
                                    'major_baselines':{'6':'6.3.12'}})
        self.assertEqual(resolver.resolve('6.1.4')['match'], 'major_baseline')
        self.assertEqual(resolver.resolve('7')['status'], 'unsupported_version')

    def test_reject_bad_catalog_baselines(self):
        for baseline in ['7.1.0','6.2.0']:
            with self.assertRaises(ValueError):
                VersionResolver({'default':'6.3.12','releases':['6.3.12','7.1.0'],
                                 'major_baselines':{'6':baseline}})

    def test_input_validation_is_not_lossy_coercion(self):
        for value in ['', 'latest', '*', '^6', '6.x', '6.01', '6.1.2.3', '6.1.2-beta.1',
                      '6 || 7', '>=6', None, 6, 'v'*100]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_version(value)


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'settings.sqlite'
        self.store = ProjectSettings(self.path)

    def test_missing_settings_are_unset_and_read_creates_no_file(self):
        self.assertIsNone(self.store.get('p')['formly_version'])
        self.assertFalse(self.path.exists())

    def test_persistence_and_partial_updates(self):
        self.store.set('p', formly_version='v6', ui_adapter='Material')
        other = ProjectSettings(self.path)
        self.assertEqual(other.get('p')['formly_version'], 'v6')
        other.set('p', formly_version='7')
        self.assertEqual(self.store.get('p')['ui_adapter'], 'material')

    def test_projects_and_worktrees_are_isolated_with_field_inheritance(self):
        self.store.set('p', formly_version='6', ui_adapter='material')
        self.store.set('p', 'upgrade', formly_version='7')
        self.store.set('q', 'upgrade', formly_version='8')
        self.assertEqual(self.store.get('p','upgrade')['formly_version'], '7')
        self.assertEqual(self.store.get('q','upgrade')['formly_version'], '8')
        self.assertEqual(self.store.get('p','main')['formly_version'], '6')
        self.assertEqual(self.store.get('p','upgrade')['ui_adapter'], 'material')
        self.assertEqual(self.store.get('p')['formly_version'], '6')

    def test_invalid_update_does_not_change_settings(self):
        self.store.set('p', formly_version='6')
        with self.assertRaises(ValueError):
            self.store.set('p', formly_version='7', ui_adapter='')
        self.assertEqual(self.store.get('p')['formly_version'], '6')
        with self.assertRaises(ValueError):
            self.store.set('p')
        for value in ['', ' ', None, 2]:
            with self.assertRaises(ValueError):
                self.store.get(value)

    def test_concurrent_connections_keep_distinct_fields_and_projects(self):
        def save(i):
            store = ProjectSettings(self.path)
            store.set(f'p{i}', formly_version='6')
            if i % 2:
                store.set('shared', formly_version='7')
            else:
                store.set('shared', ui_adapter='material')
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(save, range(16)))
        self.assertEqual(self.store.get('shared')['formly_version'], '7')
        self.assertEqual(self.store.get('shared')['ui_adapter'], 'material')
        for i in range(16):
            self.assertEqual(self.store.get(f'p{i}')['formly_version'], '6')


class FakeService:
    def __init__(self):
        self.calls = []
        self.result = {'facts':[{'id':'original'}], 'citations':{'original':{'quote':'unchanged'}},
                       'knowledge_scope':{'version':'6.3.12'}, 'evidence_status':'candidate_only'}

    async def lookup(self, request):
        self.calls.append(request)
        return self.result


class ContextTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = ProjectSettings(Path(self.tmp.name)/'settings.sqlite')
        self.service = FakeService()
        self.lookup = ContextLookup(self.service, self.store)

    async def test_legacy_request_and_every_original_response_field_preserved(self):
        result = await self.lookup.lookup('  hide without losing values  ')
        self.assertEqual(self.service.calls, ['  hide without losing values  '])
        for key, value in self.service.result.items():
            self.assertEqual(result[key], value)
        self.assertEqual(result['version_context']['source'], 'default')
        self.assertFalse(self.store.path.exists())

    async def test_lookup_saves_and_reuses_project_settings_after_restart(self):
        await self.lookup.lookup('question', project_id='p', formly_version='v6', ui_adapter='Material')
        restarted = ContextLookup(self.service, ProjectSettings(self.store.path))
        result = await restarted.lookup('follow-up', project_id='p')
        self.assertEqual(result['version_context']['requested'], 'v6')
        self.assertEqual(result['version_context']['selected'], '6.3.12')
        self.assertEqual(result['version_context']['source'], 'project')
        self.assertEqual(result['ui_adapter'], 'material')

    async def test_unavailable_version_is_saved_but_never_calls_service(self):
        first = await self.lookup.lookup('question', project_id='p', worktree_id='upgrade', formly_version='7')
        second = await self.lookup.lookup('follow-up', project_id='p', worktree_id='upgrade')
        for result in [first, second]:
            self.assertEqual(result['status'], 'unsupported_version')
            self.assertIn('web lookup', result['recommended_action'])
            self.assertNotIn('facts', result)
        self.assertEqual(self.service.calls, [])
        await self.lookup.lookup('legacy')
        self.assertEqual(self.service.calls, ['legacy'])

    async def test_explicit_version_without_project_is_not_remembered(self):
        await self.lookup.lookup('question', formly_version='7')
        result = await self.lookup.lookup('legacy')
        self.assertEqual(result['version_context']['source'], 'default')
        self.assertFalse(self.store.path.exists())

    async def test_worktree_scope_does_not_change_project_default(self):
        self.store.set('p', formly_version='6')
        await self.lookup.lookup('question', project_id='p', worktree_id='upgrade', formly_version='7')
        result = await self.lookup.lookup('question', project_id='p')
        self.assertEqual(result['version_context']['selected'], '6.3.12')

    async def test_invalid_requests_have_no_persistence_or_backend_side_effects(self):
        for request, kwargs in [('', {'project_id':'p','formly_version':'7'}),
                                ('question', {'worktree_id':'orphan'}),
                                ('question', {'project_id':'p','formly_version':'latest'})]:
            with self.assertRaises(ValueError):
                await self.lookup.lookup(request, **kwargs)
        self.assertEqual(self.service.calls, [])
        self.assertFalse(self.store.path.exists())

    async def test_unsupported_adapter_does_not_return_material_facts(self):
        result = await self.lookup.lookup('question', ui_adapter='bootstrap')
        self.assertEqual(result['status'], 'unsupported_adapter')
        self.assertEqual(self.service.calls, [])

    async def test_catalog_changes_cannot_mislabel_existing_backend_as_v7(self):
        resolver = VersionResolver({'default':'7.1.0','releases':['7.1.0'],'major_baselines':{}})
        result = await ContextLookup(self.service, self.store, resolver).lookup('question', formly_version='7')
        self.assertEqual(result['status'], 'unavailable_knowledge')
        self.assertEqual(self.service.calls, [])

    async def test_existing_service_failure_is_not_swallowed(self):
        class Broken:
            async def lookup(self, request):
                raise RuntimeError('existing integrity failure')
        with self.assertRaisesRegex(RuntimeError, 'integrity failure'):
            await ContextLookup(Broken(), self.store).lookup('question')

    async def test_real_lookup_service_and_wording_adapter_preserve_existing_flow(self):
        import copy
        from service import LookupService
        from wording_candidate_v1.candidate import NormalizingPlanner

        core = {'formly_questions':[], 'library_constraints':{'formly_version':None,'ui_adapter':None},
                'condition_bindings':[]}
        planned, retrieved = [], []

        def planner(request):
            planned.append(request)
            return copy.deepcopy(core), {'model':'fixture'}

        class Backend:
            def lookup(self, request, plan):
                retrieved.append((request, plan))
                return {'facts':[], 'evidence_status':'candidate_only'}

            def close(self):
                pass

        service = LookupService(NormalizingPlanner(planner), Backend)
        try:
            original = await service.lookup('Formly')
            wrapped = await ContextLookup(service, self.store).lookup(
                'Formly', project_id='p', formly_version='6.3.12', ui_adapter='material')
            for key, value in original.items():
                self.assertEqual(wrapped[key], value)
            self.assertEqual(planned, ['Formly', 'Formly'])
            self.assertEqual(retrieved[0], retrieved[1])
        finally:
            await service.close()


if __name__ == '__main__':
    unittest.main()
