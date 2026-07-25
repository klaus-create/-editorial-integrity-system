#!/usr/bin/env python3
import sys
from pathlib import Path
import yaml

REQUIRED = {
    'project_name': str,
    'editorial_system_version': (str, int, float),
    'authorship_model': str,
    'required_skills': list,
    'factual_verification': str,
}
ALLOWED_AUTHORSHIP = {'personal','executive_assisted','institutional','collaborative','brand','literary'}
ALLOWED_VERIFICATION = {'none','external_claims','high_risk_claims','all_material_claims'}


def fail(message: str) -> None:
    print(f'INVALID: {message}', file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail('usage: validate_manifest.py <manifest.yaml>')
    path = Path(sys.argv[1])
    if not path.exists():
        fail(f'file not found: {path}')
    try:
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'cannot parse YAML: {exc}')
    if not isinstance(data, dict):
        fail('manifest root must be a mapping')
    manifest = data.get('project_editorial_manifest', data)
    if not isinstance(manifest, dict):
        fail('project_editorial_manifest must be a mapping')
    for key, expected in REQUIRED.items():
        if key not in manifest:
            fail(f'missing required field: {key}')
        if not isinstance(manifest[key], expected):
            fail(f'{key} has invalid type')
    if manifest['authorship_model'] not in ALLOWED_AUTHORSHIP:
        fail('authorship_model is not recognised')
    if manifest['factual_verification'] not in ALLOWED_VERIFICATION:
        fail('factual_verification is not recognised')
    if not manifest['required_skills']:
        fail('required_skills must not be empty')
    print(f"VALID: {manifest['project_name']} ({manifest['editorial_system_version']})")

if __name__ == '__main__':
    main()
