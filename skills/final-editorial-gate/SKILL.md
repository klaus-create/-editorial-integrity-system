---
name: final-editorial-gate
description: Perform the final release-readiness review before submission, publication or external circulation. Use to verify required upstream artefacts, meaning, claims, attribution, voice, form, uncertainty, privacy and human approval. Decide release status without silently rewriting.
---

# Final Editorial Gate

## Purpose
Issue a traceable release decision based on required evidence and governance, not prose polish or intuition.

## Execution workflow
1. Determine required artefacts from workflow level, consequence and manifest.
2. Confirm artefacts exist, are current and cover the final draft.
3. Test thesis and meaning preservation.
4. Test facts, attribution, privacy and disclosure.
5. Test argument, voice, register, form and protected characteristics.
6. Review unresolved P0/P1 findings and material post-verification changes.
7. Apply release matrix.
8. Return ready, conditional, human decision required or blocked with evidence and next action.

## Governing rules
- Preserve verified facts, quotations, attribution, authorised uncertainty and human meaning.
- Do not invent evidence, experience, examples, sources or certainty.
- Keep review, editing, verification and release authority separate.
- Surface material uncertainty and stop conditions rather than resolving them silently.

## Required references
- Read `references/method.md` for execution, branching, examples and escalation.
- Read `references/quality-gate.md` before returning consequential work.
- Use `tests/cases.yaml` when validating changes to this Skill.
- Use `references/output-contract.yaml` for consequential or agent-to-agent output.

## Output discipline
Return a structured, portable output for agent-to-agent or consequential work. For simple user-facing tasks, return the requested result plus only material unresolved issues.
