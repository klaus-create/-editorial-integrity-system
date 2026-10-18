#!/usr/bin/env python3
"""Validate Skill output schemas, fixtures and cross-field semantics."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {"standard", "edge", "adversarial", "false_positive"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent duplicate-key overwrites."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_yaml(path: Path) -> Any:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except Exception as exc:
        fail(f"cannot parse YAML in {path}: {exc}")


def resolve_path(value: Any, path: str) -> Any:
    current = value
    if path == "":
        return current
    for part in path.split("."):
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError) as exc:
                raise KeyError(path) from exc
        elif isinstance(current, dict) and part in current:
            current = current[part]
        else:
            raise KeyError(path)
    return current


def contains(actual: Any, expected: Any) -> bool:
    if isinstance(actual, str):
        return str(expected) in actual
    if isinstance(actual, list):
        return expected in actual
    if isinstance(actual, dict):
        return expected in actual or expected in actual.values()
    return False


def discover_skills(selected: str | None) -> list[Path]:
    if selected:
        path = Path(selected)
        if not path.is_absolute():
            path = (ROOT / path).resolve()
        if not path.is_dir():
            fail(f"skill folder not found: {path}")
        return [path]
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())


from artefact_semantics import (
    SEMANTIC_VALIDATORS, semantic_fixture_fingerprint, validate_common_semantics,
)


def assert_rejected(validator: Draft202012Validator, value: Any, label: str, failures: list[str]) -> None:
    if validator.is_valid(value):
        failures.append(f"{label}: schema unexpectedly accepted an invalid mutation")


def run_negative_schema_tests(
    skill_name: str,
    schema: dict[str, Any],
    validator: Draft202012Validator,
    example: dict[str, Any],
    failures: list[str],
) -> int:
    count = 0
    mutated = copy.deepcopy(example)
    mutated["unexpected_root_property"] = True
    assert_rejected(validator, mutated, f"{skill_name}.negative.additional-property", failures)
    count += 1

    mutated = copy.deepcopy(example)
    mutated["status"] = "finished"
    assert_rejected(validator, mutated, f"{skill_name}.negative.invalid-status", failures)
    count += 1

    valid_issue = {
        "issue_id": "NEG-ISSUE",
        "description": "Generated contradictory status test.",
        "owner": "author",
        "blocking": False,
        "required_action": "Resolve the generated test issue.",
    }

    mutated = copy.deepcopy(example)
    mutated["status"] = "complete"
    mutated["unresolved_issues"] = [copy.deepcopy(valid_issue)]
    assert_rejected(validator, mutated, f"{skill_name}.negative.complete-with-issue", failures)
    count += 1

    mutated = copy.deepcopy(example)
    mutated["status"] = "conditional"
    mutated["unresolved_issues"] = []
    assert_rejected(validator, mutated, f"{skill_name}.negative.conditional-without-issue", failures)
    count += 1

    mutated = copy.deepcopy(example)
    mutated["status"] = "human_input_required"
    mutated["unresolved_issues"] = [copy.deepcopy(valid_issue)]
    mutated["human_action_required"] = False
    assert_rejected(validator, mutated, f"{skill_name}.negative.human-input-without-flag", failures)
    count += 1

    mutated = copy.deepcopy(example)
    mutated["status"] = "blocked"
    mutated["unresolved_issues"] = [copy.deepcopy(valid_issue)]
    assert_rejected(validator, mutated, f"{skill_name}.negative.blocked-without-blocking-issue", failures)
    count += 1

    for field in schema.get("required", []):
        mutated = copy.deepcopy(example)
        mutated.pop(field, None)
        assert_rejected(validator, mutated, f"{skill_name}.negative.missing-{field}", failures)
        count += 1
    return count



def run_negative_semantic_tests(example: dict[str, Any], failures: list[str]) -> int:
    """Prove that cross-field semantic validators reject contradictory outputs."""
    artefact_type = example.get("artefact_type")
    semantic = SEMANTIC_VALIDATORS.get(artefact_type)
    if semantic is None:
        return 0

    checks: list[tuple[str, dict[str, Any]]] = []

    common = copy.deepcopy(example)
    common["input_versions"] = {}
    checks.append(("empty-input-versions", common))

    common = copy.deepcopy(example)
    common["status"] = "conditional"
    common["unresolved_issues"] = []
    checks.append(("conditional-without-issue", common))

    if artefact_type == "route_declaration":
        if example.get("modules"):
            value = copy.deepcopy(example)
            value["modules"] = [copy.deepcopy(value["modules"][0]), copy.deepcopy(value["modules"][0])]
            checks.append(("duplicate-module", value))
            value = copy.deepcopy(example)
            value["modules"][0]["may_release"] = True
            if value["modules"][0]["name"] == "final-editorial-gate":
                value["modules"][0]["name"] = "source-grounded-drafter"
            checks.append(("non-gate-release-authority", value))
    elif artefact_type == "authorship_source_pack":
        value = copy.deepcopy(example)
        value["substantive_items"][0]["evidence_refs"] = ["UNKNOWN-SOURCE"]
        checks.append(("unknown-source-reference", value))
        value = copy.deepcopy(example)
        value["claim_registry"]["status"] = "blocked"
        checks.append(("claim-registry-status-drift", value))
    elif artefact_type == "voice_profile":
        value = copy.deepcopy(example)
        value["sample_assessment"]["sample_count"] += 1
        checks.append(("sample-count-mismatch", value))
        if value.get("enduring_traits"):
            value = copy.deepcopy(example)
            value["enduring_traits"][0]["evidence_refs"] = ["UNKNOWN-SAMPLE"]
            checks.append(("trait-unknown-sample", value))
    elif artefact_type == "editorial_brief":
        value = copy.deepcopy(example)
        value["evidence_duties"] = []
        checks.append(("claim-duty-mismatch", value))
        if value.get("structure_plan"):
            value = copy.deepcopy(example)
            value["structure_plan"][0]["claims"] = ["UNKNOWN-CLAIM"]
            checks.append(("structure-unknown-claim", value))
    elif artefact_type == "draft_output":
        value = copy.deepcopy(example)
        value["source_trace"][0]["evidence_move"] = "direct_evidence"
        value["source_trace"][0]["source_refs"] = []
        checks.append(("direct-evidence-without-source", value))
        value = copy.deepcopy(example)
        value["gap_markers"] = [{"marker": "SOURCE_REQUIRED", "location": "opening", "owner": "verifier"}]
        value["integrity_summary"]["claim_trace_complete"] = True
        checks.append(("complete-trace-with-gap", value))
    elif artefact_type == "argument_review":
        value = copy.deepcopy(example)
        value["argument_map"][0]["supports"] = ["UNKNOWN-NODE"]
        checks.append(("unknown-supported-node", value))
        value = copy.deepcopy(example)
        value["governing_thesis"] = {"text": None, "status": "missing"}
        value["status"] = "complete"
        checks.append(("complete-with-missing-thesis", value))
    elif artefact_type == "anti_slop_audit":
        value = copy.deepcopy(example)
        value["origin_claim_made"] = True
        checks.append(("origin-attribution", value))
        value = copy.deepcopy(example)
        value["findings"] = [{
            "finding_id": "NEG-1", "location": "opening", "category": "tool_residue",
            "severity": "P0", "confidence": 1.0, "observed_pattern": "Prompt residue remains.",
            "consequence": "Publication defect.", "false_positive_test": "Direct residue.",
            "protected_traits_considered": [], "treatment": "edit",
        }]
        checks.append(("p0-without-block", value))
    elif artefact_type == "edit_output":
        value = copy.deepcopy(example)
        value["drift_checks"]["meaning"] = "drift_detected"
        value["status"] = "complete"
        checks.append(("complete-with-drift", value))
        if value.get("edit_log"):
            value = copy.deepcopy(example)
            value["edit_log"][0]["edit_level"] = 4
            value["material_changes"] = []
            checks.append(("unrecorded-material-edit", value))
    elif artefact_type == "verification_record":
        value = copy.deepcopy(example)
        value["overall_release_risk"] = "blocked"
        for claim in value.get("claims", []):
            claim["status"] = "verified"
        checks.append(("blocked-without-blocking-claim", value))
        value = copy.deepcopy(example)
        value["overall_release_risk"] = "low"
        if value.get("claims"):
            value["claims"][0]["status"] = "qualified"
        checks.append(("low-risk-with-qualified-claim", value))
    elif artefact_type == "gate_decision":
        value = copy.deepcopy(example)
        value["outcome"] = "ready"
        first = next(iter(value["check_results"]))
        value["check_results"][first]["result"] = "fail"
        checks.append(("ready-with-failed-check", value))
        value = copy.deepcopy(example)
        value["outcome"] = "blocked"
        value["blocking_issues"] = []
        checks.append(("blocked-without-blocker", value))

    count = 0
    for label, value in checks:
        observed: list[str] = []
        validate_common_semantics(f"negative.{artefact_type}.{label}", value, observed)
        semantic(f"negative.{artefact_type}.{label}", value, observed)
        if not observed:
            failures.append(f"negative.{artefact_type}.{label}: semantic validator unexpectedly accepted contradiction")
        count += 1
    return count

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", help="Validate one Skill folder instead of the full suite")
    args = parser.parse_args()

    failures: list[str] = []
    case_ids: set[str] = set()
    case_count = 0
    negative_count = 0
    semantic_negative_count = 0
    selected_skills = discover_skills(args.skill)

    for skill in selected_skills:
        test_path = skill / "tests" / "cases.yaml"
        data = load_yaml(test_path)
        if not isinstance(data, dict):
            failures.append(f"{skill.name}: tests/cases.yaml must contain a mapping")
            continue

        contract_rel = data.get("contract")
        if not isinstance(contract_rel, str):
            failures.append(f"{skill.name}: tests file must declare contract")
            continue
        contract_path = (test_path.parent / contract_rel).resolve()
        if not contract_path.is_file():
            failures.append(f"{skill.name}: contract not found: {contract_path}")
            continue
        schema = load_yaml(contract_path)
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            failures.append(f"{skill.name}: invalid output schema: {exc}")
            continue
        validator = Draft202012Validator(schema, format_checker=FormatChecker())

        cases = data.get("cases")
        if not isinstance(cases, list):
            failures.append(f"{skill.name}: cases must be a list")
            continue

        categories: set[str] = set()
        semantic_fingerprints: dict[str, str] = {}
        first_valid_example: dict[str, Any] | None = None
        for case in cases:
            case_count += 1
            if not isinstance(case, dict):
                failures.append(f"{skill.name}: case must be a mapping")
                continue
            case_id = case.get("case_id")
            if not isinstance(case_id, str) or not case_id:
                failures.append(f"{skill.name}: case_id is required")
                continue
            if case_id in case_ids:
                failures.append(f"duplicate case_id: {case_id}")
            case_ids.add(case_id)
            category = case.get("category")
            categories.add(str(category))
            if category not in CATEGORIES:
                failures.append(f"{case_id}: invalid category {category!r}")
            if case.get("risk") not in {"low", "moderate", "high"}:
                failures.append(f"{case_id}: risk must be low, moderate or high")
            if not isinstance(case.get("input"), dict) or not case["input"].get("summary"):
                failures.append(f"{case_id}: input.summary is required")
            if not isinstance(case.get("expected_behaviour"), str) or not case["expected_behaviour"].strip():
                failures.append(f"{case_id}: expected_behaviour is required")

            output = case.get("example_output")
            if isinstance(output, dict):
                fingerprint = semantic_fixture_fingerprint(output)
                previous = semantic_fingerprints.get(fingerprint)
                if previous:
                    failures.append(
                        f"{case_id}: scenario output duplicates the semantic fixture substance of {previous}"
                    )
                else:
                    semantic_fingerprints[fingerprint] = case_id
            errors = sorted(validator.iter_errors(output), key=lambda err: list(err.path))
            for error in errors:
                location = ".".join(str(part) for part in error.path) or "<root>"
                failures.append(f"{case_id}: example_output.{location}: {error.message}")
            if not errors and isinstance(output, dict):
                if first_valid_example is None:
                    first_valid_example = output
                validate_common_semantics(case_id, output, failures)
                semantic = SEMANTIC_VALIDATORS.get(output.get("artefact_type"))
                if semantic:
                    semantic(case_id, output, failures)

            assertions = case.get("assertions")
            if not isinstance(assertions, dict):
                failures.append(f"{case_id}: assertions mapping is required")
                continue
            for path, expected in (assertions.get("equals") or {}).items():
                try:
                    actual = resolve_path(output, path)
                except KeyError:
                    failures.append(f"{case_id}: equals path not found: {path}")
                    continue
                if actual != expected:
                    failures.append(f"{case_id}: {path} expected {expected!r}, got {actual!r}")
            for path, expected in (assertions.get("contains") or {}).items():
                try:
                    actual = resolve_path(output, path)
                except KeyError:
                    failures.append(f"{case_id}: contains path not found: {path}")
                    continue
                if not contains(actual, expected):
                    failures.append(f"{case_id}: {path} does not contain {expected!r}")
            for path, prohibited in (assertions.get("prohibited_values") or {}).items():
                try:
                    actual = resolve_path(output, path)
                except KeyError:
                    continue
                values = prohibited if isinstance(prohibited, list) else [prohibited]
                for value in values:
                    if actual == value or contains(actual, value):
                        failures.append(f"{case_id}: {path} contains prohibited value {value!r}")

        if not CATEGORIES.issubset(categories):
            failures.append(f"{skill.name}: missing case categories: {', '.join(sorted(CATEGORIES - categories))}")
        if len(cases) < 6:
            failures.append(f"{skill.name}: at least six cases are required")
        if first_valid_example is not None:
            negative_count += run_negative_schema_tests(skill.name, schema, validator, first_valid_example, failures)
            semantic_negative_count += run_negative_semantic_tests(first_valid_example, failures)

    if failures:
        print("CONTRACT TEST FAILURES", file=sys.stderr)
        for item in failures:
            print(f"- {item}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"PASS: {case_count} contract fixtures, {negative_count} schema rejection checks and "
        f"{semantic_negative_count} semantic rejection checks validated across "
        f"{len(selected_skills)} Skill(s), with unique scenario outputs."
    )


if __name__ == "__main__":
    main()
