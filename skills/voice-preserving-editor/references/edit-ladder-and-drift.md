# Edit Ladder and Drift Control

## Purpose

Use this guide to select the smallest sufficient intervention and prove that apparently local edits have not changed the proposition, evidence boundary or authorship.

## 1. Preservation baseline

Before editing, record:

- governing thesis and reader effect;
- material claims and evidence strength;
- causal force;
- attribution and quotation boundaries;
- uncertainty and dissent;
- emotional stance and first-person ownership;
- protected wording and terminology;
- characteristic rhythm, recurrence and punctuation;
- form-specific constraints.

The baseline is the comparison object for the final drift check.

## 2. Edit ladder

### Level 0: preserve

No material defect or the apparent irregularity is protected.

### Level 1: mechanical correction

Spelling, punctuation, grammar or formatting where meaning cannot reasonably change.

### Level 2: word or phrase repair

Remove generic setup, correct a local ambiguity or replace an imprecise term using authorised language.

### Level 3: sentence repair

Change clause order, split or combine syntax, or clarify reference while preserving the proposition.

### Level 4: paragraph restructuring

Reorder or rebuild paragraph logic. Requires explicit substantive editing authority and before/after proposition records.

### Level 5: section restructuring

Change section sequence or function. Requires structural diagnosis or explicit transformation authority and downstream re-review.

### Level 6: whole-piece transformation

Rebuild the piece for a new form, architecture or thesis. Requires explicit authority, refreshed brief and likely re-verification and re-gating.

## 3. Selecting the level

Ask:

1. What observable problem exists?
2. What consequence does it create?
3. Can deletion solve it without removing meaning?
4. Can a phrase or sentence repair solve it?
5. Does the problem belong to structure rather than prose?
6. Would local repair create a patchwork more damaging than reconstruction?

Choose the lowest level that resolves the consequence, not the level that produces the most polished prose.

## 4. Proposition comparison

For each material edit, write a neutral before and after proposition.

Check whether the edit changes:

- who acts;
- what happened;
- degree or certainty;
- causality;
- comparison set;
- time period;
- attribution;
- obligation or recommendation;
- emotional ownership.

If any changes, `semantic_change_authorised` must be true and the authority reference must be explicit. Otherwise stop.

## 5. Compression

Safe targets:

- generic setup;
- duplicated explanation with no structural function;
- redundant qualification already carried by a nearer statement;
- examples that do not add evidence or understanding;
- procedural detail outside the reader’s need.

Do not remove:

- evidence;
- material limitation;
- counterargument;
- source attribution;
- decision condition;
- protected recurrence;
- context needed to avoid misleading the reader.

## 6. Expansion

Expansion may use:

- authorised evidence already in the source pack;
- reasoning already permitted by the brief;
- explicit explanation of a named mechanism;
- supplied examples;
- form-required signposting.

Expansion may not invent facts, motives, dialogue, personal experience, client examples, causal mechanisms or consensus.

## 7. Drift checks

### Certainty

Did may, suggests or could become will, proves or causes?

### Causality

Did sequence or association become causal force?

### Attribution

Did a named view become an unattributed assertion?

### Emotional stance

Did restrained, ambivalent or vulnerable language become confident corporate uplift?

### First person

Did the editor create personal ownership or distance that the author did not supply?

### Protected language

Did the edit remove strategic, technical, cultural or rhythmic precision?

## 8. Voice preservation

Preserve behavioural patterns, not surface quirks mechanically. A long sentence may be shortened when it genuinely impairs comprehension, but do not impose uniform sentence length. A fragment may be retained when it performs emphasis, but do not insert fragments to imitate a profile.

## 9. Material-change invalidation

Every Level 4 to 6 edit receives a stable edit ID and downstream actions:

- `reverify` when material claims, figures, causal force, quotations or qualifications change;
- `regate` for any material change after a gate decision;
- `re_review_structure` when section or whole-piece architecture changes;
- `refresh_brief` when the form, thesis, audience or required outcome changes.

`none` may appear only when no downstream artefact is invalidated.

## 10. Stop tests

Stop and escalate when:

- the desired edit requires a new thesis;
- a fact or example is missing;
- the verified evidence does not support the stronger wording;
- the edit would erase a protected characteristic;
- the authorised edit level is lower than the necessary intervention;
- the original and proposed propositions cannot be reconciled.
