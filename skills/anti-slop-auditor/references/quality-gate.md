# Quality Gate

## Mandatory checks
- [ ] The complete piece, form, audience and purpose were considered.
- [ ] Voice and protected characteristics informed the baseline where available.
- [ ] Every finding identifies an observable pattern and consequence.
- [ ] Clusters and material residue outrank isolated words or punctuation.
- [ ] Severity and confidence are independent.
- [ ] False-positive alternatives were tested.
- [ ] Preserve and query decisions appear where irregularity may be functional.
- [ ] Necessary technical language and genre conventions are not penalised automatically.
- [ ] No claim about AI authorship or text origin is made.
- [ ] Factual and structural failures are escalated to the correct specialist.
- [ ] Audit remains separate from editing authority.
- [ ] Output validates against the anti-slop-audit schema.

- [ ] Exact input versions are recorded for every material upstream artefact.
- [ ] No stale input is treated as current, and the output states its own invalidation conditions.

## Failure outcomes
- `conditional`: useful findings can be returned with explicit context limitations.
- `human_input_required`: authorial intent or protected-characteristic status is necessary for a material decision.
- `blocked`: the available excerpt is insufficient to support the requested whole-piece judgement.

## Evidence to return
Return the context baseline, grouped findings, consequence, false-positive test, treatment and origin-claim flag.

## Final self-check
Would the finding still matter if the prose were unquestionably human-authored? Would the proposed change reduce meaning, rhythm or distinctiveness? Have I diagnosed rather than detected?
