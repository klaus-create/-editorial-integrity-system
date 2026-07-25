# Authorship and Editorial Integrity System

A platform-neutral system for preserving human authorship, factual integrity, voice, genre and editorial accountability across AI-assisted writing.

## Mission

Ensure AI amplifies human authorship rather than replacing it with statistically polished sameness.

The system supports writing across emails, messages, reports, proposals, presentations, articles, scripts and long-form books. It combines one shared editorial constitution with modular Skills, project-specific manifests and proportional workflow routing.

## Current status

**Release:** `v0.1-foundation`

The repository currently contains the first deployable component:

- `editorial-integrity-router`: routes writing assignments through the minimum necessary editorial controls.
- Project Editorial Manifest schema and template.
- Form-routing and workflow-depth guidance.
- Manifest validation script.

## Architecture

```text
Editorial constitution
        ↓
Project editorial manifest
        ↓
Editorial integrity router
        ↓
Required capability modules
        ├── Authorship Capture
        ├── Voice Profile Builder
        ├── Brief Compiler
        ├── Argument Reviewer
        ├── Anti-Slop Auditor
        ├── Voice-Preserving Editor
        ├── Factual Verifier
        └── Final Editorial Gate
```

## Operating model

- **This repository** is the canonical source of truth.
- **Installed Skills** make stable workflows available across AI environments.
- **Project manifests** hold local voice, audience, source and governance requirements.
- **Assignment briefs** hold temporary direction for an individual piece of work.

## Repository structure

```text
constitution/        Shared editorial laws and decision hierarchy
schemas/             Platform-neutral data contracts
skills/              Installable modular Skills
references/          Taxonomies, examples and operating guidance
adapters/            Platform-specific wrappers
projects/             Example project manifests
scripts/              Validation, packaging and regression utilities
tests/                Regression corpus and expected behaviours
governance/           Versions, change control and release policy
```

## Governing principles

1. Human meaning is primary.
2. Truth and attribution outrank style.
3. Ground before generating.
4. Voice is behavioural, not cosmetic.
5. Diagnose broadly and edit locally.
6. Audit and editing remain separate.
7. Stylistic irregularity is not automatically defective.
8. Uncertainty must remain visible.
9. Anti-slop heuristics are advisory.
10. Human accountability remains final.

## Initial installation

The current Skill is located at:

```text
skills/editorial-integrity-router/
```

Package that folder as a ZIP when installing it into a compatible Skill environment.

## Roadmap

See [`ROADMAP.md`](ROADMAP.md).

## Repository visibility

This repository is currently private while the system, tests, product position and licensing model are developed.
