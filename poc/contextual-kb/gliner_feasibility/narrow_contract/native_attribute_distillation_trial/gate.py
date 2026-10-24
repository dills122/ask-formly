"""Predeclared correctness-preservation rules; unsafe validity is not a gain."""
def case_issues(gold,original,previous,current,previous_exact,original_invalid,current_invalid,current_exact):
 issues=[]
 if (gold&original)-current:issues.append('original_correct_lost')
 if (gold&previous)-current:issues.append('previous_correct_lost')
 if previous_exact and not current_exact:issues.append('previous_exact_lost')
 if original_invalid and not current_invalid and not current_exact:issues.append('invalid_to_valid_wrong')
 return issues
def paired_gate(checks):
 return len(checks)==2 and all(not c['issues'] and c['correct_resolutions']>=1 and c['wrong_resolutions']==0 for c in checks)
