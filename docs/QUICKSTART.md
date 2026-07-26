# Quick Start

This guide shows the shortest reliable path from a writing need to a governed output.

## 1. Choose the operating mode

### Ad hoc task

Use this when the work is low-risk and no continuing project configuration exists.

Provide:

- what you need written or reviewed;
- audience;
- purpose;
- tone or voice constraints;
- source material or draft;
- any facts that must be verified.

The Router will select the lowest adequate workflow level.

### Continuing project

Use this when work repeats for a brand, business, client, product, research programme or book.

Provide the active project workspace with:

```text
project-editorial-manifest.yaml
approved sources
author or brand samples
terminology or definitions
current assignment material
```

Validate the suite, fixtures and manifest before consequential use:

```bash
python scripts/validate_skill_suite.py
python scripts/run_contract_tests.py
python scripts/validate_manifest.py projects/<project>/project-editorial-manifest.yaml
```

## 2. Start with one of these requests

### Create

> Draft this report from the supplied research and use the project editorial manifest.

### Rewrite

> Improve this email without changing the meaning or making it sound generic.

### Review

> Audit this proposal for argument, unsupported claims, voice drift and AI-like genericity. Separate findings from edits.

### Verify

> Verify all material claims in this article. Qualify or block anything that cannot be supported.

### Release check

> Run the final editorial gate and tell me whether this is ready, conditionally ready or blocked.

## 3. Understand what the system may return

For simple work, it may return only the finished writing.

For consequential work, expect validated artefacts or explicit references to them, including:

- route declaration;
- source pack, claim registry or voice profile;
- editorial brief or draft output;
- review, audit, edit or verification record;
- gate decision;
- unresolved issues with owners and required actions.

Every specialist artefact uses `complete`, `conditional`, `human_input_required` or `blocked`. The Gate separately returns `ready`, `conditional`, `human_decision_required` or `blocked`. See [`ARTEFACTS-AND-HANDOFFS.md`](ARTEFACTS-AND-HANDOFFS.md).

## 4. Human approval

The agent may prepare, analyse, qualify or block work, but the accountable human remains responsible for consequential publication.

Do not treat `ready` as permission to publish when the project manifest requires a named approver, editor, legal review or project-owner approval.