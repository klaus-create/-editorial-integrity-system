> **Historical review.** This document was superseded by [`governance/AUDIT-2026-07-26.md`](../governance/AUDIT-2026-07-26.md), which identified additional release blockers and corrected the maturity claim.

# Repository Review: 25 July 2026

## Scope

The review assessed:

- roadmap clarity;
- stated use cases;
- paths into and out of the system;
- user and agent roles;
- artefact hand-offs;
- consistency between documentation, schemas, examples, validation and CI.

## Material findings

### 1. README was stale

The README described the Router as the first deployable component despite the repository containing a complete ten-Skill foundation.

**Resolution:** Rewritten to reflect the actual release, actors, entry paths, outputs, architecture and operating model.

### 2. Roadmap described completed work as future work

The original roadmap was a feature list rather than an outcome-based delivery plan. It did not show dependencies, user value or release exit criteria.

**Resolution:** Replaced with staged outcomes from foundation alignment through pilot readiness, measured reliability, portability, enterprise governance and production 1.0.

### 3. User and agent journeys were implicit

The Router described internal routing, but the repository lacked a clear operating map for users, agents, tools, human approvers and artefacts.

**Resolution:** Added `docs/USE-CASES-AND-INTERACTION-FLOWS.md` and `docs/QUICKSTART.md`.

### 4. Manifest examples and validator contradicted the canonical schema

The canonical schema used `manifest_version`, `project`, `authorship`, `defaults` and `governance`. Example manifests and the validator used a separate `project_editorial_manifest` wrapper and different fields.

**Resolution:** Migrated all examples to the canonical schema and replaced the validator with JSON Schema validation.

### 5. CI did not validate against the canonical schema

CI checked only a small legacy field set.

**Resolution:** CI now installs `jsonschema`, validates all project manifests against the canonical schema and confirms the Router's declared reference files exist.

### 6. Router referenced missing supporting documents

The Router listed `manifest-guide.md`, `default-manifest.md` and `examples.md`, but those files were absent.

**Resolution:** Added all missing Router references and kept them one level from `SKILL.md`.

### 7. Repository naming remains incorrect

The repository still has a leading hyphen.

**Owner action required:** Rename it in GitHub settings to `editorial-integrity-system`, then update canonical repository references.

## Review conclusion

The architecture is strong, but the repository previously overstated coherence because documentation, examples and validation did not share one contract. The corrective changes make the operating paths explicit and align the user-facing documentation with the runtime artefacts.

The main residual maturity gap is not architecture. It is empirical validation through real use, larger regression coverage, human preference testing and cross-platform installation tests.