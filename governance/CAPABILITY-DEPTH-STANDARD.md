# Capability Depth Standard

## Purpose

This standard defines the evidence required before an editorial Skill may be described as specialist-capable, pilot-ready, measured or production-ready. It exists to prevent file completeness, prompt length or successful packaging from being mistaken for capability.

## Governing distinction

A Skill may be:

1. **Structurally valid**: required files exist and the package can be installed.
2. **Contract-valid**: inputs, outputs, statuses and hand-offs are enforceable and internally consistent.
3. **Method-ready**: the Skill contains sufficient specialist procedure, branching, failure handling and authority boundaries for controlled evaluation.
4. **Pilot-tested**: representative real work has exercised the method and produced adjudicated evidence.
5. **Measured**: performance, drift and false-positive thresholds are defined and met against a baseline.
6. **Production-ready**: governance, portability, monitoring, change control and operational evidence support dependable use.

No lower state implies a higher one.

## Required Skill package

Every stable Skill must contain:

```text
SKILL.md
agents/openai.yaml
references/method.md
references/<domain-specific-guide>.md
references/quality-gate.md
references/output-contract.yaml
tests/cases.yaml
```

The domain-specific guide is mandatory for specialist Skills. It must contain the professional models, calibration rules, form playbooks, evidence standards or decision matrices that are unique to the capability. A generic method file alone is insufficient.

Additional references or scripts are required when the task depends on fragile deterministic logic, complex domain standards or further form-specific playbooks.

## 1. Entrypoint acceptance

`SKILL.md` must:

- use valid YAML frontmatter;
- use a directory-matching hyphen-case name;
- state positive trigger conditions;
- state material exclusions or authority boundaries;
- identify required inputs;
- direct the agent to the specialist method, quality gate, output schema and test fixtures;
- use the canonical completion statuses;
- remain a concise control plane rather than a knowledge dump.

A long entrypoint is not evidence of depth.

## 2. Metadata acceptance

`agents/openai.yaml` must:

- contain a human-readable display name;
- contain a complete short description, not a clipped phrase;
- describe the user-visible capability accurately;
- contain a concrete default instruction;
- avoid claims of proven expertise that the maturity evidence does not support.

Metadata is a routing surface and must be reviewed as product copy, not only parsed as YAML.

## 3. Specialist-method acceptance

The method must contain all of the following:

- scope and authority;
- required inputs and intake checks;
- an explicit execution procedure;
- decision logic and branching;
- stop, escalation and re-entry conditions;
- failure modes;
- examples and counterexamples;
- output assembly rules;
- explicit input-version recording and capability-specific staleness rules.

The method must encode non-obvious professional judgement. Restating the Skill name as a checklist does not qualify.

Reviewers must ask:

- Could a capable general model have produced this guidance without domain analysis?
- Does the method determine what to do when evidence is incomplete or contradictory?
- Does it say when not to proceed?
- Does it distinguish adjacent professional responsibilities?
- Does it protect against predictable overreach and false positives?

## 4. Authority acceptance

Each Skill must state what it may and may not do.

Authority must cover, where relevant:

- source retrieval;
- factual interpretation;
- drafting;
- local and structural editing;
- accountable human choices;
- approval and release;
- use of private or restricted information;
- changes that invalidate upstream or downstream artefacts.

A Skill must escalate rather than absorb work outside its authority.

## 5. Output-contract acceptance

`references/output-contract.yaml` must be a valid JSON Schema Draft 2020-12 schema, not a sample object.

Every Skill output must require:

- `schema_version`;
- `artefact_type`;
- `assignment_id`;
- `artefact_version`;
- `status`;
- `input_versions`;
- `unresolved_issues`;
- `human_action_required`.

The canonical status vocabulary is:

- `complete`;
- `conditional`;
- `human_input_required`;
- `blocked`.

The Final Editorial Gate additionally uses these release outcomes:

- `ready`;
- `conditional`;
- `human_decision_required`;
- `blocked`.

