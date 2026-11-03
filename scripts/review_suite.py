"""Coordinate bounded reviews; validate evidence, never judge defects or spawn agents."""
import argparse
import copy
import fcntl
import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from review_contract import Invalid, need, capture, current, validate, load, save

ROLES = ('implementation', 'architecture', 'security', 'data', 'testing', 'operations')
TERMINAL = ('completed', 'failed', 'timeout', 'cancelled')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def prepare(request, now=None):
    required = {'root', 'paths', 'criteria', 'implementer', 'lead', 'coverage',
                'bounds', 'capabilities'}
    need(type(request) is dict and set(request) == required, 'Request fields differ')
    need(request['criteria'] and set(request['criteria']) <= set(request['paths']),
         'Capture explicit criteria files with the source')
    coverage = request['coverage']
    need(type(coverage) is dict and coverage and set(coverage) <= set(ROLES),
         'Select relevant domains; empty projects need explicit missing-input reporting')
    for role, assignment in coverage.items():
        need(set(assignment) == {'owner', 'reason'} and assignment['owner'] in {'lead', 'specialist'}
             and isinstance(assignment['reason'], str) and assignment['reason'].strip(),
             'Each domain needs an owner and reason')
    bounds = request['bounds']
    need(set(bounds) == {'max_calls', 'max_seconds', 'max_concurrent'}, 'Explicit bounds required')
    need(all(type(v) is int for v in bounds.values()) and 0 <= bounds['max_calls'] <= 32
         and 1 <= bounds['max_seconds'] <= 7200 and 1 <= bounds['max_concurrent'] <= 6,
         'Bounds exceed supported limits')
    caps = request['capabilities']
    need(set(caps) == {'lead_dispatch', 'parent_dispatch'} and
         all(type(v) is bool for v in caps.values()), 'Record observed dispatch capabilities')
    snap = capture(request['root'], request['paths'], request['implementer'], request['lead'])
    now = time.time() if now is None else now
    return {'version': 2, 'id': str(uuid.uuid4()), 'request': copy.deepcopy(request),
            'binding': digest({'files': snap['files'], 'criteria': request['criteria'],
                               'coverage': coverage}), 'capture': snap, 'started': now,
            'revoked': False, 'tasks': {}, 'events': [{'phase': 'prepare', 'at': now}],
            'final': None}


def active(state, now, deadline=True):
    need(state.get('version') == 2 and not state.get('revoked'), 'Missing or revoked review')
    current(state['capture'])
    need(state['binding'] == digest({'files': state['capture']['files'],
         'criteria': state['request']['criteria'], 'coverage': state['request']['coverage']}),
         'Source or criteria binding changed')
    need(state['final'] is None, 'Review already finalized')
    if deadline:
        need(now - state['started'] <= state['request']['bounds']['max_seconds'], 'Review deadline exhausted')


def dispatch(state, task, now):
    active(state, now)
    need(set(task) == {'id', 'domain', 'actor', 'route', 'depends_on'}, 'Dispatch fields differ')
    need(isinstance(task['id'], str) and task['id'] and task['id'] not in state['tasks'],
         'Task identity must be new; retain prior attempts')
    domain = task['domain']; req = state['request']
    need(domain in req['coverage'], 'Domain is outside planned coverage')
    need(task['actor'] and task['actor'] != req['implementer'], 'Reviewer must differ from implementer')
    need(type(task['depends_on']) is list and len(set(task['depends_on'])) == len(task['depends_on']), 'Invalid dependencies')
    for dep in task['depends_on']:
        need(dep in state['tasks'] and state['tasks'][dep]['status'] == 'completed', 'Prerequisite result is unavailable')
    need(not any(t['domain'] == domain and t['status'] in {'running', 'completed'} for t in state['tasks'].values()),
         'Domain already running or completed')
    owner = req['coverage'][domain]['owner']
    if owner == 'lead':
        need(task['route'] == 'lead' and task['actor'] == req['lead'], 'Lead work remains with accountable lead')
    else:
        need(task['actor'] != req['lead'], 'Specialist needs a separate performing context')
        caps=req['capabilities']
        need((task['route'] == 'nested' and caps['lead_dispatch']) or
             (task['route'] == 'sibling' and caps['parent_dispatch']), 'Dispatch tool or depth unavailable')
        calls=sum(t['route'] != 'lead' for t in state['tasks'].values())
        running=sum(t['status'] == 'running' and t['route'] != 'lead' for t in state['tasks'].values())
        need(calls < req['bounds']['max_calls'] and running < req['bounds']['max_concurrent'], 'Dispatch budget exhausted')
    state['tasks'][task['id']]={**task, 'binding':state['binding'], 'status':'running', 'started':now, 'result':None}
    state['events'].append({'phase':'dispatch','task':task['id'],'at':now})


