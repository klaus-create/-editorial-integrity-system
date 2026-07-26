# Specialist Method

## Scope and authority
The Router classifies, sequences and tracks work. It does not draft substantive prose, diagnose arguments, edit text, verify claims or approve release. It may summarise specialist statuses only when the summary preserves their wording, severity and unresolved conditions.

## Required inputs and intake
1. Identify the assignment, requested output and output surface.
2. Determine whether the request is creation, review, editing, verification, release, profile-building or a combination.
3. Load the project manifest if the work belongs to a continuing project.
4. Inventory available artefacts, versions and approval records.
5. Rate five risk dimensions as low, moderate or high: consequence, factual exposure, privacy, voice sensitivity and continuity.
6. Identify the accountable author, project owner and final approver. Unknown ownership is an unresolved issue, not an assumed role.

## Execution procedure
1. Normalise the request into an assignment record.
2. Select a workflow level using the decision table below.
3. Identify missing prerequisite artefacts.
4. Select only modules whose authority is required.
5. Order modules so that substance precedes drafting, diagnosis precedes editing, verification covers the final factual version and the final gate reviews the actual release candidate.
6. Declare each module's authority to retrieve, edit or release.
7. Attach stop conditions, expected output artefacts and named downstream consumers to every hand-off.
8. Mark stale artefacts before execution.
9. Run or delegate the route.
10. Assemble statuses without resolving specialist disagreement silently.

## Decision logic
| Condition | Workflow level | Mandatory default |
|---|---|---|
| Clear, private, low-consequence wording task with negligible factual risk | lightweight | Direct edit or surface check |
| Client-facing or public short-form work with moderate voice or claim risk | standard | Brief direction, relevant specialist, final surface check |
| Strategic, decision-relevant, materially factual or reputation-sensitive work | full | Source/brief controls, relevant reviews, verification and gate |
| Long-form continuity, regulated, highly sensitive or publication-critical work | extended | Versioned source pack, claim registry, continuity, audit record and explicit approval |

Escalate one level when two or more risk dimensions are high. Never downgrade solely because the requested output is short.

Module selection rules:
- Missing or disputed substance: Authorship Capture.
- Reusable voice evidence needed: Voice Profile Builder.
- Multiple inputs or constraints need one execution contract: Editorial Brief Compiler.
- New substantive writing: Source-Grounded Drafter.
- Logic, sequence or decision usefulness in question: Argument Structure Reviewer.
- Generic-model residue or voice-erasure risk: Anti Slop Auditor.
- Authorised textual change: Voice Preserving Editor.
- Material external, numerical, causal, quoted or current claims: Factual Verifier.
- Submission, publication or consequential circulation: Final Editorial Gate.

## Authority and hand-off rules
Every hand-off must state assignment ID, workflow level, input versions, requested artefact, permissions to retrieve/edit/release, stop conditions, approval owner and one or more downstream consumers. A specialist may refuse work outside its authority. The Router may re-route but may not override an integrity blocker.

## Version and staleness
Record the assignment, manifest and available artefact versions in `input_versions`. The route becomes stale when the task, release surface, risk rating, available artefacts, permissions or approval context changes.

## Stop, escalation and re-entry
Stop before execution when the requested outcome is undefined, a high-consequence task has no accountable owner, essential private-source permission is unknown or the route depends on a missing thesis that cannot be inferred safely.

Re-enter the workflow when:
- a new source changes a material claim;
- a structural rewrite invalidates review findings;
- a factual edit occurs after verification;
- any edit occurs after the final gate;
- the manifest, audience, purpose or approval context changes.

Safety and truth outrank human preference; verified evidence outranks style; authorised human meaning outranks convenience. Unresolved conflicts go to the accountable human.

## Failure modes
- Over-routing: adds cost and noise. Remove modules that do not change a decision.
- Under-routing: exposes claims, voice or governance. Escalate based on consequence, not length.
- Hidden stale artefact: invalidates downstream confidence. Mark it explicitly.
- Router-as-writer: blurs authority. Return the task to the correct specialist.
- Generic hand-off: causes agents to rely on conversational memory. Use the route contract.

## Examples and counterexamples
Valid: a current investor claim triggers full routing, verification and gate even when it appears on one slide.
Invalid: sending an audit-only request to the Editor because the user said “improve”. First determine whether editing authority was actually granted.
Valid: a book chapter with an authorised thesis but unresolved continuity question may proceed conditionally to drafting with a visible marker.
Invalid: treating an unavailable source as proof that a claim is false.

## Output assembly
Return one route declaration that validates against `references/output-contract.yaml`. Include risk ratings, selected modules with reasons, permissions and downstream consumers, input versions, stale artefacts, approval requirements, unresolved issues and a status of complete, conditional, blocked or human_input_required.
