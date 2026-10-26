"""Reuse accepted settings/coverage gates before dispatching candidate scopes."""
import asyncio
from mcp_v1.request_context import ContextLookup

class GateOnly:
    async def lookup(self,request):
        return {}

class Context:
    def __init__(self,service_factory,settings=None):
        self.gate=ContextLookup(GateOnly(),settings=settings)
        self.settings=self.gate.settings
        self.factory=service_factory
        self.services={}
        self.lock=asyncio.Lock()
        self.closed=False

    async def lookup(self,request,project_id=None,worktree_id=None,formly_version=None,ui_adapter=None):
        async with self.lock:
            if self.closed:raise RuntimeError('Context closed')
            resolved=await self.gate.lookup(request,project_id,worktree_id,formly_version,ui_adapter)
            if 'status' in resolved:return resolved
            adapter=resolved['ui_adapter']
            if adapter not in self.services:self.services[adapter]=self.factory(adapter)
            result=await self.services[adapter].lookup(request)
            result['knowledge_scope']={'version':resolved['version_context']['selected'],'adapters':['core'] if adapter=='core' else ['core','material'],'coverage':'bounded authored sample; exact migrated applicability'}
            return dict(result,**resolved)

    async def close(self):
        async with self.lock:
            self.closed=True
            try:
                for service in self.services.values():await service.close()
            finally:self.services.clear()
