"""Scoped regression controls. These authored probes are not agent-performance evidence."""
import argparse
import copy
import json
from pathlib import Path
import tempfile

import review_v3 as v
from review_manifest import digest, current


def request(folder):
    root=folder/'target';root.mkdir()
    (root/'module.py').write_text('def clamp(x):\n    return min(10, max(0, x))\n')
    (root/'caller.py').write_text('from module import clamp\nresult = clamp(0)\n')
    log=folder/'log.txt';log.write_text('Supplied external test log; authored control, not actual target execution.\n')
    coverage={d:{'status':'not_applicable','owner':None,'reason':'No relevant flow in this bounded control','evidence':['C1']} for d in v.DOMAINS}
    coverage['implementation'].update(status='applicable',owner='lead',reason='Required input/output flow')
    return {'root':str(root),'profile':{'mode':'component','scope':['.'],'exclusions':[],'systems':['Python library'],'versions':['Python 3'],'critical_flows':['clamp boundary'],'assumptions':[]},'paths':['module.py','caller.py'],'criteria':[{'id':'C1','text':'Clamp integers to 0..10; independently inspect the boundary','origin':'User conversation copied outside target','required_domains':['implementation']}],'evidence':[{'id':'E1','path':str(log),'origin':'Supplied authored fixture log'}],'coverage':coverage,'participants':{'implementer':'author-context','lead':'review-context','requested_model':None,'observed_model':None},'bounds':{'max_calls':4,'max_seconds':600,'max_concurrent':2},'capabilities':{'direct':True,'parent':True},'predecessor':None}


def task(identifier='T1',kind='initial',predecessor=None,route='lead'):
    return {'id':identifier,'domain':'implementation','actor':'review-context' if route=='lead' else 'worker-context','route':route,'question':'Does clamp preserve the boundary contract?','paths':['module.py'],'criteria':['C1'],'depends_on':[],'kind':kind,'predecessor':predecessor}


def result(state,folder,tid='T1',status='completed'):
    t=state['tasks'][tid];trace=folder/(tid+'.trace');trace.write_text('Authored mechanical control, not an actual performing-agent trace.\n')
    return {'event_id':'O-'+tid,'task_id':tid,'binding':state['binding'],'actor':t['actor'],'status':status,
      'inspection':{'paths':t['paths'],'notes':'Inspected boundary expression and criterion in authored control.'},
      'report':{'version':2,'binding':state['binding'],'reviewer':t['actor'],'decision':'no_findings','summary':'The captured clamp matches the supplied boundary.','findings':[],'limitations':[],'checks':[{'name':'Target execution','status':'not_run','evidence_id':None}],'observed_model':None,'source_instructions_followed':False},
      'trace':{'path':str(trace),'sha256':digest(trace.read_bytes())},'limitations':[] if status=='completed' else ['Simulated '+status+' for a mechanical control.']}



def finding(state, category='risk_or_improvement'):
    return {'id':'F1','category':category,'title':'Clarify supported argument types','criterion':'C1','severity':'P3','severity_reason':'Documentation clarity, with no demonstrated boundary defect','trigger':'Caller passes an unsupported argument type','impact':'Callers cannot predict error handling','references':[{'kind':'source','id':'module.py','sha256':state['capture']['files']['module.py']['sha256'],'start_line':1,'end_line':2}],'correction':'Document the integer input contract','tradeoff':'A runtime guard adds overhead and is not required by C1','verification':'Review documented supported inputs against callers','absence_evidence':None}

def assessment(decision='no_findings'):
    return {'lead':'review-context','decision':decision,'summary':'Source-bound control assessment.','dispositions':[],'conflicts':[],'limitations':[] if decision!='incomplete' else ['Incomplete control scope.']}


def refused(call):
    try:call()
    except (v.Invalid,ValueError,KeyError,TypeError,AttributeError):return
    raise AssertionError('Expected rejection did not occur')


def complete(state,folder,route='lead'):
    v.dispatch(state,task(route=route),1);r=result(state,folder);out=v.collect(state,r,2)
    assert out['accepted'],out
    return r


