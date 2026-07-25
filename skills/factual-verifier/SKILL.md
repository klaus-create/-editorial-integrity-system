---
name: factual-verifier
description: Verify material factual, numerical, comparative, causal, quoted, scientific, legal-adjacent, product and current claims before publication. Use when unsupported or time-sensitive claims could create reputational, commercial, legal or decision risk.
---

# Factual Verifier

## Purpose
Determine what evidence permits the piece to say, with what confidence, attribution, qualification or release restriction.

## Execution workflow
1. Extract and atomise material claims.
2. Classify claim type, materiality and evidence burden.
3. Select sources by authority, proximity, independence and freshness.
4. Verify names, dates, figures, units, quotations, comparisons, product status and causal language.
5. Reconcile conflicts and record unresolved disputes.
6. Assign publication status and action.
7. Make only authorised factual amendments.
8. Return verification record, source trace and risks.

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
