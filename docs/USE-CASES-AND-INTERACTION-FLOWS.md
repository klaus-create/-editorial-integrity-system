# Use Cases and Interaction Flows

## Purpose

This document defines how people, agents, tools and artefacts enter, move through and leave the Authorship and Editorial Integrity System.

It is the operating map for both conversational use and multi-agent orchestration.

## Actors

### Requesting user

Starts the task and supplies the requested outcome, source material, draft or constraints.

### Accountable author

Owns the substantive meaning and claims. May be the requesting user, an executive, a brand owner or a named project contributor.

### Project owner

Owns the project manifest, approved sources, governance settings and release process.

### Router agent

Acts as the control plane. It classifies the assignment, loads project rules, selects the minimum adequate workflow and requests specialist modules.

### Specialist agent

Performs one bounded function. It must not silently assume authority belonging to another module.

### Tool or connector agent

Retrieves sources, validates files, packages Skills or performs other deterministic operations.

### Human approver

Makes decisions the system is not authorised to make, including accepting unresolved risk, approving material claims and releasing high-consequence work.

## Core artefacts

| Artefact | Produced by | Consumed by | Purpose |
|---|---|---|---|
| Assignment contract | User or calling agent | Router | Defines form, audience, purpose, risk and expected output |
| Project Editorial Manifest | Project owner | Router and all modules | Defines project-level rules and governance |
| Authorship Source Pack | Authorship Capture | Brief Compiler, Drafter, Verifier | Captures authorised human substance |
| Claim Registry | Authorship Capture or Verifier | Drafter, Verifier, Gate | Tracks claim type, support and publication status |
| Voice Profile | Voice Profile Builder | Drafter, Editor, Gate | Describes stable voice behaviours and protected traits |
| Editorial Brief | Brief Compiler | Drafter, Reviewers, Editor | Defines the assignment-level contract |
| Draft | Drafter or user | Reviewers, Editor, Verifier | Working authored output |
| Editorial Findings | Reviewers or Auditor | Editor, user, Gate | Diagnoses issues without silently rewriting |
| Verification Record | Factual Verifier | Gate and approver | Records supported, qualified, unresolved and blocked claims |
| Gate Decision | Final Editorial Gate | User, approver, calling agent | Returns ready, conditional, human-decision-required or blocked release status |
| Output Package | Router | User or calling agent | Bundles finished work and material governance notes |

## Entry paths

### Path A: User asks for new writing

**Input**

- writing request;
- audience and purpose;
- supplied facts, notes or sources;
- project manifest when available.

**Flow**

```text
User
  -> Router
  -> classify form, risk and workflow level
  -> capture missing authorship substance when material
  -> compile brief
  -> draft
  -> review, edit and verify as required
  -> final gate
  -> User or approver
```

**Output**

- finished draft;
- unresolved issues where material;
- release state for consequential work.

**Human decision points**

- missing source material;
- disputed intent;
- unsupported consequential claims;
- publication approval.

### Path B: User provides an existing draft

**Input**

- existing draft;
- desired review or editing mode;
- voice and meaning constraints;
- sources when factual review is required.

**Flow**

```text
User draft
  -> Router
  -> determine review scope
  -> Argument and Structure Reviewer and/or Anti-Slop Auditor
  -> findings returned separately
  -> Voice-Preserving Editor only when editing is requested
  -> Factual Verifier if claims changed or are consequential
  -> final gate where appropriate
```

**Output**

- findings only, revised draft only, or both as requested;
- material change note;
- unresolved verification issues.

**Protection rule**

A review request does not automatically authorise rewriting. An audit module must not silently become an editor.

### Path C: User asks for factual verification

**Input**

- draft or claim list;
- approved sources or permission to retrieve sources;
- publication context.

**Flow**

```text
Claims
  -> Factual Verifier
  -> classify claim type and evidence requirement
  -> retrieve or inspect sources
  -> mark supported, qualified, unresolved or contradicted
  -> return corrections and verification record
  -> Human decision for residual risk
```

**Output**

- corrected factual spans where authorised;
- verification notes;
- blocked or qualified claims.

### Path D: User asks for final release approval

**Input**

- final draft;
- required upstream artefacts;
- project manifest;
- approval context.

**Flow**

```text
Draft + artefacts
  -> Final Editorial Gate
  -> check meaning, claims, voice, form, protected traits and unresolved issues
  -> `ready` / `conditional` / `human_decision_required` / `blocked`
  -> Human approver when required
```

**Output**

- gate status;
- blocking issues;
- conditions for release;
- named approval requirement.

**Boundary**

The Gate does not rewrite the piece. It decides release status.

### Path E: Agent calls the system

**Input contract**

A calling agent should provide:

