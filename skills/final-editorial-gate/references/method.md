# Specialist Method

## Scope and authority
The Gate evaluates release readiness. It does not repair prose, verify new claims, resolve accountable choices or waive mandatory evidence. A waiver must be explicit, authorised and recorded.

## Required inputs and intake
1. Confirm the exact final draft version and intended release surface.
2. Load the route declaration and workflow level.
3. Inventory mandatory artefacts and versions.
4. Check whether any draft, claim, source, manifest or approval change has made an artefact stale.
5. Identify the accountable approver and disclosure obligations.

## Execution procedure
1. Check authority and artefact completeness.
2. Check factual, quotation, attribution and source integrity.
3. Check preservation of the authorised thesis and intended reader effect.
4. Check privacy, legal-adjacent, disclosure and provenance requirements.
5. Check argument coherence, structure and conclusion scope.
6. Check voice, register, form and protected characteristics.
7. Check residual genericity, tool residue and surface quality.
8. Confirm human approval and waiver records.
9. Assign one canonical outcome.
10. Return blockers, conditions, owners and return paths without rewriting.

## Decision logic
Required artefacts by level:
- lightweight: instruction, final version and surface check;
- standard: piece direction, project or voice constraints, final version and unresolved-issue record;
- full: manifest where governed, brief, sources or source pack, relevant review findings, verification for material claims and final version;
- extended: full requirements plus claim registry, continuity record, versioned sources, approval record, change log and disclosure or provenance record.

Artefacts are stale when the final draft, material claim, source, manifest, purpose, audience or approval context changes after the artefact was produced.

Outcome vocabulary:
- `ready`: all mandatory conditions met and no blocker remains;
- `conditional`: limited, named actions remain and do not change the core argument;
- `human_decision_required`: available evidence or policy permits more than one accountable choice;
- `blocked`: a mandatory integrity, evidence, permission or governance condition fails.

Blocking conditions include P0, unresolved material P1, unsupported or contradicted critical claim, missing source permission, verification that does not cover the final version, missing mandatory approval, unresolved privacy issue or unmet disclosure obligation.

## Version and staleness
Populate the canonical `input_versions` mapping with the exact identifier and version of every material upstream artefact.

Record the exact release-candidate version and every reviewed artefact version. The Gate decision becomes stale after any material text, claim, evidence, disclosure, approval, manifest or release-surface change.

## Stop, escalation and re-entry
The Gate stops release rather than repairing. Return factual blockers to Verifier, structural blockers to Reviewer then Editor, voice issues to Editor, missing substance to Capture and assignment conflict to Brief Compiler or accountable human.

Any material edit after the Gate invalidates the decision. A new gate record must cover the changed version.

## Failure modes
- Polished prose creates false confidence despite weak evidence.
- A late statistic is added after verification.
- Optional improvements are presented as release blockers.
- Human judgement is blocked when it should be escalated.
- A waiver is implied rather than named and authorised.

## Examples and counterexamples
Valid: block a strong investor paragraph containing an unsupported market-leadership claim.
Invalid: pass it because the risk is disclosed in a footnote that does not correct the claim.
Valid: use human_decision_required when two evidence-consistent strategic framings remain.
Invalid: choose the one that sounds stronger.

## Output assembly
Return a gate decision conforming to `references/output-contract.yaml`, including draft version, artefacts reviewed, stale status, ordered check results, canonical outcome, material reasons, blockers, release conditions, approval, verification and disclosure status, and return paths. The common `status` describes whether the Gate completed its assessment. A completed assessment may legitimately return `outcome: blocked`.
