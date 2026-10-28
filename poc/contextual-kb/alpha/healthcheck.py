"""Real stdio startup and read-only lookup check; no caller/model inference."""
import asyncio
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check():
    root = Path(__file__).resolve().parent
    params = StdioServerParameters(command=sys.executable, args=['-I', str(root / 'ask_formly.py'), 'serve'])
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            names = {tool.name for tool in (await session.list_tools()).tools}
            if not {'lookup_formly', 'discover_formly_candidates', 'get_formly_facts'} <= names:
                raise ValueError('Required MCP tools unavailable')
            question = 'How does Formly resetOnHide work?'
            result = await session.call_tool('lookup_formly', {'request': question, 'plan': {
                'formly_questions': [{'question': question, 'reason': 'Read-only installation smoke check.'}],
                'library_constraints': {'formly_version': '6.3.12', 'ui_adapter': 'material'}, 'condition_bindings': []}})
            packet = result.structuredContent
            if result.isError or not packet or packet.get('status') != 'ok' or not packet.get('facts'):
                raise ValueError('Read-only MCP lookup failed')
    print('MCP initialization, tool catalog and read-only lookup passed; answer quality not assessed.')


def main():
    asyncio.run(asyncio.wait_for(check(), timeout=30))


if __name__ == '__main__':
    main()
