"""Test caller helper: follow-up fetches inherit resolved lookup scope exactly."""
def fetch_arguments(ids,packet):
    return dict(fact_ids=ids,formly_version=packet['version_context']['selected'],ui_adapter=packet['ui_adapter'])


def same_scope(first,second):
    return (first['version_context']['selected'],first['ui_adapter'])==(second['version_context']['selected'],second['ui_adapter'])
