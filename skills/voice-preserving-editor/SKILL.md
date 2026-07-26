---
name: voice-preserving-editor
description: Edit existing writing with the smallest sufficient intervention while preserving human meaning, factual boundaries, voice, rhythm, register and protected characteristics. Use after diagnosis or when the user explicitly requests polishing, shortening, expansion or transformation. Do not invent substance, silently strengthen claims, normalise distinctive language merely because it is unusual or perform whole-piece regeneration without authority.
---

# Voice Preserving Editor

## Purpose
Repair authorised problems locally and make every material change traceable to a justified editorial need.

## Required inputs
- original draft and version
- requested change and editing authority
- brief, findings and factual constraints
- voice and register profile
- protected language and characteristics
- required output and change-report depth

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
- Read `references/edit-ladder-and-drift.md` when choosing edit authority, compressing or expanding, testing semantic drift or identifying downstream invalidation.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
