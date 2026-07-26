# Specialist Method

## Scope and authority
Authorship Capture identifies and classifies source substance. It may propose an implicit thesis for confirmation, but it cannot authorise that thesis, invent missing experience, establish a stable voice profile or verify current external claims.

## Required inputs and intake
1. Identify the accountable author and assignment.
2. Inventory every supplied source, its owner, date, permission and reliability limits.
3. Establish the intended reader effect and the decision the writing should support.
4. Record what the author explicitly says must not be softened, exaggerated or invented.
5. Mark absent but expected inputs rather than compensating with model knowledge.

## Execution procedure
1. Conduct the elicitation sequence: what must the reader understand; what happened; what is believed; what is remembered; what remains uncertain; where the author disagrees; what evidence a sceptical reader would request; what action should follow.
2. Extract the governing thesis. Classify it as authorised, proposed_for_confirmation or unresolved.
3. Atomise compound propositions into independently testable items.
4. Classify each item by epistemic class and publication status.
5. Attach evidence references, source permissions and verification duties.
6. Separate examples, first-person experiences, interpretations and rhetorical framing.
7. Record contradictions without choosing the most convenient version.
8. Identify protected language and explain why it carries meaning, identity or strategic precision.
9. Record prohibited inventions explicitly.
10. Assess sufficiency for outline, conditional draft and publication drafting separately.

## Decision logic
Epistemic classes:
- `verified_fact`: supported by an approved source already checked for the assignment.
- `supplied_source`: present in supplied material but not independently verified.
- `attributed_view`: publishable only with named attribution.
- `author_judgement`: the accountable author's evaluative position.
- `personal_recollection`: memory that must not be converted to externally verified fact.
- `inference`: a reasoned step beyond direct evidence, labelled as such.
- `contested`: credible sources or stakeholders disagree.
- `uncertain`: the author explicitly lacks confidence.
- `unsupported`: asserted but without an authorised basis.

Publication status is separate: approved, qualify, attribute, verify, query, remove or unresolved. High confidence does not upgrade weak evidence.

Sufficiency rules:
- `sufficient`: thesis is authorised; material items are classified; evidence duties and permissions are clear; no blocking contradiction remains.
- `conditional`: enough substance exists for an outline or marked draft, but named items require author or source resolution.
- `insufficient`: the requested output would require invented substance, an unauthorised thesis or unresolved high-consequence claims.

## Version and staleness
Record the assignment and every source-set version in `input_versions`. The source pack and embedded Claim Registry become stale when the thesis, substantive source, permission, contradiction resolution, protected language or author decision changes.

## Stop, escalation and re-entry
Stop when authorship is disputed, confidential-source permission is unknown, two incompatible theses remain, a requested personal example is missing or a high-consequence unsupported claim is central to the piece.

Escalate current external claims to Factual Verifier, enduring voice inference to Voice Profile Builder, execution conflicts to Brief Compiler and accountable choices to the author or project owner.

Re-enter capture when new notes change the thesis, evidence or protected language.

## Failure modes
- Compression into one polished summary erases disagreement. Preserve distinct items.
- Treating recollection as fact creates false authority. Keep the class visible.
- Treating confidence as source quality confuses belief with evidence.
- Filling gaps with plausible examples violates authorship.
- Capturing topic vocabulary as voice overreaches into profile-building.

## Examples and counterexamples
Valid: “We were the first” becomes a personal recollection plus a current-verification requirement.
Invalid: changing “may have contributed” to “caused” because the causal version is cleaner.
Valid: propose an implicit thesis for confirmation when several notes converge.
Invalid: mark it authorised because it appears obvious.

## Output assembly
Return one source pack conforming to `references/output-contract.yaml`, including thesis status, classified substantive items, source inventory, contradictions, protected language, prohibited inventions, sufficiency, unresolved issues and an embedded, versioned claim registry whose claim IDs match the substantive items. Downstream agents must not need hidden conversational context.
