# Quality Gate

## Mandatory checks
- [ ] The exact final draft version is recorded.
- [ ] Every material claim is atomised and classified.
- [ ] Evidence burden matches claim type and consequence.
- [ ] Sources are evaluated for authority, proximity, independence and freshness.
- [ ] Numerical claims include period, denominator, unit, method and arithmetic.
- [ ] Comparative claims define set, metric and period.
- [ ] Causal claims test mechanism and alternatives.
- [ ] Quotations are checked against originals or removed from quotation marks.
- [ ] Product roadmap, beta and live capability remain separate.
- [ ] Current claims include a current-as-of date and authoritative source.
- [ ] Conflicting sources remain visible and are reconciled by scope, not preference.
- [ ] Every claim has a status, action and reproducible source record.
- [ ] Factual amendments do not silently change the thesis.
- [ ] Output validates against the verification-record schema.

- [ ] Exact input versions are recorded for every material upstream artefact.
- [ ] No stale input is treated as current, and the output states its own invalidation conditions.

## Failure outcomes
- Use `status: complete` when the verification assessment is finished, even if `overall_release_risk` is `blocked`.
- Use `status: conditional` when material checks remain incomplete but the record is still useful.
- Use `status: human_input_required` when evidence supports more than one accountable framing or a thesis-impacting correction.
- Use `status: blocked` only when the verification task itself cannot be performed because access, permission or authority is unavailable.

## Evidence to return
Return source references and access dates, claim-type checks, conflict notes, corrections and unresolved publication risk.

## Final self-check
Did I verify the proposition rather than familiar wording? Could a sceptical reviewer reproduce the result? Have I distinguished false, unsupported, unverifiable, contested and judgement?
