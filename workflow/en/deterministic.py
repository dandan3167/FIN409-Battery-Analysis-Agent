"""Deterministic arithmetic and English word counting; no analytical conclusions."""
from decimal import Decimal as D
import re
def number(x):return D(str(x).replace(',','').replace('%','').replace('＋','+').replace('−','-'))
def measurements(f):return {m['name']:m for m in f['measurements']}
def calculate(fs):
 by={f['id']:f for f in fs};out=[]
 for f in fs:
  if f['id'].startswith('FIN-'):
   m=measurements(f);r=number(m['revenue_original']['value']);c=number(m['cost_original']['value'])
   mult={'元':D(1),'万元':D(10000),'千元':D(1000)}[m['revenue_original']['unit']]
   margin=(r-c)/r*100;delta=margin-number(m['margin_disclosed']['value'])
   out.append({'id':'CAL-'+f['id'],'evidence_ids':[f['id']],'values':{'revenue_yi':str(r*mult/D(10**8)),'cost_yi':str(c*mult/D(10**8)),'gross_profit_yi':str((r-c)*mult/D(10**8)),'margin_recomputed_percent':str(margin),'margin_rounding_delta_pp':str(delta)},'formula':'original amount * unit multiplier / 1e8; (revenue-cost)/revenue*100','check_pass':abs(delta)<=D('.01'),'limitations':'RMB 100 million (yi) conversion; this row only. Do not splice original 2023 costs into restated 2024 comparisons.'})
 for year in [2023,2024,2025]:
  ranks=sorted([f for f in fs if f['id'].startswith(f'RANK-{year}-')],key=lambda f:int(measurements(f)['rank']['value']))
  total=by.get(f'IND-{year}');prev=by.get(f'IND-{year-1}')
  if len(ranks)==15:
   vals={f'CR{k}_reported_share_sum_percent':str(sum(number(measurements(f)['share_reported']['value']) for f in ranks[:k])) for k in [2,3,5]}
   vals['leader_gap_second_pp']=str(number(measurements(ranks[0])['share_reported']['value'])-number(measurements(ranks[1])['share_reported']['value']))
   out.append({'id':f'CAL-RANK-{year}','evidence_ids':[f['id'] for f in ranks],'values':vals,'formula':'Sum ranking-disclosed shares; first share minus second share','check_pass':True,'limitations':'Within-year source boundaries. Cross-year scopes may differ. Do not infer force intensity from concentration alone.'})
   if total:
    denom=number(measurements(total)['total_gwh']['value'])
    rows=[{'evidence_id':f['id'],'share_disclosed_percent':measurements(f)['share_reported']['value'],'share_recomputed_percent':str(number(measurements(f)['volume_gwh']['value'])/denom*100)} for f in ranks]
    out.append({'id':f'CAL-SHARE-{year}','evidence_ids':[total['id']]+[f['id'] for f in ranks],'values':rows,'formula':'Company GWh / industry total GWh * 100','check_pass':True,'limitations':'Keep disclosed and recomputed shares separate. Differences are not assumed to be rounding only.'})
  if total and prev:
   growth=(number(measurements(total)['total_gwh']['value'])/number(measurements(prev)['total_gwh']['value'])-1)*100
   out.append({'id':f'CAL-GROWTH-{year}','evidence_ids':[prev['id'],total['id']],'values':{'growth_percent':str(growth)},'formula':'(current total / preceding total - 1) * 100','check_pass':True,'limitations':'China annual installations only; no automatic inference that growth reduces rivalry.'})
  keys=[f'VEH-{year}-{kind}_total' for kind in ['bev','phev','fcev']];nt=by.get(f'VEH-{year}-nev_total')
  if nt and all(k in by and by[k]['evidence_type']!='missing' for k in keys):
   delta=sum(number(by[k]['measurements'][0]['value']) for k in keys)-number(nt['measurements'][0]['value'])
   out.append({'id':f'CAL-VEH-{year}','evidence_ids':keys+[nt['id']],'values':{'type_sum_minus_total_wan':str(delta)},'formula':'BEV + PHEV + FCEV - NEV total','check_pass':abs(delta)<=D('.2'),'limitations':'Original units: ten thousand vehicles. Retain original rounding residuals; includes exports, not consumer retail shares.'})
 return out

