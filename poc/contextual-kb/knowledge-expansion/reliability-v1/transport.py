"""Explicit caller connection requirements for this isolated candidate."""
def connection_options():
    return ['-c', 'mcp_optional_startup_grace_ms=0',
            '-c', 'mcp_servers.formly.required=true',
            '-c', 'mcp_servers.formly.startup_timeout_sec=60',
            '-c', 'mcp_servers.formly.tool_timeout_sec=600']
