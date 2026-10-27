"""Audit transport provenance and explicit caller judgments, never infer semantic success."""
import copy


def compare_repeats(first,repeat):
    def stable(rows):
        return [{k:v for k,v in row.items() if k!='seconds'} for row in rows]
    if stable(first)!=stable(repeat):
        raise ValueError('Changed packets require separate judgment')


def validate_judgments(answers,packets):
    ids=[r['id'] for r in answers]
    if len(ids)!=len(set(ids)) or set(ids)!=set(packets):
        raise ValueError('Missing/duplicate judgments')
    for row in answers:
        if type(row['usable']) is not bool or type(row['critical_unsupported_claim']) is not bool:
            raise ValueError('Judgment flags must be explicit booleans')
        if row['usable'] and row['critical_unsupported_claim']:
            raise ValueError('Critical unsupported claim cannot pass')
        if not row['answer'].strip() or not row['reason'].strip():
            raise ValueError('Missing caller answer or rationale')
        delivered={f['id'] for f in packets[row['id']].get('facts',[])}
        if not set(row['citations'])<=delivered:
            raise ValueError('Undelivered citation')
    return sum(r['usable'] for r in answers)


def validate_observation(rows,plans):
    initial={};completed={};seen={};budgets={}
    for row in rows:
        ident=row['id'];tool=row['tool'];args=row['arguments']
        if ident not in plans or row.get('operational_or_tool_error') or row.get('result',{}).get('isError'):
            raise ValueError('Unknown case or tool failure')
        packet=row['result']['structuredContent'];original=plans[ident]
        if tool=='lookup_formly':
            if ident in initial or args!=original:
                raise ValueError('Duplicate or changed initial plan')
            initial[ident]=copy.deepcopy(packet);completed[ident]=copy.deepcopy(packet)
            seen[ident]={f['id'] for f in packet.get('facts',[])}|{i for q in packet.get('questions',[]) for i in q.get('omitted_ids',[])}
            budgets[ident]={'discover_formly_candidates':0,'get_formly_facts':0}
            continue
        if ident not in initial or initial[ident].get('status') not in ('ok','no_evidence'):
            raise ValueError('Recovery requires eligible initial result')
        if tool not in budgets[ident]:raise ValueError('Unknown recovery tool')
        budgets[ident][tool]+=1
        if budgets[ident][tool]>2:raise ValueError('Recovery budget exceeded')
        for key in ('formly_version','ui_adapter'):
            if args.get(key)!=original.get(key):raise ValueError('Recovery changed scope')
        if tool=='discover_formly_candidates':
            for key in ('request','plan'):
                if args.get(key)!=original.get(key):raise ValueError('Discovery changed plan')
            if args.get('limit',16)>16:raise ValueError('Discovery page too large')
            seen[ident].update(f['id'] for f in packet.get('candidates',[]))
        else:
            requested=args['fact_ids']
            if len(requested)>16 or not set(requested)<=seen[ident]:raise ValueError('Unseen or excessive fetch')
            if not {f['id'] for f in packet.get('facts',[])}<=set(requested):raise ValueError('Unexpected fetched fact')
            completed[ident].setdefault('facts',[]).extend(copy.deepcopy(packet.get('facts',[])))
            completed[ident].setdefault('citations',{}).update(copy.deepcopy(packet.get('citations',{})))
    if set(initial)!=set(plans):raise ValueError('Missing initial calls')
    return initial,completed
