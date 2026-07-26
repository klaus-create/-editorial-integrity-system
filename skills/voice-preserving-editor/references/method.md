# Specialist Method

## Scope and authority
The Editor changes text only within explicit authority. It may repair mechanics, clarity, compression, expansion or structure as authorised. It cannot invent facts, examples or experiences, override verification, resolve an accountable thesis choice or conceal material transformation.

## Required inputs and intake
1. Confirm original version, requested outcome and editing scope.
2. Determine maximum authorised edit level.
3. Load brief, findings, verified claims, quotations and protected characteristics.
4. Record exact spans that must remain unchanged.
5. Identify unresolved issues that editing cannot solve.

## Execution procedure
1. Establish the preservation baseline.
2. For each proposed change, state the problem and consequence.
3. Select the lowest sufficient level on the edit ladder.
4. Apply local repairs before paragraph, section or whole-piece change.
5. For compression, remove only non-functional setup, duplication or qualification.
6. For expansion, use only authorised substance and reasoning.
7. Preserve evidence limits, attribution, causal force and emotional stance.
8. Compare original and revised propositions for material paragraphs.
9. Run voice, factual and semantic drift checks.
10. Return revised text plus stable edit IDs, a material change log and unresolved issues.

## Decision logic
Edit ladder:
- 0: preserve;
- 1: mechanical correction;
- 2: word or phrase repair;
- 3: sentence repair;
- 4: paragraph restructuring;
- 5: section restructuring;
- 6: whole-piece transformation.

Levels 4 to 6 are material. Level 6 requires explicit transformation authority or demonstrably unusable architecture. A request to “polish” does not authorise level 6.

Preservation baseline:
- thesis, claims and intended reader effect;
- quotations, attributions and approved terminology;
- uncertainty, dissent and evidence limits;
- emotional distance and first-person stance;
- characteristic rhythm, variation, punctuation and purposeful repetition;
- genre-specific irregularity and protected language.

Compression must not remove evidence, material limitation, counterargument or a necessary decision path. Expansion must not introduce new facts, experience, motives or examples.

## Version and staleness
Populate the canonical `input_versions` mapping with the exact identifier and version of every material upstream artefact.

Record the original draft, brief, findings, voice profile and verification versions used. The edit record becomes stale if the revised text changes again; material edits must explicitly mark affected verification, review or Gate artefacts for re-entry.

## Stop, escalation and re-entry
Stop when the requested edit changes the thesis, requires new evidence, conflicts with verification, erases a protected characteristic or exceeds authorised level.

Escalate logic to Argument Reviewer, claims to Verifier, missing substance to Capture and accountable transformation to the author or project owner.

Re-edit only after upstream issues are resolved. Material edits invalidate downstream verification or gate artefacts that covered the earlier version.

## Failure modes
- Regeneration replaces authorship with model defaults.
- “Clarity” can strengthen certainty or causality silently.
- Shortening can remove limitations that make a claim accurate.
- Expansion can invent explanation or examples.
- Smoothing every irregularity destroys voice.

## Examples and counterexamples
Valid: replace a generic phrase with specific authorised evidence already present in the source pack.
Invalid: add a statistic to make the sentence more persuasive.
Valid: retain a deliberate fragment when it performs emphasis.
Invalid: combine it solely because complete sentences are more conventional.

## Output assembly
Return an edit output conforming to `references/output-contract.yaml`, including editing mode, revised content, edit log with stable IDs, levels and justifications, preserved characteristics, drift checks, structured material changes and the downstream actions each material edit invalidates.
