import json,unittest
from pathlib import Path
from experiment import caller_command,HERE
class HarnessTests(unittest.TestCase):
    def test_same_caller_and_startup_settings_for_both_arms(self):
        for arm in ('baseline','candidate'):
            command=caller_command(HERE/'test-output/fixture',arm,1702)
            self.assertIn('mcp_servers.formly.required=true',command)
            self.assertIn('mcp_optional_startup_grace_ms=0',command)
            arg=next(x for x in command if x.startswith('mcp_servers.formly.args='))
            args=json.loads(arg.split('=',1)[1]);self.assertEqual(args[args.index('--arm')+1],arm)
            self.assertTrue(any('mcp_foundation/CALLER.md' in x for x in command))
    def test_unknown_arm_cannot_launch(self):
        with self.assertRaises(ValueError):caller_command(HERE/'test-output/fixture','typo',1701)
if __name__=='__main__':unittest.main()
