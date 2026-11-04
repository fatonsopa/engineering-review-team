"""V3 review ledger. Record outcomes independently of acceptance. No target execution."""
import argparse
import copy
import fcntl
import json
import os
from pathlib import Path
import tempfile
import time
import uuid

from review_contract import Invalid, need, load, save
from review_manifest import capture, current, digest, text
import review_alignment as alignment

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ('implementation', 'architecture', 'security', 'data', 'testing', 'operations')
TERMINAL = ('completed', 'failed', 'timeout', 'cancelled')


def guidance():
    roles = load(ROOT / 'config/roles.json')
    paths = {'SKILL.md', 'references/review_policy.md', 'references/review_standard.md', 'config/roles.json', 'config/review_contracts.json'}
    for r in roles['specialists'].values():
        paths.update([r['reference'], r['claude'], r['codex']])
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'references').rglob('*.md'))
    paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'assets').rglob('*') if p.is_file() and p.suffix in {'.md', '.toml'})
    return {p: digest((ROOT / p).read_bytes()) for p in sorted(paths)}


def binding(state):
    keys = ['capture', 'coverage', 'participants', 'bounds', 'capabilities', 'guidance', 'predecessor']
    if state.get('version') == 4: keys += ['version', 'alignment']
    return digest({k: state[k] for k in keys})


def identity(state):
    need(state.get('version') in {3, 4} and state['binding'] == binding(state), 'Immutable review binding changed')


def eligible(state, now=None):
    identity(state)
    need(not state['revoked'] and state['final'] is None, 'Review revoked or finalized')
    current(state['capture'])
    if state['version'] == 4: alignment.current(state['alignment'])
    need(state['guidance'] == guidance(), 'Review guidance changed')
    if now is not None:
        need(now - state['started'] <= state['bounds']['max_seconds'], 'Review time bound exhausted')


def prepare(req, now=None, *, version=3):
    fields = {'root', 'profile', 'paths', 'criteria', 'evidence', 'coverage', 'participants', 'bounds', 'capabilities', 'predecessor'}
    need(version in {3, 4}, 'Unknown ledger version')
    if version == 4: fields.add('alignment')
    need(type(req) is dict and set(req) == fields, 'Versioned request fields differ')
    part = req['participants']
    need(type(part) is dict and set(part) == {'implementer', 'lead', 'requested_model', 'observed_model'}, 'Participant fields differ')
    text(part['implementer'], 'Implementer'); text(part['lead'], 'Lead')
    need(part['implementer'] != part['lead'], 'Independent review needs a distinct performer')
    for k in ['requested_model', 'observed_model']:
        need(part[k] is None or isinstance(part[k], str), 'Unknown model identity must be null')
    b = req['bounds']
    need(type(b) is dict and set(b) == {'max_calls', 'max_seconds', 'max_concurrent'}, 'Explicit bounds required')
    need(all(type(v) is int for v in b.values()) and 0 <= b['max_calls'] <= 32 and 1 <= b['max_seconds'] <= 7200 and 1 <= b['max_concurrent'] <= 6, 'Unsupported bounds')
    caps = req['capabilities']
    need(type(caps) is dict and set(caps) == {'direct', 'parent'} and all(type(x) is bool for x in caps.values()), 'Record observed dispatch capabilities')
    need(req['predecessor'] is None or isinstance(req['predecessor'], str), 'Predecessor must identify prior review or be null')
    snap = capture(req)
    cov = req['coverage']
    need(type(cov) is dict and set(cov) == set(DOMAINS), 'Decide applicability for all six domains')
    required = set()
    for c in snap['criteria']:
        need(set(c['required_domains']) <= set(DOMAINS), 'Unknown required domain')
        required.update(c['required_domains'])
    for domain, row in cov.items():
        need(set(row) == {'status', 'owner', 'reason', 'evidence'}, 'Coverage fields differ')
        need(row['status'] in {'applicable', 'not_applicable', 'unresolved'}, 'Invalid applicability')
        need(row['owner'] in {'lead', 'specialist', None}, 'Invalid coverage owner')
        text(row['reason'], 'Applicability reason')
        need(isinstance(row['evidence'], list) and row['evidence'], 'Applicability needs evidence')
        allowed = set(snap['files']) | {c['id'] for c in snap['criteria']} | {e['id'] for e in snap['evidence']}
        need(set(row['evidence']) <= allowed, 'Unknown applicability evidence')
        need(domain not in required or row['status'] == 'applicable', 'Explicitly required domain omitted: ' + domain)
        need(row['status'] != 'applicable' or row['owner'] is not None, 'Applicable domain needs an owner')
    need(any(r['status'] != 'not_applicable' for r in cov.values()), 'No reviewable coverage')
    now = time.time() if now is None else now
    state = {'version': version, 'id': str(uuid.uuid4()), 'capture': snap, 'coverage': copy.deepcopy(cov),
             'participants': copy.deepcopy(part), 'bounds': copy.deepcopy(b), 'capabilities': copy.deepcopy(caps),
             'guidance': guidance(), 'predecessor': req['predecessor'], 'started': now, 'revoked': False,
             'tasks': {}, 'events': [], 'final': None}
    if version == 4: state['alignment'] = copy.deepcopy(alignment.capture(req['alignment'], snap))
    state['binding'] = binding(state)
    event(state, 'prepare', {'binding': state['binding']}, now)
    return state


