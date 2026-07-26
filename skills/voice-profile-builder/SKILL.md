---
name: voice-profile-builder
description: Build or refresh an evidence-based voice profile from representative, authorised samples. Use when repeated writing must preserve an author, brand or institution across multiple forms or registers, or when editors need operational traits and protected characteristics rather than vague tone adjectives. Do not use it to clone a living writer, infer permanent traits from one sample or learn automatically from unapproved AI output.
---

# Voice Profile Builder

## Purpose
Convert representative writing evidence into operational voice decisions while preserving variation, uncertainty and imitation boundaries.

## Required inputs
- profile owner and consent or organisational authority
- representative samples with known authorship and editing history
- target forms and registers
- accepted and rejected edits when available
- project or brand constraints

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
- Read `references/voice-analysis-and-sampling.md` when selecting samples, separating enduring voice from register, weighting evidence, resolving contradictions or setting confidence.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
