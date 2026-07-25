---
name: editorial-integrity-router
description: Route any writing task through a governed editorial integrity workflow. Use for emails, messages, reports, proposals, presentations, articles, scripts, books, and other authored work when the user wants writing that preserves meaning, facts, voice, genre, and project context while reducing generic AI defaults. Reads a project editorial manifest when available, chooses the minimum necessary workflow, protects project-specific voice and constraints, and identifies when source capture, fact verification, argument review, anti-slop audit, or local editing is required.
---

# Editorial Integrity Router

Use this Skill as the control plane for writing work across projects. It does not replace form-specific writing Skills. It decides which editorial controls are necessary, loads the relevant project manifest, and routes the task proportionately.

## Governing rules

1. Preserve verified facts, exact quotations, attribution, and human meaning before style.
2. Never invent evidence, experience, examples, or certainty to complete a weak brief.
3. Treat voice, genre, audience, and project instructions as distinct inputs.
4. Diagnose broadly but edit locally. Avoid full regeneration unless the user requests it or the structure is unusable.
5. Anti-slop heuristics are advisory. Do not remove fragments, repetition, unusual syntax, rhetorical questions, em dashes, technical language, or other devices merely because they may appear in model-written text.
6. Use the lightest workflow that adequately protects the work.
7. Surface unresolved factual, strategic, ethical, or authorship questions instead of silently resolving them.
8. Do not optimise for AI-detector scores or claim to prove human authorship.

## Workflow

### 1. Identify the writing assignment

Classify form, audience, purpose, consequence, expected length, source sensitivity, factual risk, authorship model and output surface.

### 2. Load the project manifest

Look for `project-editorial-manifest.yaml`, `project-editorial-manifest.yml`, `editorial-manifest.yaml`, or `editorial-manifest.yml`.

If no manifest exists, use the default rules and infer only what the project context clearly supports.

### 3. Select workflow depth

- **Lightweight**: routine emails, messages, captions and low-risk copy.
- **Standard**: client-facing copy, articles, social posts and marketing content.
- **Full**: reports, proposals, strategy, investor materials and public claims.
- **Extended**: books, major research, regulated and continuity-sensitive writing.

### 4. Determine required modules

Select only what is needed: authorship capture, claim registry, audience and register profile, brief compilation, drafting, argument review, anti-slop audit, voice-preserving edit, factual verification, final gate, continuity review or presentation narrative review.

### 5. Execute or hand off

When another installed Skill is more specific, invoke or defer to it while preserving this Skill's governing rules and the active manifest.

### 6. Apply the final gate

Check that meaning is preserved, claims are authorised, voice and register fit, the form is appropriate, high-confidence model artefacts are reduced, protected characteristics survive and unresolved issues are visible.

## Precedence

1. Safety, legality, privacy, attribution and exact-source constraints.
2. Verified facts and quotations.
3. Human thesis, intent and substantive meaning.
4. Explicit assignment direction.
5. Project manifest.
6. Voice and register profile.
7. Audience, genre, channel and format.
8. Local editorial improvements.
9. Anti-slop heuristics.
10. Generic readability defaults.

## Output behaviour

For simple tasks, return only the finished writing unless review detail is requested.

For consequential tasks, provide the finished work plus concise unresolved issues or verification notes where material.

For audits, separate findings from edits and use P0 to P3 severity.

## References

- `references/project-editorial-manifest.schema.yaml`
- `references/project-editorial-manifest.template.yaml`
- `references/manifest-guide.md`
- `references/default-manifest.md`
- `references/workflow-levels.md`
- `references/form-routing.md`
- `references/examples.md`

## Validation

Use `scripts/validate_manifest.py <manifest.yaml>` before relying on a consequential project manifest.