def event(state, kind, payload, now):
    row = {'sequence': len(state['events']), 'kind': kind, 'at': now, 'payload': copy.deepcopy(payload),
           'previous': state['events'][-1]['sha256'] if state['events'] else None}
    row['sha256'] = digest(row)
    state['events'].append(row)


def dispatch(state, task, now):
    eligible(state, now)
    fields = {'id', 'domain', 'actor', 'route', 'question', 'paths', 'criteria', 'depends_on', 'kind', 'predecessor'}
    if state['version'] == 4: fields.add('documents')
    need(type(task) is dict and set(task) == fields, 'Task fields differ')
    text(task['id'], 'Task ID'); text(task['actor'], 'Actor'); text(task['question'], 'Review question')
    need(task['id'] not in state['tasks'], 'Task ID already exists')
    domain = task['domain']; need(domain in DOMAINS, 'Unknown domain')
    row = state['coverage'][domain]
    need(row['status'] == 'applicable', 'Domain is not applicable')
    need(task['actor'] != state['participants']['implementer'], 'Reviewer is implementer')
    if row['owner'] == 'lead':
        need(task['route'] == 'lead' and task['actor'] == state['participants']['lead'], 'Lead work must remain with lead')
    else:
        need(task['actor'] != state['participants']['lead'], 'Specialist requires a separate context')
        need(task['route'] in {'direct', 'parent'} and state['capabilities'][task['route']], 'Required dispatch unavailable')
        calls = sum(t['route'] != 'lead' for t in state['tasks'].values())
        running = sum(t['route'] != 'lead' and t['status'] == 'running' for t in state['tasks'].values())
        need(calls < state['bounds']['max_calls'] and running < state['bounds']['max_concurrent'], 'Dispatch budget exhausted')
    for name in ['paths', 'criteria', 'depends_on']:
        need(type(task[name]) is list and len(task[name]) == len(set(task[name])), 'Task list invalid: ' + name)
    need(task['paths'] and set(task['paths']) <= state['capture']['files'].keys(), 'Assign captured source subset')
    need(task['criteria'] and set(task['criteria']) <= {c['id'] for c in state['capture']['criteria']}, 'Assign known criteria')
    if state['version'] == 4: alignment.dispatch(state, task)
    for dep in task['depends_on']:
        need(dep in state['tasks'] and state['tasks'][dep]['accepted'], 'Task dependency incomplete')
    same = [t for t in state['tasks'].values() if t['domain'] == domain]
    need(not any(t['status'] == 'running' for t in same), 'Reconcile running domain before dispatch')
    need(task['kind'] in {'initial', 'retry', 'followup'}, 'Unknown task kind')
    if task['kind'] == 'initial':
        need(not same and task['predecessor'] is None, 'Initial task cannot replace history')
    else:
        prev = state['tasks'].get(task['predecessor'])
        need(prev is not None and prev['domain'] == domain and prev['status'] in TERMINAL, 'Link terminal predecessor')
        need(task['kind'] != 'retry' or not prev['accepted'], 'Use followup after accepted review')
    state['tasks'][task['id']] = {**copy.deepcopy(task), 'binding': state['binding'], 'status': 'running', 'started': now, 'accepted': False, 'result': None, 'validation': []}
    event(state, 'dispatch', task, now)


