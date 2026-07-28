#!/usr/bin/env python3
"""Validate and package one Skill as skill.zip."""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

MAX_SKILL_ZIP_BYTES = 25 * 1024 * 1024
SCRIPT_DIR = Path(__file__).resolve().parent


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def run_check(script: str, root: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / script), "--skill", str(root)],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        fail(f"validation failed before packaging: {script}")


def package(root: Path, out_dir: Path, *, validate_first: bool = True) -> Path:
    """Build one validated Skill archive and return its path."""
    root = root.resolve()
    out_dir = out_dir.resolve()
    if not root.is_dir():
        fail(f"skill folder does not exist: {root}")

    if validate_first:
        run_check("validate_skill_suite.py", root)
        run_check("run_contract_tests.py", root)

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "skill.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, root.name / path.relative_to(root))

    if out.stat().st_size > MAX_SKILL_ZIP_BYTES:
        out.unlink()
        fail("package exceeds 25 MB")

    expected = f"{root.name}/SKILL.md"
    with zipfile.ZipFile(out) as archive:
        names = set(archive.namelist())
        if expected not in names:
            out.unlink()
            fail(f"package is missing {expected}")

    return out


def main() -> None:
    if len(sys.argv) not in (2, 3):
        fail("usage: package_skill.py <skill-folder> [output-dir]")

    root = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) == 3 else Path.cwd()
    print(package(root, out_dir))


if __name__ == "__main__":
    main()
