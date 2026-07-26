#!/usr/bin/env python3
"""Run and verify the deterministic repository acceptance report."""
from __future__ import annotations
import argparse, json, subprocess, sys, tempfile, time
from pathlib import Path
from typing import Any
import yaml
from validate_packages import validate_packages

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'governance' / 'AUDIT-ACCEPTANCE-0.1.4.yaml'
EXPECTED_SKILLS = {
 'anti-slop-auditor','argument-structure-reviewer','authorship-capture',
 'editorial-brief-compiler','editorial-integrity-router','factual-verifier',
 'final-editorial-gate','source-grounded-drafter','voice-preserving-editor',
 'voice-profile-builder',
}

def run(script: str, *args: str) -> tuple[bool,str]:
    started=time.monotonic()
    print(f'[audit] running {script}', file=sys.stderr, flush=True)
    with tempfile.TemporaryFile(mode='w+t', encoding='utf-8') as out:
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/script),*args],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT,text=True)
        out.seek(0); evidence=out.read().strip()
    print(f"[audit] {'passed' if result.returncode==0 else 'failed'} {script} in {time.monotonic()-started:.1f}s",file=sys.stderr,flush=True)
    return result.returncode==0,evidence

def build() -> dict[str,Any]:
    checks=[]
    def add(check_id: str, passed: bool, evidence: str): checks.append({'check_id':check_id,'passed':bool(passed),'evidence':evidence})
    for script in ('validate_skill_suite.py','run_contract_tests.py','check_repository_links.py'):
        ok,evidence=run(script); add(script,ok,evidence)
    manifests={}; manifests_ok=True
    for path in sorted((ROOT/'projects').glob('*/project-editorial-manifest.yaml')):
        ok,evidence=run('validate_manifest.py',str(path)); manifests_ok &= ok; manifests[path.parent.name]=evidence
    add('project-manifest-validation',manifests_ok and len(manifests)==3,json.dumps(manifests,sort_keys=True))
    try:
        package_evidence=validate_packages(prevalidated=True); packages_ok=True
    except BaseException as exc:
        package_evidence=f'{type(exc).__name__}: {exc}'; packages_ok=False
    add('extracted-package-validation',packages_ok,package_evidence)
    readme=(ROOT/'README.md').read_text(encoding='utf-8')
    roadmap=(ROOT/'ROADMAP.md').read_text(encoding='utf-8')
    release=(ROOT/'governance'/'RELEASE-0.1.4.md').read_text(encoding='utf-8')
    active='\n'.join((readme,roadmap,release))
    add('released-state-language','v0.1.4-post-merge-hardening' in readme and 'v0.1.4-post-merge-hardening' in roadmap and not any(p in active for p in ('Current release candidate','Release candidate:','only after the corrective pull request passes and is merged')),'Active release documentation identifies 0.1.4 without stale pre-merge language.')
    requirements={line.strip() for line in (ROOT/'requirements-validation.txt').read_text().splitlines() if line.strip() and not line.startswith('#')}
    add('validation-dependency-pins',requirements=={'PyYAML==6.0.3','jsonschema==4.26.0'},f'requirements={sorted(requirements)}')
    workflow=(ROOT/'.github/workflows/validate.yml').read_text(encoding='utf-8')
    add('ci-hardening',all(token in workflow for token in ('workflow_dispatch:','contents: read','cancel-in-progress: true','requirements-validation.txt','audit_repository.py')),'CI uses pinned dependencies, least privilege, concurrency control and one acceptance orchestrator.')
    skills={p.name for p in (ROOT/'skills').iterdir() if p.is_dir()}
    add('skill-inventory',skills==EXPECTED_SKILLS,f'skills={sorted(skills)}')
    versions={}
    for path in sorted((ROOT/'projects').glob('*/project-editorial-manifest.yaml')):
        data=yaml.safe_load(path.read_text(encoding='utf-8')); versions[path.parent.name]=data.get('editorial_system',{}).get('required_version')
    add('project-version-alignment',set(versions.values())=={'0.1.4'},json.dumps(versions,sort_keys=True))
    failed=[c for c in checks if not c['passed']]
    return {'audit_version':'1.4','release':'0.1.4','checks':checks,'summary':{'passed':len(checks)-len(failed),'failed':len(failed)},'deterministic_result':'pass' if not failed else 'fail','performance_evidence':'not_assessed_by_this_audit'}

def render(report): return yaml.safe_dump(report,sort_keys=False,allow_unicode=True)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true'); args=parser.parse_args()
    report=build(); output=render(report); print(output,end='')
    if args.write: REPORT.write_text(output,encoding='utf-8')
    elif not REPORT.is_file() or REPORT.read_text(encoding='utf-8')!=output:
        print('ERROR: tracked audit report is stale; run python scripts/audit_repository.py --write after review.',file=sys.stderr); raise SystemExit(1)
    if report['deterministic_result']!='pass': raise SystemExit(1)
if __name__=='__main__': main()
