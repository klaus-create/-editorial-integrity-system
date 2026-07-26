---
name: authorship-capture
description: Capture the authorised human substance for consequential AI-assisted writing. Use when the thesis, claims, evidence, examples, experience, disagreement or uncertainty is scattered, implicit or incomplete, and downstream agents need a traceable source pack. Do not use it to beautify prose, manufacture missing experience, infer final voice rules or verify current external claims.
---

# Authorship Capture

## Purpose
Turn supplied human thought and evidence into an authorised source pack without inventing, smoothing or prematurely drafting the piece.

## Required inputs
- assignment and accountable author
- notes, transcripts, drafts and supplied sources
- known audience and intended reader effect
- source permissions and confidentiality constraints
- project manifest when applicable

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
- Read `references/elicitation-and-epistemic-classification.md` when eliciting an undeveloped position, classifying knowledge states, atomising claims, resolving contradictions or judging source sufficiency.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
