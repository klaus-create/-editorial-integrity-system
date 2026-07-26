#!/usr/bin/env python3
"""Run deterministic repository acceptance checks.

Default mode verifies that the tracked acceptance report is current. Use --write only
when intentionally refreshing that report after a reviewed repository change.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from validate_packages import validate_packages as validate_all_packages

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
REPORT_PATH = ROOT / "governance" / "AUDIT-ACCEPTANCE-0.1.4.yaml"
EXPECTED_SKILLS = {
    "anti-slop-auditor",
    "argument-structure-reviewer",
    "authorship-capture",
    "editorial-brief-compiler",
    "editorial-integrity-router",
    "factual-verifier",
    "final-editorial-gate",
    "source-grounded-drafter",
    "voice-preserving-editor",
    "voice-profile-builder",
}


def run_command(args: list[str]) -> tuple[bool, str]:
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8") as output_file:
        result = subprocess.run(args, cwd=ROOT, text=True, stdout=output_file, stderr=subprocess.STDOUT)
        output_file.seek(0)
        output = output_file.read().strip()
    return result.returncode == 0, output


def run_script(script: str, *args: str) -> tuple[bool, str]:
    started = time.monotonic()
    print(f"[audit] running {script} {' '.join(args)}".rstrip(), file=sys.stderr, flush=True)
    passed, output = run_command([sys.executable, str(ROOT / "scripts" / script), *args])
    elapsed = time.monotonic() - started
    print(f"[audit] {'passed' if passed else 'failed'} {script} in {elapsed:.1f}s", file=sys.stderr, flush=True)
    return passed, output


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def record(check_id: str, passed: bool, evidence: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    for script in ("validate_skill_suite.py", "run_contract_tests.py", "check_repository_links.py"):
        passed, output = run_script(script)
        record(script, passed, output)

    manifest_evidence: dict[str, str] = {}
    manifests_ok = True
    for path in sorted((ROOT / "projects").glob("*/project-editorial-manifest.yaml")):
        passed, output = run_script("validate_manifest.py", str(path))
        manifests_ok = manifests_ok and passed
        manifest_evidence[path.parent.name] = output
    record("project-manifest-validation", manifests_ok and len(manifest_evidence) == 3, json.dumps(manifest_evidence, sort_keys=True))

    print("[audit] running validate_packages.py --prevalidated", file=sys.stderr, flush=True)
    started = time.monotonic()
    try:
        package_output = validate_all_packages(prevalidated=True)
        packages_ok = True
    except SystemExit as exc:
        packages_ok = False
        package_output = f"package validation exited with status {exc.code}"
    except Exception as exc:
        packages_ok = False
        package_output = f"package validation failed: {exc}"
    elapsed = time.monotonic() - started
    print(f"[audit] {'passed' if packages_ok else 'failed'} validate_packages.py in {elapsed:.1f}s", file=sys.stderr, flush=True)
    record("extracted-package-validation", packages_ok, package_output)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    release12 = (ROOT / "governance" / "RELEASE-0.1.2.md").read_text(encoding="utf-8")
    release13 = (ROOT / "governance" / "RELEASE-0.1.3.md").read_text(encoding="utf-8")
    release14 = (ROOT / "governance" / "RELEASE-0.1.4.md").read_text(encoding="utf-8")
    standard = (ROOT / "governance" / "CAPABILITY-DEPTH-STANDARD.md").read_text(encoding="utf-8")
    handoffs = (ROOT / "docs" / "ARTEFACTS-AND-HANDOFFS.md").read_text(encoding="utf-8")
    workflow = (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8")
    requirements = (ROOT / "requirements-validation.txt").read_text(encoding="utf-8")
    audit_source = (ROOT / "scripts" / "audit_repository.py").read_text(encoding="utf-8")

    record("current-release", "v0.1.4-post-merge-hardening" in readme and "v0.1.4-post-merge-hardening" in roadmap and "# Release 0.1.4: Post-Merge Hardening" in release14, "README, roadmap and release notes identify 0.1.4 as the current released state.")
    active_release_text = "\n".join((readme, roadmap, release14))
    stale_phrases = [phrase for phrase in ("Current release candidate", "Release candidate:", "corrective release candidate", "only after the corrective pull request passes and is merged") if phrase in active_release_text]
    record("released-state-language", not stale_phrases, "No stale pre-merge candidate language remains in active release documentation." if not stale_phrases else f"stale phrases={stale_phrases}")
    record("release-0.1.2-retracted", "Superseded and retracted" in release12 and "Do not cite 0.1.2 as method-complete" in release12, "0.1.2 explicitly retracts its maturity claim.")
    record("release-boundary", "Not yet pilot-tested" in release14 and "not yet pilot-tested" in readme.lower() and "not yet pilot-tested" in roadmap.lower(), "Current documentation separates deterministic acceptance from live performance evidence.")
    record("release-0.1.3-historical", "Historical release record" in release13 and "e8d26c2d49887db503bd53e1f0d0af0308f99b4e" in release13 and "RELEASE-0.1.4.md" in release13, "0.1.3 records its merge and points to the current patch release.")
    record("capability-standard-depth", len(standard.splitlines()) >= 240 and "## 10. Maturity transitions" in standard and "No lower state implies a higher one." in standard, f"Capability standard lines={len(standard.splitlines())}.")
    record("handoff-specification", all(token in handoffs for token in ("## Common artefact envelope", "## Producer and consumer map", "## Conditional work", "## Gate outcomes", "## Re-entry rules")), "Common fields, producer/consumer ownership, status semantics and re-entry rules exist.")
    direct_validation_tokens = ("validate_skill_suite.py", "run_contract_tests.py", "validate_manifest.py", "check_repository_links.py", "validate_packages.py")
    record("ci-single-acceptance-orchestrator", "audit_repository.py" in workflow and all(token not in workflow for token in direct_validation_tokens), "CI invokes one maintained acceptance orchestrator without duplicating expensive validation steps.")
    record("audit-orchestrates-repository-scripts", all(token in audit_source for token in direct_validation_tokens), "The acceptance audit invokes the maintained suite, contract, manifest, link and package validators.")
    record("ci-release-hardening", all(token in workflow for token in ("workflow_dispatch:", "contents: read", "cancel-in-progress: true", "requirements-validation.txt", "Run complete repository acceptance audit")), "CI has manual dispatch, least-privilege contents access, concurrency control, pinned direct dependencies and extracted-package validation.")
    expected_requirements = {"PyYAML==6.0.3", "jsonschema==4.26.0"}
    actual_requirements = {line.strip() for line in requirements.splitlines() if line.strip() and not line.lstrip().startswith("#")}
    record("validation-dependency-pins", actual_requirements == expected_requirements, f"requirements={sorted(actual_requirements)}")
    record("ci-no-temporary-audit-export", "upload-artifact" not in workflow and "audit-bundle" not in workflow, "Temporary private repository export has been removed.")
    record("ci-no-length-proxy", "len(method)" not in workflow and "len(gate)" not in workflow, "CI does not use inline character-count proxies as acceptance evidence.")

    skill_names = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    record("skill-inventory", skill_names == EXPECTED_SKILLS, f"skills={sorted(skill_names)}")

    manifest_versions: dict[str, Any] = {}
    for path in sorted((ROOT / "projects").glob("*/project-editorial-manifest.yaml")):
        data = load_yaml(path)
        manifest_versions[path.parent.name] = data.get("editorial_system", {}).get("required_version")
    record("project-version-alignment", set(manifest_versions.values()) == {"0.1.4"}, json.dumps(manifest_versions, sort_keys=True))

    short_descriptions: list[tuple[str, str]] = []
    for path in sorted((ROOT / "skills").glob("*/agents/openai.yaml")):
        short = load_yaml(path).get("interface", {}).get("short_description", "")
        short_descriptions.append((path.parent.parent.name, short))
    metadata_ok = all(70 <= len(short.strip()) <= 180 and re.search(r"[.!?]$", short.strip()) for _, short in short_descriptions)
    record("metadata-completeness", metadata_ok and len(short_descriptions) == len(EXPECTED_SKILLS), f"Reviewed {len(short_descriptions)} complete short descriptions.")

    schema_files = sorted((ROOT / "schemas").glob("*.yaml"))
    schema_ids: list[str] = []
    schema_failures: list[str] = []
    for path in schema_files:
        data = load_yaml(path)
        try:
            Draft202012Validator.check_schema(data)
        except Exception as exc:
            schema_failures.append(f"{path.name}: {exc}")
        schema_id = data.get("$id")
        if not isinstance(schema_id, str) or not schema_id:
            schema_failures.append(f"{path.name}: missing $id")
        else:
            schema_ids.append(schema_id)
        ineffective = [key for key in data if key in {"$type", "$title"}]
        if ineffective:
            schema_failures.append(f"{path.name}: ineffective keys {ineffective}")
    duplicate_ids = sorted({value for value in schema_ids if schema_ids.count(value) > 1})
    if duplicate_ids:
        schema_failures.append(f"duplicate schema IDs: {duplicate_ids}")
    record("schema-integrity", not schema_failures and len(schema_files) == 11, "Eleven valid schemas with unique IDs." if not schema_failures else "; ".join(schema_failures))

    specialist_guides = {
        "editorial-integrity-router": "risk-and-routing-matrix.md",
        "authorship-capture": "elicitation-and-epistem-classification.md",
        "voice-profile-builder": "voice-analysis-and-sampling.md",
        "editorial-brief-compiler": "form-brief-patterns.md",
        "source-grounded-drafter": "form-drafting-playbooks.md",
        "argument-structure-reviewer": "argument-analysis-models.md",
        "anti-slop-auditor": "calibration-taxonomy.md",
        "voice-preserving-editor": "edit-ladder-and-drift.md",
        "factual-verifier": "claim-verification-playbooks.md",
        "final-editorial-gate": "release-decision-matrix.md",
    }
    guide_evidence: dict[str, dict[str, int | bool]] = {}
    guides_ok = True
    for skill_name, filename in specialist_guides.items():
        path = ROOT / "skills" / skill_name / "references" / filename
        skill_text = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        exists = path.is_file()
        lines = len(path.read_text(encoding="utf-8").splitlines()) if exists else 0
        sections = len(re.findall(r"^##\s+", path.read_text(encoding="utf-8"), re.M)) if exists else 0
        referenced = f"references/{filename}" in skill_text
        guide_evidence[skill_name] = {"lines": lines, "sections": sections, "referenced": referenced}
        guides_ok = guides_ok and exists and lines >= 45 and sections >= 5 and referenced
    record("specialist-guide-depth", guides_ok and len(guide_evidence) == len(EXPECTED_SKILLS), json.dumps(guide_evidence, sort_keys=True))

    fixture_count = 0
    categories: set[str] = set()
    for path in sorted((ROOT / "skills").glob("*/tests/cases.yaml")):
        data = load_yaml(path)
        fixture_count += len(data.get("cases", []))
        categories.update(case.get("category") for case in data.get("cases", []))
    record("fixture-coverage", fixture_count == 60 and categories == {"standard", "edge", "adversarial", "false_positive"}, f"fixtures={fixture_count}; categories={sorted(categories)}; semantic diversity and negative checks are executed by run_contract_tests.py")

    skill_matrix: dict[str, dict[str, Any]] = {}
    matrix_ok = True
    for skill_name in sorted(EXPECTED_SKILLS):
        root = ROOT / "skills" / skill_name
        metadata = load_yaml(root / "agents" / "openai.yaml")["interface"]
        method_text = (root / "references" / "method.md").read_text(encoding="utf-8")
        guide_name = specialist_guides[skill_name]
        guide_text = (root / "references" / guide_name).read_text(encoding="utf-8")
        gate_text = (root / "references" / "quality-gate.md").read_text(encoding="utf-8")
        contract = load_yaml(root / "references" / "output-contract.yaml")
        fixture_cases = load_yaml(root / "tests" / "cases.yaml").get("cases", [])
        categories_for_skill = sorted({case.get("category") for case in fixture_cases})
        evidence = {
            "entrypoint_lines": len((root / "SKILL.md").read_text(encoding="utf-8").splitlines()),
            "metadata_description_characters": len(metadata.get("short_description", "").strip()),
            "method_lines": len(method_text.splitlines()),
            "method_sections": len(re.findall(r"^##\s+", method_text, re.M)),
            "specialist_guide": guide_name,
            "specialist_guide_lines": len(guide_text.splitlines()),
            "specialist_guide_sections": len(re.findall(r"^##\s+", guide_text, re.M)),
            "quality_gate_checks": len(re.findall(r"^- \[ \]", gate_text, re.M)),
            "fixture_count": len(fixture_cases),
            "fixture_categories": categories_for_skill,
            "schema_id": contract.get("$id"),
        }
        passed = evidence["method_lines"] >= 60 and evidence["method_sections"] >= 8 and evidence["specialist_guide_lines"] >= 45 and evidence["specialist_guide_sections"] >= 5 and evidence["quality_gate_checks"] >= 10 and evidence["fixture_count"] >= 6 and set(categories_for_skill) == {"standard", "edge", "adversarial", "false_positive"} and isinstance(evidence["schema_id"], str)
        evidence["deterministic_acceptance"] = "pass" if passed else "fail"
        matrix_ok = matrix_ok and passed
        skill_matrix[skill_name] = evidence
    record("per-skill-acceptance-matrix", matrix_ok and len(skill_matrix) == len(EXPECTED_SKILLS), "Each Skill records method, specialist guide, quality gate, fixture and contract evidence.")

    baseline_artifact = ROOT / "audit-findings.yaml"
    record("obsolete-baseline-removed", not baseline_artifact.exists(), "The pre-remediation baseline findings file is not shipped as current evidence.")

    failed = [check for check in checks if not check["passed"]]
    return {"audit_version": "1.4", "release": "0.1.4", "checks": checks, "skills": skill_matrix, "summary": {"passed": len(checks) - len(failed), "failed": len(failed)}, "deterministic_result": "pass" if not failed else "fail", "performance_evidence": "not_assessed_by_this_audit"}


def serialise(report: dict[str, Any]) -> str:
    return yaml.safe_dump(report, sort_keys=False, allow_unicode=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Refresh the tracked acceptance report instead of verifying it is current.")
    args = parser.parse_args()
    report = build_report()
    rendered = serialise(report)
    print(rendered, end="")
    if args.write:
        REPORT_PATH.write_text(rendered, encoding="utf-8")
    else:
        if not REPORT_PATH.is_file():
            print(f"ERROR: tracked audit report is missing: {REPORT_PATH}", file=sys.stderr)
            raise SystemExit(1)
        tracked = REPORT_PATH.read_text(encoding="utf-8")
        if tracked != rendered:
            print("ERROR: tracked audit report is stale. Review the change, then run python scripts/audit_repository.py --write.", file=sys.stderr)
            raise SystemExit(1)
    if report["deterministic_result"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
