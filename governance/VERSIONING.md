# Versioning and Change Control

## Version model

Use semantic versions for the editorial system:

- MAJOR: constitutional, contract or governance changes that invalidate existing integrations or expected behaviour;
- MINOR: new Skills, output fields, workflow routes or materially expanded capabilities;
- PATCH: compatible corrections, clarifications, tests and non-breaking method improvements.

A version number does not imply a maturity level. Maturity evidence is governed separately by the Capability Depth Standard.

## Rule status

Every durable rule should be classified as one of:

- constitutional;
- mandatory;
- recommended;
- experimental;
- deprecated.

## Change requirements

A material change requires:

1. written rationale;
2. affected Skills, contracts, manifests and hand-offs identified;
3. standard, edge, adversarial and false-positive fixtures added or updated;
4. semantic-drift, factual and voice-erasure risks reviewed;
5. shared and packaged contracts kept identical;
6. version and release boundary updated;
7. accountable release-owner approval.

## Release gate

A release candidate may be created only when:

- every Skill passes `scripts/validate_skill_suite.py`;
- every fixture passes `scripts/run_contract_tests.py`;
- every project manifest validates;
- every Skill passes pre-package validation and produces a valid `skill.zip`;
- `scripts/audit_repository.py` reports no deterministic blocker;
- README, roadmap, release note and hand-off documentation agree;
- superseded maturity claims are explicitly corrected.

A release may be tagged as **method-ready** only when the contract and method criteria in the Capability Depth Standard pass.

A release may be tagged as **pilot-tested**, **measured** or **production-ready** only when the corresponding live evidence exists. Deterministic CI cannot grant those states.

## Contract changes

Output-contract changes require:

- a schema version decision;
- compatibility analysis for every consumer;
- fixture updates;
- stale-artefact and re-entry review;
- migration guidance when existing artefacts no longer validate.

## Exceptions

A release waiver must name the failed criterion, risk, authorising owner and re-review condition. A waiver cannot convert absent performance evidence into a higher maturity state.

## Profile learning

Accepted edits must not update an author or project profile automatically. Profile changes require explicit human approval, evidence references and version history.
