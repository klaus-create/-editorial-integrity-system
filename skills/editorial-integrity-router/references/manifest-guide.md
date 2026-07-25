# Project Editorial Manifest Guide

## Purpose

A Project Editorial Manifest tells the Router and specialist Skills how a continuing project should be handled. It contains project-level rules, not the temporary instructions for one assignment.

Use one canonical `project-editorial-manifest.yaml` per project workspace.

## What belongs in the manifest

- project identity and ownership;
- authorship model and accountable people;
- default language, locale, voice, register and audiences;
- form-specific workflow routing;
- factual verification and source rules;
- required and optional Skills;
- approval, privacy, retention and traceability requirements;
- explicit project exceptions.

## What does not belong in the manifest

- the full text of an individual assignment;
- transient deadlines or one-off requests;
- large source documents;
- unapproved assumptions about the author's voice;
- secrets that should be stored in a protected source system.

## Setup process

1. Copy `project-editorial-manifest.template.yaml` into the project workspace.
2. Complete project, authorship, defaults and governance first.
3. Add voice rules supported by representative, authorised material.
4. Add form-specific routes only where the project genuinely differs from the defaults.
5. Add approved source locations and authority levels.
6. Record exceptions as rules with rationales, not as unexplained preferences.
7. Validate the file before consequential use.

```bash
python scripts/validate_manifest.py projects/<project>/project-editorial-manifest.yaml
```

## Workflow level guidance

- `lightweight`: low-risk routine communication;
- `standard`: client-facing, public short-form or brand work;
- `full`: strategic, externally published or materially factual work;
- `extended`: long-form, regulated, high-risk or continuity-sensitive work;
- `auto`: allow the Router to choose the lowest adequate level.

## Authorship models

- `personal`: the named individual is the author;
- `executive_assisted`: an agent or editor assists a named executive author;
- `institutional`: the organisation is the speaking entity;
- `collaborative`: several contributors shape the substantive work;
- `brand`: the output represents a defined brand voice;
- `literary`: the individual author's artistic and rhetorical choices require heightened protection;
- `mixed`: more than one model applies and the assignment must identify which is active.

## Governance guidance

Use `block_release` for unresolved issues when unsupported claims, privacy, legal or product-truth risks must prevent publication.

Use `human_decision` when the system should surface the issue but the accountable author must decide.

Use `surface` for moderate-risk work where visibility is required but the issue is not automatically blocking.

## Change control

Update the manifest when project ownership, source authority, voice, terminology, approval or risk requirements change. Material changes should trigger revalidation and may require downstream work to be rechecked.