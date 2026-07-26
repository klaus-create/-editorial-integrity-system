#!/usr/bin/env python3
"""Check local Markdown links and Skill-declared repository paths."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKILL_PATH = re.compile(r"`((?:references|tests|agents)/[^`]+)`")


def normalise_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().split()[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()


def main() -> None:
    failures: list[str] = []
    checked = 0
    for source in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "dist", "packages-repo", "packages-official"} for part in source.parts):
            continue
        text = source.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK.findall(text):
            target = normalise_target(source, raw)
            if target is None:
                continue
            checked += 1
            try:
                target.relative_to(ROOT)
            except ValueError:
                failures.append(f"{source.relative_to(ROOT)}: local link escapes repository: {raw}")
                continue
            if not target.exists():
                failures.append(f"{source.relative_to(ROOT)}: missing local link target: {raw}")

    for skill_file in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        for raw in SKILL_PATH.findall(text):
            checked += 1
            target = (skill_file.parent / raw).resolve()
            if not target.is_file():
                failures.append(f"{skill_file.relative_to(ROOT)}: missing declared Skill resource: {raw}")

    if failures:
        print("REPOSITORY LINK FAILURES", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {checked} local documentation and Skill resource references resolve.")


if __name__ == "__main__":
    main()
