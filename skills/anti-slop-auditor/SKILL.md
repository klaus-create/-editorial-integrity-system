---
name: anti-slop-auditor
description: Audit existing writing for generic model defaults, inflated or empty language, structural over-regularity, unsupported certainty, chatbot residue and voice-erasure risk. Use when reviewing or de-genericising AI-assisted writing. Diagnose clusters in context and do not infer text origin.
---

# Anti Slop Auditor

## Purpose
Identify high-confidence editorial artefacts and credibility failures without treating unusual human style as proof of AI authorship.

## Execution workflow
1. Read the whole piece, brief, voice profile and form.
2. Establish a context baseline.
3. Scan linguistic, rhetorical, structural, epistemic, conversational, formatting and voice-erasure categories.
4. Require a cluster, consequence or clear residue.
5. Check protected traits and false positives.
6. Assign severity, confidence and preserve/query/edit/block treatment.
7. Return findings only unless editing is separately authorised.

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