```yaml
assignment:
  form: report
  subtype: strategic-recommendation
  audience: executive-team
  purpose: decision-support
  consequence_level: high
  factual_risk: high
  source_sensitivity: confidential
  expected_length: 2500-3500 words
  output_surface: document
project_manifest_location: project-editorial-manifest.yaml
source_locations:
  - research/
requested_output:
  - final_draft
  - unresolved_issues
  - gate_decision
```

**Flow**

```text
Calling agent
  -> Router
  -> route declaration
  -> specialist agent calls
  -> explicit artefact returns
  -> Router status assembly
  -> Human approval if required
  -> output package to calling agent
```

**Output contract**

```yaml
status: complete | conditional | human_input_required | blocked
workflow_level: lightweight | standard | full | extended
modules_run: []
artefacts:
  final_draft: path-or-content-reference
  findings: path-or-content-reference
  verification_record: path-or-content-reference
  gate_decision: path-or-content-reference
unresolved_issues: []
human_action_required: true | false
```

**Agent rule**

Do not pass only prose between agents when a structured artefact exists. Every hand-off should identify the artefact type, version, source and unresolved status.

## Exit paths

### Finished writing

Used for simple tasks where no governance note is material.

### Finished writing plus notes

Used when the writing is usable but contains unresolved, qualified or approval-dependent elements.

### Findings without edits

Used for audits and reviews where the user has not authorised rewriting.

### Conditional release

Used when the piece can proceed only after a named action, source confirmation or approval.

### Blocked release

Used when factual, legal, privacy, authorship or source-integrity issues make release inappropriate.

### Re-entry

Any output can re-enter the system after:

- the user supplies missing sources;
- the author resolves intent;
- an approver accepts or rejects a condition;
- a draft changes materially;
- a project manifest or profile changes.

Material changes should trigger the relevant downstream checks again.

## Skill-level input and output map

| Skill | Required input | Primary output | Must not do |
|---|---|---|---|
| Editorial Integrity Router | Assignment and project context | Route, workflow level, required modules, output package | Perform every specialist task itself |
| Authorship Capture | Human notes, sources, discussion or draft | Source Pack and initial Claim Registry | Invent missing substance |
| Voice Profile Builder | Representative, authorised writing samples | Voice Profile | Clone a living author or infer unsupported traits |
| Editorial Brief Compiler | Assignment, manifest, profiles and source pack | Editorial Brief | Add claims not authorised by sources |
| Source-Grounded Drafter | Brief, source pack, claims and profiles | Draft plus unresolved-items note | Invent facts, sources or experiences |
| Argument and Structure Reviewer | Draft, brief and form requirements | Structural findings | Rewrite the draft silently |
| Anti-Slop Auditor | Draft, profile and context | Prioritised findings | Ban stylistic devices by default |
| Voice-Preserving Editor | Draft, findings and profiles | Locally revised draft and material change note | Flatten voice or change meaning casually |
| Factual Verifier | Draft or claims and source access | Verification record and factual corrections | Treat inference as verified fact |
| Final Editorial Gate | Final draft and required artefacts | Ready, conditional, human-decision-required or blocked decision | Rewrite or waive required approval |

## Failure and escalation paths

### Missing manifest

Use default rules for low-risk work. For recurring or consequential work, recommend creating a manifest before continued use.

### Invalid manifest

Stop reliance on project-specific governance until validation passes. Do not silently fall back for high-consequence work.

### Missing sources

Proceed only with clearly labelled judgement or uncertainty, or block claims that require evidence.

### Conflicting instructions

Apply the precedence order:

1. safety, law, privacy and exact-source constraints;
2. verified facts and quotations;
3. human thesis and meaning;
4. explicit assignment direction;
5. project manifest;
6. voice and register profile;
7. audience, genre and format;
8. local editorial improvement;
9. anti-slop heuristics;
10. generic model defaults.

### Agent failure or unavailable capability

Return the failed module, missing capability, affected artefacts and safe next action. Do not imply that a check was completed when it was not.

### Unresolved high-risk claim

Qualify, remove or block the claim according to the project manifest. Escalate to the accountable human.

## Typical use cases

### Routine communication

A user asks for a client email. The Router selects Level 1, preserves relationship context, makes the requested action clear and returns the send-ready message.

### Strategic report

A project team supplies research, notes and intended recommendations. The system captures authorship, compiles a brief, drafts, reviews argument and evidence, edits locally, verifies material claims and returns a gated report.

### Presentation narrative

A user supplies report findings and asks for an executive presentation. The system treats the slide idea as the primary unit, separates slide content from speaker narrative and prevents report prose from being pasted onto slides.

### Book chapter

An author supplies a manuscript map, chapter brief, prior chapters and source material. The system preserves cumulative argument, motif, rhythm and uncertainty, and checks the chapter at sentence, section, chapter and manuscript levels.

### Investor or policy publication

The system requires claim traceability, full factual verification, explicit unresolved issues and named human approval before release.