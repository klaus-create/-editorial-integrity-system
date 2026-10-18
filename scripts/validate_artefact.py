#!/usr/bin/env python3
"""Validate a produced JSON/YAML artefact and selected release dependencies.

A successful check establishes record consistency, not factual truth or authentic
human approval. The host must obtain dependencies from its trusted assignment state.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from artefact_semantics import SEMANTIC_VALIDATORS, validate_common_semantics
from validate_skill_suite import load_yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {p.stem.replace('.schema', '').replace('-', '_'): p
           for p in (ROOT / 'schemas').glob('*.schema.yaml')}


def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ['artefact must be an object']
    kind = record.get('artefact_type')
    if not isinstance(kind, str):
        return ['artefact_type must be a string']
    schema_path = SCHEMAS.get(kind)
    if schema_path is None:
        return ['unknown artefact_type']
    validator = Draft202012Validator(load_yaml(schema_path), format_checker=FormatChecker())
    errors = [f"{'.'.join(map(str, e.path)) or '<root>'}: {e.message}"
              for e in validator.iter_errors(record)]
    if not errors:
        validate_common_semantics('artefact', record, errors)
        semantic = SEMANTIC_VALIDATORS.get(record['artefact_type'])
        if semantic:
            semantic('artefact', record, errors)
    return errors


def validate_release_context(record: dict, route: dict | None = None,
                             manifest: dict | None = None,
                             verification: dict | None = None,
                             draft: dict | None = None,
                             registry: dict | None = None) -> list[str]:
    """Check declared requirements against caller-supplied trusted dependencies."""
    errors: list[str] = []
    if record['artefact_type'] != 'gate_decision':
        if any(x is not None for x in (route, manifest, verification, draft, registry)):
            errors.append('release context options apply only to gate_decision')
        return errors
    releasable = record['outcome'] in {'ready', 'conditional'}
    if releasable and record['workflow_level'] in {'full', 'extended'} and route is None:
        errors.append('full or extended release assessment requires --route; use --record-only for isolated checks')
    reviewed = {x['artefact_type']: x for x in record['artefacts_reviewed']}

    def require(name: str) -> None:
        item = reviewed.get(name, {})
        if releasable and (not item.get('required') or item.get('status') != 'present'
                          or item.get('stale') is not False or not item.get('version')):
            errors.append(f'required by release context but absent or stale: {name}')

    def dependency(obj: dict, kind: str) -> bool:
        problems = validate_record(obj)
        if problems:
            errors.extend(f'{kind}: {e}' for e in problems)
            return False
        if obj['artefact_type'] != kind:
            errors.append(f'expected {kind} dependency')
            return False
        if obj['assignment_id'] != record['assignment_id']:
            errors.append(f'{kind} belongs to another assignment')
        if record['input_versions'].get(kind) != obj['artefact_version']:
            errors.append(f'{kind} does not match input_versions')
        if reviewed.get(kind, {}).get('version') != obj['artefact_version']:
            errors.append(f'{kind} does not match reviewed version')
        if releasable and obj['status'] != 'complete':
            errors.append(f'{kind} is not complete')
        return True

    if route is not None and dependency(route, 'route_declaration'):
        if route['workflow_level'] != record['workflow_level']:
            errors.append('route workflow level differs from gate')
        for module in route['modules']:
            if module['expected_artefact'] != 'gate_decision':
                require(module['expected_artefact'])
            if releasable and module['expected_artefact'] == 'verification_record' and record['verification_status'] != 'complete':
                errors.append('route requires verification; gate must mark it complete')
        if route['approval']['required']:
            if not record['approval']['required']:
                errors.append('gate cannot disable approval required by route')
            if route['approval']['approver'] != record['approval']['approver']:
                errors.append('gate approver differs from route')
        if 'manifest' in route['input_versions'] and manifest is None:
            errors.append('route references a manifest; supply --manifest')
    if manifest is not None:
        schema = load_yaml(ROOT / 'skills/editorial-integrity-router/references/project-editorial-manifest.schema.yaml')
        manifest_errors = list(Draft202012Validator(schema).iter_errors(manifest))
        if manifest_errors:
            errors.extend(f'manifest: {e.message}' for e in manifest_errors)
        else:
            governance = manifest['governance']
            if governance['final_approval'] != 'not_required' and not record['approval']['required']:
                errors.append('gate cannot disable approval required by manifest')
            approver = governance.get('named_approver')
            if governance['final_approval'] != 'not_required' and approver and approver != record['approval']['approver']:
                errors.append('gate approver differs from manifest')
            require('project_manifest')
            if governance.get('change_log_required'):
                require('change_log')
            if governance.get('claim_traceability_required'):
                require('claim_registry')
    if releasable and record['verification_status'] == 'complete' and verification is None:
        errors.append('complete verification requires --verification; use --record-only for isolated checks')
    if verification is not None and dependency(verification, 'verification_record'):
        if verification['draft_version'] != record['draft_version']:
            errors.append('verification covers another draft version')
        if releasable and verification['overall_release_risk'] == 'blocked':
            errors.append('verification blocks release')
        if releasable and record['verification_status'] != 'complete':
            errors.append('supplied verification cannot be marked not_required')
    needs_coverage = releasable and record['verification_status'] == 'complete'
    if needs_coverage and (draft is None or registry is None):
        errors.append('complete verification requires --draft and --registry for claim coverage')
    draft_valid = draft is not None and dependency(draft, 'draft_output')
    registry_valid = registry is not None and dependency(registry, 'claim_registry')
    if draft_valid and draft['artefact_version'] != record['draft_version']:
        errors.append('supplied draft differs from release candidate')
    if draft_valid and registry_valid:
        claims = registry['claims']
        ids = [c['claim_id'] for c in claims]
        if len(set(ids)) != len(ids):
            errors.append('registry claim IDs must be unique')
        traced = {cid for trace in draft['source_trace'] for cid in trace['claim_ids']}
        by_id = {c['claim_id']: c for c in claims}
        if traced - set(by_id):
            errors.append('draft traces unknown registry claims')
        if releasable and not draft['integrity_summary']['claim_trace_complete']:
            errors.append('release draft requires complete claim trace')
        if verification is not None and not validate_record(verification):
            checked = {c['claim_id']: c for c in verification['claims']}
            for cid in traced & set(by_id):
                claim = by_id[cid]
                if claim['verification_required']:
                    result = checked.get(cid)
                    if result is None:
                        errors.append(f'claim {cid} missing from verification')
                    elif result['claim_text'] != claim['claim_text'] or result['claim_class'] != {'factual': 'simple_fact', 'interpretive': 'interpretation'}.get(claim['claim_class'], claim['claim_class']):
                        errors.append(f'claim {cid} differs between registry and verification')
                    elif releasable and result['status'] not in {'verified', 'author_judgement'}:
                        errors.append(f'claim {cid} remains unresolved in release draft')
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artefact', type=Path)
    parser.add_argument('--record-only', action='store_true', help='Schema and cross-field checks only; no release dependency checks')
    parser.add_argument('--route', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--verification', type=Path)
    parser.add_argument('--draft', type=Path)
    parser.add_argument('--registry', type=Path)
    args = parser.parse_args()
    if args.record_only and any((args.route, args.manifest, args.verification, args.draft, args.registry)):
        parser.error('--record-only cannot be combined with release dependencies')
    try:
        record = load_yaml(args.artefact)
        errors = validate_record(record)
        if not errors and not args.record_only:
            errors += validate_release_context(record, **{
                key: load_yaml(getattr(args, key)) if getattr(args, key) else None
                for key in ('route', 'manifest', 'verification', 'draft', 'registry')})
    except (ValueError, OSError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f'INVALID: {error}', file=sys.stderr)
        raise SystemExit(1)
    scope = 'record only' if args.record_only else 'record and supplied release context'
    print(f'PASS: {scope}. This does not authenticate approval, prove source truth or authorise publication.')


if __name__ == '__main__':
    main()
