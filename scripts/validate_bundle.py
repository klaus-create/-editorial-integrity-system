#!/usr/bin/env python3
"""Check a locally pinned assignment bundle. Hashes detect drift, not authenticity."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
from validate_artefact import validate_record, validate_release_context
from validate_skill_suite import load_yaml


def validate_bundle(path: Path) -> list[str]:
    try:
        bundle = load_yaml(path)
        if not isinstance(bundle, dict) or bundle.get('bundle_version') != '1.0' or not isinstance(bundle.get('files'), dict):
            return ['invalid bundle envelope']
        errors, loaded = [], {}
        root = path.resolve().parent
        for role, entry in bundle['files'].items():
            if not isinstance(entry, dict) or set(entry) != {'path', 'sha256'} or not isinstance(entry['path'], str):
                errors.append(f'{role}: invalid file entry')
                continue
            file = (root / entry['path']).resolve()
            if not file.is_relative_to(root):
                errors.append(f'{role}: file escapes bundle directory')
                continue
            if hashlib.sha256(file.read_bytes()).hexdigest() != entry['sha256']:
                errors.append(f'{role}: content hash mismatch')
                continue
            if role in {'gate', 'route', 'verification', 'draft', 'registry', 'manifest'}:
                loaded[role] = load_yaml(file)
        if errors:
            return errors
        if 'gate' not in loaded:
            return ['bundle requires gate']
        gate = loaded.pop('gate')
        errors = validate_record(gate)
        if not errors:
            errors += validate_release_context(gate, **loaded)
        return errors
    except (OSError, ValueError, TypeError) as exc:
        return [str(exc)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    args = parser.parse_args()
    errors = validate_bundle(args.bundle)
    if errors:
        for error in errors:
            print(f'INVALID: {error}')
        raise SystemExit(1)
    print('PASS: pinned files and supplied context are consistent. Human approval and factual truth remain external checks.')


if __name__ == '__main__':
    main()