def check_trace(trace, root):
    need(type(trace) is dict and set(trace) == {'path', 'sha256'}, 'Trace needs path and exact digest')
    path=Path(trace['path'])
    need(path.is_absolute() and not path.is_symlink() and not path.resolve().is_relative_to(Path(root)),
         'Trace must be an external regular evidence file')
    need(path.is_file() and 0 < path.stat().st_size <= 2*1024*1024, 'Trace is missing, empty or too large')
    need(hashlib.sha256(path.read_bytes()).hexdigest() == trace['sha256'], 'Trace evidence changed')


def check_results(state):
    for task in state['tasks'].values():
        if task['result'] is not None:
            check_trace(task['result']['trace'],state['capture']['root'])


def collect(state, result, now):
    active(state, now, deadline=False)
    need(set(result) == {'task_id','binding','actor','status','inspection','report','trace','limitations'}, 'Result fields differ')
    need(result['task_id'] in state['tasks'], 'Result has no prior dispatch')
    task=state['tasks'][result['task_id']]
    need(task['status'] == 'running', 'Task already terminal; preserve the original outcome')
    need(result['binding'] == task['binding'] and result['actor'] == task['actor'], 'Result source or actor differs')
    need(result['status'] in TERMINAL and isinstance(result['limitations'],list), 'Invalid terminal result')
    check_trace(result['trace'],state['capture']['root'])
    if result['status'] == 'completed':
        need(now-state['started'] <= state['request']['bounds']['max_seconds'], 'Late completion cannot satisfy bounded review')
        snap=copy.deepcopy(state['capture']);snap['reviewer']=task['actor']
        need(isinstance(result['inspection'].get('notes'),str) and result['inspection']['notes'].strip(), 'Inspection notes required')
        validate(snap,result['inspection'],result['report'])
        need(result['report']['decision'] != 'blocked', 'Blocked coverage must remain incomplete')
    else:
        need(result['limitations'], 'Failure needs explicit limits')
    task.update(status=result['status'], result=copy.deepcopy(result), ended=now)
    state['events'].append({'phase':'collect','task':task['id'],'status':result['status'],'at':now})


