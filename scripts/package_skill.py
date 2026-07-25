#!/usr/bin/env python3
import sys
import zipfile
from pathlib import Path


def fail(message: str) -> None:
    print(f'ERROR: {message}', file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) not in (2, 3):
        fail('usage: package_skill.py <skill-folder> [output-dir]')
    root = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else Path.cwd()
    if not root.is_dir():
        fail('skill folder does not exist')
    if not (root / 'SKILL.md').is_file() or not (root / 'agents' / 'openai.yaml').is_file():
        fail('skill must contain SKILL.md and agents/openai.yaml')
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / 'skill.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:
                archive.write(path, Path(root.name) / path.relative_to(root))
    if out.stat().st_size > 25 * 1024 * 1024:
        out.unlink()
        fail('package exceeds 25 MB')
    print(out)

if __name__ == '__main__':
    main()
