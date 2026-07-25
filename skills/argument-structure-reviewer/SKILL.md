---
name: argument-structure-reviewer
description: Review logic, structure, evidence flow and decision usefulness without silently rewriting. Use when a draft needs thesis, premise, causality, sequencing, counterargument, repetition, conclusion or whole-piece architecture analysis before editing.
---

# Argument Structure Reviewer

## Purpose
Diagnose whether the piece earns its claims and fulfils its structural promise while separating logical defects from stylistic preference.

## Execution workflow
1. Identify governing thesis, narrative promise or decision.
2. Map claims, premises, evidence, warrants, counterclaims and conclusion.
3. Label section/slide functions and dependencies.
4. Test support, causal links, alternatives and conclusion scope.
5. Review local, section and whole-piece structure separately.
6. Assign severity and confidence.
7. Return prioritised findings only unless editing is separately authorised.

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
