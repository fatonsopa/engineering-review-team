"""V4 optional intent context and exact criterion coverage. No target execution."""
from pathlib import Path

from review_contract import need, source
from review_manifest import text

DOMAINS = {'implementation', 'architecture', 'security', 'data', 'testing', 'operations'}
STATUSES = {'satisfied', 'contradicted', 'partially_satisfied', 'not_assessed'}


def capture(value, snap):
    need(type(value) is dict and set(value) == {'documents', 'criterion_sources', 'deviations'}, 'Alignment fields differ')
    need(type(value['documents']) is list and type(value['deviations']) is list, 'Document/deviation lists required')
    criteria = {c['id']: c for c in snap['criteria']}
    for c in criteria.values():
        domains = c['required_domains']
        need(domains and len(domains) == len(set(domains)) and set(domains) <= DOMAINS, 'V4 criterion needs distinct required domains')
    documents = []; sections = {}
    for item in value['documents']:
        fields = {'id', 'path', 'origin', 'version', 'status', 'authority', 'reason', 'sections'}
        need(type(item) is dict and set(item) == fields, 'Document fields differ')
        for k in ['id', 'origin', 'version', 'reason']: text(item[k], 'Document ' + k)
        need(':' not in item['id'] and item['id'] not in {d['id'] for d in documents}, 'Duplicate or ambiguous document ID')
        need(item['status'] in {'available', 'missing', 'stale', 'conflicting', 'not_applicable'}, 'Unknown document status')
        need(item['authority'] in {'agreed', 'proposed', 'unknown', 'superseded'}, 'Unknown document authority')
        need(type(item['sections']) is list, 'Document sections required')
        doc = dict(item)
        if item['path'] is None:
            need(item['status'] in {'missing', 'not_applicable'} and not item['sections'], 'Uncaptured document cannot supply sections')
            doc['capture'] = None
        else:
            need(item['status'] not in {'missing', 'not_applicable'}, 'Unavailable document must have null path')
            p = Path(item['path'])
            need(p.is_absolute() and not any(x.is_symlink() for x in [p, *p.parents]), 'Document needs an absolute non-symlink path')
            root = Path(snap['root'])
            if p.is_relative_to(root):
                need(p.relative_to(root).as_posix() in snap['files'], 'Internal document must be in captured source')
            doc['capture'] = source(p.parent, p.name)
        for section in item['sections']:
            need(type(section) is dict and set(section) == {'id', 'start_line', 'end_line', 'criteria', 'domains'}, 'Section fields differ')
            text(section['id'], 'Section ID'); token = item['id'] + ':' + section['id']
            need(':' not in section['id'] and token not in sections, 'Duplicate or ambiguous section ID')
            need(type(section['criteria']) is list and len(section['criteria']) == len(set(section['criteria'])) and set(section['criteria']) <= criteria.keys(), 'Section criterion IDs differ')
            need(type(section['domains']) is list and section['domains'] and len(section['domains']) == len(set(section['domains'])) and set(section['domains']) <= DOMAINS, 'Section needs distinct known domain recipients')
            a, b = section['start_line'], section['end_line']
            need(type(a) is int and type(b) is int and 1 <= a <= b <= doc['capture']['lines'], 'Section line bounds differ')
            sections[token] = (doc, section)
        documents.append(doc)
    sources = value['criterion_sources']
    need(type(sources) is dict and set(sources) == criteria.keys(), 'Map every criterion to an authoritative section or null for explicit task criteria')
    for cid, token in sources.items():
        if token is None:
            continue
        need(type(token) is str and token in sections, 'Unknown criterion source section')
        doc, section = sections[token]
        need(doc['status'] == 'available' and doc['authority'] == 'agreed', 'Only available agreed document intent can bind a criterion')
        need(cid in section['criteria'] and set(criteria[cid]['required_domains']) <= set(section['domains']), 'Criterion source must reach every required domain')
    deviations = value['deviations']; ids = set()
    for d in deviations:
        need(type(d) is dict and set(d) == {'id', 'criterion', 'domain', 'evidence_id', 'reason'}, 'Deviation fields differ')
        text(d['id'], 'Deviation ID'); text(d['reason'], 'Deviation reason')
        need(d['id'] not in ids, 'Duplicate deviation ID'); ids.add(d['id'])
        need(d['criterion'] in criteria and d['domain'] in criteria[d['criterion']]['required_domains'], 'Deviation must identify an applicable criterion/domain')
        need(d['evidence_id'] in {e['id'] for e in snap['evidence']}, 'Deviation needs captured approval evidence; lead must verify its meaning and authority')
    return {'documents': documents, 'criterion_sources': dict(sources), 'deviations': deviations}


def current(alignment):
    for doc in alignment['documents']:
        if doc['capture'] is not None:
            p = Path(doc['path'])
            need(not any(x.is_symlink() for x in [p, *p.parents]) and source(p.parent, p.name) == doc['capture'], 'Project document drifted: ' + doc['id'])


