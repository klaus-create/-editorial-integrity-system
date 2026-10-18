#!/usr/bin/env python3
"""Regression tests for the October review findings and live validation command."""
from __future__ import annotations
import copy
import json
import shutil
from validate_bundle import validate_bundle
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from contextlib import redirect_stderr
from io import StringIO

from package_skill import package
from validate_artefact import validate_record, validate_release_context
from validate_skill_suite import load_yaml

ROOT = Path(__file__).resolve().parents[1]


def example(skill: str, index: int = 0) -> dict:
    return copy.deepcopy(load_yaml(ROOT / 'skills' / skill / 'tests/cases.yaml')['cases'][index]['example_output'])


def include(gate: dict, name: str, version: str = '1.0') -> None:
    gate['input_versions'][name] = version
    gate['artefacts_reviewed'].append(dict(artefact_type=name, version=version,
        required=True, status='present', stale=False, reason='Required by the trusted context.'))


class ReleaseControls(unittest.TestCase):
    def setUp(self):
        self.gate = example('final-editorial-gate')
        self.route = example('editorial-integrity-router')
        self.route['input_versions'].pop('manifest')
        self.route['approval']['approver'] = self.gate['approval']['approver']
        self.verification = example('factual-verifier')
        self.verification['draft_version'] = self.gate['draft_version']
        self.draft = example('source-grounded-drafter')
        self.draft['artefact_version'] = self.gate['draft_version']
        self.registry = example('authorship-capture')['claim_registry']
        claim = self.registry['claims'][0]
        verified = self.verification['claims'][0]
        claim.update(claim_id=verified['claim_id'], claim_text=verified['claim_text'],
                     claim_class=verified['claim_class'], verification_required=True)
        self.registry['claims'] = [claim]
        self.draft['source_trace'][0]['claim_ids'] = [claim['claim_id']]
        self.draft['source_trace'] = self.draft['source_trace'][:1]
        for record in (self.draft, self.registry):
            record['assignment_id'] = self.gate['assignment_id']
        include(self.gate, 'claim_registry', self.registry['artefact_version'])

    def assertRejected(self, record, message):
        errors = validate_record(record)
        self.assertTrue(errors)
        self.assertIn(message, '\n'.join(errors))

    def context(self, **overrides):
        args = dict(route=self.route, verification=self.verification, draft=self.draft, registry=self.registry)
        args.update(overrides)
        return validate_release_context(self.gate, **args)

    def test_valid_ready_with_dependencies(self):
        self.assertEqual(validate_record(self.gate), [])
        self.assertEqual(self.context(), [])

    def test_required_approval_cannot_be_not_required(self):
        self.gate['approval'].update(status='not_required', approver=None)
        self.assertTrue(validate_record(self.gate))

    def test_approved_requires_identity(self):
        for value in (None, '', '   '):
            with self.subTest(value=value):
                self.gate['approval']['approver'] = value
                self.assertTrue(validate_record(self.gate))

    def test_pending_approval_cannot_be_ready(self):
        self.gate['approval']['status'] = 'pending'
        self.assertRejected(self.gate, 'approved')

    def test_empty_extended_inventory_rejected(self):
        self.gate.update(workflow_level='extended', artefacts_reviewed=[])
        self.assertTrue(validate_record(self.gate))

    def test_nonempty_inventory_still_requires_full_coverage(self):
        self.gate['artefacts_reviewed'] = self.gate['artefacts_reviewed'][:1]
        self.assertRejected(self.gate, 'mandatory current artefact missing')

    def test_extended_inventory_rejected_until_complete(self):
        self.gate['workflow_level'] = 'extended'
        self.assertTrue(validate_record(self.gate))
        for name in ('source_inventory','continuity_record','change_log','provenance_record'):
            include(self.gate, name)
        self.assertEqual(validate_record(self.gate), [])

    def test_conditional_with_blocker_rejected(self):
        gate = example('final-editorial-gate', 2)
        gate['blocking_issues'] = [dict(issue_id='B1', description='Critical false claim remains',
            owner='verifier', required_action='Remove or correct claim')]
        gate['check_results']['factual_integrity']['result'] = 'fail'
        self.assertTrue(validate_record(gate))

    def test_valid_disclosure_condition(self):
        self.assertEqual(validate_record(example('final-editorial-gate', 2)), [])

    def test_conditional_requires_approval(self):
        gate = example('final-editorial-gate', 2)
        gate['approval']['status'] = 'pending'
        self.assertTrue(validate_record(gate))

    def test_claim_free_private_gate_does_not_need_verification_or_approval(self):
        self.gate.update(workflow_level='lightweight', verification_status='not_required')
        self.gate['approval'] = dict(required=False, approver=None, status='not_required', waivers=[])
        self.gate['artefacts_reviewed'] = [x for x in self.gate['artefacts_reviewed'] if x['artefact_type']=='draft_output']
        self.gate['input_versions'] = {'draft_output':self.gate['draft_version']}
        self.assertEqual(validate_record(self.gate), [])
        self.assertEqual(validate_release_context(self.gate), [])

    def test_inventory_version_mismatch(self):
        self.gate['artefacts_reviewed'][0]['version'] = '99.0'
        self.assertRejected(self.gate, 'input_versions')

    def test_candidate_version_mismatch(self):
        self.gate['draft_version'] = '99.0'
        self.assertRejected(self.gate, 'release candidate')

    def test_missing_route_rejected_by_runtime(self):
        self.assertIn('--route', '\n'.join(self.context(route=None)))

    def test_missing_verification_rejected_by_runtime(self):
        self.assertIn('--verification', '\n'.join(self.context(verification=None)))

    def test_cross_assignment_dependency(self):
        self.route['assignment_id'] = 'OTHER'
        self.assertIn('another assignment', '\n'.join(self.context()))

    def test_stale_verification_dependency(self):
        self.verification['draft_version'] = '3.0'
        self.assertIn('another draft', '\n'.join(self.context()))

    def test_route_required_module_cannot_disappear(self):
        module = copy.deepcopy(self.route['modules'][0])
        module.update(name='editorial-brief-compiler', expected_artefact='editorial_brief', may_edit=False)
        self.route['modules'].insert(0, module)
        self.gate['artefacts_reviewed'] = [x for x in self.gate['artefacts_reviewed'] if x['artefact_type']!='editorial_brief']
        self.assertIn('editorial_brief', '\n'.join(self.context()))

    def test_route_verification_cannot_be_disabled(self):
        self.gate['verification_status'] = 'not_required'
        self.assertIn('route requires verification', '\n'.join(self.context(verification=None)))

    def test_route_approval_cannot_be_disabled(self):
        self.gate['approval'].update(required=False, status='not_required')
        self.assertIn('cannot disable approval', '\n'.join(self.context()))

    def test_referenced_manifest_required(self):
        self.route['input_versions']['manifest'] = '1.0'
        self.assertIn('--manifest', '\n'.join(self.context()))

    def test_manifest_enforces_approval_and_traceability(self):
        manifest = load_yaml(ROOT/'projects/social-marketer/project-editorial-manifest.yaml')
        self.gate['approval'].update(required=False, status='not_required')
        self.gate['artefacts_reviewed'] = [x for x in self.gate['artefacts_reviewed'] if x['artefact_type'] != 'claim_registry']
        errors = '\n'.join(self.context(manifest=manifest))
        self.assertIn('cannot disable approval required by manifest', errors)
        self.assertIn('claim_registry', errors)
        self.assertIn('project_manifest', errors)

    def test_valid_manifest_context(self):
        manifest = load_yaml(ROOT/'projects/social-marketer/project-editorial-manifest.yaml')
        self.route['input_versions']['manifest'] = '1.0'
        self.route['approval']['approver'] = manifest['governance']['named_approver']
        self.gate['approval']['approver'] = manifest['governance']['named_approver']
        include(self.gate, 'project_manifest')
        self.assertEqual(validate_record(self.gate), [])
        self.assertEqual(self.context(manifest=manifest), [])

    def test_critical_unresolved_claims_block(self):
        for status in ('unsupported', 'contradicted', 'unverifiable'):
            for risk in ('low', 'moderate', 'high'):
                with self.subTest(status=status, risk=risk):
                    record = copy.deepcopy(self.verification)
                    record['claims'][0].update(materiality='critical', status=status, correction='Proposed repair only')
                    record['overall_release_risk'] = risk
                    self.assertTrue(validate_record(record))

    def test_critical_blocked_assessment_is_valid(self):
        self.verification['claims'][0].update(materiality='critical', status='unsupported')
        self.verification['overall_release_risk'] = 'blocked'
        self.assertEqual(validate_record(self.verification), [])
        self.assertIn('verification blocks release', '\n'.join(self.context()))

    def test_removed_claim_and_owned_judgement_do_not_block(self):
        for status in ('removed', 'author_judgement'):
            record = copy.deepcopy(self.verification)
            record['claims'][0].update(materiality='critical',status=status,sources=[])
            self.assertEqual(validate_record(record), [])

    def test_current_claim_requires_current_dated_source(self):
        self.verification['claims'][0]['claim_class'] = 'current_status'
        self.verification['claims'][0]['sources'][0]['freshness'] = 'stale'
        self.assertRejected(self.verification, 'dated current source')
        self.verification['claims'][0]['sources'][0]['freshness'] = 'current'
        self.assertEqual(validate_record(self.verification), [])
        self.verification['claims'][0]['sources'][0]['accessed_on'] = None
        self.assertRejected(self.verification, 'dated current source')

    def test_historical_source_is_not_automatically_invalid(self):
        self.verification['claims'][0]['sources'][0]['freshness'] = 'stale'
        self.assertEqual(validate_record(self.verification), [])

    def test_empty_claim_set_is_not_automatically_invalid(self):
        self.verification['claims'] = []
        self.assertEqual(validate_record(self.verification), [])

    def test_single_high_risk_cannot_use_lightweight(self):
        for dimension in ('factual', 'consequence'):
            self.route['risk_dimensions'] = {k: 'low' for k in self.route['risk_dimensions']}
            self.route['risk_dimensions'][dimension] = 'high'
            self.route['workflow_level'] = 'lightweight'
            self.assertTrue(validate_record(self.route))

    def test_auditor_cannot_edit(self):
        module = self.route['modules'][0]
        module.update(name='anti-slop-auditor', expected_artefact='anti_slop_audit', may_edit=True)
        self.route['modules'] = [module]
        self.assertRejected(self.route, 'may not edit')

    def test_empty_verification_cannot_cover_declared_claim(self):
        self.verification['claims'] = []
        self.assertIn('missing from verification', '\n'.join(self.context()))

    def test_changed_claim_cannot_reuse_verification(self):
        self.registry['claims'][0]['claim_text'] = 'A different claim.'
        self.assertIn('differs between registry', '\n'.join(self.context()))

    def test_unknown_trace_claim_rejected(self):
        self.draft['source_trace'][0]['claim_ids'] = ['UNKNOWN']
        self.assertIn('unknown registry', '\n'.join(self.context()))

    def test_missing_coverage_inputs_rejected(self):
        self.assertIn('--draft and --registry', '\n'.join(self.context(draft=None, registry=None)))

    def test_bundle_example_and_content_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)/'example'
            shutil.copytree(ROOT/'examples/social-marketer', dest)
            bundle = dest/'bundle.json'
            self.assertEqual(validate_bundle(bundle), [])
            (dest/'draft.json').write_text('{}')
            self.assertIn('content hash mismatch', '\n'.join(validate_bundle(bundle)))

    def test_bundle_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            bundle = Path(temp)/'bundle.json'
            bundle.write_text(json.dumps({'bundle_version':'1.0', 'files':{
                'draft':{'path':'../outside.json','sha256':'0'*64}}}))
            self.assertIn('escapes bundle', '\n'.join(validate_bundle(bundle)))

    def test_malformed_record(self):
        for record in (None, [], {}, {'artefact_type':'unknown'}, {'artefact_type':[]}, {'artefact_type':'gate_decision'}):
            self.assertTrue(validate_record(record))

    def test_cli_reads_actual_records_and_rejects_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/'record.json'
            p.write_text(json.dumps(self.gate))
            command = [sys.executable, str(ROOT/'scripts/validate_artefact.py'), str(p)]
            result = subprocess.run(command+['--record-only'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('record only', result.stdout)
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            route = Path(temp)/'route.json'; route.write_text(json.dumps(self.route))
            verification = Path(temp)/'verification.json'; verification.write_text(json.dumps(self.verification))
            draft = Path(temp)/'draft.json'; draft.write_text(json.dumps(self.draft))
            registry = Path(temp)/'registry.json'; registry.write_text(json.dumps(self.registry))
            result = subprocess.run(command+['--route',str(route),'--verification',str(verification),'--draft',str(draft),'--registry',str(registry)],capture_output=True,text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            p.write_text('artefact_type: gate_decision\nartefact_type: draft_output\n')
            result = subprocess.run(command+['--record-only'],capture_output=True,text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('duplicate key', result.stderr)

    def test_multiple_packages_coexist_and_overwrite_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = [package(skill, Path(temp), validate_first=False)
                     for skill in sorted((ROOT/'skills').iterdir()) if skill.is_dir()]
            self.assertEqual(len(paths),10)
            self.assertEqual(len(set(paths)),10)
            for path in paths:
                with zipfile.ZipFile(path) as archive:
                    self.assertIn(f'{path.parent.name}/SKILL.md', archive.namelist())
            before = paths[0].read_bytes()
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                package(ROOT/'skills'/paths[0].parent.name,Path(temp),validate_first=False)
            self.assertEqual(paths[0].read_bytes(),before)


if __name__ == '__main__':
    unittest.main()
