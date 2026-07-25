# Roadmap

This roadmap describes how the Authorship and Editorial Integrity System moves from a controlled foundation to a production-ready, cross-platform operating system.

It is organised by outcomes, not merely by files or features. Each stage states who benefits, what becomes possible, what must be delivered and what proves the stage is complete.

## Current position

**Current release:** `v0.1.1-foundation-alignment`

The foundation now includes:

- a shared editorial constitution;
- ten modular Skills;
- a canonical Project Editorial Manifest schema;
- project manifests for Social Marketer, OneSource and long-form books;
- validation, packaging and CI;
- initial regression fixtures;
- documented user and agent interaction paths.

The current release is suitable for controlled project use and structured testing. It is not yet a production 1.0 release because performance thresholds, human preference evidence, cross-platform installation tests and mature provenance controls remain incomplete.

## Delivery principles

1. Prove reliability before adding breadth.
2. Keep human accountability explicit.
3. Prefer measurable exit criteria over feature completion claims.
4. Keep the Router thin and specialist Skills bounded.
5. Treat user experience, agent interoperability and governance as equal parts of the product.
6. Do not promote experimental capabilities into the stable path without regression evidence.

---

## Stage 0: Foundation alignment

**Target release:** `v0.1.1`

**Outcome:** A coherent repository that accurately describes and validates the system it contains.

**Primary users:** System owner, project owner, Skill maintainer, early pilot user.

### Delivered

- Current README and system map.
- Canonical manifest schema and template.
- Ten interoperable Skills.
- Project examples.
- Manifest validation and Skill packaging.
- CI checks.
- Initial regression fixtures.
- User and agent interaction documentation.

### Exit criteria

- README reflects the actual repository.
- Roadmap distinguishes completed, next and future work.
- Example manifests validate against the canonical schema.
- Router references resolve to real files.
- CI validates all manifests and packages all Skills.
- Inputs, outputs, hand-offs and human decision points are documented.

---

## Stage 1: Pilot-ready workflows

**Target release:** `v0.2`

**Outcome:** Real users can apply the system to recurring work without needing to understand the repository internals.

**Primary users:** Author, strategist, marketer, consultant, product team, book author.

### Workstreams

#### 1. Project onboarding

- Project manifest generator or guided setup flow.
- Voice profile capture template.
- Source-pack creation template.
- Example assignments for each workflow level.
- Installation and configuration checklist.

#### 2. End-to-end workflow packs

- Short-form communication pack.
- Report and proposal pack.
- Presentation narrative pack.
- Long-form manuscript pack.
- High-consequence publication pack.

#### 3. Human review experience

- Clear accept, revise, query and block states.
- Standard unresolved-issues format.
- Standard change-summary format.
- Review mode that separates findings from edits.

### Dependencies

- Stable canonical manifest.
- Router-to-Skill hand-off contract.
- Representative project source material.

### Exit criteria

- At least three real projects complete an end-to-end workflow.
- A new user can configure a project from the documentation alone.
- Each workflow produces predictable input and output artefacts.
- Human approvers can understand why an output is ready, conditional or blocked.
- Pilot feedback is logged as accepted, rejected or uncertain system behaviour.

---

## Stage 2: Measured editorial reliability

**Target release:** `v0.3`

**Outcome:** The system can demonstrate that it improves writing while preserving meaning, voice and factual integrity.

**Primary users:** System owner, evaluator, editor, risk owner.

### Workstreams

#### 1. Regression corpus expansion

- At least 50 benchmark passages.
- Coverage across short-form, marketing, reports, proposals, presentations, technical writing, policy, investor writing and books.
- Coverage across personal, brand, institutional, collaborative and literary authorship.

#### 2. Evaluation rubric

- Semantic fidelity.
- Argument fidelity.
- Factual accuracy.
- Voice and register alignment.
- Protected-trait preservation.
- Edit economy.
- False-positive edit rate.
- Reader preference and trust.

