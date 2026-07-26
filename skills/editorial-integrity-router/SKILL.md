---
name: editorial-integrity-router
description: Classify and orchestrate AI-assisted editorial work across creation, review, editing, verification and release. Use when a task may require more than one editorial capability, when project governance or factual risk affects the route, or when agents need explicit hand-offs, stale-artefact detection and human approval points. Do not use it to perform specialist drafting, editing, verification or release decisions itself.
---

# Editorial Integrity Router

## Purpose
Select the minimum adequate workflow, declare authority and assemble specialist outputs without becoming a generic super-Skill.

## Required inputs
- assignment request and intended output
- project manifest when one governs the work
- available artefacts and their versions
- form, audience, purpose and consequence
- factual, privacy, voice and continuity risks
- approval owner or unresolved ownership

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
- Read `references/risk-and-routing-matrix.md` when classifying consequence, factual risk, authority, workflow depth, staleness or downstream consumers.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
