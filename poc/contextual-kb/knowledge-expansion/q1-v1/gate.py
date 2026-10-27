"""The Q1 thresholds fixed before execution; no semantic grading here."""
def assess(cases,answers):
    ids=[r['id'] for r in cases]; answer_ids=[r['id'] for r in answers]
    if len(set(ids))!=len(ids) or len(set(answer_ids))!=len(answer_ids) or set(ids)!=set(answer_ids):
        raise ValueError('Wrong case/answer coverage')
    targets=[r for r in cases if r['kind']=='target'];controls=[r for r in cases if r['kind']=='control']
    if len(targets)!=160 or len(controls)!=16:raise ValueError('Frozen denominator changed')
    lookup={r['id']:r for r in answers}
    if any(type(r['usable']) is not bool or type(r['critical_unsupported_claim']) is not bool for r in answers):
        raise ValueError('Judgments must use boolean flags')
    usable=sum(lookup[r['id']]['usable'] for r in targets)
    failed_controls=[r['id'] for r in controls if not lookup[r['id']]['usable']]
    critical=[r['id'] for r in answers if r['critical_unsupported_claim']]
    decision='failed' if failed_controls or critical or usable<143 else 'target_met' if usable>=144 else 'accepted_lower_band'
    groups={}
    for group in sorted({r['group'] for r in cases}):
        subset=[r for r in targets if r['group']==group]
        groups[group]={'usable':sum(lookup[r['id']]['usable'] for r in subset),'targets':len(subset)}
    return dict(decision=decision,usable_targets=usable,target_count=160,percent=usable/160*100,
        failed_controls=failed_controls,critical_unsupported_claims=critical,groups=groups,
        failed_targets=[r['id'] for r in targets if not lookup[r['id']]['usable']])
