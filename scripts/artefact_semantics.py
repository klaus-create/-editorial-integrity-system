"""Shared cross-field checks for live artefacts and contract fixtures."""
from __future__ import annotations
import json
from typing import Any

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
        if module.get("may_edit") and name not in {
            "source-grounded-drafter", "voice-preserving-editor", "factual-verifier"
        }:
            add(failures, case_id, f"{name} may not edit final prose")
    risks = output.get("risk_dimensions", {})
    if any(risks.get(key) == "high" for key in ("factual", "consequence")) and output.get("workflow_level") not in {"full", "extended"}:
        add(failures, case_id, "high factual or consequence risk requires full or extended routing")
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
    if any(claim.get("materiality") == "critical" and claim.get("status") in
           {"unsupported", "contradicted", "unverifiable"} for claim in claims):
        if output.get("overall_release_risk") != "blocked":
            add(failures, case_id, "critical unresolved claims require blocked release risk")
    for claim in claims:
        if claim.get("status") == "verified" and claim.get("claim_class") == "current_status":
            if not any(source.get("freshness") == "current" and source.get("accessed_on")
                       for source in claim.get("sources", [])):
                add(failures, case_id, "verified current-status claim requires a dated current source")
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
    approval = output.get("approval", {})
    if approval.get("required") and approval.get("status") == "not_required":
        add(failures, case_id, "required approval cannot be marked not_required")
    if approval.get("status") == "approved" and not (approval.get("approver") or "").strip():
        add(failures, case_id, "approved status requires a named approver")
    inventory = output.get("artefacts_reviewed", [])
    types = [item.get("artefact_type") for item in inventory]
    if duplicate_values(types):
        add(failures, case_id, "reviewed artefact types must be unique")
    outcome = output.get("outcome")
    checks = output.get("check_results", {})
    results = [item.get("result") for item in checks.values()]
    required_stale = any(
        item.get("required") and (item.get("stale") or item.get("status") != "present" or not item.get("version"))
        for item in output.get("artefacts_reviewed", [])
    )
    approval = output.get("approval", {})
    if outcome in {"ready", "conditional"}:
        if output.get("blocking_issues") or "fail" in results or required_stale:
            add(failures, case_id, "ready or conditional outcome cannot contain an integrity blocker")
        if approval.get("required") and approval.get("status") != "approved":
            add(failures, case_id, "ready or conditional outcome requires mandatory approval")
        required_types = {"draft_output"}
        if output.get("workflow_level") in {"full", "extended"}:
            required_types |= {"route_declaration", "editorial_brief"}
        if output.get("workflow_level") == "extended":
            required_types |= {"claim_registry", "source_inventory", "continuity_record",
                               "change_log", "provenance_record", "approval_record"}
        if approval.get("required"):
            required_types.add("approval_record")
        if output.get("verification_status") == "complete":
            required_types.add("verification_record")
        reviewed = {item.get("artefact_type"): item for item in inventory}
        for name in sorted(required_types):
            item = reviewed.get(name, {})
            if (item.get("status") != "present" or item.get("stale") is not False
                    or not item.get("required") or not item.get("version")):
                add(failures, case_id, f"mandatory current artefact missing: {name}")
        for item in inventory:
            if item.get("required") and item.get("status") == "present":
                if output.get("input_versions", {}).get(item.get("artefact_type")) != item.get("version"):
                    add(failures, case_id, "reviewed artefact must match input_versions")
        if reviewed.get("draft_output", {}).get("version") != output.get("draft_version"):
            add(failures, case_id, "reviewed draft must match the release candidate")
        if output.get("verification_status") in {"partial", "stale"}:
            add(failures, case_id, "ready or conditional outcome requires current complete verification")
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

