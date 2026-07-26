# Claim Verification Playbooks

## Purpose

Use this guide to set the evidence burden before retrieval and to avoid treating familiar wording, repeated secondary reports or confident sources as verification.

## 1. Atomic claim record

Each claim record should identify:

- exact claim wording and draft location;
- claim type;
- materiality;
- evidence burden;
- sources and access dates;
- source authority, proximity, independence and freshness;
- checks performed;
- publication status;
- required action or correction;
- current-as-of date where relevant.

## 2. Simple factual claim

Evidence should directly support the named entity, event, date or property. Confirm identity and scope. Avoid sources that repeat the proposition without showing origin.

## 3. Numerical claim

Check:

- source and dataset version;
- numerator and denominator;
- unit and currency;
- period and comparison base;
- population or sample;
- methodology and exclusions;
- arithmetic and rounding;
- whether absolute and relative change are confused.

Example: 10 to 12 is an increase of two units and 20 per cent, not two per cent.

## 4. Comparative and superlative claim

Define:

- comparison universe;
- metric;
- period;
- geography or segment;
- source independence;
- whether the comparison is exhaustive.

“Leading”, “best”, “only” and “first” usually require stronger evidence than a vendor statement or incomplete market scan.

## 5. Causal claim

Require evidence capable of supporting causal inference, not merely sequence or association. Check:

- temporal order;
- plausible mechanism;
- alternative explanations;
- study or analytical design;
- consistency and dose-response where relevant;
- whether wording should be contributing, associated or causal.

## 6. Prediction and forecast

Record:

- model or reasoning basis;
- assumptions;
- forecast horizon;
- uncertainty range;
- scenario dependence;
- source date;
- whether the statement is a target, forecast or commitment.

## 7. Quotation

Use the original audio, transcript, publication or official record where possible. Confirm:

- exact wording;
- speaker;
- date;
- context;
- transcription fidelity;
- whether omitted words alter meaning.

If the original cannot be found, paraphrase with attribution or mark unverifiable. Do not preserve quotation marks because the line is memorable.

## 8. Scientific claim

Check:

- evidence hierarchy appropriate to the question;
- population and intervention;
- comparator;
- outcome and effect size;
- confidence or uncertainty;
- limitations and conflicts;
- consistency with current authoritative synthesis.

The Verifier may report evidence. Qualified domain review is required when interpretation affects health, safety or regulated decisions.

## 9. Legal-adjacent claim

Check:

- jurisdiction;
- instrument or official source;
- effective date;
- exact provision;
- distinction between rule, guidance and interpretation;
- applicability to the facts.

Do not provide professional legal sign-off. Escalate interpretation or advice to a qualified reviewer.

## 10. Product capability claim

Distinguish:

- currently generally available;
- limited release or beta;
- configured only for selected users;
- roadmap or announced intent;
- historical capability;
- inferred capability not documented.

Use current official documentation or verified live behaviour. A future-tense product page does not prove present availability.

## 11. Current-status claim

Identify the appropriate freshness window. Office-holders, prices, policies, software capabilities, schedules and market positions may change quickly. Record `current_as_of` and authoritative source access date.

## 12. Source conflict resolution

Do not average incompatible sources. Compare:

- definition;
- period;
- population;
- geography;
- methodology;
- update date;
- source interest;
- primary-data origin.

Record a claim as contested when credible conflict remains.

## 13. Publication statuses

- `verified`: evidence directly supports the proposition at its stated strength;
- `qualified`: support exists only with narrower wording or limitation;
- `attributed`: publishable as a named party’s position;
- `author_judgement`: evaluative position owned by the author;
- `contested`: credible sources disagree;
- `unverifiable`: evidence cannot establish the proposition;
- `unsupported`: no adequate supporting evidence is available;
- `contradicted`: credible evidence conflicts with the proposition;
- `removed`: claim is no longer in the release candidate.

Absence of evidence is not automatically contradiction.

## 14. Overall release risk

- **Low**: material claims are verified, removed or clearly owned judgements.
- **Moderate**: qualified or attributed claims remain but are accurately framed.
- **High**: contested or materially limited claims require close approval.
- **Blocked**: critical unsupported, contradicted or unverifiable claims remain in release wording.

The common task `status` may be complete while `overall_release_risk` is blocked.

## 15. Reproducibility test

A sceptical reviewer should be able to:

- locate each source;
- identify the exact proposition supported;
- reproduce arithmetic;
- see why a source was considered authoritative and current;
- understand conflict resolution;
- distinguish evidence from author judgement.
