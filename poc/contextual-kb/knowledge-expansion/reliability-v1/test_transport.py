import unittest
from transport import connection_options
from pathlib import Path
from run import caller_command,HERE


class ConnectionTests(unittest.TestCase):
    def test_formly_is_required_not_optional(self):
        self.assertIn('mcp_servers.formly.required=true',connection_options())

    def test_initial_catalog_waits_for_server(self):
        self.assertIn('mcp_optional_startup_grace_ms=0',connection_options())

    def test_candidate_caller_uses_exact_identity_and_isolated_server(self):
        command=caller_command(HERE/'test-output/test-command',1702)
        self.assertTrue(any(str(HERE/'server.py') in arg for arg in command))
        self.assertTrue(any(str(HERE/'CALLER.md') in arg for arg in command))
        self.assertIn('mcp_servers.formly.required=true',command)
        self.assertIn('mcp__formly__lookup_formly',(HERE/'CALLER.md').read_text())


if __name__=='__main__':unittest.main()
