---
name: final-editorial-gate
description: Perform the final release-readiness review for consequential AI-assisted writing. Use immediately before submission, publication or external circulation to confirm the actual final version preserves authorised meaning, factual boundaries, voice, form, disclosure and required human accountability. Do not rewrite the piece, waive missing evidence silently or pass polished prose that lacks mandatory artefacts.
---

# Final Editorial Gate

## Purpose
Decide whether the final version is ready, conditional, requires a human decision or is blocked, without performing uncontrolled repair.

## Required inputs
- final draft and version
- workflow level and route declaration
- brief, manifest and relevant profiles
- review findings and resolution records
- verification record and source status
- approval, privacy and disclosure requirements

## Execution
1. Establish scope, authority, input versions and missing prerequisites.
2. Read `references/method.md` and execute its procedure and decision logic.
3. Stop or escalate whenever the method's authority boundary is reached.
4. Validate the proposed output against `references/output-contract.yaml`.
5. Apply every mandatory item in `references/quality-gate.md`.
6. Return the requested user-facing result and only material unresolved issues. For agent-to-agent or consequential work, return the complete structured artefact.

## Authority boundary
Do not perform adjacent specialist work merely because it is convenient. Preserve verified facts, exact quotations, authorised uncertainty, human meaning and project governance. Never invent sources, evidence, experience, examples, approval or certainty.

## Progressive loading
- Read `references/method.md` for intake, execution, branching, failure modes and examples.
- Read `references/release-decision-matrix.md` when determining required artefacts, release blockers, conditional release, waivers, stale inputs or return paths.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