#### 3. Automated evaluation support

- Machine-readable test fixtures.
- Expected finding and prohibited-change fields.
- Diff and scoring utilities.
- Human adjudication record.

### Dependencies

- Pilot output and feedback.
- Stable artefact schemas.
- Agreed scoring thresholds.

### Exit criteria

- Benchmark corpus reaches 50 or more passages.
- Human reviewers score governed outputs against baseline outputs.
- Semantic-drift and false-positive thresholds are defined.
- No release-critical regression remains unresolved.
- Evaluation results are reproducible and versioned.

---

## Stage 3: Cross-platform portability

**Target release:** `v0.4`

**Outcome:** The same editorial rules and project configuration produce materially consistent behaviour across supported AI environments.

**Primary users:** Teams using ChatGPT, Codex, Claude, Gemini, Cursor, Copilot or other Agent Skills-compatible environments.

### Workstreams

- Platform capability matrix.
- Adapter specifications.
- Installation and packaging tests.
- Connector and browsing capability fallbacks.
- Cross-platform smoke tests.
- Output consistency comparison.

### Dependencies

- Measured reliability on one reference platform.
- Stable Skill and manifest contracts.

### Exit criteria

- Router and core Skills install successfully on supported target platforms.
- Platform limitations are explicit.
- Shared benchmark tasks are run across platforms.
- Material differences are measured and documented.
- No adapter silently weakens factual, privacy or approval controls.

---

## Stage 4: Team and enterprise governance

**Target release:** `v0.5`

**Outcome:** Organisations can manage profiles, sources, approvals and releases safely across multiple teams and projects.

**Primary users:** Editorial lead, brand lead, legal or risk reviewer, knowledge owner, platform administrator.

### Workstreams

- Workspace-scoped profiles.
- Role-based access and approval.
- Source authority and retention policies.
- Profile ownership, consent and deletion.
- Audit and change logs.
- Institutional voice profiles.
- Multi-author and collaboration rules.
- Disclosure and provenance policy.

### Dependencies

- Stable project and artefact schemas.
- Privacy and legal review.
- Proven pilot demand.

### Exit criteria

- Profiles cannot leak across projects or clients.
- Approved sources and approvers are traceable.
- Retention and deletion controls are documented and testable.
- High-consequence release paths enforce required human approval.
- Organisational governance can be configured without editing Skill internals.

---

## Stage 5: Production release

**Target release:** `v1.0`

**Outcome:** A stable, documented and measured editorial integrity operating system suitable for dependable production use.

### Required capabilities

- Stable constitution and precedence rules.
- Versioned schemas with migration guidance.
- Stable Router and bounded specialist Skills.
- Measured regression performance.
- Cross-platform support for declared environments.
- Privacy, ownership, retention and deletion controls.
- Proven installation and packaging process.
- Human approval and provenance controls.
- Clear support and change-management model.

### Exit criteria

- All Stage 1 to Stage 4 exit criteria are met.
- Production release checklist passes.
- No known critical contradiction exists between documentation, schema, validation and runtime instructions.
- Release notes describe supported and unsupported use cases.
- A rollback path exists for constitutional, schema and Skill changes.

---

## Post-1.0 research tracks

These tracks remain experimental until evidence supports promotion into the stable product.

- Retrieval over approved writing samples.
- Authorship and style embeddings.
- Multilingual voice and register profiles.
- Continuous evaluation against model changes.
- Provenance and disclosure automation.
- Editorial analytics and accepted-edit learning.
- Adaptive profiles updated only from explicitly approved changes.
- Deeper integrations with document, presentation and publishing systems.

## Explicit non-goals

The roadmap does not include:

- AI-detector evasion;
- proving that text was written by a human;
- autonomous publication without accountable approval;
- cloning a living author's voice;
- inventing facts, sources, experience or certainty;
- imposing one universal writing aesthetic across all authors and forms.