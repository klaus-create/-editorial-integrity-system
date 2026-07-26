---
name: source-grounded-drafter
description: Draft substantive writing from an authorised brief, source pack, claim registry and voice constraints. Use when the output must remain traceable to supplied evidence and human judgement, when uncertainty and source gaps must stay visible, or when form-specific architecture matters. Do not use it to invent facts, examples, quotations or personal experience, or to repair a fundamentally broken brief silently.
---

# Source Grounded Drafter

## Purpose
Create an effective first draft that expresses authorised human meaning in the required form without exceeding evidence or hiding unresolved gaps.

## Required inputs
- validated editorial brief
- authorised source pack and claim registry
- approved source material
- voice and register constraints
- form and surface requirements
- retrieval and editing authority

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
- Read `references/form-drafting-playbooks.md` when drafting a specific form, integrating evidence, handling transitions, placing gap markers or building source traceability.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
