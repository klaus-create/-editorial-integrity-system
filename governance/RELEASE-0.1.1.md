> **Historical release record.** Current maturity and release status are defined by `RELEASE-0.1.3.md`.

# Release 0.1.1: Foundation Alignment

## Status

Foundation aligned for controlled real-world use and structured testing.

## Purpose of this release

Release 0.1.1 corrects coherence gaps identified in the repository review. It does not add a new editorial philosophy. It makes the repository, documentation, manifests, validation and automated checks describe and enforce the same system.

## Included changes

### Product and roadmap clarity

- README updated to reflect the complete ten-Skill foundation.
- Outcome-based roadmap with users, dependencies and exit criteria.
- Explicit non-goals and production-release boundary.

### User and agent operation

- Quick-start guide.
- Human and agent role definitions.
- Entry, exit, re-entry, failure and escalation paths.
- Skill-level input and output map.
- Structured agent-to-agent hand-off contracts.

### Manifest alignment

- Social Marketer, OneSource and book manifests migrated to the canonical schema.
- Legacy `project_editorial_manifest` wrapper rejected by validation.
- JSON Schema validation introduced.

### Router completeness

- Manifest guide added.
- Default manifest behaviour added.
- Routing examples added.
- All references declared by the Router now resolve.

### Automated safeguards

- CI installs `pyyaml` and `jsonschema`.
- CI validates all project manifests against the canonical schema.
- CI checks the Router's required reference files.
- CI continues to verify Skill structure and packaging.

## Supported use cases

- Routine and client-facing communication.
- Social and marketing content.
- Reports, proposals and articles.
- Presentation narrative.
- Product, technical and investor writing.
- Long-form books and manuscripts.
- Factual verification and release gating.
- Agent-to-agent editorial orchestration.

## Known limitations

- Regression coverage remains below the 1.0 target of 50 benchmark passages.
- Human preference testing and quantitative thresholds are not yet complete.
- Cross-platform installation and consistency tests remain future work.
- Factual verification depends on source and connector availability.
- Presentation visual production remains delegated to presentation-building tools.
- Repository naming still requires owner correction.

## Next release target

Release 0.2 should focus on pilot-ready workflows, guided project onboarding and end-to-end use by at least three real projects.