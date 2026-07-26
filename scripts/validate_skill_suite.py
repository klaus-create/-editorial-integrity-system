#!/usr/bin/env python3
"""Validate editorial Skill structure, methods, metadata and cross-contract consistency."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)
REQUIRED_METHOD_HEADINGS = [
    "Scope and authority",
    "Required inputs and intake",
    "Execution procedure",
    "Decision logic",
    "Stop, escalation and re-entry",
    "Failure modes",
    "Examples and counterexamples",
    "Output assembly",
    "Version and staleness",
]
REQUIRED_GATE_HEADINGS = [
    "Mandatory checks",
    "Failure outcomes",
    "Evidence to return",
    "Final self-check",
]
CONTRACT_MAP = {
    "editorial-integrity-router": "route-declaration.schema.yaml",
    "authorship-capture": "authorship-source-pack.schema.yaml",
    "voice-profile-builder": "voice-profile.schema.yaml",
    "editorial-brief-compiler": "editorial-brief.schema.yaml",
    "source-grounded-drafter": "draft-output.schema.yaml",
    "argument-structure-reviewer": "argument-review.schema.yaml",
    "anti-slop-auditor": "anti-slop-audit.schema.yaml",
    "voice-preserving-editor": "edit-output.schema.yaml",
    "factual-verifier": "verification-record.schema.yaml",
    "final-editorial-gate": "gate-decision.schema.yaml",
}
SPECIALIST_CONCEPTS = {
    "editorial-integrity-router": ("consequence", "factual exposure", "privacy and permission", "voice sensitivity", "continuity", "authority matrix", "stale-artefact"),
    "authorship-capture": ("verified fact", "supplied source", "author judgement", "personal recollection", "inference", "contested", "uncertain", "unsupported", "sufficiency matrix"),
    "voice-profile-builder": ("sample design", "representativeness", "rhetorical development", "syntax and cadence", "lexical behaviour", "epistemic stance", "counterevidence", "imitation"),
    "editorial-brief-compiler": ("claim and evidence matrix", "email", "social", "report", "proposal", "presentation", "article", "speech", "book"),
    "source-grounded-drafter": ("direct evidence", "attributed view", "author judgement", "labelled inference", "report", "presentation", "article", "book", "gap marker"),
    "argument-structure-reviewer": ("premise", "warrant", "causal", "counterargument", "decision-usefulness", "conclusion", "sequence"),
    "anti-slop-auditor": ("false-positive", "linguistic", "rhetorical", "structural", "epistemic", "tool residue", "severity", "preserve", "query", "edit", "block"),
    "voice-preserving-editor": ("edit ladder", "compression", "expansion", "drift checks", "causality", "certainty", "material-change invalidation"),
    "factual-verifier": ("numerical claim", "causal claim", "quotation", "scientific claim", "legal-adjacent claim", "product capability claim", "current-status claim", "source authority"),
    "final-editorial-gate": ("required artefact", "blocker", "conditional", "waiver", "stale", "return path", "human decision"),
}
SPECIALIST_GUIDE_MAP = {
    "editorial-integrity-router": "risk-and-routing-matrix.md",
    "authorship-capture": "elicitation-and-epistemic-classification.md",
    "voice-profile-builder": "voice-analysis-and-sampling.md",
    "editorial-brief-compiler": "form-brief-patterns.md",
    "source-grounded-drafter": "form-drafting-playbooks.md",
    "argument-structure-reviewer": "argument-analysis-models.md",
    "anti-slop-auditor": "calibration-taxonomy.md",
    "voice-preserving-editor": "edit-ladder-and-drift.md",
    "factual-verifier": "claim-verification-playbooks.md",
    "final-editorial-gate": "release-decision-matrix.md",
}
COMMON_REQUIRED = {
    "schema_version", "artefact_type", "assignment_id", "artefact_version",
    "status", "input_versions", "unresolved_issues", "human_action_required",
}


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:
        raise ValueError(f"cannot parse YAML in {path}: {exc}") from exc


def discover_skills(selected: str | None) -> list[Path]:
    if selected:
        path = Path(selected)
        if not path.is_absolute():
            path = (ROOT / path).resolve()
        return [path]
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())


def extract_frontmatter(text: str) -> dict[str, Any]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("missing or malformed YAML frontmatter")
    value = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError("frontmatter must be a mapping")
    return value


def sentence_complete(value: str) -> bool:
    return bool(re.search(r"[.!?]$", value.strip()))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", help="Validate one Skill folder")
    args = parser.parse_args()
    failures: list[str] = []

    skills = discover_skills(args.skill)
    if not args.skill:
        for yaml_path in sorted(
            path for base in (ROOT / "skills", ROOT / "schemas", ROOT / "projects", ROOT / "governance")
            for path in base.rglob("*.yaml")
        ):
            try:
                load_yaml(yaml_path)
            except ValueError as exc:
                failures.append(str(exc))
    for skill in skills:
        name = skill.name
        specialist_guide = skill / "references" / SPECIALIST_GUIDE_MAP[name]
        required_paths = [
            skill / "SKILL.md",
            skill / "agents" / "openai.yaml",
            skill / "references" / "method.md",
            specialist_guide,
            skill / "references" / "quality-gate.md",
            skill / "references" / "output-contract.yaml",
            skill / "tests" / "cases.yaml",
        ]
        for path in required_paths:
            if not path.is_file():
                failures.append(f"{name}: missing {path.relative_to(skill)}")
        if any(not path.is_file() for path in required_paths):
            continue

        skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
        try:
            front = extract_frontmatter(skill_text)
        except ValueError as exc:
            failures.append(f"{name}: {exc}")
            front = {}
        if front.get("name") != name:
            failures.append(f"{name}: frontmatter name must match directory")
        description = front.get("description")
        if not isinstance(description, str) or not (180 <= len(description.strip()) <= 1024):
            failures.append(f"{name}: description must be 180-1024 characters")
        elif "Use " not in description and "Use when" not in description:
            failures.append(f"{name}: description must state positive trigger conditions")
        for ref in [
            "references/method.md",
            f"references/{SPECIALIST_GUIDE_MAP[name]}",
            "references/quality-gate.md",
            "references/output-contract.yaml",
            "tests/cases.yaml",
        ]:
            if ref not in skill_text:
                failures.append(f"{name}: SKILL.md must reference {ref}")

        metadata = load_yaml(skill / "agents" / "openai.yaml")
        interface = metadata.get("interface") if isinstance(metadata, dict) else None
        if not isinstance(interface, dict):
            failures.append(f"{name}: metadata requires interface mapping")
        else:
            display = interface.get("display_name")
            short = interface.get("short_description")
            prompt = interface.get("default_prompt")
            if not isinstance(display, str) or not display.strip():
                failures.append(f"{name}: display_name is required")
            if not isinstance(short, str) or not (70 <= len(short.strip()) <= 180) or not sentence_complete(short):
                failures.append(f"{name}: short_description must be a complete 70-180 character sentence")
            if not isinstance(prompt, str) or not (100 <= len(prompt.strip()) <= 400) or not sentence_complete(prompt):
                failures.append(f"{name}: default_prompt must be a complete 100-400 character instruction")

        specialist_text = specialist_guide.read_text(encoding="utf-8")
        specialist_sections = re.findall(r"^##\s+(.+)$", specialist_text, re.M)
        if len(specialist_text.splitlines()) < 45:
            failures.append(f"{name}: specialist guide must contain at least 45 lines of domain-specific guidance")
        if len(specialist_sections) < 5:
            failures.append(f"{name}: specialist guide requires at least five substantive sections")
        placeholder_patterns = (r"\bTODO\b", r"\bTBD\b", r"lorem ipsum", r"\[PLACEHOLDER(?:[: ]|\])")
        if any(re.search(pattern, specialist_text, re.I) for pattern in placeholder_patterns):
            failures.append(f"{name}: specialist guide contains unresolved placeholder language")

        lower_specialist = specialist_text.lower()
        missing_concepts = [concept for concept in SPECIALIST_CONCEPTS[name] if concept not in lower_specialist]
        if missing_concepts:
            failures.append(f"{name}: specialist guide is missing required professional concepts {missing_concepts}")

        method = (skill / "references" / "method.md").read_text(encoding="utf-8")
        method_headings = set(re.findall(r"^##\s+(.+)$", method, re.M))
        for heading in REQUIRED_METHOD_HEADINGS:
            if heading not in method_headings:
                failures.append(f"{name}: method missing heading '{heading}'")
        if len(method.splitlines()) < 60:
            failures.append(f"{name}: method must contain at least 60 lines of operational guidance")
        if len(re.findall(r"^\d+\.\s+", method, re.M)) < 8:
            failures.append(f"{name}: method requires an explicit multi-step procedure")
        if "input_versions" not in method:
            failures.append(f"{name}: method must require the canonical input_versions field")
        if not re.search(r"\bstale|staleness|invalidat", method, re.I):
            failures.append(f"{name}: method must define staleness or invalidation rules")

        gate = (skill / "references" / "quality-gate.md").read_text(encoding="utf-8")
        gate_headings = set(re.findall(r"^##\s+(.+)$", gate, re.M))
        for heading in REQUIRED_GATE_HEADINGS:
            if heading not in gate_headings:
                failures.append(f"{name}: quality gate missing heading '{heading}'")
        if len(re.findall(r"^- \[ \]", gate, re.M)) < 10:
            failures.append(f"{name}: quality gate requires at least ten auditable checks")
        lower_gate = gate.lower()
        if "exact input versions" not in lower_gate:
            failures.append(f"{name}: quality gate must verify exact input versions")
        if "stale input" not in lower_gate or "invalidation conditions" not in lower_gate:
            failures.append(f"{name}: quality gate must check stale inputs and invalidation conditions")

        contract = load_yaml(skill / "references" / "output-contract.yaml")
        try:
            Draft202012Validator.check_schema(contract)
        except Exception as exc:
            failures.append(f"{name}: output contract is not a valid Draft 2020-12 schema: {exc}")
            continue
        if contract.get("type") != "object" or contract.get("additionalProperties") is not False:
            failures.append(f"{name}: output schema must close an object root")
        required = set(contract.get("required", []))
        missing_common = COMMON_REQUIRED - required
        if missing_common:
            failures.append(f"{name}: output schema missing common fields {sorted(missing_common)}")
        status_enum = contract.get("properties", {}).get("status", {}).get("enum")
        if status_enum != ["complete", "conditional", "human_input_required", "blocked"]:
            failures.append(f"{name}: status vocabulary must use the canonical order and values")

        if not args.skill:
            shared_path = ROOT / "schemas" / CONTRACT_MAP[name]
            if not shared_path.is_file():
                failures.append(f"{name}: shared schema missing {shared_path.name}")
            else:
                shared = load_yaml(shared_path)
                if shared != contract:
                    failures.append(f"{name}: packaged contract differs from shared canonical schema")

    if not args.skill:
        for path in sorted((ROOT / "schemas").glob("*.yaml")):
            schema = load_yaml(path)
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:
                failures.append(f"schemas/{path.name}: invalid Draft 2020-12 schema: {exc}")
            unknown_dollar = [
                key for key in schema
                if key.startswith("$") and key not in {"$schema", "$id", "$ref", "$defs", "$anchor", "$comment", "$dynamicRef", "$dynamicAnchor", "$vocabulary"}
            ]
            if unknown_dollar:
                failures.append(f"schemas/{path.name}: unknown dollar keywords {unknown_dollar}")

    if failures:
        print("SKILL SUITE VALIDATION FAILURES", file=sys.stderr)
        for item in failures:
            print(f"- {item}", file=sys.stderr)
        raise SystemExit(1)

    print(f"PASS: {len(skills)} Skill(s) satisfy the capability-depth structure and contract rules.")


if __name__ == "__main__":
    main()