def check(case):
    flow=case['workflow']['id'];scenario=case['workflow']['scenario'];condition=next(iter(case['workflow']['covers']),None)
    with tempfile.TemporaryDirectory(prefix='engineering-review-control-') as tmp:
        folder=Path(tmp).resolve();req=request(folder);state=v.prepare(req,0)
        process_events=[]
        def observed(phase, evidence):
            process_events.append({'phase':phase,'evidence':evidence,'visible':False})
        if scenario=='success':
            if flow=='scope':
                assert state['capture']['profile']==req['profile'];observed('profile','Prepared explicit profile')
                assert state['binding']==v.binding(state);observed('bind','Verified immutable capture binding')
                assert set(state['coverage'])==set(v.DOMAINS);observed('applicability','All six decisions retained')
            elif flow=='review':
                t=task();observed('assign','Bound question and source subset prepared')
                v.dispatch(state,t,1);observed('dispatch','Task recorded before collection')
                r=result(state,folder);assert r['inspection']['paths']==t['paths'];observed('inspect','Authored inspection fixture matches assignment')
                # The shared leaf example must be consumable by the actual validator.
                # This is a format control, not an agent inspection claim.
                standard=(v.ROOT/'references/review_standard.md').read_text()
                section=standard.split('### Specialist return contract\n',1)[1]
                template=json.loads(section.split('```json\n',1)[1].split('```',1)[0])
                encoded=json.dumps(template)
                for old,new in {'ASSIGNED_SOURCE_ID':'module.py','ASSIGNED_BINDING':state['binding'],'ASSIGNED_ACTOR':'review-context','ASSIGNED_CRITERION_ID':'C1','CAPTURED_SOURCE_SHA256':state['capture']['files']['module.py']['sha256']}.items():
                    encoded=encoded.replace(old,new)
                documented=json.loads(encoded)
                r['inspection']=documented['inspection'];r['report']=documented['report']
                assert v.collect(state,r,2)['accepted'];observed('collect','Documented leaf return accepted by actual validator')
            elif flow=='reconcile':
                v.dispatch(state,task(),1);r=result(state,folder);r['report'].update(decision='needs_changes',findings=[finding(state)])
                assert v.collect(state,r,2)['accepted']
                a=assessment('needs_changes');a['dispositions']=[{'finding':'T1:F1','action':'retain','reason':'Supported bounded improvement','duplicate_of':None}]
                observed('dispositions','Every finding has an explicit retained disposition')
                assert a['conflicts']==[];observed('conflicts','No disagreement in the supplied control')
                final=v.synthesize(state,a,3);assert final['retained_findings']['T1:F1']['category']=='risk_or_improvement'
                observed('validate','Actual synthesis validated coverage and finding disposition')
                assert final['decision']=='needs_changes';observed('deliver','Validated assessment available to lead; no host delivery claimed')
            elif flow=='recover':
                v.dispatch(state,task(),1);out=v.collect(state,result(state,folder,status='timeout'),2)
                assert out['recorded'];observed('record','Simulated timeout retained as a terminal outcome')
                assert state['tasks']['T1']['status']=='timeout' and not state['tasks']['T1']['accepted'];observed('classify','Failed attempt remains ineligible')
                v.dispatch(state,task('T2','retry','T1'),3);assert v.collect(state,result(state,folder,'T2'),4)['accepted']
                assert v.synthesize(state,assessment(),5)['coverage_status']=='complete' and state['tasks']['T1']['status']=='timeout'
                observed('reconcile','Linked retry completes coverage without erasing timeout')
            elif flow=='verify':
                from review_eval import preflight
                from host_coverage import freeze,assess
                from prepare_review_case import stage
                assert preflight()['passed'];observed('preflight','Actual fixture/resource registry passed')
                matrix=freeze(v.ROOT,json.loads((v.ROOT/'config/host_validation.json').read_text()));observed('freeze','Actual package/case matrix frozen')
                case_data=next(c for c in json.loads((v.ROOT/'evals/review_v3_cases.json').read_text()) if c['kind']=='behavior')
                fixture=stage(case_data,folder/'pilot-input');assert fixture['inputs'];observed('pilot','Performing pilot inputs staged; AI execution belongs to behavioral cases, not this control')
                report=assess(matrix,v.ROOT,[]);assert not report['accepted'] and all(row['status']=='not_run' for row in report['cells'])
                observed('assess','Absent actual host captures correctly prevent acceptance')
            v.verify_history(state)
        elif scenario=='omission':
            if flow=='scope':
                altered=copy.deepcopy(req)
                if condition=='profile':del altered['profile']
                elif condition=='bind':altered['criteria']=[]
                else:del altered['coverage']['security']
                refused(lambda:v.prepare(altered,0))
            elif flow=='review':
                if condition in {'assign','dispatch'}:refused(lambda:v.collect(state,{'event_id':'x','task_id':'unknown','status':'completed'},1))
                elif condition=='inspect':
                    v.dispatch(state,task(),1);r=result(state,folder);r['inspection']['paths']=[]
                    assert not v.collect(state,r,2)['accepted']
                else:
                    v.dispatch(state,task(),1);refused(lambda:v.synthesize(state,assessment(),2))
            elif flow=='reconcile':
                complete(state,folder);a=assessment();key={'dispositions':'dispositions','conflicts':'conflicts','validate':'lead','deliver':'summary'}[condition];del a[key]
                refused(lambda:v.synthesize(state,a,3))
            elif flow=='recover':
                v.dispatch(state,task(),1)
                if condition=='record':refused(lambda:v.synthesize(state,assessment(),2))
                else:
                    r=result(state,folder,status='timeout');v.collect(state,r,2)
                    refused(lambda:v.synthesize(state,assessment(),3))
            else:
                from review_eval import preflight
                from prepare_review_case import validate_case
                if condition=='preflight':refused(lambda:validate_case({'id':'x','kind':'behavior','request':{},'resources':[]}))
                else:
                    bad={'case_files':[]};refused(lambda:preflight(host_config=bad))
        elif scenario=='order':
            if flow=='scope':
                bad=copy.deepcopy(req);bad['criteria']=[];refused(lambda:v.prepare(bad,0))
            elif flow in {'review','reconcile'}:
                if condition=='dispatch->inspect':
                    v.dispatch(state,task(),1);refused(lambda:v.synthesize(state,assessment(),2))
                else:refused(lambda:v.collect(state,{'event_id':'early','task_id':'T1','status':'completed'},0))
            elif flow=='recover':
                v.dispatch(state,task(),1);refused(lambda:v.dispatch(state,task('T2','retry','T1'),2))
            else:
                from review_eval import preflight
                refused(lambda:preflight(host_config={'case_files':[{'path':'evals/review_v3_cases.json','ids':['unknown']}]}))
        elif scenario=='boundary':
            if condition=='external-inputs':
                assert state['capture']['criteria'][0]['origin'] and state['capture']['evidence'][0]['text']
                assert sorted(p.name for p in Path(req['root']).iterdir())==['caller.py','module.py']
            elif condition=='unsupported':
                bad=copy.deepcopy(req);bad['paths']=[];refused(lambda:v.prepare(bad,0))
            elif condition in {'authority','composition'}:
                v.dispatch(state,task(),1);r=result(state,folder);r['report']['source_instructions_followed']=True
                assert not v.collect(state,r,2)['accepted']
            elif condition=='independence':
                t=task();t['actor']='author-context';refused(lambda:v.dispatch(state,t,1))
            elif condition=='subset':
                complete(state,folder);assert state['tasks']['T1']['accepted']
            elif condition=='budget':
                req['coverage']['implementation']['owner']='specialist';req['bounds']['max_calls']=0;state=v.prepare(req,0)
                refused(lambda:v.dispatch(state,task(route='direct'),1))
                req['coverage']['implementation']['owner']='lead';state=v.prepare(req,0);complete(state,folder)
                assert v.synthesize(state,assessment('incomplete'),700)['coverage_status']=='incomplete'
            elif condition=='missing-coverage':
                bad=copy.deepcopy(req);bad['criteria'][0]['required_domains'].append('security');refused(lambda:v.prepare(bad,0))
            elif condition in {'finding-basis','serious-finding'}:
                v.dispatch(state,task(),1);r=result(state,folder);r['report']['findings']=[{'id':'F1','category':'defect','severity':'P1'}]
                assert not v.collect(state,r,2)['accepted']
            elif condition in {'drift','revocation'}:
                v.dispatch(state,task(),1)
                if condition=='drift':(Path(req['root'])/'module.py').write_text('changed\n')
                else:v.revoke(state,1.5)
                r=result(state,folder,status='timeout' if condition=='drift' else 'cancelled');out=v.collect(state,r,2)
                assert out['recorded'] and not out['accepted'] and state['tasks']['T1']['status']==r['status']
                assert v.synthesize(state,assessment('incomplete'),3)['coverage_status']=='incomplete'
            elif condition=='duplicate':
                r=complete(state,folder);assert v.collect(state,r,3)['duplicate'];r['event_id']='different';r['status']='failed';assert v.collect(state,r,4)['conflict']
            elif condition=='fixtures':
                from prepare_review_case import validate_case
                refused(lambda:validate_case({'id':'bad','kind':'behavior','request':{'source':{'../escape':'bad'}},'resources':['SKILL.md']}))
            elif condition=='registry':
                from review_eval import preflight
                refused(lambda:preflight(host_config={'case_files':[]}))
                impact=json.loads((Path(__file__).resolve().parents[1]/'config/test_impact.json').read_text())
                missing=copy.deepcopy(impact);missing['final_checks'].pop('success')
                refused(lambda:preflight(final_config=missing))
                unrun=copy.deepcopy(impact);unrun['final_checks']['behavior_selective']={'argv':['{python}','scripts/evaluate.py','--case','behavior_selective']}
                refused(lambda:preflight(final_config=unrun))
                pending=copy.deepcopy(impact);pending['final_checks']['success']['argv']=['{python}','scripts/evaluate.py','--case','success']
                refused(lambda:preflight(final_config=pending))
            elif condition=='identity':
                bad=copy.deepcopy(req);bad['participants']['observed_model']=False;refused(lambda:v.prepare(bad,0))
            elif condition=='history':
                complete(state,folder);state['events'][0]['payload']['binding']='tampered';refused(lambda:v.verify_history(state))
            else:raise AssertionError(condition)
        elif scenario=='branch':
            if condition=='git-nongit':assert state['capture']['identity']['kind']=='filesystem'
            elif condition=='modes':
                for mode in ['change','component','project']:
                    req['profile']['mode']=mode;assert v.prepare(req,0)['capture']['profile']['mode']==mode
            elif condition in {'solo','specialist','parent'}:
                route={'solo':'lead','specialist':'direct','parent':'parent'}[condition]
                if route!='lead':req['coverage']['implementation']['owner']='specialist';state=v.prepare(req,0)
                complete(state,folder,route);assert v.synthesize(state,assessment(),3)['decision']=='no_findings'
            elif condition=='clean':complete(state,folder);assert v.synthesize(state,assessment(),3)['decision']=='no_findings'
            elif condition=='incomplete':
                v.dispatch(state,task(),1);v.collect(state,result(state,folder,status='failed'),2);assert v.synthesize(state,assessment('incomplete'),3)['decision']=='incomplete'
            elif condition=='improvements':
                v.dispatch(state,task(),1);r=result(state,folder);r['report'].update(decision='needs_changes',findings=[finding(state)])
                assert v.collect(state,r,2)['accepted']
                a=assessment('needs_changes');a['dispositions']=[{'finding':'T1:F1','action':'retain','reason':'Useful bounded contract clarification','duplicate_of':None}]
                assert v.synthesize(state,a,3)['retained_findings']['T1:F1']['category']=='risk_or_improvement'
            elif condition=='followup':
                complete(state,folder);v.dispatch(state,task('T2','followup','T1'),3);assert v.collect(state,result(state,folder,'T2'),4)['accepted']
            elif condition=='retry':
                v.dispatch(state,task(),1);v.collect(state,result(state,folder,status='failed'),2);v.dispatch(state,task('T2','retry','T1'),3);assert v.collect(state,result(state,folder,'T2'),4)['accepted']
            elif condition=='reuse':
                complete(state,folder);v.synthesize(state,assessment(),3);fresh=v.prepare(req,4);assert v.reuse(state,fresh)['eligible'];assert fresh['final'] is None
            elif condition=='host-unavailable':
                req['coverage']['implementation']['owner']='specialist';req['capabilities']={'direct':False,'parent':False};state=v.prepare(req,0);refused(lambda:v.dispatch(state,task(route='direct'),1))
            elif condition=='transfer':
                req['profile']['systems']=['Offline command-line utility'];req['coverage']['security']['reason']='No trust crossing in the explicitly bounded fixture';assert v.prepare(req,0)['coverage']['security']['status']=='not_applicable'
            else:raise AssertionError(condition)
        elif scenario=='recovery':
            if condition=='recapture':
                (Path(req['root'])/'caller.py').write_text('new caller\n');refused(lambda:current(state['capture']));req['predecessor']=state['id'];fresh=v.prepare(req,3);assert fresh['binding']!=state['binding']
            elif condition=='missing-input':
                t=task();t['paths'].append('missing.py');refused(lambda:v.dispatch(state,t,1))
            elif condition in {'failed-worker','bounded-retry'}:
                v.dispatch(state,task(),1);v.collect(state,result(state,folder,status='timeout'),2);v.dispatch(state,task('T2','retry','T1'),3);assert v.collect(state,result(state,folder,'T2'),4)['accepted']
            elif condition=='followup':
                complete(state,folder);v.dispatch(state,task('T2','followup','T1'),3);v.collect(state,result(state,folder,'T2'),4);assert v.synthesize(state,assessment(),5)['coverage_status']=='complete'
            elif condition=='late-return':
                v.dispatch(state,task(),1);out=v.collect(state,result(state,folder),700);assert out['recorded'] and not out['accepted']
            else:raise AssertionError(condition)
        else:raise AssertionError(scenario)
        return {'provenance':{'kind':'authored_control','source':__file__},'events':process_events,'case':case['id'],'passed':True,'limits':'Actual deterministic assertions and control-step evidence; staged pilot input is not an executed model pilot. No performing-agent evidence is claimed.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',required=True);a=p.parse_args()
    cases=json.loads((v.ROOT/'evals/review_v3_cases.json').read_text());matches=[c for c in cases if c['id']==a.case and c['kind']=='command']
    if len(matches)!=1:p.error('Select one registered mechanical case')
    print(json.dumps(check(matches[0])));return 0


if __name__=='__main__':raise SystemExit(main())
