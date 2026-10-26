"""Run active local POC regressions without hosted generation or training."""
import subprocess
import sys
from pathlib import Path

POC = Path(__file__).resolve().parents[1]
SUITES = (
    'mcp_foundation',
    'condition_candidate_v2',
    'mcp_v1',
    'wording_candidate_v1',
    'retrieval_repair_v1',
    'agent_contract/advisory_lookup_v1',
    'packaging',
    'versioned_knowledge_v1',
    'versioned_promotion_v1',
)


def main():
    for name in ('mcp_v1', 'agent_contract/advisory_lookup_v1'):
        (POC / name / 'test-output').mkdir(exist_ok=True)
    for name in SUITES:
        subprocess.run(
            [sys.executable, '-B', '-m', 'unittest', 'discover',
             '-s', str(POC / name), '-p', 'test_*.py'],
            check=True,
        )


if __name__ == '__main__':
    main()
