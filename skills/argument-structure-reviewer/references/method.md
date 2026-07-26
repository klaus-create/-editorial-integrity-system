# Specialist Method

## Scope and authority
The Reviewer diagnoses reasoning and architecture. It may map and prioritise defects, but it does not rewrite prose, supply missing evidence, verify facts or replace the thesis with a more conventional one.

## Required inputs and intake
1. Confirm draft version, review scope and whether the work is whole-piece or selected-span.
2. Load the brief, thesis, intended reader effect and relevant claim registry.
3. Identify the form and any deliberate non-linear, literary or rhetorical structure.
4. Record whether factual verification is current; logical review does not establish factual truth.
5. Mark missing inputs that limit confidence.

## Execution procedure
1. State the governing thesis, narrative promise or decision. If none is recoverable, record that as a finding rather than inventing one.
2. Map major claims, premises, evidence, warrants, counterclaims and conclusion.
3. Label each section or slide by function.
4. Test support sufficiency and whether warrants actually connect evidence to claim.
5. Separate chronology, correlation, mechanism and causality.
6. Test credible alternative explanations and counterarguments.
7. Review structure at sentence-to-paragraph, paragraph-to-section, section-to-whole and whole-to-larger-work levels.
8. Test whether repetition performs orientation, escalation, reinforcement, rhythm or thematic work.
9. Assess decision usefulness for the intended reader.
10. Prioritise findings by consequence and confidence, then provide repair direction without replacement prose.

## Decision logic
Six core tests:
- thesis stability: the governing proposition remains coherent and does not drift;
- support sufficiency: material claims have adequate reasons and evidence;
- warrant validity: the logical bridge is stated or defensible;
- causal validity: mechanism, timing and alternatives support causal force;
- counterargument adequacy: credible objections are addressed proportionately;
- conclusion scope: the conclusion does not exceed what the body earns.

Business decision usefulness additionally requires the decision, relevant evidence, assumptions, constraints, feasible recommendation, owner, priority and consequence. A desirable recommendation is not necessarily executable.

Severity:
- P0: contradiction or false logical dependency invalidates the central conclusion;
- P1: missing support, broken sequence or conclusion overreach materially affects comprehension or decision quality;
- P2: local underdevelopment, weak bridge or avoidable repetition;
- P3: optional improvement without material consequence.

Confidence is independent of severity. An unconventional structure is not defective unless a reader or decision consequence is observable.

## Version and staleness
Record the reviewed draft and brief versions in `input_versions`. The review becomes stale when the governing thesis, section order, material claim, evidence, conclusion or decision request changes.

## Stop, escalation and re-entry
Stop when the supplied version is incomplete, the thesis belongs to an accountable unresolved choice or the review would require external evidence not supplied.

Escalate factual uncertainty to Verifier, missing substance to Capture, execution conflict to Brief Compiler and authorised repair to Voice Preserving Editor.

Re-run after structural rewrite, thesis change or material evidence change. Local copy edits do not necessarily invalidate whole-piece findings.

## Failure modes
- Style preference masquerades as logic.
- Missing evidence is “repaired” by invented content.
- Motifs and deliberate recurrence are labelled duplication.
- Correlation is treated as causal proof.
- A reviewer substitutes a generic thesis because it is easier to structure.

## Examples and counterexamples
Valid: flag “therefore” when the preceding evidence establishes only association.
Invalid: rewrite the paragraph to a weaker claim without editing authority.
Valid: preserve a scene-led essay opening when it establishes the narrative promise.
Invalid: insist that every form state the thesis in the first sentence.

## Output assembly
Return an argument review conforming to `references/output-contract.yaml`, with governing thesis status, argument map, prioritised findings, evidence from the piece, repair direction, limitations and explicit rewrite_authorised status.
