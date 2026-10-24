# Annotation decision before inference

Independent A and B each annotated all 24 from CONTRACT.md and questions only.
Exact agreement: 24/24 envelopes and 90/90 typed spans, no differing issues/status.
Both sources are retained unchanged. gold.json adopts the identical annotations.
Parent reviewed every mention list against question and contract before prediction.

Both annotators identified the same representational gap: issue-region extent for
an unterminated literal is not specified. Both used opening quote through question
end for D06. Accept that agreed extent for this pilot; no label changed or model
prediction inspected. D05 marks the ambiguous quoted name itself. Both are genuinely
needs_review rather than invented registration/model-key/value labels.
A future general contract should formalize issue-region boundaries. This does not
change the six entity roles or affect the nonambiguous extraction scoring.

This is agent-agent agreement, not independent human validation. Shared blind spots
remain possible. No historical five-label gold was used as new reference labels.
