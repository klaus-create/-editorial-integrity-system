# Quality Gate

## Mandatory checks
- [ ] Assignment ID, task type, form, audience and output are explicit.
- [ ] The active manifest and all input artefact versions are recorded.
- [ ] Consequence, factual, privacy, voice and continuity risks are rated.
- [ ] Workflow level follows the routing decision table.
- [ ] Every selected module changes a necessary decision or produces a required artefact.
- [ ] No required module is omitted because the output is short or urgent.
- [ ] Retrieval, editing and release permissions, expected artefact and downstream consumers are explicit for each module.
- [ ] Missing prerequisites and stale artefacts are visible.
- [ ] Every unresolved issue has an owner and required action.
- [ ] Human approval requirements name an approver or state that ownership is unresolved.
- [ ] The Router has not performed specialist work or softened a blocker.
- [ ] Output validates against the route declaration schema.

- [ ] Exact input versions are recorded for every material upstream artefact.
- [ ] No stale input is treated as current, and the output states its own invalidation conditions.

## Failure outcomes
- `conditional`: execution may proceed with named non-blocking gaps.
- `human_input_required`: an accountable choice or missing authority prevents routing.
- `blocked`: privacy, safety, source permission or release governance prevents execution.

## Evidence to return
Return the route declaration, the decision basis for workflow level, stale-artefact notices and all hand-off authorities.

## Final self-check
Could another agent execute the route without the original conversation? Would a late edit invalidate any recorded approval or verification? Did the Router remain a Router?
