"""Serialized raw-question service; no alteration of foundation or advisory code."""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys

POC = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(POC))
from agent_contract.qualification_v3.candidate import build_plan
from agent_contract.advisory_lookup_v1.runtime import IntegrityError

class LookupService:
    def __init__(self, planner, backend_factory):
        self.planner = planner
        self.backend_factory = backend_factory
        self.backend = None
        self.integrity_failure = None
        self.closed = False
        self.lock = asyncio.Lock()
        # SQLite and native model transport always live on this same thread.
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='formly')

    def _lookup(self, request):
        if self.integrity_failure is not None:
            raise IntegrityError(self.integrity_failure)
        core, generation = self.planner(request)
        build_plan(request, core)
        try:
            if self.backend is None:
                self.backend = self.backend_factory()
            result = self.backend.lookup(request, core)
        except IntegrityError as exc:
            self.integrity_failure = str(exc)
            if self.backend is not None:
                self.backend.close()
            raise
        return dict(result, generation=generation,
                    knowledge_scope={'version':'6.3.12','adapters':['core','material'],
                                     'coverage':'bounded authored sample; not the whole Formly library'})

    async def lookup(self, request):
        if not isinstance(request, str) or not request.strip() or len(request)>12000:
            raise ValueError('request must be a nonempty string of at most 12000 characters')
        async with self.lock:
            if self.closed:
                raise RuntimeError('Service closed')
            future = asyncio.get_running_loop().run_in_executor(self.executor, self._lookup, request)
            try:
                return await asyncio.shield(future)
            except asyncio.CancelledError:
                # Native work cannot be cancelled mid-exchange. Drain before releasing
                # the lock so closure or the next call cannot race it.
                try: await asyncio.shield(future)
                except Exception: pass
                raise

    async def close(self):
        async with self.lock:
            if self.closed:
                return
            self.closed = True
            try:
                if self.backend is not None:
                    await asyncio.get_running_loop().run_in_executor(self.executor, self.backend.close)
            finally:
                self.executor.shutdown(wait=True)
