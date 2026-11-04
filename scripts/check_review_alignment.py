"""Authored V4 regression controls, not fresh reviewer-performance evidence."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import os

import check_review_v3 as base
import review_v3 as v
from review_manifest import digest


def setup(folder, *, document=False, domain='implementation'):
    req = base.request(folder)
    req['criteria'].append({'id':'C2','text':'Inspect session expiry independently','origin':'Explicit control criteria','required_domains':[domain]})
    req['criteria'][0]['required_domains'] = [domain]
    for d in v.DOMAINS:
        req['coverage'][d].update(status='not_applicable',owner=None)
    req['coverage'][domain].update(status='applicable',owner='lead')
    req['alignment'] = {'documents':[], 'criterion_sources':{'C1':None,'C2':None}, 'deviations':[]}
    if document:
        path=folder/'plan.md';path.write_text('Agreed clamp boundary.\nSession expiry is independent.\n')
        req['alignment']['documents']=[{'id':'PLAN','path':str(path),'origin':'Supplied project plan','version':'revision1','status':'available','authority':'agreed','reason':'Actual applicable contract','sections':[{'id':'behavior','start_line':1,'end_line':2,'criteria':['C1','C2'],'domains':[domain]}]}]
        req['alignment']['criterion_sources']={'C1':'PLAN:behavior','C2':'PLAN:behavior'}
    return req


def task(state, criteria=None, tid='T1', kind='initial', predecessor=None):
    t=base.task(tid,kind,predecessor);t['domain']=next(d for d,r in state['coverage'].items() if r['status']=='applicable')
    t['criteria']=['C1','C2'] if criteria is None else criteria
    t['documents']=v.alignment.routes(state['alignment'],t)
    return t


def result(state, folder, tid='T1'):
    r=base.result(state,folder,tid);t=state['tasks'][tid]
    ref={'kind':'source','id':'module.py','sha256':state['capture']['files']['module.py']['sha256'],'start_line':1,'end_line':2}
    r['report']['criterion_assessments']=[{'criterion':cid,'status':'satisfied','rationale':'Authored fixture inspection supports this criterion.','references':[copy.deepcopy(ref)],'findings':[],'deviation_id':None} for cid in t['criteria']]
    return r


def final(state, decision='no_findings'):
    a=base.assessment(decision);a['criterion_dispositions']=[]
    for c in state['capture']['criteria']:
        for domain in c['required_domains']:
            matches=[(tid,row) for tid,t in state['tasks'].items() if t['accepted'] and t['domain']==domain for row in t['result']['report']['criterion_assessments'] if row['criterion']==c['id']]
            tid,row=matches[-1] if matches else (None,{'status':'not_assessed','deviation_id':None})
            a['criterion_dispositions'].append({'criterion':c['id'],'domain':domain,'status':row['status'],'task':tid,'rationale':'Reconciled authored control evidence.','deviation_id':row['deviation_id']})
    return a


def run_control(name, folder):
    req=setup(folder,document=True);state=v.prepare(req,0,version=4)
    if name in {'proposed','stale','conflicting','missing_binding'}:
        d=req['alignment']['documents'][0]
        if name=='proposed':d['authority']='proposed'
        elif name=='missing_binding':req['alignment']['criterion_sources'].pop('C2')
        else:d['status']=name
        base.refused(lambda:v.prepare(req,0,version=4));return
    if name=='optional_missing':
        req['alignment']={'documents':[{'id':'SOD','path':None,'origin':'User reports no objectives document','version':'unknown','status':'missing','authority':'unknown','reason':'Optional, unavailable','sections':[]}],'criterion_sources':{'C1':None,'C2':None},'deviations':[]}
        state=v.prepare(req,0,version=4)
    elif name=='context_only':
        req['alignment']['documents'][0].update(status='stale',authority='proposed')
        req['alignment']['criterion_sources']={'C1':None,'C2':None};state=v.prepare(req,0,version=4)
    elif name=='drift':
        Path(req['alignment']['documents'][0]['path']).write_text('Changed project intent.\n')
        base.refused(lambda:v.dispatch(state,task(state),1));return
    elif name=='output_collision':
        path=Path(req['alignment']['documents'][0]['path']);old=path.read_bytes()
        base.refused(lambda:v.protect_output(state,path));alias=folder/'document-alias';os.link(path,alias)
        base.refused(lambda:v.protect_output(state,alias));assert path.read_bytes()==old;return
    elif name=='unapproved_deviation':
        req['alignment']['deviations']=[{'id':'DEV','criterion':'C2','domain':'implementation','evidence_id':'nonexistent','reason':'Unsupported waiver'}]
        base.refused(lambda:v.prepare(req,0,version=4));return
    elif name=='approved_deviation':
        req['alignment']['deviations']=[{'id':'DEV','criterion':'C2','domain':'implementation','evidence_id':'E1','reason':'Authored approval evidence; actual semantic authority requires lead review'}]
        state=v.prepare(req,0,version=4)
    elif name=='criterion_domain_pair':
        req['criteria'][1]['required_domains'].append('security');req['coverage']['security'].update(status='applicable',owner='lead');req['alignment']['documents'][0]['sections'][0]['domains'].append('security');state=v.prepare(req,0,version=4)
    t=task(state,criteria=['C1'] if name=='unassigned' else None)
    if name in {'route_missing','route_wrong','wrong_domain'}:
        if name=='route_missing':t['documents']=[]
        elif name=='route_wrong':t['documents']=['PLAN:other']
        else:t['domain']='security';state['coverage']['security'].update(status='applicable',owner='lead');state['binding']=v.binding(state)
        base.refused(lambda:v.dispatch(state,t,1));return
    v.dispatch(state,t,1);r=result(state,folder)
    if name in {'assigned_omitted','duplicate_row','unknown_row','fake_satisfied','unknown_deviation','unrouted_citation'}:
        rows=r['report']['criterion_assessments']
        if name=='assigned_omitted':rows.pop()
        elif name=='duplicate_row':rows[1]=copy.deepcopy(rows[0])
        elif name=='unknown_row':rows[1]['criterion']='C99'
        elif name=='fake_satisfied':
            f=base.finding(state,'defect');r['report'].update(findings=[f],decision='needs_changes');rows[0]['findings']=['F1']
        elif name=='unknown_deviation':rows[1].update(status='contradicted',deviation_id='UNKNOWN')
        else:rows[0]['references']=[{'kind':'document','id':'PLAN','sha256':state['alignment']['documents'][0]['capture']['sha256'],'start_line':3,'end_line':3}]
        assert not v.collect(state,r,2)['accepted'];assert state['tasks']['T1']['status']=='completed';return
    if name in {'partial','not_assessed'}:
        r['report']['criterion_assessments'][1]['status']='partially_satisfied' if name=='partial' else 'not_assessed';r['report']['limitations']=['C2 remains incompletely inspected.']
    if name=='approved_deviation':r['report']['criterion_assessments'][1].update(status='contradicted',deviation_id='DEV')
    assert v.collect(state,r,2)['accepted'],state['tasks']['T1']['validation']
    if name=='criterion_domain_pair':
        t2=task(state,['C1'],tid='T2');t2.update(domain='security',criteria=['C2']);t2['documents']=v.alignment.routes(state['alignment'],t2);v.dispatch(state,t2,3)
        r2=result(state,folder,'T2');assert v.collect(state,r2,4)['accepted'];a=final(state);assert v.synthesize(state,a,5)['coverage_status']=='complete';return
    a=final(state,'incomplete' if name in {'unassigned','partial','not_assessed'} else 'no_findings')
    if name=='final_omitted':a['criterion_dispositions'].pop();base.refused(lambda:v.synthesize(state,a,3));return
    if name=='final_forgery':a['criterion_dispositions'][0]['task']='imaginary';base.refused(lambda:v.synthesize(state,a,3));return
    if name=='synthesis_drift':
        Path(req['alignment']['documents'][0]['path']).write_text('Changed after collection\n');a['decision']='incomplete';a['limitations']=['Document drift.']
    out=v.synthesize(state,a,5)
    if name in {'unassigned','partial','not_assessed','synthesis_drift'}:assert out['coverage_status']=='incomplete'
    else:assert out['coverage_status']=='complete'
    if name=='unassigned':assert out['missing_criteria']==[{'criterion':'C2','domain':'implementation'}]
    if name=='approved_deviation':assert out['criterion_dispositions'][1]['status']=='contradicted' and out['approved_deviations']
    v.verify_history(state)


CONTROLS=['success','assigned_omitted','unassigned','duplicate_row','unknown_row','final_omitted','final_forgery','fake_satisfied','proposed','stale','conflicting','missing_binding','optional_missing','context_only','drift','synthesis_drift','route_missing','route_wrong','wrong_domain','unrouted_citation','partial','not_assessed','unapproved_deviation','unknown_deviation','approved_deviation','criterion_domain_pair','output_collision']


def process_controls(folder):
    req=setup(folder);state=v.prepare(req,0,version=4)
    # Omitted preparation cannot pass identity or dispatch; missing assignment cannot collect.
    base.refused(lambda:v.dispatch({},base.task(),1))
    base.refused(lambda:v.collect(state,{'event_id':'O','task_id':'T1','status':'completed'},1))
    # No accepted work and running work both prevent premature synthesis.
    base.refused(lambda:v.synthesize(state,final(state),1))
    v.dispatch(state,task(state),1);base.refused(lambda:v.synthesize(state,final(state),2))
    assert v.collect(state,result(state,folder),2)['accepted']
    # Omitting synthesis leaves a review without an accepted final assessment.
    assert state['final'] is None
    v.synthesize(state,final(state),3)
    # Finalization must precede no further dispatch/collection acceptance.
    base.refused(lambda:v.dispatch(state,task(state,tid='T2',kind='followup',predecessor='T1'),4))
    return [{'phase':p,'evidence':e,'visible':False} for p,e in [('prepare','Actual v4 binding prepared'),('dispatch','Actual task and all criterion IDs bound'),('collect','Actual validator accepted authored complete report'),('synthesize','Actual global criterion/domain coverage verified')]]


def completion_controls(folder):
    import run_tests as runner
    root=folder/'package';(root/'config').mkdir(parents=True)
    (root/'config/test_impact.json').write_text(json.dumps({'schema_version':1,'tests':{},'rules':[],'final_checks':{}}))
    path=folder/'completion.json'
    record={'artifact_sha256':runner.digest(runner.inventory(root)),'implementation_complete':True,'implementation_plan':{'source':'Authored gate control','steps':[{'id':'I1','result':'Deliver current implementation'}]},'delivered_steps':[{'id':'I1','status':'delivered','evidence':['Authored artifact inspected']}],'remaining_implementation_work':[],'verified_by':{'identity':'Authored verifier','method':'Compared explicit step with current artifact'}}
    path.write_text(json.dumps(record));selection=runner.plan(root,[],True,path)
    assert selection['implementation_completion']['record']==str(path)
    for alias in [path,folder/'linked-record',folder/'hardlinked-record']:
        if alias.name=='linked-record':alias.symlink_to(path)
        if alias.name=='hardlinked-record':os.link(path,alias)
        before=path.read_bytes()
        assert runner.main(['--package',str(root),'--changed','config/test_impact.json','--full','--completion-record',str(path),'--report',str(alias)])==2
        assert path.read_bytes()==before
    bad=copy.deepcopy(record);bad['remaining_implementation_work']=['Undelivered requirement'];path.write_text(json.dumps(bad));base.refused(lambda:runner.plan(root,[],True,path))
    bad=copy.deepcopy(record);bad['delivered_steps']=[];path.write_text(json.dumps(bad));base.refused(lambda:runner.plan(root,[],True,path))
    # The saved selection cannot execute after either the record or artifact changes.
    path.write_text(json.dumps(record)+'\n');base.refused(lambda:runner.execute(selection))
    path.write_text(json.dumps(record));(root/'changed.txt').write_text('Changed after author verification');base.refused(lambda:runner.execute(selection))


def cli_controls(folder):
    req=setup(folder,document=True);request=folder/'request.json';request.write_text(json.dumps(req));state_path=folder/'state.json'
    script=Path(v.__file__).with_name('review_suite.py')
    def call(*args, expected=0):
        p=subprocess.run([sys.executable,str(script),*args],capture_output=True,text=True,timeout=20)
        assert p.returncode==expected,(args,p.stdout,p.stderr)
        return json.loads(p.stdout) if not args[-1]=='--help' else None
    for flag in ([],['--v3'],['--v4']):call(*flag,'--help')
    call('--v4','prepare','--state',str(state_path),'--input',str(request));state=json.loads(state_path.read_text())
    task_path=folder/'task.json';task_path.write_text(json.dumps(task(state)))
    call('--v4','dispatch','--state',str(state_path),'--input',str(task_path));state=json.loads(state_path.read_text())
    out=folder/'outcome.json';out.write_text(json.dumps(result(state,folder)))
    assert call('--v4','collect','--state',str(state_path),'--input',str(out))['accepted'];state=json.loads(state_path.read_text())
    a=folder/'assessment.json';a.write_text(json.dumps(final(state)))
    assert call('--v4','synthesize','--state',str(state_path),'--input',str(a))['coverage_status']=='complete'
    call('--v3','show','--state',str(state_path),expected=2)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',choices=['all','omission','order'],default='all');args=parser.parse_args()
    completed=[]
    for name in CONTROLS if args.case=='all' else []:
        with tempfile.TemporaryDirectory() as d:run_control(name,Path(d).resolve());completed.append(name)
    with tempfile.TemporaryDirectory() as d:events=process_controls(Path(d).resolve())
    with tempfile.TemporaryDirectory() as d:completion_controls(Path(d).resolve())
    with tempfile.TemporaryDirectory() as d:cli_controls(Path(d).resolve())
    print(json.dumps({'passed':True,'authored_controls':completed,'events':events,'provenance':{'kind':'authored_control','source':'scripts/check_review_alignment.py'},'limits':'Deterministic authored controls, not agent performance or real approval evidence.'}))
    return 0


if __name__=='__main__':raise SystemExit(main())