Packaged contracts and repository-level canonical schemas must be semantically identical. Shared and packaged contracts may not drift.

## 6. Test-fixture acceptance

Each Skill must contain at least six fixtures covering:

- standard behaviour;
- edge behaviour;
- adversarial behaviour;
- false-positive protection.

Every fixture must contain:

- a globally unique case ID;
- category and risk;
- an input summary;
- expected behaviour;
- a schema-valid example output;
- machine-checkable assertions.

Fixtures prove contract and decision consistency. They do not prove model performance. Real model behaviour must be evaluated separately through pilots and benchmarks.

## 7. Quality-gate acceptance

A quality gate must provide:

- at least ten explicit pass/fail checks;
- named failure outcomes;
- exact input-version and stale-work checks;
- evidence that must be returned;
- a final self-check against predictable overreach.

A paragraph saying “pass only when…” is not an auditable gate.

## 8. Interoperability acceptance

The suite must document:

- which Skill produces each artefact;
- which Skills consume it;
- version requirements;
- stale conditions;
- canonical statuses;
- accountable owner at unresolved hand-offs.

The Router may assemble statuses but may not reinterpret specialist findings or weaken blockers.

## 9. Validation acceptance

CI must run repository scripts that:

- validate Skill entrypoints and metadata;
- validate all schemas under Draft 2020-12;
- compare packaged and shared contracts;
- validate every fixture output against its contract;
- execute fixture assertions;
- reject duplicate YAML keys;
- prove malformed schemas and contradictory cross-field outputs are rejected;
- reject semantically duplicated scenario fixtures;
- validate all local documentation and declared Skill resource links;
- validate project manifests;
- package each Skill only after its validations pass.

Character counts and file presence are supporting checks, not acceptance evidence.

## 10. Maturity transitions

### Scaffold

Evidence:

- entrypoint and metadata exist;
- purpose and boundaries are directionally clear.

May be used for design discussion only.

### Contract-valid

Evidence:

- enforceable output schema;
- canonical statuses;
- cross-Skill hand-offs defined;
- executable fixture validations pass.

May be used for integration development.

### Method-ready

Evidence:

- contract-valid;
- specialist method passes expert review;
- quality gate and false-positive protections are explicit;
- all deterministic validation and packaging checks pass.

May be used in controlled pilots. It must not be called proven expert.

### Pilot-tested

Evidence:

- at least three representative projects complete end-to-end workflows;
- inputs, routes, outputs, accepted edits, rejected edits and gate decisions are retained;
- material failures produce method or contract changes;
- an accountable reviewer approves the pilot findings.

### Measured

Evidence:

- governed outputs are compared with a baseline;
- semantic fidelity, factual accuracy, voice fit, edit economy and false-positive rates are measured;
- thresholds and adjudication rules are versioned;
- unresolved release-critical regressions are zero.

### Production-ready

Evidence:

- measured thresholds are met;
- target-platform installation and consistency are proven;
- privacy, provenance, disclosure, monitoring and rollback controls are operational;
- change control and release ownership are established.

## Review roles

- **Skill maintainer**: supplies methods, contracts, fixtures and validation evidence.
- **Domain reviewer**: judges non-obvious specialist methodology.
- **System reviewer**: checks cross-Skill consistency and stale-artefact behaviour.
- **Human evaluator**: adjudicates pilot and benchmark outputs.
- **Release owner**: assigns maturity status and records exceptions.

The same person may hold several roles, but each role must be performed explicitly.

## Exceptions and waivers

A waiver must name:

- the failed criterion;
- the reason;
- the risk;
- the authorising owner;
- the expiry or re-review condition.

A waiver cannot convert missing evidence into a maturity claim.

## Current application

Release 0.1.2 did not satisfy this standard and is superseded. Release 0.1.3 is a contract-hardened, method-ready release candidate only after the full validation suite passes. Pilot-tested, measured and production-ready remain future states.
