# Artefacts and Hand-offs

## Common artefact envelope

Every specialist output requires:

```yaml
schema_version: '1.0'
artefact_type: <canonical type>
assignment_id: <stable assignment identifier>
artefact_version: <version>
status: complete | conditional | human_input_required | blocked
input_versions:
  <input artefact>: <version>
unresolved_issues: []
human_action_required: false
```

The common `status` records whether the specialist task completed within its authority. It does not automatically describe publication readiness. Factual Verifier uses `overall_release_risk`; Final Editorial Gate uses `outcome`.

- `complete`: the specialist assessment or transformation is complete. It may still identify publication risk in a separate field.
- `conditional`: the output is usable for a named limited purpose, but at least one unresolved issue remains.
- `human_input_required`: an accountable choice, permission or missing authored input prevents completion.
- `blocked`: the specialist task cannot proceed safely or honestly within available authority, evidence or access.

`human_action_required` is true when an unresolved issue, blocker or release condition has a human owner: author, project owner, approver or an as-yet-unassigned owner. It is not a substitute for naming that owner and required action.

A hand-off is invalid when the assignment ID is missing, `input_versions` is empty, a required issue has no owner or action, a schema-invalid output is supplied, or the consumer cannot determine whether an input has become stale.

## Producer and consumer map

| Producer | Artefact type | Primary consumers | Becomes stale when |
|---|---|---|---|
| Editorial Integrity Router | `route_declaration` | All named module consumers, project owner | task, risk, manifest, available artefacts or approval context changes |
| Authorship Capture | `authorship_source_pack` | Brief Compiler, Drafter, Verifier | thesis, source permission, evidence or author decision changes |
| Authorship Capture | `claim_registry` embedded in the source pack | Brief Compiler, Drafter, Verifier, Gate | a material claim, source status, wording or final location changes |
| Voice Profile Builder | `voice_profile` | Brief Compiler, Drafter, Editor, Auditor | accepted human samples, provenance or register evidence materially changes |
| Editorial Brief Compiler | `editorial_brief` | Drafter, reviewers, Gate | assignment, thesis, claims, audience, form, manifest or release conditions change |
| Source Grounded Drafter | `draft_output` | reviewers, Editor, Verifier, Gate | draft content changes |
| Argument Structure Reviewer | `argument_review` | Editor, Brief Compiler, Gate | thesis, structure or material evidence changes |
| Anti Slop Auditor | `anti_slop_audit` | Editor, Gate, calling agent | audited text or protected-voice context changes materially |
| Voice Preserving Editor | `edit_output` | Verifier, Gate, human approver | revised text changes after the edit record |
| Factual Verifier | `verification_record` | Editor, Gate, approver | material claim, source, current date or covered draft version changes |
| Final Editorial Gate | `gate_decision` | approver, Router, calling agent | any material change occurs after the decision |

## Authority hand-off

Every Router module declaration states:

- why the module is required;
- whether it may retrieve sources;
- whether it may edit content;
- whether it may issue a release decision;
- the expected output artefact;
- stop conditions;
- one or more downstream consumers.

A downstream Skill must not infer broader authority from the user’s general desire for improvement. Only Final Editorial Gate may issue a release outcome. `may_release` is release-decision authority, not permission to send or publish on the user’s behalf.

## Traceability requirements

- Voice Profile evidence references must resolve to an included entry in `sample_inventory`.
- Authorship Source Pack substantive item IDs must match the embedded Claim Registry claim IDs.
- Editorial Brief required claims must each have one evidence duty; release conditions require IDs, owners and actions.
- Draft source traces must identify claim IDs and source references; visible gap markers remain until upstream resolution.
- Editor material changes must reference stable edit IDs and name downstream actions such as re-verification or re-gating.
- Gate blockers and release conditions require owners, actions and return paths.

## Conditional work

`conditional` means the output remains useful for a named limited purpose and every limitation is visible. It does not mean a release blocker may be ignored.

Examples:

- a provisional voice profile may guide low-risk internal writing but not institutional publication;
- a draft with `[SOURCE REQUIRED]` may support review but not final verification;
- a brief may propose a five-slide priority structure pending project-owner approval.

## Gate outcomes

The Gate uses a distinct release decision:

- `ready`;
- `conditional`;
- `human_decision_required`;
- `blocked`.

A Gate decision always has common `status: complete` when it successfully performs the assessment. It can therefore return `status: complete` and `outcome: blocked` without contradiction.

## Staleness and invalidation

- New or changed material claim: update Claim Registry and re-run verification.
- Structural rewrite: re-run argument review and any affected audit.
- Material edit after verification: mark verification stale.
- Any material edit after the Gate: mark the gate decision stale.
- Manifest, purpose, audience, permission or approval change: re-route and recompile the brief.
- Voice sample provenance or accepted-edit evidence changes: refresh the profile before relying on its changed traits.

## Re-entry rules

A returned issue must name:

- the affected artefact or span;
- the owner;
- whether it blocks the current task or a later release;
- the required action;
- the Skill or human decision point to which work returns.

The Router may re-sequence work after re-entry, but may not weaken or reinterpret a specialist blocker.

## Agent-to-agent requirements

Agents should exchange validated artefacts or explicit references to them. Unstructured prose summaries may accompany an artefact but must not replace it for consequential workflows. The consuming agent must verify assignment ID, artefact version, input versions, status, unresolved issues, authority and staleness before acting.
