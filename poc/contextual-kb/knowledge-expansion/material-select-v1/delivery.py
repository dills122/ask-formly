"""Audit exact sequential MCP calls without concealing failed tool responses."""
def verify_calls(events, requests):
    completed=[]; active=None
    for event in events:
        kind=event.get('type'); item=event.get('item',{})
        if kind not in ('item.started','item.updated','item.completed'):continue
        typ=item.get('type')
        if typ in ('reasoning','agent_message'):continue
        if typ!='mcp_tool_call':raise ValueError('Unexpected agent tool/item: '+str(typ))
        if item.get('server')!='formly' or item.get('tool')!='lookup_formly':raise ValueError('Unexpected MCP server/tool')
        index=len(completed)
        if index>=len(requests) or item.get('arguments')!={'request':requests[index]}:raise ValueError('Request sequence/arguments differ')
        if kind=='item.started':
            if active is not None:raise ValueError('Overlapping MCP calls')
            active=item.get('id')
            if not active:raise ValueError('Missing MCP identity')
        elif kind=='item.completed':
            if active is None or item.get('id')!=active:raise ValueError('MCP completion identity differs')
            completed.append(requests[index]);active=None
        elif item.get('id')!=active:raise ValueError('MCP update identity differs')
    if active is not None or completed!=requests:raise ValueError('Missing MCP calls/completions')
    return len(completed)