SECTIONS=['INTRO','RIV','BUY','SUP','ENT','SUB','CONCLUSION']
def plain_counted_text(text):
 text=re.sub(r'<!--.*?-->',' ',text,flags=re.S)
 text=re.sub(r'\[C\d{3,}\]',' ',text)
 text=re.sub(r'!?(\[[^\]]*\])\([^)]*\)',lambda m:m[1][1:-1],text)
 text=re.sub(r'https?://\S+',' ',text)
 # Keep apostrophes, hyphenated compounds, thousands/decimals, and numerical ratios.
 return text
def count_words(text):
 text=plain_counted_text(text)
 return len(re.findall(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*(?:[-‐‑][A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*)*(?:[.,:/][0-9]+)*",text))
def section_counts(report):
 errors=[];bodies=re.findall(r'<!-- REPORT_BODY_START -->(.*?)<!-- REPORT_BODY_END -->',report,re.S)
 if len(bodies)!=1:return {},['Exactly one marked report body is required']
 body=bodies[0];counts={};spans=[]
 for name in SECTIONS:
  pat=rf'<!-- SECTION:{name}:START -->(.*?)<!-- SECTION:{name}:END -->'
  matches=list(re.finditer(pat,body,re.S))
  if len(matches)!=1:errors.append('Exactly one section required: '+name);continue
  m=matches[0];counts[name]=count_words(m[1]);spans.append((m.start(),m.end(),name))
 if len(spans)==7:
  ordered=sorted(spans)
  if [x[2] for x in ordered]!=SECTIONS:errors.append('Sections must follow configured order')
  if any(a[1]>b[0] for a,b in zip(ordered,ordered[1:])):errors.append('Nested/overlapping body sections')
  remainder=body
  for a,b,n in reversed(ordered):remainder=remainder[:a]+remainder[b:]
  if re.sub(r'<!--.*?-->','',remainder,flags=re.S).strip():errors.append('Uncounted text outside the seven sections')
 counts['FIVE_FORCES_TOTAL']=sum(counts.get(k,0) for k in ['RIV','BUY','SUP','ENT','SUB'])
 counts['BODY_TOTAL']=sum(counts.get(k,0) for k in SECTIONS)
 if re.search(r'[\u3400-\u9fff]',body):errors.append('Chinese characters in English report body; move original quotations to source appendix')
 outside=re.sub(r'<!-- REPORT_BODY_START -->.*?<!-- REPORT_BODY_END -->','',report,flags=re.S)
 # Outside body, allow only one title; references/methods belong in appendices_en.md.
 outside_lines=[s for s in outside.splitlines() if s.strip()]
 if any(not s.startswith('# ') for s in outside_lines) or len(outside_lines)>1:errors.append('Only a document title may be outside the counted body; use appendices_en.md')
 return counts,errors
def length_checks(counts,cfg,strict_targets=False):
 errors=[];warnings=[];r=cfg['report_length'];n=counts.get('BODY_TOTAL',0)
 if n>r['hard_maximum']:errors.append('Body exceeds absolute maximum')
 if counts.get('FIVE_FORCES_TOTAL',0)>r['five_forces_maximum']:errors.append('Five-force subtotal exceeds maximum')
 targets=[('BODY_TOTAL',r['target_minimum'],r['target_maximum']),('INTRO',r['introduction_target_minimum'],r['introduction_target_maximum']),('CONCLUSION',r['conclusion_target_minimum'],r['conclusion_target_maximum'])]
 for key,lo,hi in targets:
  if not lo<=counts.get(key,0)<=hi:
   (errors if strict_targets else warnings).append(f'{key} outside requested target {lo}-{hi}: {counts.get(key,0)}')
 return errors,warnings
