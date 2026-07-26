# Quality Gate

## Mandatory checks
- [ ] The brief is executable for the returned output type.
- [ ] Every section performs a defined function in the form architecture.
- [ ] Material claims map to authorised evidence, attribution, judgement or labelled inference.
- [ ] No fact, quotation, example, source or first-person experience was invented.
- [ ] Uncertainty, disagreement and limitations remain visible where material.
- [ ] Transitions do not create unsupported causality, consensus or sequence.
- [ ] Gap markers use the standard vocabulary and remain unresolved until upstream change.
- [ ] Voice instructions are applied without phrase copying.
- [ ] The conclusion stays within the evidence and argument developed.
- [ ] Source trace covers all material claims.
- [ ] Full regeneration was not used when local repair was sufficient.
- [ ] Output validates against the draft-output schema.

- [ ] Exact input versions are recorded for every material upstream artefact.
- [ ] No stale input is treated as current, and the output states its own invalidation conditions.

## Failure outcomes
- `conditional`: a marked draft is useful and all gaps are explicit.
- `human_input_required`: core thesis, experience or accountable choice is missing.
- `blocked`: drafting would require invention, prohibited disclosure or unsupported core claims.

## Evidence to return
Return the draft, source trace, gap markers, unresolved issue owners and integrity summary.

## Final self-check
Can every material claim be traced? Did a transition smuggle in a stronger relation? Does the output behave like its form rather than generic prose in a different container?
