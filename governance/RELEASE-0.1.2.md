# Release 0.1.2: Capability Depth

## Status

**Superseded and retracted as a maturity claim.**

The release was merged on 25 July 2026 and described the suite as method-complete. A full second-pass audit found that this claim was premature.

## What the release added

Release 0.1.2 introduced:

- specialist method files;
- quality-gate files;
- per-Skill output-contract files;
- per-Skill case files;
- stronger structural CI checks.

These additions were directionally valuable and formed the basis for the remediation release.

## Why the maturity claim was retracted

The audit identified release blockers:

- several user-facing metadata descriptions were truncated;
- output contracts were sample YAML objects rather than enforceable JSON Schemas;
- shared schemas used ineffective `$type` and `$title` keys;
- packaged and shared contracts conflicted;
- the Final Gate used different outcome vocabularies across files;
- test cases were descriptive examples rather than executable fixtures;
- quality gates were short prose paragraphs rather than auditable checklists;
- CI relied on file presence, YAML parsing and character counts;
- the capability-depth standard was too short to govern acceptance.

## Corrective action

Release 0.1.3 replaces the contracts, fixtures, validation and maturity standard. The 0.1.2 methods were also reviewed and expanded.

## Historical use

Do not cite 0.1.2 as method-complete, pilot-tested or production-ready. Treat it as the first capability-depth scaffold.
