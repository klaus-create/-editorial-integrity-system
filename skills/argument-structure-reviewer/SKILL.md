---
name: argument-structure-reviewer
description: Review the logic and architecture of reports, proposals, presentations, articles, essays and books. Use when a draft needs thesis, premise, evidence, warrant, causal, counterargument, sequencing, repetition, conclusion or decision-usefulness analysis before editing. Diagnose and prioritise findings only; do not silently rewrite or replace the author’s thesis.
---

# Argument Structure Reviewer

## Purpose
Determine whether the piece earns its claims, fulfils its structural promise and supports the intended reader decision.

## Required inputs
- draft and version
- editorial brief and thesis
- claim and evidence artefacts when available
- form, audience and reader decision
- review scope and rewrite authority

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
- Read `references/argument-analysis-models.md` when mapping premises, warrants, causal chains, counterarguments, section functions or decision usefulness.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
