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
HUMAN_OWNERS = {"author", "project_owner", "approver", "unknown"}
MODULE_ORDER = [
    "authorship-capture",
    "voice-profile-builder",
    "editorial-brief-compiler",
    "source-grounded-drafter",
    "argument-structure-reviewer",
    "anti-slop-auditor",
    "voice-preserving-editor",
    "factual-verifier",
    "final-editorial-gate",
]
EXPECTED_ARTEFACT = {
    "authorship-capture": "authorship_source_pack",
    "voice-profile-builder": "voice_profile",
    "editorial-brief-compiler": "editorial_brief",
    "source-grounded-drafter": "draft_output",
    "argument-structure-reviewer": "argument_review",
    "anti-slop-auditor": "anti_slop_audit",
    "voice-preserving-editor": "edit_output",
    "factual-verifier": "verification_record",
    "final-editorial-gate": "gate_decision",
}


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


def duplicate_values(values: list[Any]) -> list[Any]:
    return sorted({value for value in values if values.count(value) > 1})


def semantic_fixture_fingerprint(output: dict[str, Any]) -> str:
    """Fingerprint scenario substance while ignoring common envelope bookkeeping."""
    ignored = {
        "schema_version", "artefact_type", "assignment_id", "artefact_version",
        "input_versions",
    }
    substance = {key: value for key, value in output.items() if key not in ignored}
    return json.dumps(substance, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def add(failures: list[str], case_id: str, message: str) -> None:
    failures.append(f"{case_id}: {message}")


def validate_common_semantics(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    status = output.get("status")
    issues = output.get("unresolved_issues", [])
    if status in {"conditional", "human_input_required", "blocked"} and not issues:
        add(failures, case_id, f"status {status!r} requires at least one unresolved issue")
    if status == "human_input_required" and output.get("human_action_required") is not True:
        add(failures, case_id, "human_input_required must set human_action_required=true")
    if status == "blocked" and not any(issue.get("blocking") is True for issue in issues):
        add(failures, case_id, "blocked status requires at least one blocking unresolved issue")
    if not isinstance(output.get("input_versions"), dict) or not output["input_versions"]:
        add(failures, case_id, "input_versions must identify at least one input artefact")

    issue_ids = [issue.get("issue_id") for issue in issues]
    duplicates = duplicate_values(issue_ids)
    if duplicates:
        add(failures, case_id, f"duplicate unresolved issue IDs: {duplicates}")

    # human_action_required means a human-owned action is explicitly present. Gate
    # conditions and blockers are included because its common status represents task
    # completion rather than publication disposition.
    owned_items = list(issues)
    if output.get("artefact_type") == "editorial_brief":
        owned_items += output.get("release_conditions", [])
    if output.get("artefact_type") == "gate_decision":
        owned_items += output.get("blocking_issues", []) + output.get("conditions_for_release", [])
    human_owned = any(item.get("owner") in HUMAN_OWNERS for item in owned_items)
    if bool(output.get("human_action_required")) != human_owned:
        add(
            failures,
            case_id,
            "human_action_required must match the presence of a human-owned unresolved action",
        )


def validate_route(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    modules = output.get("modules", [])
    names = [module.get("name") for module in modules]
    duplicates = duplicate_values(names)
    if duplicates:
        add(failures, case_id, f"duplicate modules: {duplicates}")
    indexes = [MODULE_ORDER.index(name) for name in names if name in MODULE_ORDER]
    if indexes != sorted(indexes):
        add(failures, case_id, "modules are not in canonical workflow order")
    for module in modules:
        name = module.get("name")
        if module.get("expected_artefact") != EXPECTED_ARTEFACT.get(name):
            add(failures, case_id, f"{name} declares the wrong expected artefact")
        if module.get("may_release") is True and name != "final-editorial-gate":
            add(failures, case_id, f"{name} may not issue release authority")
        if name == "final-editorial-gate" and module.get("may_release") is not True:
            add(failures, case_id, "Final Editorial Gate must have release-decision authority")
    high_count = sum(value == "high" for value in output.get("risk_dimensions", {}).values())
    if high_count >= 2 and output.get("workflow_level") not in {"full", "extended"}:
        add(failures, case_id, "two or more high risk dimensions require full or extended routing")
    if output.get("stale_artefacts") and output.get("status") == "complete":
        add(failures, case_id, "a route with stale artefacts may not be complete")
    approval = output.get("approval", {})
    if approval.get("required") and approval.get("approver") is None and output.get("status") != "human_input_required":
        add(failures, case_id, "required approval without an approver must require human input")


def validate_authorship(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    source_ids = [item.get("source_id") for item in output.get("source_inventory", [])]
    item_ids = [item.get("item_id") for item in output.get("substantive_items", [])]
    if duplicate_values(source_ids):
        add(failures, case_id, "source IDs must be unique")
    if duplicate_values(item_ids):
        add(failures, case_id, "substantive item IDs must be unique")
    source_set = set(source_ids)
    for item in output.get("substantive_items", []):
        unknown = set(item.get("evidence_refs", [])) - source_set
        if unknown:
            add(failures, case_id, f"{item.get('item_id')} references unknown sources {sorted(unknown)}")
    registry = output.get("claim_registry", {})
    for field in ("assignment_id", "status", "human_action_required"):
        if registry.get(field) != output.get(field):
            add(failures, case_id, f"embedded claim registry {field} does not match source pack")
    claim_ids = [claim.get("claim_id") for claim in registry.get("claims", [])]
    if set(claim_ids) != set(item_ids):
        add(failures, case_id, "claim registry IDs must match substantive item IDs")
    for claim in registry.get("claims", []):
        unknown = set(claim.get("supporting_sources", [])) - source_set
        if unknown:
            add(failures, case_id, f"claim {claim.get('claim_id')} references unknown sources {sorted(unknown)}")
    if any(item.get("permission_status") in {"restricted", "unknown"} for item in output.get("source_inventory", [])) and output.get("status") == "complete":
        add(failures, case_id, "restricted or unknown source permission cannot produce a complete source pack")


def _voice_traits(output: dict[str, Any]) -> list[dict[str, Any]]:
    traits = list(output.get("enduring_traits", []))
    for register_traits in output.get("register_profiles", {}).values():
        traits.extend(register_traits)
    return traits


def validate_voice(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    inventory = output.get("sample_inventory", [])
    sample_ids = [item.get("sample_id") for item in inventory]
    if duplicate_values(sample_ids):
        add(failures, case_id, "sample IDs must be unique")
    if len(inventory) != output.get("sample_assessment", {}).get("sample_count"):
        add(failures, case_id, "sample_count must equal the sample inventory length")
    included = {item.get("sample_id") for item in inventory if item.get("inclusion_status") == "included"}
    for trait in _voice_traits(output):
        refs = set(trait.get("evidence_refs", []))
        unknown = refs - included
        if unknown:
            add(failures, case_id, f"trait {trait.get('trait_id')} cites excluded or unknown samples {sorted(unknown)}")
        if trait.get("scope") == "enduring" and len(refs) < 2:
            add(failures, case_id, f"enduring trait {trait.get('trait_id')} requires at least two included samples")
    if not included and _voice_traits(output):
        add(failures, case_id, "no traits may be asserted when every sample is excluded")


def validate_brief(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    claims = [item.get("claim_id") for item in output.get("required_claims", [])]
    duties = [item.get("claim_id") for item in output.get("evidence_duties", [])]
    if duplicate_values(claims):
        add(failures, case_id, "required claim IDs must be unique")
    if duplicate_values(duties):
        add(failures, case_id, "evidence duty claim IDs must be unique")
    if set(claims) != set(duties):
        add(failures, case_id, "every required claim must have exactly one evidence duty")
    claim_set = set(claims)
    for unit in output.get("structure_plan", []):
        unknown = set(unit.get("claims", [])) - claim_set
        if unknown:
            add(failures, case_id, f"structure unit {unit.get('unit_id')} references unknown claims {sorted(unknown)}")
    condition_ids = [item.get("condition_id") for item in output.get("release_conditions", [])]
    if duplicate_values(condition_ids):
        add(failures, case_id, "release condition IDs must be unique")


def validate_draft(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    draft = output.get("draft")
    marker_renderings = {
        'SOURCE_REQUIRED': '[SOURCE REQUIRED]',
        'AUTHOR_DECISION': '[AUTHOR DECISION]',
        'EXAMPLE_REQUIRED': '[EXAMPLE REQUIRED]',
        'CURRENT_VERIFICATION_REQUIRED': '[CURRENT VERIFICATION REQUIRED]',
    }
    for marker in output.get("gap_markers", []):
        rendered = marker_renderings.get(marker.get('marker'))
        if isinstance(draft, str) and rendered and rendered not in draft:
            add(failures, case_id, f"gap marker {marker.get('marker')} is absent from the draft text")
    for trace in output.get("source_trace", []):
        if trace.get("evidence_move") == "direct_evidence" and not trace.get("source_refs"):
            add(failures, case_id, "direct evidence trace requires at least one source reference")
    if output.get("integrity_summary", {}).get("claim_trace_complete") and output.get("gap_markers"):
        add(failures, case_id, "claim_trace_complete cannot be true while gap markers remain")


def validate_argument(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    nodes = output.get("argument_map", [])
    node_ids = [node.get("node_id") for node in nodes]
    if duplicate_values(node_ids):
        add(failures, case_id, "argument node IDs must be unique")
    node_set = set(node_ids)
    for node in nodes:
        unknown = set(node.get("supports", [])) - node_set
        if unknown:
            add(failures, case_id, f"argument node {node.get('node_id')} supports unknown nodes {sorted(unknown)}")
    finding_ids = [item.get("finding_id") for item in output.get("findings", [])]
    if duplicate_values(finding_ids):
        add(failures, case_id, "finding IDs must be unique")
    thesis_status = output.get("governing_thesis", {}).get("status")
    if thesis_status in {"missing", "human_decision_required"} and output.get("status") == "complete":
        add(failures, case_id, "missing or human-dependent thesis cannot produce a complete review")


def validate_audit(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    finding_ids = [item.get("finding_id") for item in output.get("findings", [])]
    if duplicate_values(finding_ids):
        add(failures, case_id, "finding IDs must be unique")
    if output.get("origin_claim_made") is not False or output.get("rewrite_authorised") is not False:
        add(failures, case_id, "Auditor may neither infer origin nor perform rewriting")
    for finding in output.get("findings", []):
        if finding.get("severity") == "P0" and finding.get("treatment") != "block":
            add(failures, case_id, f"P0 finding {finding.get('finding_id')} must block")


def validate_edit(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    edits = output.get("edit_log", [])
    edit_ids = [item.get("edit_id") for item in edits]
    if duplicate_values(edit_ids):
        add(failures, case_id, "edit IDs must be unique")
    material = output.get("material_changes", [])
    material_ids = [item.get("edit_id") for item in material]
    if duplicate_values(material_ids):
        add(failures, case_id, "material change IDs must be unique")
    if set(material_ids) - set(edit_ids):
        add(failures, case_id, "material changes must reference an edit_log edit_id")
    level_by_id = {item.get("edit_id"): item.get("edit_level") for item in edits}
    for edit_id, level in level_by_id.items():
        if isinstance(level, int) and level >= 4 and edit_id not in material_ids:
            add(failures, case_id, f"material edit {edit_id} is missing from material_changes")
    for item in material:
        actions = item.get("downstream_actions", [])
        if "none" in actions and len(actions) > 1:
            add(failures, case_id, f"material change {item.get('edit_id')} mixes 'none' with downstream actions")
    if "drift_detected" in output.get("drift_checks", {}).values() and output.get("status") == "complete":
        add(failures, case_id, "detected drift cannot produce a complete edit")
    for item in edits:
        if item.get("edit_level") == 0 and item.get("before_proposition") != item.get("after_proposition"):
            add(failures, case_id, f"level-0 edit {item.get('edit_id')} must preserve the proposition exactly")


def validate_verification(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    claims = output.get("claims", [])
    claim_ids = [item.get("claim_id") for item in claims]
    if duplicate_values(claim_ids):
        add(failures, case_id, "claim IDs must be unique")
    for claim in claims:
        source_ids = [source.get("source_id") for source in claim.get("sources", [])]
        if duplicate_values(source_ids):
            add(failures, case_id, f"claim {claim.get('claim_id')} has duplicate source IDs")
    if output.get("overall_release_risk") == "blocked" and not any(
        claim.get("status") in {"contradicted", "unsupported", "unverifiable"}
        for claim in claims
    ):
        add(failures, case_id, "blocked release risk requires a contradicted, unsupported or unverifiable claim")
    if output.get("overall_release_risk") == "low" and any(
        claim.get("status") not in {"verified", "author_judgement", "removed"}
        for claim in claims
    ):
        add(failures, case_id, "low release risk is inconsistent with unresolved claim statuses")


def validate_gate(case_id: str, output: dict[str, Any], failures: list[str]) -> None:
    for field in ("blocking_issues", "conditions_for_release"):
        ids = [item.get("issue_id") for item in output.get(field, [])]
        if duplicate_values(ids):
            add(failures, case_id, f"duplicate IDs in {field}")
    outcome = output.get("outcome")
    checks = output.get("check_results", {})
    results = [item.get("result") for item in checks.values()]
    required_stale = any(
        item.get("required") and (item.get("stale") or item.get("status") == "missing")
        for item in output.get("artefacts_reviewed", [])
    )
    approval = output.get("approval", {})
    if outcome == "ready":
        if any(result not in {"pass", "not_applicable"} for result in results):
            add(failures, case_id, "ready outcome requires all checks to pass or be not applicable")
        if required_stale:
            add(failures, case_id, "ready outcome cannot include missing or stale required artefacts")
        if approval.get("status") not in {"approved", "not_required"}:
            add(failures, case_id, "ready outcome requires approved or not-required approval")
        if output.get("verification_status") not in {"complete", "not_required"}:
            add(failures, case_id, "ready outcome requires complete or not-required verification")
        if output.get("disclosure_status") not in {"complete", "not_required"}:
            add(failures, case_id, "ready outcome requires complete or not-required disclosure")
    if outcome == "blocked":
        if not output.get("blocking_issues"):
            add(failures, case_id, "blocked outcome requires blocking issues")
        if not ("fail" in results or required_stale or output.get("verification_status") == "stale"):
            add(failures, case_id, "blocked outcome requires a failed check, stale required artefact or stale verification")
    if outcome == "human_decision_required" and output.get("human_action_required") is not True:
        add(failures, case_id, "human_decision_required must require human action")


SEMANTIC_VALIDATORS = {
    "route_declaration": validate_route,
    "authorship_source_pack": validate_authorship,
    "voice_profile": validate_voice,
    "editorial_brief": validate_brief,
    "draft_output": validate_draft,
    "argument_review": validate_argument,
    "anti_slop_audit": validate_audit,
    "edit_output": validate_edit,
    "verification_record": validate_verification,
    "gate_decision": validate_gate,
}


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
