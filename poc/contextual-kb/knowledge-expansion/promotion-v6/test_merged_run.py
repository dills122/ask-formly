import unittest
from merged_run import authorized_lookup_command

class CallerAuthorizationTests(unittest.TestCase):
    def test_only_lookup_is_enabled_and_approved_without_changing_base_policy(self):
        original=['codex','exec','-c','approval_policy="never"','-']
        result=authorized_lookup_command(original)
        self.assertEqual(original,['codex','exec','-c','approval_policy="never"','-'])
        self.assertEqual(result,original[:-1]+[
            '-c','mcp_servers.formly.enabled_tools=["lookup_formly"]',
            '-c','mcp_servers.formly.tools.lookup_formly.approval_mode="approve"','-'])
        self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',result)

    def test_unexpected_prompt_position_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'stdin prompt'):
            authorized_lookup_command(['codex','exec','actual prompt'])
