# Release 0.1.4: Post-Merge Hardening

## Status

**Contract-valid and method-ready release. Not yet pilot-tested.**

Merged release 0.1.3 established the corrected capability foundation. This patch closes its pre-merge lifecycle language and strengthens the reproducibility and package-integrity controls that protect the foundation after release.

## Included hardening

### Release-state closure

- README and roadmap identify 0.1.4 as the current release rather than a release candidate.
- Release 0.1.3 is retained as the historical audit-remediation release.
- The acceptance report and audit script use released-state terminology.
- The full audit records that its deterministic acceptance criteria were satisfied and the corrective pull request was merged.
- Project manifests require editorial system version 0.1.4.

### Reproducible validation

- Validation dependencies are pinned in `requirements-validation.txt`.
- GitHub Actions installs the pinned dependency set with pip caching.
- The workflow declares read-only repository permissions, concurrency control and manual dispatch support.

### Package integrity

- `scripts/validate_packages.py` builds every Skill package.
- Every archive is checked for corruption, unsafe paths and exact expected topology.
- Packaged bytes are compared with the source Skill.
- Every archive is extracted and its metadata, output schema and executable fixtures are directly revalidated; exact byte parity ties the package to the fully validated source Skill.
- The acceptance orchestrator treats extracted-package validation as a release requirement.

### Governance

- Versioning now includes a post-merge closure gate.
- The repository audit checks current release language, pinned validation dependencies and extracted-package validation.
- Candidate language remains valid only where it describes a writing artefact, voice-trait state or historical release process.

## Acceptance evidence

Release 0.1.4 is acceptable only when:

- all ten Skills pass suite validation;
- all sixty positive fixtures, 220 schema rejection checks and 40 semantic contradiction checks pass;
- all three project manifests validate against the current system version;
- all repository links resolve;
- all ten packages are built, byte-compared, safely extracted and directly revalidated;
- the tracked repository acceptance report is current;
- GitHub Actions passes on the patch pull request and merged `main` state.

## Release boundary

This patch strengthens release hygiene and deterministic assurance. It does not establish:

- expert-level performance on real assignments;
- superiority to an ungoverned baseline;
- acceptable semantic-drift or false-positive rates;
- cross-platform consistency;
- pilot-tested, measured or production-ready maturity.

## Next evidence required

Run governed pilots across Social Marketer, OneSource and a long-form book project. Retain the assignment, route, input versions, outputs, accepted and rejected changes, verification record, gate decision and human evaluation for every case.
