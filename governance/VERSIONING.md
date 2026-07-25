# Versioning and Change Control

## Version model

Use semantic versions for the editorial system:

- MAJOR: constitutional or schema changes that alter expected behaviour
- MINOR: new Skills, fields, form routes or material capabilities
- PATCH: corrections, clarifications and non-breaking improvements

## Rule status

Every durable rule should be classified as one of:

- constitutional
- mandatory
- recommended
- experimental
- deprecated

## Change requirements

A material change requires:

1. written rationale;
2. affected Skills and schemas identified;
3. regression cases added or updated;
4. false-positive and voice-flattening risk reviewed;
5. version incremented;
6. editorial owner approval.

## Release gate

A release may be tagged only when:

- every Skill contains `SKILL.md` and `agents/openai.yaml`;
- all project manifests validate;
- regression fixtures have expected outcomes;
- packaging utilities complete successfully;
- README and roadmap reflect the release boundary.

## Profile learning

Accepted edits must not update an author or project profile automatically. Profile changes require explicit human approval and version history.