def synthesize(state, assessment, now):
    active(state,now,deadline=False)
    check_results(state)
    need(set(assessment)=={'lead','decision','summary','dispositions','conflicts','limitations'}, 'Assessment fields differ')
    need(assessment['lead']==state['request']['lead'] and isinstance(assessment['summary'],str)
         and assessment['summary'].strip(), 'Lead owns substantive synthesis')
    need(isinstance(assessment['limitations'],list) and isinstance(assessment['conflicts'],list), 'State unresolved limits and conflicts')
    need(state['tasks'] and all(t['status'] in TERMINAL for t in state['tasks'].values()), 'Collect terminal outcomes before synthesis')
    completed={t['domain'] for t in state['tasks'].values() if t['status']=='completed'}
    missing=sorted(set(state['request']['coverage'])-completed)
    expected={f'{tid}:{i}' for tid,t in state['tasks'].items() if t['status']=='completed'
              for i,_ in enumerate(t['result']['report']['findings'])}
    dispositions=assessment['dispositions']
    need(isinstance(dispositions,list), 'Finding dispositions required')
    need(len(dispositions)==len(expected) and {d.get('finding') for d in dispositions}==expected, 'Every returned finding needs one disposition')
    accepted=[]
    for d in dispositions:
        need(set(d)=={'finding','action','reason','duplicate_of'} and d['action'] in {'retain','reject','duplicate'}
             and isinstance(d['reason'],str) and d['reason'].strip(), 'Explain each finding disposition')
        if d['action']=='duplicate':
            need(d['duplicate_of'] in expected and d['duplicate_of'] != d['finding'], 'Duplicate needs another finding')
        else:need(d['duplicate_of'] is None,'Only duplicates have a target')
        if d['action']=='retain':accepted.append(d['finding'])
    retained=set(accepted)
    for d in dispositions:
        if d['action']=='duplicate':need(d['duplicate_of'] in retained,'Duplicate must resolve to retained finding')
    for conflict in assessment['conflicts']:
        need(set(conflict)=={'finding_ids','resolution','resolved'} and type(conflict['resolved']) is bool
             and conflict['finding_ids'] and set(conflict['finding_ids']) <= expected
             and isinstance(conflict['resolution'],str) and conflict['resolution'].strip(),'Conflict needs evidence and explicit resolution')
    incomplete=bool(missing or any(not c['resolved'] for c in assessment['conflicts']))
    decision='incomplete' if incomplete else ('needs_changes' if accepted else 'no_findings')
    need(assessment['decision']==decision,'Decision contradicts coverage, conflicts or retained findings')
    need(not incomplete or assessment['limitations'], 'Incomplete review needs visible limitations')
    state['final']={**copy.deepcopy(assessment),'missing_domains':missing,'retained_findings':accepted,
                    'binding':state['binding'],'limits':'Mechanical consistency only; lead judgment and actual host trace need review.'}
    state['events'].append({'phase':'synthesize','at':now})
    return state['final']


def reuse(previous, fresh):
    current(previous['capture']);current(fresh['capture']);check_results(previous)
    need(not previous['revoked'] and previous['final'] is not None and
         previous['final']['decision'] != 'incomplete' and previous['binding']==fresh['binding'],
         'Reuse needs active complete evidence with exact source, criteria and coverage')
    return {'eligible':True,'previous_review':previous['id'],'binding':fresh['binding'],
            'limits':'Lead must verify trace, participant independence and continued authority before reuse.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare','dispatch','collect','synthesize','revoke','reuse'])
    parser.add_argument('--state',required=True);parser.add_argument('--input');parser.add_argument('--previous')
    args=parser.parse_args()
    try:
        if args.command=='prepare':
            state=prepare(load(args.input));save(args.state,state,Path(state['capture']['root']));out={'id':state['id'],'binding':state['binding']}
        else:
            path=Path(args.state)
            need(not path.is_symlink(),'State symlinks are unsupported')
            with path.open('r+',encoding='utf-8') as stream:
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX)
                state=json.load(stream);need(not path.resolve().is_relative_to(Path(state['capture']['root'])),'State must remain outside target')
                now=time.time();value=load(args.input) if args.input else None
                if args.command=='dispatch':dispatch(state,value,now);out={'task':value['id'],'status':'running'}
                elif args.command=='collect':collect(state,value,now);out={'task':value['task_id'],'status':value['status']}
                elif args.command=='synthesize':out=synthesize(state,value,now)
                elif args.command=='reuse':out=reuse(load(args.previous),state)
                else:state['revoked']=True;state['events'].append({'phase':'revoke','at':now});out={'revoked':True}
                stream.seek(0);json.dump(state,stream,indent=2,allow_nan=False);stream.write('\n');stream.truncate();stream.flush();os.fsync(stream.fileno())
        print(json.dumps(out,ensure_ascii=False));return 0
    except (Invalid,OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'status':'refused','reason':str(error)}));return 2

if __name__=='__main__':raise SystemExit(main())
