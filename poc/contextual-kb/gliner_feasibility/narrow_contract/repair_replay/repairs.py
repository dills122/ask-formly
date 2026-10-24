"""Bounded source normalization. No model calls, gold access, or semantic lookup."""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'pilot'))
from contract import ROLES, envelope, validate, check_span
from hardened import adapt

IDENT = re.compile(r'[A-Za-z_$][A-Za-z0-9_$]*')
NUMBER = re.compile(r'-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?')
VALUE_ROLES = {'registration_name', 'model_key', 'value'}


def escaped(text, index):
    n = 0
    index -= 1
    while index >= 0 and text[index] == '\\':
        n += 1
        index -= 1
    return n % 2 == 1


def boundaries(text):
    """Balanced lexical quotes; intraword apostrophes are ordinary prose."""
    strings, unfinished = [], []
    i = 0
    while i < len(text):
        char = text[i]
        if char not in "'\"" or escaped(text, i):
            i += 1
            continue
        if char == "'" and i > 0 and text[i-1].isalnum():
            i += 1
            continue
        j = i + 1
        while j < len(text):
            if text[j] == char and not escaped(text, j):
                break
            if text[j] == '`':
                break
            j += 1
        if j < len(text) and text[j] == char:
            strings.append((i, j+1))
            i = j+1
        else:
            unfinished.append((i, len(text)))
            break
    return strings, unfinished


def inside(start, end, regions, strict=False):
    return any(a <= start and end <= b and (not strict or (a < start and end < b))
               for a, b in regions)


def path_end(text, start, strings):
    root = IDENT.match(text, start)
    if root is None:
        return None, False
    end = root.end()
    while end < len(text):
        char = text[end]
        if char == '.':
            member = IDENT.match(text, end+1)
            if member is None:
                return end, True
            end = member.end()
        elif char == '[':
            pos = end+1
            while pos < len(text) and text[pos].isspace():
                pos += 1
            quoted = next((b for a,b in strings if a == pos), None)
            if quoted is not None:
                pos = quoted
            else:
                number = re.match(r'-?[0-9]+', text[pos:])
                if number is None:
                    return end, True
                pos += number.end()
            while pos < len(text) and text[pos].isspace():
                pos += 1
            if pos >= len(text) or text[pos] != ']':
                return end, True
            end = pos+1
        elif char == '(':
            return end, True
        else:
            break
    return end, False


def bindings(text, strings):
    result = []
    for word in IDENT.finditer(text):
        prop = word.group()
        if prop not in ('type', 'key', 'defaultValue') or inside(word.start(),word.end(),strings):
            continue
        if word.start() and (text[word.start()-1] in '._$' or text[word.start()-1].isalnum()):
            continue
        if re.search(r'\bcustom\s+$', text[:word.start()]):
            continue
        pos = word.end()
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos < len(text) and text[pos] in ':=':
            pos += 1
            while pos < len(text) and text[pos].isspace():
                pos += 1
        quoted = next((b for a,b in strings if a == pos), None)
        end = quoted
        if end is None and prop == 'defaultValue':
            token = re.match(r'(?:true|false|null)\b', text[pos:]) or NUMBER.match(text,pos)
            if token:
                end = pos+token.end() if token.re.pattern.startswith('(?:true') else token.end()
                if end < len(text) and (text[end].isalnum() or text[end] in '._$'):
                    end = None
        if end is not None:
            result.append((pos,end,{'type':'registration_name','key':'model_key','defaultValue':'value'}[prop],word.start()))
    return result


def mention(kind, start, end, text):
    return dict(kind=kind,raw=text[start:end],start=start,end=end)


