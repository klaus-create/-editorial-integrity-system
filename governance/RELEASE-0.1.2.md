# Release 0.1.2: Capability Depth

## Status

Method-complete release candidate for controlled pilot use.

This release does not claim that the Skills are proven expert systems. It moves them from architectural scaffolds to specialist methods that can now be meaningfully tested.

## Why this release exists

The repository review found that the capability boundaries and governing philosophy were strong, but most Skills contained only broad workflows and safeguards. They did not yet encode enough branching logic, professional method, calibrated examples, stop conditions or testable output contracts.

## Included changes

Every core Skill now contains:

- explicit intake and sufficiency logic;
- specialist operating method;
- branching, stop and escalation rules;
- bounded authority and hand-off behaviour;
- calibrated positive, negative and false-positive cases;
- a quality gate and self-check;
- a structured output contract;
- at least four adversarial or edge-case tests.

The ten deepened Skills are:

1. Editorial Integrity Router
2. Authorship Capture
3. Voice Profile Builder
4. Editorial Brief Compiler
5. Source-Grounded Drafter
6. Argument and Structure Reviewer
7. Anti-Slop Auditor
8. Voice-Preserving Editor
9. Factual Verifier
10. Final Editorial Gate

## Repository safeguards

CI now requires each Skill to contain and reference:

- `SKILL.md`
- `agents/openai.yaml`
- `references/method.md`
- `references/quality-gate.md`
- `references/output-contract.yaml`
- `tests/cases.yaml`

CI parses the YAML contracts and cases, requires at least four calibrated cases per Skill, checks minimum method and quality-gate substance, validates project manifests and packages every Skill.

## Local validation

Before publication, all ten Skills passed the official Skill validator and were packaged successfully with the official Skill packaging utility. Each package remained well below the 25 MB limit.

## Maturity boundary

The Skills are now **method-complete**.

They are not yet:

- pilot-tested across representative real assignments;
- measured against baseline model behaviour;
- validated through accepted and rejected human edits;
- calibrated to quantified semantic-drift or false-positive thresholds;
- proven consistent across supported AI environments;
- production-ready.

## Next required stage

Run controlled pilots across Social Marketer, OneSource and a long-form book project. Record routes, artefacts, outputs, accepted edits, rejected edits, verification outcomes and gate decisions. Use that evidence to refine the methods before declaring the suite pilot-tested.
