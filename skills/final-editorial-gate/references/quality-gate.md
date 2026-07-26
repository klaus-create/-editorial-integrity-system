# Quality Gate for the Gate

## Mandatory checks
- [ ] The actual final draft version and release surface are recorded.
- [ ] Workflow level and mandatory artefacts are identified.
- [ ] Every reviewed artefact includes version and stale status.
- [ ] Factual verification covers the final material claims.
- [ ] Thesis, reader effect, uncertainty and attribution remain authorised.
- [ ] Privacy, permission, disclosure and provenance obligations are satisfied.
- [ ] Argument, structure, voice, register and form checks are complete.
- [ ] Blocking and non-blocking issues are separated.
- [ ] Outcome uses ready, conditional, human_decision_required or blocked consistently.
- [ ] Every condition or blocker has an owner and next action.
- [ ] Required human approval and any waiver are explicit.
- [ ] The Gate did not rewrite or silently repair the piece.
- [ ] Output validates against the gate-decision schema.

- [ ] Exact input versions are recorded for every material upstream artefact.
- [ ] No stale input is treated as current, and the output states its own invalidation conditions.

## Failure outcomes
- Use `status: complete` when the Gate has issued a valid decision, including an `outcome` of `blocked`.
- Use `outcome: conditional` when only named limited release actions remain and the core claim set is stable.
- Use `outcome: human_decision_required` when an accountable choice remains within evidence and policy.
- Use `outcome: blocked` when any mandatory integrity, evidence, permission, approval or disclosure condition fails.
- Use a non-complete common `status` only when the Gate itself cannot complete the assessment.

## Evidence to return
Return artefact inventory and versions, ordered check results, blockers, conditions, approval and waiver records, and exact return paths.

## Final self-check
Am I passing polish instead of evidence? Did a post-verification change stale the record? Could another reviewer reproduce the outcome from the listed artefacts?
