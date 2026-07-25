# Authorship and Editorial Integrity System

A platform-neutral system for preserving human authorship, factual integrity, voice, genre and editorial accountability across AI-assisted writing.

## Purpose

The system helps people and agents create, review and release writing without replacing human meaning with generic model defaults.

It supports emails, messages, social and marketing copy, reports, proposals, presentations, articles, scripts and long-form books. It combines:

- one shared editorial constitution;
- a project-specific editorial manifest;
- a routing Skill that selects the minimum adequate workflow;
- specialist Skills for capture, drafting, review, editing, verification and release;
- explicit human accountability at consequential decision points.

## Current status

**Release:** `v0.1.1-foundation-alignment`

The foundation is suitable for controlled project use and structured testing. It includes ten modular Skills, canonical schemas, project manifests, validation, packaging, regression fixtures and governance.

This is not yet a production 1.0 release. Production confidence requires broader benchmark coverage, human preference testing, cross-platform installation tests and measured false-positive and semantic-drift thresholds.

## Start here

| Need | Start with |
|---|---|
| Understand what the system does | This README |
| Use it on a writing task | [`docs/QUICKSTART.md`](docs/QUICKSTART.md) |
| Understand user and agent journeys | [`docs/USE-CASES-AND-INTERACTION-FLOWS.md`](docs/USE-CASES-AND-INTERACTION-FLOWS.md) |
| Configure a project | [`skills/editorial-integrity-router/references/manifest-guide.md`](skills/editorial-integrity-router/references/manifest-guide.md) |
| Review delivery priorities | [`ROADMAP.md`](ROADMAP.md) |
| Understand governing rules | [`constitution/editorial-constitution.md`](constitution/editorial-constitution.md) |
| Review the release boundary | [`governance/RELEASE-0.1.1.md`](governance/RELEASE-0.1.1.md) |

## Who interacts with the system

The system distinguishes between several roles. One person or agent may perform more than one role.

| Actor | Responsibility |
|---|---|
| Requesting user | Supplies the task, source material, draft or intended outcome |
| Accountable author or project owner | Owns meaning, claims and final accountability |
| Router agent | Classifies the task, loads project rules and selects the workflow |
| Specialist Skill agent | Performs a bounded task such as capture, drafting, review or verification |
| Tool or connector agent | Retrieves approved sources or performs deterministic validation |
| Human approver | Accepts, rejects or qualifies consequential outputs before release |

## Paths into the system

A task can enter through five primary paths.

### 1. Direct writing request

```text
User request
  -> Router classifies form and risk
  -> Minimum required Skills
  -> Finished writing
  -> User review or approval
```

Best for routine emails, messages, captions and clearly specified short-form work.

### 2. Project-governed creation

```text
Project manifest + project sources + assignment
  -> Router loads project rules
  -> Source and authorship capture where needed
  -> Brief, draft, review, edit and verification
  -> Final gate
  -> Approved output + unresolved issues
```

Best for recurring client, brand, product, research or book work.

### 3. Existing-draft review or revision

```text
Draft + requested review mode
  -> Argument and structure review and/or anti-slop audit
  -> Findings separated from edits
  -> Voice-preserving local revision
  -> Verification where claims changed
  -> Revised draft + material change notes
```

Best when the user already has authored material and wants improvement without voice flattening.

### 4. High-consequence publication

```text
Authorised sources + claim registry + draft
  -> Full factual and attribution verification
  -> Human decision on unresolved claims
  -> Final editorial gate
  -> Release, conditional release or block
```

Best for investor, policy, regulated, public-claim and reputation-sensitive work.

### 5. Agent-to-agent orchestration

```text
Calling agent submits assignment contract
  -> Router emits route and required artefacts
  -> Specialist agents return bounded outputs
  -> Router assembles status
  -> Human approval when required
  -> Calling agent receives output package
```

Best for automated or multi-agent workflows. Agents must exchange explicit artefacts rather than relying on hidden conversational assumptions.

## Inputs and outputs

### Common inputs

