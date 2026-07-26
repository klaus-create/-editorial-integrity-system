---
name: editorial-brief-compiler
description: Compile project context, authorised substance, audience, form, voice, claim status and governance into a single editorial brief. Use before substantive drafting or transformation when multiple constraints must be reconciled, when agents need a portable execution contract, or when evidence and release duties must be explicit. Do not use it to invent the thesis, verify claims or resolve accountable human choices silently.
---

# Editorial Brief Compiler

## Purpose
Produce the smallest complete execution contract that tells downstream agents what the piece must do, preserve, evidence and avoid.

## Required inputs
- assignment and output requirements
- active project manifest
- authorship source pack and claim registry
- audience, form and surface constraints
- voice and register profiles
- approval, privacy and release requirements

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
- Read `references/form-brief-patterns.md` when compiling a brief for a specific form, surface or decision context.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
