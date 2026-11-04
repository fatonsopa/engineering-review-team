"""Preserved v3 corpus entry and current alignment registration preflight."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from review_contract import need
from prepare_review_case import validate_case

ROOT=Path(__file__).resolve().parents[1]


def preflight(host_config=None, final_config=None):
    cases=json.loads((ROOT/'evals/review_v3_cases.json').read_text())
    ids=[c['id'] for c in cases];need(len(ids)==len(set(ids)) and ids,'Unique registered cases required')
    behavior=[c for c in cases if c['kind']=='behavior']
    inputs=[validate_case(c) for c in behavior]
    config=host_config if host_config is not None else json.loads((ROOT/'config/host_validation.json').read_text())
    selected=[]
    for row in config['case_files']:
        need(row['path']=='evals/review_v3_cases.json','V3 host acceptance must select authoritative corpus')
        chosen=row.get('ids',[c['id'] for c in behavior]);need(set(chosen)<={c['id'] for c in behavior},'Unknown host case')
        selected+=chosen
    need(len(selected)==len(set(selected)) and set(selected)=={c['id'] for c in behavior},'Host matrix omits or duplicates intended cases')
    # Final mechanical checks must execute controls, not an evaluator awaiting
    # fresh AI observations or a separate semantic judgment. Legacy behavioral
    # cases remain frozen historical evidence; v3 owns current host acceptance.
    impact=final_config if final_config is not None else json.loads((ROOT/'config/test_impact.json').read_text())
    legacy=json.loads((ROOT/'evals/cases.json').read_text())
    commands={c['id']:['{python}',*c['command'][1:]] for c in [*legacy,*cases] if c['kind']=='command'}
    final=impact['final_checks']
    need(set(final)==set(commands)|{'v3-preflight','alignment-controls'},'Final checks must cover every legacy/v3 mechanical control, alignment controls and preflight; behavior is assessed separately')
    need(final['alignment-controls']['argv']==['{python}','scripts/check_review_alignment.py'],'Final alignment command differs')
    for identifier,argv in commands.items():
        configured=final[identifier]['argv']
        if identifier=='success' or identifier not in {c['id'] for c in legacy}:
            need(configured==argv,'Final control must execute its frozen command directly: '+identifier)
    need(final['v3-preflight']['argv']==['{python}','scripts/review_eval.py','--preflight'],'Final preflight command differs')
    roles=json.loads((ROOT/'config/roles.json').read_text())
    for role,row in roles['specialists'].items():
        need(row['recipient']=='lead' and not row['owns_final_response'] and not row['delegates'],'Leaf role contract conflicts')
        for key in ['reference','claude','codex']:need((ROOT/row[key]).is_file(),'Missing role resource')
        claude=(ROOT/row['claude']).read_text();need('\nskills:' not in claude,'Leaf must not preload lead entry')
    alignment=json.loads((ROOT/'evals/alignment_cases.json').read_text())
    need({c['id'] for c in alignment}=={'review-use','review-transfer'} and len(alignment)==2 and all(c['kind']=='behavior' for c in alignment),'Scoped alignment regression/transfer cases differ')
    for case in alignment:
        for f in case['fixtures']:
            path=(ROOT/f['path']).resolve()
            need(path.is_relative_to(ROOT) and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==f['sha256'],'Alignment fixture missing or changed')
    return {'passed':True,'mechanical_cases':len(cases)-len(behavior),'behavior_cases':len(behavior),'alignment_behavior_cases':len(alignment),'fixtures':inputs,'limits':'Registration and input checks only; actual host and semantic review remain required. Scoped v4 behavior does not establish the full default v3 host matrix.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--preflight',action='store_true');args,rest=p.parse_known_args()
    report=preflight()
    if args.preflight:print(json.dumps(report,indent=2));return 0
    need('--suite' not in rest and '--package' not in rest,'Package and corpus are fixed by this entry point')
    return subprocess.call([sys.executable,str(ROOT/'scripts/evaluate.py'),'--package',str(ROOT),'--suite',str(ROOT/'evals/review_v3_cases.json'),*rest])


if __name__=='__main__':raise SystemExit(main())
