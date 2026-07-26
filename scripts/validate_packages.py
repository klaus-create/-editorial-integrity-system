#!/usr/bin/env python3
"""Build, inspect, extract and revalidate every Skill package."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import stat
import subprocess
import sys
import tempfile
import zipfile
import re
from pathlib import Path, PurePosixPath

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from package_skill import package

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_files(skill: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(skill.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(skill).as_posix()
        files[relative] = digest_bytes(path.read_bytes())
    return files


def run(args: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        fail(f"command failed: {' '.join(args)}")
    return result.stdout.strip()


def validate_extracted_skill(skill: Path) -> int:
    required = (
        skill / "SKILL.md",
        skill / "agents" / "openai.yaml",
        skill / "references" / "output-contract.yaml",
        skill / "tests" / "cases.yaml",
    )
    missing = [path.relative_to(skill).as_posix() for path in required if not path.is_file()]
    if missing:
        fail(f"{skill.name}: extracted package missing required files {missing}")

    skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
    if not match:
        fail(f"{skill.name}: extracted SKILL.md has malformed frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill.name:
        fail(f"{skill.name}: extracted SKILL.md name does not match package directory")

    metadata = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = metadata.get("interface") if isinstance(metadata, dict) else None
    if not isinstance(interface, dict) or not interface.get("display_name") or not interface.get("short_description"):
        fail(f"{skill.name}: extracted metadata is incomplete")

    contract_path = skill / "references" / "output-contract.yaml"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(contract)
    validator = Draft202012Validator(contract, format_checker=FormatChecker())

    cases_path = skill / "tests" / "cases.yaml"
    cases_document = yaml.safe_load(cases_path.read_text(encoding="utf-8"))
    cases = cases_document.get("cases") if isinstance(cases_document, dict) else None
    if not isinstance(cases, list) or not cases:
        fail(f"{skill.name}: extracted package has no executable fixtures")
    for case in cases:
        case_id = case.get("case_id", "<unknown>") if isinstance(case, dict) else "<invalid>"
        output = case.get("example_output") if isinstance(case, dict) else None
        errors = sorted(validator.iter_errors(output), key=lambda error: list(error.path))
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.path) or "<root>"
            fail(f"{skill.name}: extracted fixture {case_id} failed at {location}: {first.message}")
    return len(cases)


def validate_archive(skill: Path, archive_path: Path, extract_root: Path) -> int:
    name = skill.name
    expected = source_files(skill)
    expected_members = {f"{name}/{relative}" for relative in expected}

    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        if bad is not None:
            fail(f"{name}: corrupt archive member {bad}")

        members = [item for item in archive.infolist() if not item.is_dir()]
        actual_members = {item.filename for item in members}
        if len(actual_members) != len(members):
            fail(f"{name}: archive contains duplicate member names")
        if actual_members != expected_members:
            missing = sorted(expected_members - actual_members)
            extra = sorted(actual_members - expected_members)
            fail(f"{name}: archive topology mismatch; missing={missing}, extra={extra}")

        for item in members:
            path = PurePosixPath(item.filename)
            if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != name:
                fail(f"{name}: unsafe archive path {item.filename!r}")
            mode = (item.external_attr >> 16) & 0xFFFF
            if stat.S_ISLNK(mode):
                fail(f"{name}: symbolic links are not permitted in Skill packages")
            relative = PurePosixPath(*path.parts[1:]).as_posix()
            if digest_bytes(archive.read(item)) != expected[relative]:
                fail(f"{name}: packaged bytes differ for {relative}")

        archive.extractall(extract_root)

    extracted = extract_root / name
    extracted_files = source_files(extracted)
    if extracted_files != expected:
        fail(f"{name}: extracted package differs from source Skill")

    validate_extracted_skill(extracted)
    return len(expected)


def discover(selected: str | None) -> list[Path]:
    if selected:
        path = Path(selected)
        if not path.is_absolute():
            path = (ROOT / path).resolve()
        if not path.is_dir():
            fail(f"Skill folder not found: {path}")
        return [path]
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())


def validate_packages(selected: str | None = None, *, prevalidated: bool = False) -> str:
    skills = discover(selected)
    if not prevalidated:
        if selected:
            run([sys.executable, str(SCRIPTS / "validate_skill_suite.py"), "--skill", str(skills[0])])
            run([sys.executable, str(SCRIPTS / "run_contract_tests.py"), "--skill", str(skills[0])])
        else:
            run([sys.executable, str(SCRIPTS / "validate_skill_suite.py")])
            run([sys.executable, str(SCRIPTS / "run_contract_tests.py")])

    total_files = 0
    lines: list[str] = []
    with tempfile.TemporaryDirectory(prefix="editorial-package-validation-") as temp_value:
        temp = Path(temp_value)
        packages = temp / "packages"
        extracted = temp / "extracted"
        packages.mkdir()
        extracted.mkdir()

        jobs: list[tuple[int, Path, Path, Path]] = []
        for index, skill in enumerate(skills, start=1):
            output = packages / skill.name
            output.mkdir()
            archive = package(skill, output, validate_first=False)
            if not archive.is_file() or archive.stat().st_size == 0:
                fail(f"{skill.name}: package was not created")
            extract_parent = extracted / f"{index:02d}-{skill.name}"
            extract_parent.mkdir()
            jobs.append((index, skill, archive, extract_parent))

        def validate_job(job: tuple[int, Path, Path, Path]) -> tuple[int, str, int]:
            index, skill, archive, extract_parent = job
            print(f"[package] start {index}/{len(skills)} {skill.name}", file=sys.stderr, flush=True)
            count = validate_archive(skill, archive, extract_parent)
            print(f"[package] pass {index}/{len(skills)} {skill.name}", file=sys.stderr, flush=True)
            return index, skill.name, count

        max_workers = min(4, len(jobs))
        results: list[tuple[int, str, int]] = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(validate_job, job) for job in jobs]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        for index, name, count in sorted(results):
            lines.append(f"[{index}/{len(skills)}] validated package {name}")
            total_files += count

    lines.append(
        f"PASS: {len(skills)} Skill package(s) built, byte-compared, safely extracted and directly revalidated "
        f"across {total_files} packaged files."
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", help="Validate one Skill package instead of the full suite")
    parser.add_argument(
        "--prevalidated",
        action="store_true",
        help="Skip source-suite validation when the caller has already completed it.",
    )
    args = parser.parse_args()
    print(validate_packages(args.skill, prevalidated=args.prevalidated))


if __name__ == "__main__":
    main()