def routes(alignment, task):
    return sorted(d['id'] + ':' + s['id'] for d in alignment['documents'] for s in d['sections']
                  if task['domain'] in s['domains'] and (not s['criteria'] or set(s['criteria']) & set(task['criteria'])))


def dispatch(state, task):
    need(type(task['documents']) is list and sorted(task['documents']) == routes(state['alignment'], task), 'Task must carry exactly its relevant captured document sections')
    criteria = {c['id']: c for c in state['capture']['criteria']}
    need(all(task['domain'] in criteria[c]['required_domains'] for c in task['criteria']), 'Task criterion is not assigned to this domain')


def reference(alignment, ref, task):
    need(ref['kind'] == 'document', 'Unknown alignment evidence kind')
    doc = next((d for d in alignment['documents'] if d['id'] == ref['id']), None)
    need(doc is not None and doc['capture'] is not None, 'Uncaptured document reference')
    need(ref['sha256'] == doc['capture']['sha256'], 'Document reference hash differs')
    a, b = ref['start_line'], ref['end_line']
    need(type(a) is int and type(b) is int and any(doc['id'] + ':' + s['id'] in task['documents'] and s['start_line'] <= a <= b <= s['end_line'] for s in doc['sections']), 'Document citation must remain inside assigned section')


def deviation(alignment, identifier, criterion, domain):
    need(identifier is None or any(d['id'] == identifier and d['criterion'] == criterion and d['domain'] == domain for d in alignment['deviations']), 'Unknown or unrelated approved deviation')


def validate_report(state, task, report, validate_reference):
    rows = report['criterion_assessments']
    need(type(rows) is list and len(rows) == len(task['criteria']) and {r.get('criterion') for r in rows} == set(task['criteria']), 'Every assigned criterion needs exactly one assessment')
    findings = {f['id']: f for f in report['findings']}
    for row in rows:
        need(type(row) is dict and set(row) == {'criterion', 'status', 'rationale', 'references', 'findings', 'deviation_id'}, 'Criterion assessment fields differ')
        cid = row['criterion']; status = row['status']
        need(status in STATUSES, 'Unknown criterion assessment status'); text(row['rationale'], 'Criterion rationale')
        need(type(row['references']) is list and (row['references'] or status == 'not_assessed'), 'Assessed criterion needs actual evidence')
        for ref in row['references']: validate_reference(ref)
        need(type(row['findings']) is list and len(row['findings']) == len(set(row['findings'])) and all(f in findings and findings[f]['criterion'] == cid for f in row['findings']), 'Assessment finding links differ')
        linked = {f['id'] for f in findings.values() if f['criterion'] == cid}
        need(set(row['findings']) == linked, 'Criterion assessment must include all related findings')
        deviation(state['alignment'], row['deviation_id'], cid, task['domain'])
        defects = [findings[f] for f in linked if findings[f]['category'] == 'defect']
        need(status != 'contradicted' or defects or row['deviation_id'] is not None, 'Contradiction needs a defect finding or captured approved deviation')
        need(status != 'satisfied' or not defects, 'Satisfied criterion contradicts returned defect')
        need(row['deviation_id'] is None or status == 'contradicted', 'Approved deviation records a contradiction separately; it does not assert conformance')
        need(status not in {'not_assessed', 'partially_satisfied'} or report['limitations'], 'Incomplete criterion needs visible limitations')


def synthesize(state, assessment, accepted):
    expected = {(c['id'], d) for c in state['capture']['criteria'] for d in c['required_domains']}
    rows = assessment['criterion_dispositions']
    need(type(rows) is list and len(rows) == len(expected) and {(r.get('criterion'), r.get('domain')) for r in rows} == expected, 'Every required criterion/domain needs exactly one final disposition')
    latest = {}
    for tid, task in accepted.items():
        for r in task['result']['report']['criterion_assessments']:
            latest[r['criterion'], task['domain']] = (tid, r)
    missing = []; contradictions = False
    for r in rows:
        need(type(r) is dict and set(r) == {'criterion', 'domain', 'status', 'task', 'rationale', 'deviation_id'}, 'Final criterion disposition fields differ')
        text(r['rationale'], 'Final criterion rationale'); pair = (r['criterion'], r['domain'])
        actual = latest.get(pair)
        if actual is None:
            need(r['status'] == 'not_assessed' and r['task'] is None and r['deviation_id'] is None, 'Unassigned criterion cannot be reported assessed')
        else:
            tid, row = actual
            need(r['task'] == tid and r['status'] == row['status'] and r['deviation_id'] == row['deviation_id'], 'Final criterion must match latest accepted assessment; resolve disagreement through followup')
        if r['status'] in {'not_assessed', 'partially_satisfied'}: missing.append({'criterion':pair[0], 'domain':pair[1]})
        contradictions |= r['status'] == 'contradicted' and r['deviation_id'] is None
    return missing, contradictions
