import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import candidate
import experiment

class MaterialSelectBatchTests(unittest.TestCase):
    def test_both_arms_use_installed_qualified_planner(self):
        from condition_candidate_v2.planner import CodexPlanner
        self.assertIs(experiment.CodexPlanner,CodexPlanner)

    def test_reviewed_candidate_size_cannot_silently_change(self):
        self.assertEqual(candidate.EXPECTED_FACTS,93)
        self.assertEqual(candidate.EXPECTED_DOCUMENTS,21)

    def test_both_arms_have_only_explicitly_authorized_lookup(self):
        for arm in ('baseline','candidate'):
            command=experiment.caller_command(experiment.HERE/'test-output/fixture',arm,1702)
            self.assertIn('mcp_servers.formly.enabled_tools=["lookup_formly"]',command)
            self.assertIn('mcp_servers.formly.tools.lookup_formly.approval_mode="approve"',command)
            self.assertIn('mcp_servers.formly.required=true',command)
            self.assertIn('mcp_optional_startup_grace_ms=0',command)
            self.assertNotIn('--dangerously-bypass-approvals-and-sandbox',command)
            arg=next(x for x in command if x.startswith('mcp_servers.formly.args='))
            args=json.loads(arg.split('=',1)[1]);self.assertEqual(args[args.index('--arm')+1],arm)

    def test_call_output_cannot_escape_batch(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'must-not-create'
            with self.assertRaisesRegex(ValueError,'test-output'):
                experiment.run_agent([], 'candidate',1701,out)
            self.assertFalse(out.exists())

    def test_size_drift_fails_before_manifest_publication(self):
        candidate.verify_candidate_counts({'facts':93,'documents':21})
        for counts in ({'facts':92,'documents':21},{'facts':93,'documents':20}):
            with self.assertRaisesRegex(ValueError,'candidate size'):
                candidate.verify_candidate_counts(counts)

    def test_candidate_arm_uses_only_its_pinned_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'candidate-build').mkdir()
            db=root/'candidate-build/knowledge.sqlite';db.write_bytes(b'candidate')
            (root/'candidate-build/manifest.json').write_text(json.dumps({
                'database':'candidate-build/knowledge.sqlite','sha256':candidate.digest(db),'inputs':{}}))
            with patch.object(candidate,'HERE',root):
                self.assertEqual(candidate.checked_database('candidate'),(db,candidate.digest(db)))
                db.write_bytes(b'drift')
                with self.assertRaisesRegex(ValueError,'Preservation mismatch'):
                    candidate.checked_database('candidate')

    def test_unknown_arm_cannot_launch(self):
        with self.assertRaises(ValueError):experiment.caller_command(experiment.HERE/'test-output/x','typo',1701)

if __name__=='__main__':unittest.main()
