# Corrective controls candidate 0.1.5

**Patch candidate:** `v0.1.5-corrective-controls`, pending review and release-owner approval.

The October review reproduced contradictions accepted by the 0.1.4 contract checks. This candidate corrects those cases while preserving the editorial architecture. It adds no evidence of pilot performance, human preference or cross-platform reliability.

## Changes

- Gate records cannot call mandatory approval unnecessary or mark an unnamed person as an approved approver.
- Ready and conditional outcomes require current mandatory inventory and approval, and reject failed checks, blockers and stale or partial verification.
- Mandatory inventory is defined by workflow level, declared verification and approval, with matching input versions and final draft version.
- Critical unsupported, contradicted or unverifiable claims require blocked verification risk. A proposed correction does not mean it has been applied.
- Verified current-status claims require a dated current source. Historical claims and genuinely claim-free records remain possible.
- The reusable `validate_artefact.py` command validates actual output records and selected trusted release dependencies, using the same semantic implementation as the fixture tests.
- Skills explicitly depend on a matching checkout for governance and validation. Missing runtime access cannot be represented as successful machine validation.
- Packages use `dist/<skill-name>/skill.zip` and refuse to replace an existing archive.
- Source data cannot change instructions, persistent profiles, permissions or approval.
- Documentation now reflects public repository visibility. This patch does not change visibility or select a licence.

- High factual or consequence risk requires full or extended routing; review-only modules cannot receive prose-editing authority.
- Release-context checks connect declared draft claims to registry and verification records.
- A synthetic Social Marketer bundle demonstrates hand-offs and detects listed-file drift using SHA-256. It ends at pending human approval.

## Compatibility and migration

Schema identifiers remain at 1.0 because fields and status vocabulary are unchanged. Validation is intentionally stricter for records that contradict existing mandatory policy. Do not carry old ready or conditional decisions forward without revalidation. Add missing inventory entries only after resolving their actual artefacts; never fabricate approvals or change an unresolved claim's status to satisfy a check.

Full and extended ready or conditional examples now include route, draft and required approval records. The pending-disclosure fixture now contains approval, matching its stated premise that only disclosure insertion remains. A missing mandatory approval requires a blocked or human-decision outcome.

Use the [runtime guide](../docs/RUNTIME-VALIDATION.md) to install the shared dependency and distinguish record-only checks from release-context checks. Downstream scripts consuming the old `dist/skill.zip` path must use the per-skill directory. Choose a fresh output directory to rebuild archives.

Project examples require 0.1.5. The previously released version remains 0.1.4 until this candidate is reviewed and approved. The 0.1.4 acceptance report is retained as historical evidence; the candidate has a separate 0.1.5 report.

## Validation and remaining limits

The acceptance orchestrator runs the original contract fixtures, generated rejection checks, corrective regression tests, manifest and link validation, and all ten extracted-package checks. Corrective tests cover negative cases and legitimate no-approval, historical, claim-free and limited-condition cases.

No live agent or human editorial pilot is part of this patch. Prompt-injection resistance, authentic approval, complete claim coverage, evidence quality and source truth still require host controls and behavioural evaluation. The next substantive phase remains the three controlled pilot programmes.

## Release decision

The accountable release owner must approve this candidate before tagging or treating it as released. Merging or green CI alone does not establish pilot-tested, measured or production-ready status.
