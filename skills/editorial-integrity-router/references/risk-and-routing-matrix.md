# Risk and Routing Matrix

## Purpose

Use this guide when the assignment is ambiguous, spans multiple editorial capabilities, or appears deceptively small relative to its consequence. The Router should select the minimum adequate route, not the shortest route and not the largest available route.

## 1. Rate the five risk dimensions

Rate the assignment as it will be released, not as it appears in the prompt.

### Consequence

- **Low**: private wording with no meaningful decision, commercial, reputational or wellbeing effect.
- **Moderate**: client-facing, team-decision, public marketing or professional communication where error creates friction or embarrassment.
- **High**: investor, executive, policy, regulated, contractual, employment, health, safety, public controversy or major reputation exposure.

### Factual exposure

- **Low**: no material external claim, or only stable facts already authorised and verified.
- **Moderate**: a small number of externally checkable claims, comparisons or figures that are not central to the decision.
- **High**: current, numerical, causal, scientific, legal-adjacent, quoted, superlative or product-capability claims; a material claim drives the recommendation.

### Privacy and permission

- **Low**: public or clearly authorised material.
- **Moderate**: internal context with established access but unclear redistribution limits.
- **High**: personal, confidential, commercially sensitive, restricted-source, child, health, legal or employment information; source permission is unknown.

### Voice sensitivity

- **Low**: utility copy where authorship identity is immaterial.
- **Moderate**: public brand, founder, client or executive communication where recognisable register matters.
- **High**: personal authorship, literary work, speech, movement manifesto, culturally or dialectically distinctive writing, or work with protected phrasing and rhythm.

### Continuity

- **Low**: self-contained short item.
- **Moderate**: recurring campaign, report series, multi-slide narrative or content family.
- **High**: book, research programme, product narrative, regulated record, multi-agent workflow or long-lived institutional knowledge.

## 2. Select the workflow level

Start from consequence, then escalate for interacting risks.

| Base condition | Default level |
|---|---|
| All dimensions low, private, no substantive invention | lightweight |
| Public or client-facing, one moderate risk, stable substance | standard |
| Any high factual or consequence risk, or two high dimensions | full |
| High continuity plus high consequence, privacy or factual risk | extended |

Escalate one level when:

- two moderate risks interact to create a material failure mode;
- the final approver cannot inspect the underlying sources easily;
- multiple agents will exchange artefacts;
- a late edit could silently invalidate verification or approval;
- the output is short but contains a concentrated high-risk claim.

Do not escalate merely because many Skills are available. Each module must change a decision or produce a required artefact.

## 3. Determine the task type

- **Create**: substantive new wording or structure is required.
- **Review**: diagnosis only; no textual authority is implied.
- **Edit**: existing text may be changed within a defined scope.
- **Verify**: factual publication claims are the primary object.
- **Release**: final readiness decision against a fixed version.
- **Profile**: reusable voice behaviour is being inferred from samples.
- **Combined**: more than one authority is explicitly requested.

Words such as “improve”, “fix”, “make stronger” or “humanise” do not by themselves grant editing, factual or release authority. Resolve the requested operation.

## 4. Module dependency rules

### Substance before expression

Run Authorship Capture when the thesis, evidence, experience or disagreement is missing or implicit. Do not send missing substance directly to the Drafter.

### Contract before drafting

Run Editorial Brief Compiler when multiple sources, audiences, constraints, claims or agents must be reconciled. A simple direct request may not need a formal brief.

### Diagnosis before repair

Use Argument Structure Reviewer and Anti Slop Auditor before Voice Preserving Editor when the problem is not already local and explicit.

### Final wording before verification

Verification must cover the material final claim wording. If editing changes a number, comparison, causal force, quotation, current claim or qualification, re-verify.

### Verification before gate

For full and extended factual work, the Gate consumes a verification record covering the release candidate. The Gate does not substitute for verification.

### Gate after all material edits

Any material edit after the Gate invalidates its decision.

## 5. Authority matrix

| Skill | Retrieve sources | Change text | Issue release outcome |
|---|---:|---:|---:|
| Router | only as needed to identify artefacts | no | no |
| Authorship Capture | supplied/authorised sources | no final prose | no |
| Voice Profile Builder | authorised samples | no final prose | no |
| Brief Compiler | authorised artefacts | no final prose | no |
| Source Grounded Drafter | only within route permission | yes, new draft | no |
| Argument Reviewer | no external verification by default | no | no |
| Anti Slop Auditor | no external verification by default | no | no |
| Voice Preserving Editor | only within route permission | yes, scoped | no |
| Factual Verifier | yes, when authorised | minimal factual amendments only | no |
| Final Editorial Gate | inspect required artefacts | no | yes, decision only |

`may_release` means authority to issue the gate outcome. It never means authority to send, publish or submit without an explicit user action.

## 6. Common route patterns

### Private local correction

`Voice Preserving Editor`

Use only when the requested change is local, meaning and facts are stable, and there is no public or consequential release.

### Client-facing short copy

`Brief direction -> Drafter or Editor -> targeted audit -> surface check`

Add Verifier when claims are material or current. Add Gate when external circulation carries meaningful consequence.

### Strategic report or investor material

`Capture -> Brief -> Drafter -> Argument Review -> Editor -> Verifier -> Gate`

Voice profiling is optional when a reusable or distinctive voice is required. Anti-slop audit is added when model-default language or voice erasure is a material risk.

### Existing authored manuscript

`Argument Review and/or Anti-Slop Audit -> Voice Preserving Editor -> targeted verification -> Gate`

Do not force Capture or fresh drafting when the manuscript already contains authorised substance.

### Factual correction only

`Verifier -> minimal factual amendment -> Gate or calling agent`

Do not run broad stylistic editing unless requested.

## 7. Stale-artefact propagation

Mark an artefact stale when any input named in `input_versions` changes materially.

- source or author decision changes: Source Pack, Claim Registry, Brief and downstream draft may be stale;
- thesis or audience changes: Brief, Draft, reviews and Gate are stale;
- material draft edit: relevant reviews, Verification and Gate may be stale;
- current-as-of date passes the claim’s acceptable freshness window: Verification is stale;
- sample provenance changes: Voice Profile and dependent voice decisions may be stale;
- approval context changes: Route and Gate are stale.

A stale artefact may still be informative. It may not be presented as current evidence.

## 8. Routing failure tests

Before returning a route, ask:

1. Which selected module changes a decision that no other module owns?
2. Which material risk would remain if a selected module were removed?
3. Has any specialist been asked to exceed its authority?
4. Can every downstream consumer identify the artefact it receives?
5. Does the route still work without hidden conversational memory?
6. Is an urgent or short output being under-routed because it looks small?
7. Is a low-risk task being over-routed because the framework is available?
