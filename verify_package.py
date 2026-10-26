"""Verify a portable package; optional smoke test prepares inputs, never model prose."""
from pathlib import Path
import argparse, ast, hashlib, importlib.util, json, os, re, subprocess, sys

ROOT = Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def local(rel):
    p = (ROOT / rel).resolve()
    if not p.is_relative_to(ROOT): raise ValueError('Path escapes package: ' + rel)
    if not p.is_file(): raise FileNotFoundError(rel)
    return p

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-smoke', action='store_true')
    parser.add_argument('--run-id', default='package_smoke_test')
    args=parser.parse_args()
    cfg=read(local('workflow/en/task_en.json'))
    formal=read(local('workflow/en/INPUT_FILES_EN.json'))
    for rel in formal['formal_instructions']+formal['formal_evidence']+[formal['entry_point']]+formal['deterministic_tools']: local(rel)
    for key in ['master_prompt','method_file','execution_instructions','output_contract']: local(cfg[key])
    if cfg['evidence_directory']!='evidence/english/v001' or cfg['output_directory']!='runs_en': raise ValueError('Unexpected configured paths')
    manifest=read(local(cfg['evidence_directory']+'/manifest.json'))
    facts_path=local(cfg['evidence_directory']+'/facts.jsonl')
    if digest(facts_path)!=manifest['facts_sha256']: raise ValueError('Fact hash mismatch')
    if digest(local(cfg['evidence_directory']+'/'+manifest['package_notes_file']))!=manifest['package_notes_sha256']: raise ValueError('Evidence notes changed')
    assets={a['path']:a for a in manifest['source_assets']}
    for rel,a in assets.items():
        if digest(local(rel))!=a['sha256']: raise ValueError('Source hash mismatch: '+rel)
    facts=[json.loads(s) for s in facts_path.read_text(encoding='utf-8').splitlines()]
    if len(facts)!=manifest['fact_count'] or len({f['id'] for f in facts})!=len(facts): raise ValueError('Fact count/ID mismatch')
    source_refs=0
    for f in facts:
        for s in f['sources']:
            for key in ['source_file','text_file','screenshot']:
                if s.get(key):
                    local(s[key]); source_refs+=1
                    if s[key] not in assets: raise ValueError('Unmanifested active source reference')
            if s.get('source_sha256') and digest(local(s['source_file']))!=s['source_sha256']: raise ValueError('Record source hash mismatch')
    if 'examples/' in json.dumps(formal)+json.dumps(cfg): raise ValueError('Example in formal input configuration')
    # Compile without writing cache files, and import the actual deterministic dependencies.
    sys.dont_write_bytecode=True
    sys.path.insert(0,str(ROOT/'workflow/en'))
    for rel in ['workflow/en/run_en.py','workflow/en/deterministic.py']:
        text=local(rel).read_text(encoding='utf-8'); tree=ast.parse(text); compile(tree,rel,'exec')
        for node in ast.walk(tree):
            names=[a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else []
            for name in names:
                if name!='deterministic' and name not in sys.stdlib_module_names: raise ValueError('Unexpected non-standard-library import: '+name)
    spec=importlib.util.spec_from_file_location('package_runtime',local('workflow/en/run_en.py'))
    runtime=importlib.util.module_from_spec(spec); spec.loader.exec_module(runtime)
    calculations=runtime.calculate(facts)
    if not all(c['check_pass'] for c in calculations): raise ValueError('Arithmetic failure')
    example=read(local('examples/completed_english_report/claim_source_map.json'))
    known={f['id'] for f in facts}; mapped={c['claim_id'] for c in example}
    report=local('examples/completed_english_report/report_en.md').read_text(encoding='utf-8')
    if set(re.findall(r'\[(C\d{3,})\]',report))!=mapped: raise ValueError('Example citation mismatch')
    for c in example:
        if not set(c['evidence_ids'])<=known: raise ValueError('Example inactive evidence')
        for locator in c['source_locators']:
            for s in locator['sources']:
                for key in ['source_file','text_file','screenshot']:
                    if s.get(key): local(s[key])
    result={'status':'passed','python_version':sys.version.split()[0],'stdlib_dependencies_only':True,'formal_paths':'passed','fact_records':len(facts),'source_assets':len(assets),'active_source_references_checked':source_refs,'source_sha256':'all passed','calculation_records':len(calculations),'example_claims':len(mapped),'examples_in_formal_inputs':False,'fresh_model_analysis_performed':False,'missing_assets':[]}
    if args.prepare_smoke:
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',args.run_id): raise ValueError('Unsafe run ID')
        run=ROOT/'runs_en'/args.run_id
        if run.exists(): raise ValueError('Smoke ID already exists; use a new ID')
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8'}
        def call(*parts):
            p=subprocess.run([sys.executable,'-B','workflow/en/run_en.py',*parts],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8')
            return p
        prepared=call('prepare','--config','workflow/en/task_en.json','--run-id',args.run_id)
        if prepared.returncode: raise RuntimeError(prepared.stderr)
        state=read(run/'state.json')
        if state['state']!='AWAITING_MODEL' or list((run/'outputs').iterdir()): raise ValueError('Preparation generated analytical output')
        im=read(run/'input_manifest.json')
        for x in im['files']:
            if digest(run/'inputs'/x['file'])!=x['sha256']: raise ValueError('Snapshot mismatch')
        if im['history_files_in_snapshot'] or read(run/'calculations.json')!=calculations: raise ValueError('Snapshot isolation/calculation mismatch')
        shown=call('show','--run-id',args.run_id,'--ids','IND-2025')
        if shown.returncode or json.loads(shown.stdout)['id']!='IND-2025': raise ValueError('Show failed')
        invalid=call('validate','--run-id',args.run_id)
        validation=read(run/'validation.json')
        if invalid.returncode!=2 or len(validation['errors'])!=5 or not all(e.startswith('Live-model output missing: ') for e in validation['errors']): raise ValueError('Missing model-output guard failed')
        refused=call('finalize','--run-id',args.run_id)
        if refused.returncode!=2 or (run/'output_manifest.json').exists() or read(run/'state.json')['state']!='AWAITING_MODEL': raise ValueError('Premature finalisation guard failed')
        result['smoke_test']={'run_id':args.run_id,'prepare':'passed','show':'passed','snapshot_integrity':'passed','validate_without_model_outputs':'expected refusal: five missing outputs','finalize_without_model_outputs':'expected refusal; no seal created','state':'AWAITING_MODEL','model_report_generated':False}
    delivery=ROOT/'package_manifest.json'
    if delivery.exists():
        for item in read(delivery)['files']:
            if digest(local(item['path']))!=item['sha256']: raise ValueError('Delivery file hash mismatch: '+item['path'])
        result['delivery_manifest']='passed'
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