def repair(id, text, row, stage=3):
    if stage not in (0,1,2,3):
        raise ValueError('stage')
    baseline, raw, error = adapt(id,text,row)
    if stage == 0:
        return dict(envelope=baseline,log=[],raw_mentions=raw,duplicate_count=len(raw)-len({tuple(m.values()) for m in raw}))
    # Reject malformed output rather than repairing a valid prefix of a broken row.
    try:
        if not isinstance(row,dict) or 'error' in row:
            raise ValueError('runtime')
        entities=row['output']['entities']
        if set(row['output']) != {'entities'} or not isinstance(entities,dict) or set(entities)-set(ROLES):
            raise ValueError('shape')
        original=[]
        for kind,items in entities.items():
            if not isinstance(items,list):
                raise ValueError('items')
            for item in items:
                m=dict(kind=kind,raw=item['text'],start=item['start'],end=item['end'])
                check_span(m,text)
                original.append(m)
    except (ValueError,TypeError,KeyError):
        return dict(envelope=baseline,log=[],raw_mentions=raw,duplicate_count=0)
    original.sort(key=lambda m:(m['start'],m['end'],m['kind']))
    nodes=[dict(m=m.copy(),ids=[i]) for i,m in enumerate(original)]
    log=[]
    issues=[]
    strings,unfinished=boundaries(text)

    def event(op, node, after, evidence, reason):
        log.append(dict(operation=op,prediction_ids=node['ids'],before=node['m'].copy(),
                        after=after,evidence=dict(start=evidence[0],end=evidence[1],raw=text[evidence[0]:evidence[1]]),reason=reason))
    def transform(node, after, op, evidence, reason):
        event(op,node,after,evidence,reason)
        node['m']=after
    def review(node, reason, region):
        issues.append(dict(reason=reason,start=region[0],end=region[1]))
        event('review',node,None,region,reason)

    kept=[]
    for node in nodes:
        m=node['m']
        region=next(((a,b) for a,b in unfinished if a <= m['start'] < b),None)
        if region:
            review(node,'boundary_ambiguous',region)
            continue
        quote=next(((a,b) for a,b in strings if m['start']==a+1 and m['end']==b-1),None)
        if quote and m['kind'] in VALUE_ROLES:
            transform(node,mention(m['kind'],*quote,text),'quote',quote,'exact literal interior')
        kept.append(node)
    nodes=kept
    # An unclosed recognized literal is an issue even if no candidate covered it.
    for a,b in unfinished:
        issues.append(dict(reason='boundary_ambiguous',start=a,end=b))

    owners=[]
    if stage >= 2:
        kept=[]
        for node in nodes:
            m=node['m']
            if m['kind']=='api_reference' and not inside(m['start'],m['end'],strings,strict=True):
                end,unsupported=path_end(text,m['start'],strings)
                if unsupported:
                    review(node,'boundary_ambiguous',(m['start'],m['end']))
                    continue
                if end is not None and end >= m['end'] and not (m['start'] and text[m['start']-1] in '._$'):
                    path=text[m['start']:end]
                    if '.' in path or '[' in path:
                        owners.append((m['start'],end,'api_reference'))
                        if end != m['end']:
                            transform(node,mention('api_reference',m['start'],end,text),'path',(m['start'],end),'adjacent supported property path')
            kept.append(node)
        nodes=kept
        kept=[]
        for node in nodes:
            m=node['m']
            owner=next(((a,b) for a,b,k in owners if a <= m['start'] and m['end'] <= b
                        and (a < m['start'] or m['end'] < b)),None)
            if owner:
                event('suppress_component',node,None,owner,'internal to API path')
            else:
                kept.append(node)
        nodes=kept

    if stage >= 3:
        syntax=bindings(text,strings)
        for node in nodes:
            m=node['m']
            match=next(((a,b,k,s) for a,b,k,s in syntax
                if (m['start'],m['end']) == (a,b) or ((a,b) in strings and (m['start'],m['end']) == (a+1,b-1))),None)
            if match:
                a,b,kind,start=match
                after=mention(kind,a,b,text)
                if after!=m:
                    transform(node,after,'role',(start,b),'explicit local configuration binding')
        # Only independently bound or explicitly described whole value literals own payload.
        literal_owners=[]
        for node in nodes:
            m=node['m']
            region=(m['start'],m['end'])
            if m['kind']=='value' and region in strings:
                bound=any((a,b,k)==(*region,'value') for a,b,k,_ in syntax)
                cue=re.search(r'\b(?:literal text|literal value|exact string)\s*$',text[:m['start']])
                if bound or cue:
                    literal_owners.append(region)
        kept=[]
        for node in nodes:
            m=node['m']
            owner=next(((a,b) for a,b in literal_owners if a<m['start'] and m['end']<b),None)
            if owner:
                event('suppress_payload',node,None,owner,'content of independently established literal')
            else:
                kept.append(node)
        nodes=kept

    dedup={}
    for node in nodes:
        m=node['m'];key=(m['kind'],m['start'],m['end'])
        if key in dedup:
            event('merge_duplicate',node,dedup[key]['m'],(m['start'],m['end']),'identical delivered mention')
            dedup[key]['ids'].extend(node['ids'])
        else:
            dedup[key]=node
    nodes=sorted(dedup.values(),key=lambda n:(n['m']['start'],n['m']['end'],n['m']['kind']))
    delivered=[]
    i=0
    while i<len(nodes):
        group=[nodes[i]];a=nodes[i]['m']['start'];b=nodes[i]['m']['end'];j=i+1
        while j<len(nodes) and nodes[j]['m']['start']<b:
            group.append(nodes[j]);b=max(b,nodes[j]['m']['end']);j+=1
        if len(group)>1:
            for node in group:
                review(node,'role_ambiguous',(a,b))
        else:
            delivered.append(group[0]['m'])
        i=j
    issues=[dict(reason=r,start=a,end=b) for r,a,b in sorted({(v['reason'],v['start'],v['end']) for v in issues},key=lambda x:(x[1],x[2],x[0]))]
    result=envelope(id,text,delivered,status='needs_review' if issues else 'ok')
    result['issues']=issues
    validate(result,id,text)
    return dict(envelope=result,log=log,raw_mentions=original,
                duplicate_count=len(original)-len({(m['kind'],m['start'],m['end']) for m in original}))
