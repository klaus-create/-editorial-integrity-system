---
name: anti-slop-auditor
description: Audit existing writing for generic model defaults, inflated or empty language, structural over-regularity, unsupported certainty, chatbot residue and voice-erasure risk. Use when the user asks to review, de-genericise, humanise or assess AI-assisted writing. Diagnose only unless editing is explicitly requested.
---

# Anti-Slop Auditor

## Purpose
Identify material editorial weaknesses without treating stylistic preference or detector-like signals as proof of AI authorship.

## Workflow
1. Read the full piece and active project or voice profile.
2. Identify clusters of linguistic, rhetorical, structural, epistemic, conversational and formatting issues.
3. Assess each finding in context of author, audience, genre and purpose.
4. Check protected characteristics before recommending change.
5. Assign severity and confidence.
6. Return ranked findings with preserve, query or edit recommendations.

## Severity
- P0: clear error, tool residue or publication blocker
- P1: materially harms meaning, credibility or quality
- P2: likely weak but context-sensitive
- P3: stylistic observation only

## Rules
- Clusters matter more than isolated words or punctuation.
- Fragments, repetition, rhetorical questions, long syntax, archaism and unusual punctuation are not defects by default.
- Unsupported claims outrank stylistic polish.
- The auditor is advisory and must not automatically rewrite.

## Output
For each finding provide location, category, severity, confidence, consequence, protected traits considered and recommended treatment. Use `../../schemas/editorial-finding.schema.yaml` when available.