import unittest
import scope

class ScopeTests(unittest.TestCase):
    def test_fetch_copies_resolved_scope_not_optional_defaults(self):
        packet={'version_context':{'selected':'6.3.12'},'ui_adapter':'material'}
        self.assertEqual(scope.fetch_arguments(['fact'],packet),{'fact_ids':['fact'],'formly_version':'6.3.12','ui_adapter':'material'})
    def test_a_missing_adapter_is_a_mismatch_even_for_a_core_fact(self):
        expected={'version_context':{'selected':'6.3.12'},'ui_adapter':'material'}
        broadened={'version_context':{'selected':'6.3.12'},'ui_adapter':None}
        self.assertFalse(scope.same_scope(expected,broadened))
        self.assertTrue(scope.same_scope(expected,expected))
if __name__=='__main__':unittest.main()