- assignment request;
- project editorial manifest;
- existing draft or notes;
- approved sources;
- voice, register and audience profiles;
- output form and surface;
- factual risk and consequence level;
- approval and privacy requirements.

### Common outputs

- finished or revised writing;
- Authorship Source Pack;
- Claim Registry;
- Voice Profile;
- Editorial Brief;
- review or audit findings;
- verified, qualified or blocked claims;
- final gate decision;
- unresolved-issues list;
- change or audit record where required.

The specific input and output contract for each Skill is documented in [`docs/USE-CASES-AND-INTERACTION-FLOWS.md`](docs/USE-CASES-AND-INTERACTION-FLOWS.md).

## Architecture

```text
Editorial constitution
        |
Project editorial manifest
        |
Editorial Integrity Router
        |
        +-- Authorship Capture
        +-- Voice Profile Builder
        +-- Editorial Brief Compiler
        +-- Source-Grounded Drafter
        +-- Argument and Structure Reviewer
        +-- Anti-Slop Auditor
        +-- Voice-Preserving Editor
        +-- Factual Verifier
        +-- Final Editorial Gate
        |
Human-accountable release
```

The Router is the control plane. Specialist Skills remain bounded. Review Skills diagnose; editing Skills edit; verification can override style for factual integrity; the final gate decides release status but does not silently rewrite the work.

## Workflow levels

| Level | Typical work | Default handling |
|---|---|---|
| 0: Direct | Informal emails, brief messages, minor corrections | Preserve meaning and tone, then surface-check |
| 1: Guided | Client email, social, marketing, short public copy | Add audience, voice, anti-slop and final-gate controls |
| 2: Governed | Reports, proposals, articles, executive presentations | Use source capture, brief, review, editing, verification and gate as required |
| 3: Extended | Books, major research, regulated or continuity-sensitive work | Add claim registry, continuity, versioned source packs, audit trail and explicit approval |

Use the lowest level that adequately protects truth, meaning, voice and consequence.

## Project manifests

Each continuing project should contain one canonical `project-editorial-manifest.yaml`. It defines:

- ownership and authorship model;
- default audience, voice and register;
- form-specific routing;
- source and verification rules;
- required Skills;
- approval, privacy and retention controls;
- project-specific exceptions.

The canonical schema is:

```text
skills/editorial-integrity-router/references/project-editorial-manifest.schema.yaml
```

Validate a manifest with:

```bash
python scripts/validate_manifest.py projects/<project>/project-editorial-manifest.yaml
```

## Repository structure

```text
constitution/        Shared editorial laws and decision hierarchy
docs/                User journeys, agent contracts and quick-start guidance
schemas/             Platform-neutral artefact contracts
skills/              Installable modular Skills
projects/            Canonical project manifest examples
scripts/             Validation and packaging utilities
tests/               Regression corpus and expected behaviours
governance/          Versions, release boundaries and change control
.github/workflows/   Automated repository validation
```

## Installation and packaging

Skills are packaged individually because each Skill has its own `SKILL.md` entrypoint.

```bash
python scripts/package_skill.py skills/editorial-integrity-router dist
```

The resulting archive is `dist/skill.zip`. Repeat for each Skill required by the target environment.

For first use, install the Router and the specialist Skills required by the project. Then place the project's validated manifest and approved sources in the active project workspace.

## Governing principles

1. Human meaning is primary.
2. Truth and attribution outrank style.
3. Ground before generating.
4. Voice is behavioural, not cosmetic.
5. Genre, audience and voice are distinct inputs.
6. Diagnose broadly and edit locally.
7. Audit and editing remain separate.
8. Stylistic irregularity is not automatically defective.
9. Uncertainty must remain visible.
10. Human accountability remains final.

## Roadmap

The roadmap is outcome-based and distinguishes completed foundation work from the next maturity stages. See [`ROADMAP.md`](ROADMAP.md).

## Repository visibility and naming

This repository is private while the system, tests, product position and licensing model are developed.

The repository currently has a leading hyphen in its name. Renaming it to `editorial-integrity-system` is recommended. GitHub should preserve redirects, but canonical repository references should be updated after the rename.