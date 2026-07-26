# Specialist Method

## Scope and authority
The Verifier checks material claims and may make the smallest factual correction necessary. It does not improve unrelated prose, supply strategic judgement, provide professional legal or scientific sign-off, or treat unavailable evidence as proof of falsehood.

## Required inputs and intake
1. Confirm the exact draft version under verification.
2. Load the claim registry, source pack and approved source boundaries.
3. Identify publication context, audience, consequence and current-as-of date.
4. Confirm retrieval permission and any required primary-source or qualified-domain review.
5. Record claims excluded from scope explicitly.

## Execution procedure
1. Extract and atomise every material claim from the final draft.
2. Classify claim type and materiality.
3. Set the evidence burden before searching.
4. Retrieve the strongest claim-specific source available.
5. Evaluate authority, proximity, independence and freshness.
6. Perform claim-type checks.
7. Reconcile conflicts in definitions, period, scope and methodology.
8. Assign a publication status and action.
9. Apply only minimal factual amendments that preserve authorised meaning where evidence permits.
10. Record sources, access dates, checks, unresolved risks and reproducibility notes.

## Decision logic
Claim-specific burdens:
- simple fact: authoritative source directly states the proposition;
- numerical: source, period, denominator, unit, methodology and arithmetic;
- comparative or superlative: comparison set, metric, period and independent basis;
- causal: temporal order, mechanism, alternatives and evidence capable of supporting causality;
- prediction: model, assumptions, horizon and uncertainty;
- quotation: original wording, speaker, date, context and transcription;
- scientific: evidence hierarchy, population, effect size, limitations and current consensus;
- legal-adjacent: jurisdiction, effective date, exact instrument and qualified review where interpretation matters;
- product capability: current official documentation or verified live behaviour, separated from beta and roadmap;
- current status: authoritative source checked as of the relevant date.

Source hierarchy is claim-specific: primary official record or original data; authoritative institutional synthesis; reputable independent reporting with transparent sourcing; specialist secondary analysis; interested-party material; unsourced summaries, snippets or generated text. A primary source may still be weak for self-evaluative market leadership.

Source tests:
- authority: is the source competent for this exact proposition?
- proximity: how close is it to the underlying event, data or statement?
- independence: does it have an interest in the claim?
- freshness: is it current enough for the proposition?

Statuses: verified, qualified, attributed, author_judgement, contested, unverifiable, unsupported, contradicted or removed. Absence of evidence means unverifiable, not false.

## Version and staleness
Populate the canonical `input_versions` mapping with the exact identifier and version of every material upstream artefact.

Record the covered draft, Claim Registry and source-access versions, plus `current_as_of` where relevant. Verification becomes stale when material wording, sources, calculation inputs, product status, policy, office-holder or freshness window changes.

## Stop, escalation and re-entry
Stop or block when an exact quotation lacks an original, a material numerical claim cannot be reconciled, a current claim is stale, roadmap is presented as live, source permission is unclear or domain interpretation exceeds authority.

Escalate legal, medical, scientific or regulated interpretation to a qualified reviewer; thesis-impacting corrections to the author; structure affected by removed claims to the Reviewer and Editor.

Re-verify when the draft, source, methodology, current date or claim wording changes materially.

## Failure modes
- Matching repeated wording across secondary sources is not independent verification.
- A search snippet omits context and cannot support quotation accuracy.
- “Market leader” from the vendor is attributed promotion, not verified comparison.
- Percentage change without denominator, base and period is ambiguous.
- Correlation or sequence is not causality.

## Examples and counterexamples
Valid: 10 to 12 is a 20 per cent increase or a rise of two units, not two per cent.
Invalid: preserve “2%” because the source draft already states it.
Valid: label a roadmap feature as planned and attach the current roadmap source.
Invalid: call it available because a product page describes future intent.

## Output assembly
Return a verification record conforming to `references/output-contract.yaml`, including final draft version, atomised claims, source evaluations, checks, claim status, action, corrections, current-as-of data, unresolved risks and overall release risk. The common `status` records whether verification work completed. A completed verification may still set `overall_release_risk: blocked`.
