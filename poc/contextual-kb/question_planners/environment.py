"""Host provenance collection, performed outside timed planner workers."""
import platform
import subprocess


def hardware_snapshot():
    fields = {'model': 'hw.model', 'cpu': 'machdep.cpu.brand_string',
              'memory_bytes': 'hw.memsize', 'physical_cores': 'hw.physicalcpu',
              'logical_cores': 'hw.logicalcpu'}
    result = {'platform': platform.platform(), 'architecture': platform.machine(),
              'gpu': 'unavailable; runtime Ollama size_vram is recorded separately'}
    for label, key in fields.items():
        try:
            if platform.system() != 'Darwin':
                raise OSError('No platform-specific collector')
            result[label] = subprocess.check_output(
                ['/usr/sbin/sysctl', '-n', key], text=True,
                stderr=subprocess.DEVNULL, timeout=5).strip() or 'unavailable'
        except (OSError, subprocess.SubprocessError):
            result[label] = 'unavailable'
    return result
