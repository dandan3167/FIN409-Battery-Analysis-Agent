"""English deterministic companion: prepare/show/validate/finalize, no model call.
Analysis and English report prose must be authored by the live Codex session.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,csv,hashlib,json,re,shutil,sys
from deterministic import calculate,measurements,section_counts,length_checks
ROOT=Path(__file__).resolve().parents[2]
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def safe(rel):
 p=(ROOT/rel).resolve()
 if ROOT.resolve() not in p.parents and p!=ROOT.resolve():raise ValueError('Path escapes workspace')
 return p
def runpath(runid):
 if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}',runid):raise ValueError('Invalid run ID')
 return ROOT/'runs_en'/runid
def log(run,event,**fields):
 with (run/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'time_utc':datetime.now(timezone.utc).isoformat(),'event':event,**fields},ensure_ascii=False)+'\n')
def facts(run):return [json.loads(x) for x in (run/'inputs/facts.jsonl').read_text(encoding='utf-8').splitlines() if x]
def verify_sources(manifest):
 for x in manifest['source_assets']:
  assert sha(safe(x['path']))==x['sha256'],'Packaged original source changed: '+x['path']
def prepare(args):
 cfg=read(safe(args.config));assert cfg['output_language']=='en' and cfg['output_directory']=='runs_en'
 assert cfg['framework']=="Porter's Five Forces only"
 run=runpath(args.run_id)
 if run.exists():raise ValueError('Run already exists; use a new ID')
 pack=safe(cfg['evidence_directory']);manifest=read(pack/'manifest.json')
 assert sha(pack/'facts.jsonl')==manifest['facts_sha256'],'Evidence version changed'
 assert sha(pack/manifest['package_notes_file'])==manifest['package_notes_sha256']
 verify_sources(manifest)
 fs=[json.loads(x) for x in (pack/'facts.jsonl').read_text(encoding='utf-8').splitlines()]
 assert len(fs)==manifest['fact_count'] and len({x['id'] for x in fs})==len(fs)
 run.mkdir(parents=True);(run/'inputs').mkdir();(run/'outputs').mkdir();(run/'runtime').mkdir()
 dump(run/'inputs/config.json',cfg);dump(run/'inputs/source_manifest.json',manifest)
 shutil.copyfile(pack/'facts.jsonl',run/'inputs/facts.jsonl')
 for name,key in [('master_prompt.md','master_prompt'),('method.md','method_file'),('output_contract.json','output_contract'),('execution_instructions.md','execution_instructions')]:shutil.copyfile(safe(cfg[key]),run/'inputs'/name)
 shutil.copyfile(ROOT/'workflow/en/INPUT_FILES_EN.json',run/'inputs/formal_input_list.json')
 shutil.copyfile(pack/'README_EN.md',run/'inputs/evidence_readme.md')
 snap=[{'file':p.name,'sha256':sha(p)} for p in sorted((run/'inputs').iterdir())]
 digest=hashlib.sha256(json.dumps(snap,sort_keys=True).encode()).hexdigest()
 dump(run/'input_manifest.json',{'input_digest':digest,'files':snap,'history_files_in_snapshot':[],'evidence_record_count':len(fs)})
 for name in ['run_en.py','deterministic.py']:shutil.copyfile(ROOT/'workflow/en'/name,run/'runtime'/name)
 dump(run/'runtime_manifest.json',{'captured_at':'prepare','python_executable':sys.executable,'python_version':sys.version,'files':[{'file':'runtime/'+p.name,'sha256':sha(p)} for p in sorted((run/'runtime').iterdir())]})
 calcs=calculate(fs);assert all(x['check_pass'] for x in calcs);dump(run/'calculations.json',calcs)
 lines=['# Active curated evidence (original-language facts; no prescribed judgments)','']
 for f in fs:lines.append('- '+f['id']+' | '+f['title']+' | '+f['period']+' | '+f['evidence_type'])
 (run/'evidence_digest.md').write_text('\n'.join(lines),encoding='utf-8')
 dump(run/'state.json',{'state':'AWAITING_MODEL','run_id':args.run_id,'input_digest':digest,'requires_live_model_analysis':True,'python_performed_analysis':False})
 log(run,'prepared',facts=len(fs),input_digest=digest,model_analysis_performed=False)
 print(json.dumps({'run_id':args.run_id,'state':'AWAITING_MODEL','facts':len(fs),'input_digest':digest,'english_report_generated':False,'next':'Live Codex must read evidence and write analysis/report/claims/appendices/semantic review.'}))
def show(args):
 run=runpath(args.run_id);fs=facts(run);selected=fs if args.all else [f for f in fs if f['id'] in set(args.ids or [])]
 if not args.all:assert {f['id'] for f in selected}==set(args.ids or []),'Unknown evidence ID'
 log(run,'facts_shown_to_model',ids=[f['id'] for f in selected])
 for f in selected:print(json.dumps(f,ensure_ascii=False))
def validate(args,strict_targets=False):
 run=runpath(args.run_id);cfg=read(run/'inputs/config.json');im=read(run/'input_manifest.json');errors=[];warnings=[]
 if read(run/'state.json')['state']=='FINALIZED':
  for x in read(run/'output_manifest.json'):assert sha(run/x['file'])==x['sha256'],'Sealed output changed; create a new run'
 for x in im['files']:
  if sha(run/'inputs'/x['file'])!=x['sha256']:errors.append('Input snapshot changed: '+x['file'])
 for x in read(run/'runtime_manifest.json')['files']:
  if sha(run/x['file'])!=x['sha256']:errors.append('Captured implementation changed: '+x['file'])
 # Do not silently validate with an implementation different from the captured version.
 for name in ['run_en.py','deterministic.py']:
  if sha(ROOT/'workflow/en'/name)!=sha(run/'runtime'/name):errors.append('Current implementation differs from run snapshot: '+name)
 verify_sources(read(run/'inputs/source_manifest.json'))
 contract=read(run/'inputs/output_contract.json');out=run/'outputs'
 missing=[n for n in contract['required_outputs'] if not (out/n).is_file()]
 errors.extend('Live-model output missing: '+n for n in missing)
 if missing:
  result={'mechanical_checks':'failed','errors':errors,'warnings':warnings,'model_analysis_verified':False,'notice':'Preparation is not a model run.'};dump(run/'validation.json',result);log(run,'validation',result='failed',errors=errors);print(json.dumps(result));return False
 fs={f['id']:f for f in facts(run)};a=read(out/'analysis.json');claims=read(out/'claims.json');review=read(out/'semantic_review.json');report=(out/'report_en.md').read_text(encoding='utf-8')
 for k in contract['analysis_required_fields']:
  if k not in a:errors.append('Missing analysis field: '+k)
 if a.get('run_id')!=args.run_id or a.get('input_digest')!=im['input_digest']:errors.append('Analysis must identify this active snapshot')
 if a.get('reasoning_origin')!='live_codex_session':errors.append('Live model analysis origin required')
 used=set()
 def refs(ids,where):
  if not isinstance(ids,list):errors.append('Invalid evidence ID list: '+where);return
  used.update(ids)
  for eid in ids:
   if eid not in fs:errors.append('Unknown/inactive evidence '+str(eid)+' in '+where)
 def walk(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k=='evidence_ids':refs(v,'structured output')
    else:walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(a)
 ff=a.get('five_forces',[])
 if len(ff)!=5 or {f.get('id') for f in ff}!=set(contract['force_ids']):errors.append('Exactly five unique force analyses required')
 for f in ff:
  for k in contract['force_required_fields']:
   if k not in f or not f[k]:errors.append('Missing force field '+str(f.get('id'))+':'+k)
  if f.get('rating') not in contract['rating_values']:errors.append('Rating must use permitted English labels')
  for role in ['support','counterweights']:
   if not isinstance(f.get(role),list):errors.append('Expected reasoning list: '+role);continue
   for x in f[role]:
    if not x.get('reason') or not x.get('evidence_ids'):errors.append('Each mechanism needs reasoning and evidence')
 for k in ['industry_attractiveness','catl_position','overlap_review']:
  if not a.get(k):errors.append('Empty synthesis/review: '+k)
 ids=[c.get('claim_id') for c in claims]
 if len(ids)!=len(set(ids)):errors.append('Duplicate claim IDs')
 metric_count=0
 for c in claims:
  for k in contract['claim_required_fields']:
   if k not in c:errors.append('Missing claim field '+k)
  if not re.fullmatch(r'C\d{3,}',str(c.get('claim_id',''))):errors.append('Invalid claim ID')
  if c.get('kind') not in contract['claim_kinds']:errors.append('Invalid claim type')
  refs(c.get('evidence_ids',[]),'claim '+str(c.get('claim_id')))
  if not c.get('evidence_ids'):errors.append('Unmapped key claim')
  for metric in c.get('reported_metrics',[]):
   try:
    v=measurements(fs[metric['evidence_id']])[metric['name']]['value']
    if v!=metric['value']:errors.append('Declared metric does not match original type/value: '+str(metric))
    metric_count+=1
   except KeyError:errors.append('Unknown declared measurement')
 if metric_count==0:warnings.append('No key numerical values declared for automatic verification; add reported_metrics where used')
 cites=set(re.findall(r'\[(C\d{3,})\]',report))
 if not cites or cites-set(ids):errors.append('Missing/unknown body citations')
 counts,structure_errors=section_counts(report);errors+=structure_errors
 le,lw=length_checks(counts,cfg,strict_targets);errors+=le;warnings+=lw
 checks=review.get('checks',[])
 if review.get('reviewer')!='current_codex_session' or len(checks)<8:errors.append('Live model semantic self-review incomplete')
 for x in checks:
  if x.get('result') not in contract['semantic_check_results'] or x.get('result')=='fail':errors.append('Unresolved/invalid semantic check result')
  if not x.get('explanation'):errors.append('Semantic review explanation missing')
 if not (out/'appendices_en.md').read_text(encoding='utf-8').strip():errors.append('Methods/prompt/tool appendix must not be empty')
 if read(run/'calculations.json')!=calculate(list(fs.values())):errors.append('Calculations changed or differ from recomputation')
 seen=set()
 for line in (run/'events.jsonl').read_text(encoding='utf-8').splitlines():
  event=json.loads(line)
  if event['event']=='facts_shown_to_model':seen.update(event['ids'])
 if used-seen:warnings.append('Cited facts not logged via show; verify actual inspection: '+','.join(sorted(used-seen)))
 mapping=[{**c,'source_locators':[{'evidence_id':i,'sources':fs[i]['sources'],'period':fs[i]['period'],'geography':fs[i]['geography'],'unit':fs[i]['unit'],'business_scope':fs[i]['business_scope'],'evidence_type':fs[i]['evidence_type'],'limitations':fs[i]['limitations']} for i in c.get('evidence_ids',[]) if i in fs]} for c in claims]
 dump(out/'claim_source_map.json',mapping)
 with (out/'claim_source_map.csv').open('w',encoding='utf-8-sig',newline='') as stream:
  fields=list(dict.fromkeys(k for c in mapping for k in c));w=csv.DictWriter(stream,fieldnames=fields);w.writeheader()
  for c in mapping:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in c.items()})
 dump(out/'word_counts.json',{'counts':counts,'targets':cfg['report_length'],'target_compliance_required_to_finalize':True,'count_basis':cfg['report_length']['count_basis']})
 (out/'word_counts.md').write_text('# English report word counts\n\n|Section|Words|\n|---|---:|\n'+'\n'.join('|'+k+'|'+str(v)+'|' for k,v in counts.items())+'\n\n'+cfg['report_length']['count_basis']+'\n',encoding='utf-8')
 result={'mechanical_checks':'failed' if errors else 'passed','errors':errors,'warnings':warnings,'word_counts':counts,'declared_metrics_checked':metric_count,'calculation_records_checked':len(read(run/'calculations.json')),'same_session_semantic_review':True,'semantic_correctness_proven_by_python':False,'independent_model_execution_verified':False,'strict_targets':strict_targets}
 dump(run/'validation.json',result);log(run,'validation',result=result['mechanical_checks'],errors=errors,warnings=warnings);print(json.dumps(result));return not errors
def finalize(args):
 run=runpath(args.run_id);assert read(run/'state.json')['state']!='FINALIZED','Already sealed'
 if not validate(args,strict_targets=True):raise ValueError('Cannot seal: checks or requested targets failed')
 dump(run/'output_manifest.json',[{'file':str(p.relative_to(run)).replace('\\','/'),'sha256':sha(p)} for p in sorted((run/'outputs').iterdir()) if p.is_file()])
 dump(run/'state.json',{'state':'FINALIZED','run_id':args.run_id,'input_digest':read(run/'input_manifest.json')['input_digest'],'purpose':'English acceptance research draft, not final submission','independent_semantic_review':False})
 log(run,'finalized');print('FINALIZED: model-authored draft plus deterministic checks; no independent semantic guarantee.')
def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 x=sub.add_parser('prepare');x.add_argument('--config',default='workflow/en/task_en.json');x.add_argument('--run-id',required=True)
 x=sub.add_parser('show');x.add_argument('--run-id',required=True);x.add_argument('--ids',nargs='*');x.add_argument('--all',action='store_true')
 for name in ['validate','finalize']:sub.add_parser(name).add_argument('--run-id',required=True)
 args=p.parse_args()
 if args.command=='prepare':prepare(args)
 elif args.command=='show':show(args)
 elif args.command=='validate':sys.exit(0 if validate(args) else 2)
 else:finalize(args)
if __name__=='__main__':
 try:main()
 except (ValueError,AssertionError,KeyError) as e:print('ERROR: '+str(e),file=sys.stderr);sys.exit(2)
