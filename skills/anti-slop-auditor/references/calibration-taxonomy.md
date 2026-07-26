# Anti-Slop Calibration Taxonomy

## Purpose

Use this guide to distinguish material editorial artefacts from superficial “AI-sounding” preferences. The Auditor evaluates consequence, context and clustering. It does not detect authorship origin.

## 1. Finding threshold

A normal finding requires at least two of:

- an observable pattern;
- repetition or clustering;
- a material consequence for meaning, credibility, reader effort or voice.

One instance may stand alone when it is a false claim, prompt residue, placeholder, private-data leak or publication-breaking formatting defect.

## 2. Linguistic genericity

Look for:

- abstract nouns replacing actors and actions;
- interchangeable uplift language;
- inflated modifiers unsupported by evidence;
- vague verbs such as enable, empower or drive without mechanism;
- nominalisation chains that obscure responsibility;
- phrases that could move to any organisation or topic unchanged.

Do not blacklist individual words. “Transform” may be precise when the transformation is defined.

## 3. Rhetorical defaulting

Patterns include:

- formulaic “not X, but Y” repeated mechanically;
- generic hooks about a fast-changing world;
- false balance inserted for symmetry;
- repeated three-part uplift lists without hierarchy;
- question openings that are never answered;
- conclusions that restate aspiration rather than earned implication.

A familiar rhetorical form is acceptable when it performs a real job and is not overused.

## 4. Structural over-regularity

Look for:

- identical paragraph lengths and internal shapes;
- every section using the same number of bullets;
- headings that flatten priority;
- one-sentence setup followed by three equal points throughout;
- transitions that announce structure rather than carry meaning.

Symmetry is not inherently defective. It is useful in comparison tables, procedures and parallel arguments.

## 5. Epistemic failure

Prioritise:

- unsupported certainty;
- vague authority such as “experts agree”;
- fabricated specificity;
- causal wording unsupported by the evidence relation;
- unmarked prediction or assumption;
- invented quotations, examples or first-person experience;
- current claims without current support.

These are integrity issues, not merely style issues.

## 6. Conversational residue

Examples:

- “Here is the revised version” inside the artefact;
- apologies or offers to continue;
- references to the prompt or user instructions;
- assistant self-description;
- option labels accidentally retained;
- unresolved questions presented to the final reader.

Context matters. A customer-service chatbot transcript may legitimately contain conversational framing.

## 7. Formatting residue

Examples:

- raw markdown where the surface does not support it;
- placeholder brackets;
- production notes;
- broken citation tokens;
- duplicated headings;
- template fields;
- malformed tables or slide instructions inside final copy.

## 8. Voice-erasure risk

Protect before recommending change:

- fragments used for emphasis;
- long syntax used for reflective movement;
- dialect and second-language patterns that carry identity;
- purposeful repetition;
- unusual but coherent punctuation;
- emotional restraint or distance;
- technical density required by expert readers;
- literary ambiguity.

The test is functional: what is lost if the irregularity is normalised?

## 9. False-positive library

### Necessary technical repetition

Repeated defined terms may preserve precision. Replacing them with synonyms can introduce ambiguity.

### Deliberate motif

A repeated phrase across a chapter may create continuity or escalation. Assess manuscript function before calling duplication.

### Short fragments

“Not yet. And that matters.” may be a strong emphasis device. It is not a defect because it is incomplete syntax.

### Structured parallelism

Parallel headings can make a complex comparison legible. Regularity becomes a problem only when it flattens meaningful hierarchy.

### Formal qualification

Repeated caveats may be required in regulated or scientific writing. The question is whether they are proportionate and located effectively.

## 10. Severity and confidence

### P0

Publication blocker: falsehood, private-data leak, prompt/tool residue, broken attribution or unusable output surface.

### P1

Material harm to meaning, credibility, reader decision or authorship.

### P2

Likely weakness with local consequence or contextual uncertainty.

### P3

Observation or optional preference. Preserve or query is often more appropriate than edit.

Confidence depends on context, recurrence, voice evidence and alternative explanations. Do not convert high severity into high confidence automatically.

## 11. Treatment selection

- **Preserve**: functional, protected or false-positive risk outweighs benefit.
- **Query**: intent or authorship boundary is material and unresolved.
- **Edit**: local repair is authorised and the defect is clear.
- **Block**: publication integrity, privacy, evidence or production failure requires upstream action.

The Auditor itself returns findings only. `rewrite_authorised` remains false even when the route includes a later Editor.
