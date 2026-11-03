"""Frozen authored suite controls, separate from actual host observations."""
import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from review_contract import Invalid, inspect
from review_suite import prepare, dispatch, collect, synthesize, reuse

CASES=('success','boundary_authority','boundary_binding','boundary_bounds','branch_incomplete',
       'branch_siblings','branch_solo','omission_collect','omission_dispatch','omission_prepare',
       'omission_synthesize','order_collect_synthesize','order_dispatch_collect','order_prepare_dispatch','recovery_reuse')


def must_refuse(fn):
    try:fn()
    except (Invalid,KeyError,TypeError,ValueError):return
    raise AssertionError('Invalid transition accepted')


def exercise(name):
    with tempfile.TemporaryDirectory(prefix='review-suite-') as tmp:
        root=Path(tmp).resolve()/'target';root.mkdir()
        (root/'module.py').write_text('answer = 42\n')
        (root/'criteria.txt').write_text('The answer must equal 42.\n')
        request={'root':str(root),'paths':['module.py','criteria.txt'],'criteria':['criteria.txt'],
          'implementer':'author','lead':'lead','coverage':{'implementation':{'owner':'lead','reason':'One function'}},
          'bounds':{'max_calls':2,'max_seconds':60,'max_concurrent':1},
          'capabilities':{'lead_dispatch':False,'parent_dispatch':True}}
        state=prepare(request,100)
        trace=Path(tmp)/'trace.json';trace.write_text('{"kind":"authored_control"}\n')
        trace_ref={'path':str(trace.resolve()),'sha256':hashlib.sha256(trace.read_bytes()).hexdigest()}
        task={'id':'t1','domain':'implementation','actor':'lead','route':'lead','depends_on':[]}
        def result(status='completed'):
            snap=copy.deepcopy(state['capture']);snap['reviewer']=task['actor']
            report={'capture_id':snap['capture_id'],'reviewer':task['actor'],'decision':'no_findings',
              'summary':'Authored control only','findings':[],'limitations':['No performing AI'],
              'observed_model':None,'observed_effort':None,'actions':['read_source','capture','inspect','report'],
              'checks':[{'name':'target tests','status':'not_run','source':None}],'source_instructions_followed':False}
            return {'task_id':'t1','binding':state['binding'],'actor':task['actor'],'status':status,
                    'inspection':inspect(snap,list(snap['files']),'Authored control inspection'),
                    'report':report,'trace':trace_ref,'limitations':['Authored control']}
        assessment={'lead':'lead','decision':'no_findings','summary':'Authored complete control',
                    'dispositions':[],'conflicts':[],'limitations':['No actual AI or host behavior']}
        if name=='omission_prepare':must_refuse(lambda:dispatch({},task,101))
        elif name=='order_prepare_dispatch':
            empty=copy.deepcopy(state);empty['capture']={};must_refuse(lambda:dispatch(empty,task,101))
        elif name in {'omission_dispatch','order_dispatch_collect'}:must_refuse(lambda:collect(state,result(),102))
        elif name in {'omission_collect','order_collect_synthesize'}:
            dispatch(state,task,101);must_refuse(lambda:synthesize(state,assessment,103))
        elif name=='omission_synthesize':
            dispatch(state,task,101);collect(state,result(),102);must_refuse(lambda:reuse(state,prepare(request,103)))
        elif name=='boundary_authority':
            bad=copy.deepcopy(task);bad['actor']='author';must_refuse(lambda:dispatch(state,bad,101))
            dispatch(state,task,101);r=result();r['report']['source_instructions_followed']=True
            must_refuse(lambda:collect(state,r,102));r=result();r['report']['actions'].append('edit_target')
            must_refuse(lambda:collect(state,r,102))
        elif name=='boundary_binding':
            dispatch(state,task,101);r=result();r['binding']='bad';must_refuse(lambda:collect(state,r,102))
            r=result();r['trace']={'path':str(Path(tmp)/'absent'),'sha256':'0'*64};must_refuse(lambda:collect(state,r,102))
            r=result();state['revoked']=True;must_refuse(lambda:collect(state,r,102));state['revoked']=False
            (root/'criteria.txt').write_text('Changed criteria\n');must_refuse(lambda:collect(state,r,102))
        elif name=='boundary_bounds':
            must_refuse(lambda:dispatch(state,task,161))
            request['coverage']['implementation']['owner']='specialist';request['bounds']['max_calls']=0
            state=prepare(request,100);task.update(actor='specialist',route='sibling');must_refuse(lambda:dispatch(state,task,101))
            request['bounds']['max_calls']=2;state=prepare(request,100)
            bad=copy.deepcopy(task);bad['route']='nested';must_refuse(lambda:dispatch(state,bad,101))
            bad=copy.deepcopy(task);bad['depends_on']=['missing'];must_refuse(lambda:dispatch(state,bad,101))
            dispatch(state,task,101);must_refuse(lambda:collect(state,result(),161));collect(state,result('timeout'),161)
        elif name=='branch_incomplete':
            dispatch(state,task,101);collect(state,result('timeout'),162)
            must_refuse(lambda:synthesize(state,assessment,163));assessment['decision']='incomplete'
            assert synthesize(state,assessment,163)['missing_domains']==['implementation']
        else:
            if name=='branch_siblings':
                request['coverage']['implementation']['owner']='specialist';state=prepare(request,100)
                task.update(actor='specialist',route='sibling')
            dispatch(state,task,101);collect(state,result(),102);synthesize(state,assessment,103)
            if name=='recovery_reuse':
                fresh=prepare(request,104);assert reuse(state,fresh)['eligible'];state['revoked']=True
                must_refuse(lambda:reuse(state,fresh))
        assert (root/'module.py').read_text()=='answer = 42\n'
        events=[{'phase':e['phase'],'evidence':json.dumps(e),'visible':e['phase']=='synthesize'} for e in state['events']]
        return {'provenance':{'kind':'authored_control','source':'scripts/check_suite_cases.py:'+name},
                'events':events,'case':name,'passed':True,'limits':'No fresh model performance or host enforcement evidence.'}

if __name__=='__main__':
    name=sys.argv[1] if len(sys.argv)>1 else 'all'
    if name=='all':
        results=[exercise(n) for n in CASES];print(json.dumps({'passed':len(results),'cases':list(CASES)}))
    elif name in CASES:print(json.dumps(exercise(name)))
    else:raise SystemExit('Unknown frozen case')
