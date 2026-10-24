"""Temperature-one teacher preservation; masked wrong teachers teach nothing."""
import torch
import torch.nn.functional as F

def correct_mask(probabilities,gold_indices):
 confidence,predicted=probabilities.max(-1)
 return (predicted==gold_indices)&(confidence>.5)

def preservation_kl(student_logits,teacher_probabilities,mask):
 if not bool(mask.any()):raise ValueError('no teacher-correct anchors')
 return F.kl_div(student_logits[mask].log_softmax(-1),teacher_probabilities.detach()[mask],reduction='batchmean')