def reference(snap, ref, task, context=None):
    need(type(ref) is dict and set(ref) == {'kind', 'id', 'sha256', 'start_line', 'end_line'}, 'Evidence reference fields differ')
    if ref['kind'] == 'document' and context is not None:
        return alignment.reference(context, ref, task)
    if ref['kind'] == 'source':
        need(ref['id'] in task['paths'], 'Finding cites source outside task')
        value = snap['files'][ref['id']]
    elif ref['kind'] == 'evidence':
        value = next((e for e in snap['evidence'] if e['id'] == ref['id']), None)
        need(value is not None, 'Unknown supplied evidence')
    else:
        raise Invalid('Evidence kind must be source or evidence')
    need(ref['sha256'] == value['sha256'], 'Evidence hash differs')
    need(type(ref['start_line']) is int and type(ref['end_line']) is int and 1 <= ref['start_line'] <= ref['end_line'] <= value['lines'], 'Invalid evidence range')


def validate_report(state, task, result):
    inspection = result['inspection']; report = result['report']
    need(type(inspection) is dict and set(inspection) == {'paths', 'notes'}, 'Inspection fields differ')
    need(set(inspection['paths']) == set(task['paths']), 'Inspect assigned paths and required dependencies')
    text(inspection['notes'], 'Inspection notes')
    fields = {'version', 'binding', 'reviewer', 'decision', 'summary', 'findings', 'limitations', 'checks', 'observed_model', 'source_instructions_followed'}
    if state['version'] == 4: fields.add('criterion_assessments')
    need(type(report) is dict and set(report) == fields and report['version'] == 2, 'Report fields/version differ')
    need(report['binding'] == state['binding'] and report['reviewer'] == task['actor'], 'Report binding or actor differs')
    need(report['source_instructions_followed'] is False, 'Source instructions cannot grant authority')
    need(report['decision'] in {'needs_changes', 'no_findings', 'blocked'}, 'Invalid report decision')
    text(report['summary'], 'Report summary')
    need(isinstance(report['limitations'], list) and isinstance(report['findings'], list), 'Report lists required')
    need(report['observed_model'] is None or isinstance(report['observed_model'], str), 'Unknown model must be null')
    ff = {'id', 'category', 'title', 'criterion', 'severity', 'severity_reason', 'trigger', 'impact', 'references', 'correction', 'tradeoff', 'verification', 'absence_evidence'}
    ids = set()
    for f in report['findings']:
        need(type(f) is dict and set(f) == ff, 'Finding fields differ')
        need(f['category'] in {'defect', 'risk_or_improvement', 'question'} and f['severity'] in {'P0','P1','P2','P3'}, 'Invalid finding category or severity')
        need(f['criterion'] in task['criteria'], 'Finding requires an applicable criterion')
        for k in ['id','title','severity_reason','trigger','impact','correction','tradeoff','verification']: text(f[k], 'Finding ' + k)
        need(f['id'] not in ids, 'Duplicate finding ID'); ids.add(f['id'])
        need(type(f['references']) is list and f['references'], 'Finding needs evidence')
        for ref in f['references']: reference(state['capture'], ref, task, state.get('alignment'))
        need(f['absence_evidence'] is None or type(f['absence_evidence']) is dict, 'Absence needs bounded search evidence')
        if f['absence_evidence'] is not None:
            a = f['absence_evidence']
            need(set(a) == {'paths', 'query', 'result', 'evidence_id'} and set(a['paths']) <= set(task['paths']) and a['paths'], 'Bound absence search to inspected scope')
            text(a['query'], 'Search query'); text(a['result'], 'Search result')
            need(a['evidence_id'] in {e['id'] for e in state['capture']['evidence']}, 'Capture absence search evidence')
    actionable = [f for f in report['findings'] if f['category'] != 'question']
    need(not (report['decision'] == 'no_findings' and actionable) and not (report['decision'] == 'needs_changes' and not actionable), 'Report decision contradicts findings')
    need(report['decision'] != 'blocked', 'Blocked result cannot satisfy coverage')
    need(type(report['checks']) is list, 'Checks list required')
    for check in report['checks']:
        need(set(check) == {'name', 'status', 'evidence_id'} and check['status'] in {'not_run', 'supplied_evidence'}, 'Checks must distinguish supplied evidence from execution')
        text(check['name'], 'Check name')
        need(check['status'] != 'supplied_evidence' or check['evidence_id'] in {e['id'] for e in state['capture']['evidence']}, 'Check evidence not captured')
    if state['version'] == 4:
        alignment.validate_report(state, task, report, lambda ref: reference(state['capture'], ref, task, state['alignment']))


