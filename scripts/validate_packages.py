#!/usr/bin/env python3
"""Build, inspect, extract and revalidate Skill packages."""
from __future__ import annotations
import argparse, hashlib, re, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath
import yaml
from jsonschema import Draft202012Validator, FormatChecker
from package_skill import package

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr, flush=True)
    raise SystemExit(1)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_files(skill: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(skill.rglob("*")):
        if path.is_symlink():
            fail(f"{skill.name}: symbolic links are not permitted: {path.relative_to(skill)}")
        if path.is_file() and "__pycache__" not in path.parts:
            files[path.relative_to(skill).as_posix()] = digest(path)
    return files

def run(args: list[str]) -> None:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        if result.stdout: print(result.stdout, file=sys.stderr)
        if result.stderr: print(result.stderr, file=sys.stderr)
        fail(f"command failed: {' '.join(args)}")

def validate_extracted_skill(skill: Path) -> int:
    skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", skill_text, re.S)
    if not match:
        fail(f"{skill.name}: extracted SKILL.md has malformed frontmatter")
    frontmatter = yaml.safe_load(match.group(1))
    if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill.name:
        fail(f"{skill.name}: extracted SKILL.md name does not match package directory")
    metadata = yaml.safe_load((skill / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = metadata.get("interface") if isinstance(metadata, dict) else None
    if not isinstance(interface, dict) or not interface.get("display_name") or not interface.get("short_description"):
        fail(f"{skill.name}: extracted metadata is incomplete")
    contract = yaml.safe_load((skill / "references" / "output-contract.yaml").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(contract)
    validator = Draft202012Validator(contract, format_checker=FormatChecker())
    cases_doc = yaml.safe_load((skill / "tests" / "cases.yaml").read_text(encoding="utf-8"))
    cases = cases_doc.get("cases") if isinstance(cases_doc, dict) else None
    if not isinstance(cases, list) or not cases:
        fail(f"{skill.name}: extracted package has no executable fixtures")
    for case in cases:
        errors = list(validator.iter_errors(case.get("example_output") if isinstance(case, dict) else None))
        if errors:
            first = errors[0]
            location = ".".join(str(part) for part in first.path) or "<root>"
            fail(f"{skill.name}: extracted fixture failed at {location}: {first.message}")
    return len(cases)

def validate_one(skill: Path, workspace: Path) -> int:
    expected = source_files(skill)
    package_dir = workspace / "package"
    extract_dir = workspace / "extract"
    package_dir.mkdir(parents=True)
    extract_dir.mkdir(parents=True)
    archive_path = package(skill, package_dir, validate_first=False)
    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        if bad:
            fail(f"{skill.name}: corrupt archive member {bad}")
        members = [item for item in archive.infolist() if not item.is_dir()]
        names = [item.filename for item in members]
        if len(names) != len(set(names)):
            fail(f"{skill.name}: archive contains duplicate member names")
        expected_names = {f"{skill.name}/{name}" for name in expected}
        if set(names) != expected_names:
            fail(f"{skill.name}: archive topology mismatch")
        for item in members:
            path = PurePosixPath(item.filename)
            if path.is_absolute() or ".." in path.parts or not path.parts or path.parts[0] != skill.name:
                fail(f"{skill.name}: unsafe archive path {item.filename!r}")
            relative = PurePosixPath(*path.parts[1:]).as_posix()
            if hashlib.sha256(archive.read(item)).hexdigest() != expected[relative]:
                fail(f"{skill.name}: packaged bytes differ for {relative}")
        archive.extractall(extract_dir)
    extracted = extract_dir / skill.name
    if source_files(extracted) != expected:
        fail(f"{skill.name}: extracted package differs from source Skill")
    validate_extracted_skill(extracted)
    return len(expected)

def discover(selected: str | None) -> list[Path]:
    if selected:
        path = Path(selected)
        if not path.is_absolute(): path = (ROOT / path).resolve()
        if not path.is_dir(): fail(f"Skill folder not found: {path}")
        return [path]
    return sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())

def validate_packages(selected: str | None = None, *, prevalidated: bool = False) -> str:
    skills = discover(selected)
    if not prevalidated:
        args = ["--skill", str(skills[0])] if selected else []
        run([sys.executable, str(SCRIPTS / "validate_skill_suite.py"), *args])
        run([sys.executable, str(SCRIPTS / "run_contract_tests.py"), *args])
    lines: list[str] = []
    total = 0
    with tempfile.TemporaryDirectory(prefix="editorial-package-validation-") as temp:
        root = Path(temp)
        for index, skill in enumerate(skills, start=1):
            print(f"[package] start {index}/{len(skills)} {skill.name}", file=sys.stderr, flush=True)
            count = validate_one(skill, root / f"{index:02d}-{skill.name}")
            total += count
            lines.append(f"[{index}/{len(skills)}] validated package {skill.name}")
            print(f"[package] pass {index}/{len(skills)} {skill.name}", file=sys.stderr, flush=True)
    lines.append(f"PASS: {len(skills)} Skill package(s) built, byte-compared, safely extracted and directly revalidated across {total} packaged files.")
    return "\n".join(lines)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill")
    parser.add_argument("--prevalidated", action="store_true")
    args = parser.parse_args()
    print(validate_packages(args.skill, prevalidated=args.prevalidated))

if __name__ == "__main__": main()
