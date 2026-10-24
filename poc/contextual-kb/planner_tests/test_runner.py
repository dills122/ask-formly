import sys,time,unittest
from pathlib import Path
from question_planners.runner import PlannerProcess

DUMMY = '''import sys,json,time
print(json.dumps({'ready':True}),flush=True)
for line in sys.stdin:
 q=json.loads(line)['question']
 if q=='sleep': time.sleep(2)
 elif q=='partial':
  sys.stdout.write('{');sys.stdout.flush();time.sleep(2)
 else: print(json.dumps({'broken':True}),flush=True)
'''


class RunnerTests(unittest.TestCase):
    def runner(self):
        return PlannerProcess(command=[sys.executable,'-u','-c',DUMMY], deadline=.15)

    def test_deadline_kills_unresponsive_process(self):
        with self.runner() as runner:
            start=time.monotonic(); result=runner.query('sleep')
            self.assertEqual(result['plan']['failure']['code'],'timeout')
            self.assertLess(time.monotonic()-start,1)
            self.assertIsNotNone(runner.process.poll())

    def test_partial_line_cannot_block_deadline(self):
        with self.runner() as runner:
            result=runner.query('partial')
            self.assertEqual(result['plan']['failure']['code'],'timeout')

    def test_malformed_worker_output_rejected(self):
        with self.runner() as runner:
            result=runner.query('normal')
            self.assertEqual(result['plan']['failure']['code'],'invalid_output')

    def test_invalid_input_never_sent(self):
        with self.runner() as runner:
            result=runner.query('')
            self.assertEqual(result['plan']['failure']['code'],'invalid_input')
            self.assertIsNone(runner.process.poll())

    def test_deadline_also_covers_blocked_input_write(self):
        code="import time; print('{\"ready\":true}',flush=True); time.sleep(2)"
        with PlannerProcess(command=[sys.executable,'-u','-c',code], deadline=.15) as runner:
            start=time.monotonic()
            result=runner.query('🧭'*8000)
            self.assertLess(time.monotonic()-start,1)
            self.assertEqual(result['plan']['failure']['code'],'timeout')

if __name__=='__main__': unittest.main()
