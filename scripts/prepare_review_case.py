"""Validate and materialize performing inputs without grading answers."""
import argparse
import json
from pathlib import Path
import shutil

from review_manifest import relative, digest
from review_contract import need

ROOT=Path(__file__).resolve().parents[1]


def validate_case(case):
    need(case.get('kind')=='behavior' and isinstance(case.get('request'),dict),'Behavioral request required')
    request=case['request'];files=request.get('source')
    need(isinstance(files,dict) and files,'Complete source fixtures required')
    need(isinstance(request.get('instruction'),str) and request['instruction'].strip(),'Performing instruction required')
    for name,value in files.items():
        relative(name);need(name not in {'.',''} and isinstance(value,str),'Source fixture must be named UTF-8 text')
        need(not name.startswith(('.agents/','.claude/','.codex/')),'Task inputs cannot configure the host')
    for name in case.get('resources',[]):
        relative(name);need(not name.startswith(('evals/','tests/')),'Grader/development files cannot be performing resources')
        need((ROOT/name).is_file(),'Missing performing resource: '+name)
    return {'case_id':case['id'],'case_sha256':digest(case),'inputs':{n:digest(v.encode()) for n,v in files.items()}}


def stage(case,destination):
    manifest=validate_case(case);destination=Path(destination).absolute()
    need(not destination.exists() and not destination.resolve().is_relative_to(ROOT),'Use a new external workspace')
    destination.mkdir(parents=True)
    target=destination/'input';target.mkdir()
    for name,value in case['request']['source'].items():
        p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
    request={k:v for k,v in case['request'].items() if k!='source'};request['source_path']=str(target)
    (destination/'request.json').write_text(json.dumps(request,indent=2))
    (destination/'fixture-manifest.json').write_text(json.dumps(manifest,indent=2))
    (destination/'evidence').mkdir()
    return manifest


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    cases=json.loads((ROOT/'evals/review_v3_cases.json').read_text());matches=[c for c in cases if c['id']==a.case]
    need(len(matches)==1,'Unknown or duplicate case');print(json.dumps(stage(matches[0],a.output)))


if __name__=='__main__':main()
