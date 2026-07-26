# Release 0.1.3: Audit Remediation

## Status

**Contract-hardened, method-ready release candidate. Not yet pilot-tested.**

## Purpose

This release corrects the premature maturity claim in 0.1.2 and replaces structural assurance with enforceable contracts, executable fixture checks and a documented acceptance standard.

## Included remediation

### Ten reviewed Skills and specialist playbooks

Every Skill now contains:

- explicit scope and authority;
- required-input and intake checks;
- a multi-step execution procedure;
- decision logic and branching;
- stop, escalation and re-entry rules;
- failure modes;
- examples and counterexamples;
- output assembly guidance;
- an auditable quality gate;
- a domain-specific reference containing the professional models, evidence standards, calibration rules or form playbooks unique to the capability.

### Canonical contracts

- Eleven canonical JSON Schema Draft 2020-12 contracts cover ten Skill outputs and the embedded Claim Registry.
- Every per-Skill output contract is self-contained and matches its shared canonical schema.
- Every output uses a common artefact envelope and completion statuses.
- Packaged contracts match canonical repository schemas.
- The Gate uses one release-outcome vocabulary across method, schema and documentation.

### Executable fixtures

- Sixty distinct fixtures cover standard, edge, adversarial and false-positive behaviour.
- Every example output validates against the relevant Skill contract.
- Machine-checkable assertions verify critical decisions and prohibited outcomes.
- 220 generated schema mutations prove malformed contracts are rejected.
- 40 generated semantic contradictions prove cross-field validators reject internally inconsistent outputs.
- Duplicate YAML keys and semantically duplicated fixture outputs fail validation.

These are executable contract fixtures. They are not a substitute for live model-performance evaluation.

### Validation and packaging

- `scripts/validate_skill_suite.py` checks entrypoints, metadata, methods, quality gates, schemas and contract parity.
- `scripts/run_contract_tests.py` validates all fixture outputs and assertions.
- `scripts/validate_manifest.py` validates project manifests.
- `scripts/check_repository_links.py` validates local documentation and declared Skill resources.
- `scripts/package_skill.py` validates each Skill before creating `skill.zip`.
- CI runs the same repository scripts instead of inline character-count proxies.

### Governance

- The Capability Depth Standard now defines evidence for scaffold, contract-valid, method-ready, pilot-tested, measured and production-ready states.
- Release 0.1.2 is explicitly superseded.
- The audit record preserves original findings and corrective evidence.

## Release boundary

This release candidate may proceed to controlled pilots only after all deterministic checks and package tests pass.

It does not establish:

- expert-level performance on real assignments;
- superiority to an ungoverned baseline;
- acceptable semantic-drift or false-positive rates;
- cross-platform consistency;
- production readiness.

## Next evidence required

Run governed pilots across Social Marketer, OneSource and a long-form book project. Retain the assignment, route, input versions, outputs, accepted and rejected changes, verification record, gate decision and human evaluation for every case.
