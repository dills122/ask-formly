"""Real stdio startup and read-only lookup check; no caller/model inference."""
import asyncio
import json
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check():
    root = Path(__file__).resolve().parent
    expected_identity = json.loads((root / 'ALPHA-MANIFEST.json').read_text())['build_identity']
    params = StdioServerParameters(command=sys.executable, args=['-I', str(root / 'ask_formly.py'), 'serve'])
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            if initialized.serverInfo.version != expected_identity['build_id']:
                raise ValueError('MCP handshake build identity mismatch')
            names = {tool.name for tool in (await session.list_tools()).tools}
            if not {'lookup_formly', 'discover_formly_candidates', 'get_formly_facts', 'help_formly'} <= names:
                raise ValueError('Required MCP tools unavailable')
            help_result = await session.call_tool('help_formly', {})
            help_packet = help_result.structuredContent or json.loads(help_result.content[0].text)
            if help_result.isError or help_packet.get('build_identity') != expected_identity:
                raise ValueError('MCP help build identity mismatch')
            question = 'How does Formly resetOnHide work?'
            result = await session.call_tool('lookup_formly', {'request': question, 'plan': {
                'formly_questions': [{'question': question, 'reason': 'Read-only installation smoke check.'}],
                'library_constraints': {'formly_version': '6.3.12', 'ui_adapter': 'material'}, 'condition_bindings': []}})
            packet = result.structuredContent or json.loads(result.content[0].text)
            if result.isError or not packet or packet.get('status') != 'ok' or not packet.get('facts'):
                raise ValueError('Read-only MCP lookup failed')
    print('MCP initialization, build identity, tool catalog and read-only lookup passed; answer quality not assessed.')


def main():
    asyncio.run(asyncio.wait_for(check(), timeout=30))


if __name__ == '__main__':
    main()
