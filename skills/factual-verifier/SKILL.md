---
name: factual-verifier
description: Verify factual, numerical, comparative, causal, quoted, scientific, legal-adjacent, product and current claims before consequential publication. Use when unsupported or time-sensitive claims could create decision, commercial or reputational risk. Do not infer truth from confident wording, rely on search snippets, average incompatible sources or convert author judgement into verified fact.
---

# Factual Verifier

## Purpose
Determine exactly what the evidence permits the final draft to say, with what qualification, attribution and release risk.

## Required inputs
- final draft version to be covered
- claim registry and source pack
- approved sources and retrieval permissions
- claim consequence and publication context
- current-as-of requirement
- domain review or approver requirements

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
- Read `references/claim-verification-playbooks.md` when verifying numerical, causal, quoted, scientific, legal-adjacent, product or time-sensitive claims.
- Read `references/quality-gate.md` before returning consequential work.
- Use `references/output-contract.yaml` as the canonical output schema.
- Use `tests/cases.yaml` only for development, regression review or calibration of this Skill.

## Completion status
Use `complete`, `conditional`, `human_input_required` or `blocked`. State the reason, owner and required action for every non-complete status.