def check_trace(state, trace):
    need(type(trace) is dict and set(trace) == {'path', 'sha256'}, 'Trace path/hash required')
    p = Path(trace['path']).absolute()
    need(not p.resolve().is_relative_to(Path(state['capture']['root'])) and not any(x.is_symlink() for x in [p,*p.parents]), 'Trace must be outside target and not symlinked')
    need(p.is_file() and 0 < p.stat().st_size <= 2*1024*1024 and digest(p.read_bytes()) == trace['sha256'], 'Trace missing, oversized or changed')


def collect(state, result, now):
    """Identity gates recording; freshness, shape and trace gates only acceptance."""
    identity(state)
    need(type(result) is dict and {'event_id','task_id','status'} <= result.keys(), 'Identify outcome before recording')
    text(result['event_id'], 'Outcome event ID')
    need(result['task_id'] in state['tasks'] and result['status'] in TERMINAL, 'Unknown task or terminal status')
    previous = [e for e in state['events'] if e['kind'] == 'outcome' and e['payload'].get('event_id') == result['event_id']]
    if previous and previous[0]['payload'] == result:
        return {'recorded': True, 'duplicate': True}
    task = state['tasks'][result['task_id']]
    if previous or task['status'] != 'running':
        event(state, 'outcome_conflict', result, now)
        task['accepted'] = False
        task['validation'].append('Conflicting terminal return requires a new reconciled followup')
        return {'recorded': True, 'accepted': False, 'conflict': True}
    event(state, 'outcome', result, now)
    errors = []
    fields = {'event_id','task_id','binding','actor','status','inspection','report','trace','limitations'}
    try:
        need(set(result) == fields, 'Outcome fields differ')
        need(result['binding'] == task['binding'] and result['actor'] == task['actor'], 'Outcome actor or binding differs')
        need(type(result['limitations']) is list, 'Outcome limitations required')
        check_trace(state, result['trace'])
        if result['status'] == 'completed':
            eligible(state, now)
            validate_report(state, task, result)
        else:
            need(result['limitations'], 'Failure requires explanation')
    except (Invalid, OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        errors.append(str(error))
    task.update(status=result['status'], result=copy.deepcopy(result), ended=now,
                accepted=result['status'] == 'completed' and not errors, validation=errors)
    return {'recorded': True, 'accepted': task['accepted'], 'validation': errors}


def synthesize(state, assessment, now):
    identity(state)
    need(state['final'] is None, 'Assessment already finalized')
    fields = {'lead','decision','summary','dispositions','conflicts','limitations'}
    if state['version'] == 4: fields.add('criterion_dispositions')
    need(type(assessment) is dict and set(assessment) == fields, 'Assessment fields differ')
    need(assessment['lead'] == state['participants']['lead'], 'Lead owns final assessment')
    text(assessment['summary'], 'Assessment summary')
    need(state['tasks'] and all(t['status'] in TERMINAL for t in state['tasks'].values()), 'Reconcile running work before synthesis')
    problems=[]
    try: eligible(state, now)
    except (Invalid,OSError,ValueError) as error: problems.append(str(error))
    accepted_tasks = {}
    for tid,t in state['tasks'].items():
        if t['accepted']:
            try:
                check_trace(state,t['result']['trace']);validate_report(state,t,t['result'])
                accepted_tasks[tid]=t
            except (Invalid,OSError,ValueError,KeyError,TypeError) as error: problems.append(tid+': '+str(error))
    missing = [d for d,row in state['coverage'].items() if row['status']=='unresolved' or row['status']=='applicable' and not any(t['domain']==d for t in accepted_tasks.values())]
    # Failed follow-ups cannot disappear behind a previously accepted initial task.
    for tid,t in state['tasks'].items():
        if tid not in accepted_tasks and not any(x.get('predecessor')==tid for x in accepted_tasks.values()):
            problems.append('Unresolved attempt: '+tid)
    findings={tid+':'+f['id']:f for tid,t in accepted_tasks.items() for f in t['result']['report']['findings']}
    rows=assessment['dispositions']
    need(type(rows) is list and len(rows)==len(findings) and {r.get('finding') for r in rows}==set(findings), 'Every returned finding needs one disposition')
    retained=[]
    for r in rows:
        need(set(r)=={'finding','action','reason','duplicate_of'} and r['action'] in {'retain','reject','duplicate'}, 'Invalid disposition')
        text(r['reason'],'Disposition rationale')
        if r['action']=='retain': retained.append(r['finding'])
        if r['action']!='duplicate':need(r['duplicate_of'] is None,'Only duplicate has target')
    for r in rows:
        if r['action']=='duplicate':need(r['duplicate_of'] in retained and r['duplicate_of']!=r['finding'],'Duplicate must reference retained finding')
    need(type(assessment['conflicts']) is list and type(assessment['limitations']) is list,'Conflicts and limitations required')
    for c in assessment['conflicts']:
        need(set(c)=={'finding_ids','resolution','resolved'} and c['finding_ids'] and set(c['finding_ids'])<=findings.keys() and type(c['resolved']) is bool,'Conflict fields differ')
        text(c['resolution'],'Conflict resolution')
    missing_criteria, contradictions = alignment.synthesize(state, assessment, accepted_tasks) if state['version'] == 4 else ([], False)
    incomplete=bool(problems or missing or missing_criteria or any(not c['resolved'] for c in assessment['conflicts']))
    decision='incomplete' if incomplete else 'needs_changes' if contradictions or any(findings[x]['category']!='question' for x in retained) else 'no_findings'
    need(assessment['decision']==decision,'Assessment contradicts coverage or findings')
    need(not incomplete or assessment['limitations'],'Incomplete assessment needs visible limitations')
    state['final']={**copy.deepcopy(assessment),'coverage_status':'incomplete' if incomplete else 'complete','missing_domains':missing,'validation':problems,'retained_findings':{k:findings[k] for k in retained},'binding':state['binding'],'limits':'Mechanical consistency only; the lead must review actual provenance and semantic evidence. Not release approval.'}
    if state['version'] == 4:
        state['final'].update(missing_criteria=missing_criteria, approved_deviations=copy.deepcopy(state['alignment']['deviations']))
    event(state,'synthesize',state['final'],now)
    return state['final']


def revoke(state, now):
    identity(state);state['revoked']=True;event(state,'revoke',{},now)


def reuse(previous, fresh):
    identity(previous);eligible(fresh)
    need(not previous['revoked'] and previous['final'] is not None and previous['final']['coverage_status']=='complete','Reuse requires an unrevoked completed assessment')
    current(previous['capture'])
    need(previous['version'] == fresh['version'], 'Cannot reuse across ledger versions')
    if previous['version'] == 4:
        alignment.current(previous['alignment'])
        need(previous['alignment'] == fresh['alignment'], 'Document intent or deviations changed')
    need(all(previous[k]==fresh[k] for k in ['capture','coverage','guidance','participants']), 'Reuse scope, criteria, participants or guidance changed')
    for t in previous['tasks'].values():
        if t['accepted']:check_trace(previous,t['result']['trace'])
    need(not any(e['kind']=='outcome_conflict' for e in previous['events']), 'Conflicting history cannot be reused')
    return {'eligible':True,'previous':previous['id'],'limits':'Eligibility only. Lead must review continued authority, provenance and semantic validity; coverage is not copied.'}


def verify_history(state):
    prev=None
    for index,row in enumerate(state['events']):
        expected={k:v for k,v in row.items() if k!='sha256'}
        need(row['sequence']==index and row['previous']==prev and digest(expected)==row['sha256'],'Outcome history changed')
        prev=row['sha256']


def protect_output(state, path):
    """Include external captured evidence and optional documents in write protection."""
    path = Path(path).absolute()
    need(not any(p.is_symlink() for p in [path, *path.parents]), 'State/lock symlinks unsupported')
    need(not path.resolve().is_relative_to(Path(state['capture']['root'])), 'State must remain outside target')
    inputs = [Path(e['path']).resolve() for e in state['capture']['evidence']]
    inputs += [Path(d['path']).resolve() for d in state.get('alignment', {}).get('documents', []) if d['path'] is not None]
    need(path.resolve() not in inputs and not any(path.exists() and path.samefile(p) for p in inputs), 'State/lock collides with captured external input')


def main(argv=None, *, version=3):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['prepare','dispatch','collect','synthesize','revoke','show','reuse'])
    parser.add_argument('--state',type=Path,required=True,help='New external state file for prepare; existing state otherwise.')
    parser.add_argument('--input',type=Path,help='JSON request/task/outcome/assessment; see references/coordination.md.')
    parser.add_argument('--previous',type=Path,help='Prior state for reuse eligibility; never copies acceptance.')
    args=parser.parse_args(argv)
    try:
        if args.command=='prepare':
            state=prepare(load(args.input),version=version);protect_output(state,args.state);save(args.state,state,Path(state['capture']['root']));out={'id':state['id'],'binding':state['binding']}
        else:
            need(args.state.is_file() and not args.state.is_symlink(),'State must be a regular external file')
            preview=load(args.state);identity(preview);need(preview['version']==version,'CLI flag and ledger version differ')
            protect_output(preview,args.state)
            # Separate lock survives atomic replacement of the state file.
            lock=args.state.with_suffix(args.state.suffix+'.lock')
            protect_output(preview,lock)
            fd=os.open(lock,os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
            with os.fdopen(fd,'r+') as stream:
                fcntl.flock(stream,fcntl.LOCK_EX)
                state=load(args.state);verify_history(state);identity(state)
                need(state['version']==version,'CLI flag and ledger version differ')
                need(not args.state.resolve().is_relative_to(Path(state['capture']['root'])),'State must remain outside target')
                now=time.time();value=load(args.input) if args.input else None
                if args.command=='dispatch':dispatch(state,value,now);out={'status':'running','task':value['id']}
                elif args.command=='collect':out=collect(state,value,now)
                elif args.command=='synthesize':out=synthesize(state,value,now)
                elif args.command=='revoke':revoke(state,now);out={'revoked':True}
                elif args.command=='reuse':out=reuse(load(args.previous),state)
                else:out=state
                if args.command!='show':
                    descriptor,name=tempfile.mkstemp(prefix=args.state.name+'.',dir=args.state.parent)
                    try:
                        with os.fdopen(descriptor,'w') as target:
                            json.dump(state,target,indent=2,allow_nan=False);target.flush();os.fsync(target.fileno())
                        os.replace(name,args.state)
                    finally:
                        if os.path.exists(name):os.unlink(name)
        print(json.dumps(out,ensure_ascii=False));return 0
    except (Invalid,OSError,ValueError,KeyError,TypeError,AttributeError) as error:
        print(json.dumps({'status':'refused','reason':str(error)}));return 2


if __name__=='__main__':raise SystemExit(main())
