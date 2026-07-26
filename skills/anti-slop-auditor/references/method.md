# Specialist Method

## Scope and authority
The Auditor diagnoses material artefacts and recommends preserve, query, edit or block. It does not determine text origin, rewrite automatically, verify claims or treat model-likelihood signals as evidence of authorship.

## Required inputs and intake
1. Read the whole piece, not only highlighted phrases.
2. Establish form, audience, purpose and intended reader effect.
3. Load voice and register evidence where available.
4. Identify protected characteristics and deliberate formal devices.
5. Confirm whether the request is diagnosis only or includes later editing authority.

## Execution procedure
1. Establish a context baseline: what normal variation, density and repetition should look like for this author and form.
2. Scan seven categories: linguistic genericity, rhetorical defaulting, structural over-regularity, epistemic failure, conversational residue, formatting residue and voice-erasure risk.
3. Apply the three-part finding test.
4. Locate the exact span or pattern and explain its consequence.
5. Test false-positive alternatives before assigning severity.
6. Separate severity from confidence.
7. Choose preserve, query, edit or block.
8. Group related spans into one pattern when they share a cause.
9. Prioritise issues that affect truth, credibility or meaning before cosmetic polish.
10. Return findings only unless a separate editing step is authorised.

## Decision logic
A finding normally requires at least two of:
- an identifiable pattern or residue;
- a material reader, credibility or meaning consequence;
- repetition or clustering across the piece.

Clear falsehood, prompt residue, placeholder leakage or publication-breaking formatting may stand alone.

Categories:
- linguistic genericity: abstraction hides actor/action, inflated modifiers, interchangeable phrasing;
- rhetorical defaulting: formulaic hooks, generic uplift, false balance, repeated contrast machinery;
- structural over-regularity: identical paragraph, sentence or list shapes flatten hierarchy;
- epistemic failure: unsupported certainty, vague authority, fabricated specificity;
- conversational residue: apologies, offers, prompt references or assistant framing;
- formatting residue: placeholders, raw markdown or production notes;
- voice-erasure risk: proposed smoothing would remove fragments, asymmetry, purposeful repetition, dialect, uncertainty or distinctive verbs.

Treatments:
- preserve: unusual but functional or protected;
- query: intent or authorship is ambiguous;
- edit: a clear material weakness can be repaired locally;
- block: factual, privacy, attribution, tool-residue or publication failure needs upstream action.

## Version and staleness
Populate the canonical `input_versions` mapping with the exact identifier and version of every material upstream artefact.

Record the audited draft, voice profile, brief and protected-characteristic versions used. The audit becomes stale when the audited spans, form, audience, voice evidence or protected characteristics change materially.

## Stop, escalation and re-entry
Stop or lower confidence when only an isolated preference is present, the full piece is unavailable, protected voice evidence is missing or the finding depends on guessing text origin.

Escalate factual or attribution failures to Verifier, structural defects to Argument Reviewer and authorised repair to Voice Preserving Editor.

Re-audit affected sections after substantive editing. Do not re-audit unchanged protected irregularity repeatedly.

## Failure modes
- “This word sounds AI” is detector logic, not editorial evidence.
- Normalising every fragment erases cadence and emphasis.
- Penalising necessary technical repetition reduces precision.
- Treating symmetrical structure as inherently generic ignores form.
- Editing during audit conceals the diagnosis and author decision.

## Examples and counterexamples
Valid: “three consecutive abstract verbs delay the concrete claim and make the opening interchangeable”.
Invalid: “delve is banned”.
Valid: preserve “Not yet. And that matters.” when it performs emphasis in the author's register.
Invalid: combine it into a complete sentence because fragments score as suspicious.

## Output assembly
Return an audit conforming to `references/output-contract.yaml`, including context baseline, grouped findings, location, category, severity, confidence, consequence, protected traits considered and treatment. Set `origin_claim_made: false` and `rewrite_authorised: false`; any authorised repair belongs to the Editor.
