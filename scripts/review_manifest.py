"""Versioned read-only source and external evidence manifests."""
import hashlib
import json
from pathlib import Path
import subprocess

from review_contract import Invalid, need, source

MAX_FILES = 4096


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def text(value, label):
    need(isinstance(value, str) and value.strip(), label + ' must be nonempty text')
    return value


def relative(name):
    text(name, 'Path')
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and '\\' not in name, 'Path leaves root')
    return p.as_posix()


def git_identity(root):
    def call(*args):
        p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, timeout=10)
        return p.stdout.decode('utf-8', errors='replace').strip() if p.returncode == 0 else None
    top = call('rev-parse', '--show-toplevel')
    if not top:
        return {'kind': 'filesystem'}
    return {'kind': 'git', 'repository': top, 'head': call('rev-parse', 'HEAD')}


def inventory(root, scopes, exclusions):
    """Inspect the explicit scope, without following symlinks or reading excluded bytes."""
    need(isinstance(scopes, list) and scopes, 'Declare nonempty source scope')
    need(isinstance(exclusions, list), 'Declare exclusions')
    omitted = []
    for item in exclusions:
        need(set(item) == {'path', 'reason'}, 'Exclusions need path and reason')
        omitted.append(relative(item['path']).rstrip('/'))
        text(item['reason'], 'Exclusion reason')
    result = {}
    def visit(path):
        name = path.relative_to(root).as_posix()
        if any(name == x or name.startswith(x + '/') for x in omitted):
            return
        if path.name in {'.git', '.DS_Store', '__pycache__'}:
            return
        need(not path.is_symlink(), 'Source symlinks unsupported: ' + name)
        if path.is_dir():
            for child in sorted(path.iterdir()):
                visit(child)
        else:
            need(path.is_file(), 'Missing source scope: ' + name)
            need(len(result) < MAX_FILES, 'Scope exceeds inventory limit; partition the review')
            # Use the protected, bounded UTF-8 reader shared with legacy captures.
            result[name] = source(root, name)['sha256']
    for name in scopes:
        relative(name)
        visit(root / name)
    need(result, 'Scope has no supported reviewable files')
    return result


def external(item, root):
    need(type(item) is dict and set(item) == {'id', 'path', 'origin'}, 'External evidence needs id, path and origin')
    text(item['id'], 'Evidence ID'); text(item['origin'], 'Evidence origin')
    p = Path(item['path'])
    need(p.is_absolute(), 'Evidence requires an absolute path')
    need(p.is_absolute() and not p.resolve().is_relative_to(root), 'Evidence must remain outside target')
    need(not any(x.is_symlink() for x in [p, *p.parents]), 'Evidence symlinks unsupported')
    value = source(p.parent, p.name)
    return {**item, 'path': str(p), **value}


def capture(request):
    root = Path(request['root']).absolute()
    need(root.is_dir() and root.resolve() == root, 'Use an explicit real root')
    profile = request['profile']
    fields = {'mode', 'scope', 'exclusions', 'systems', 'versions', 'critical_flows', 'assumptions'}
    need(type(profile) is dict and set(profile) == fields, 'Profile fields differ')
    need(profile['mode'] in {'change', 'component', 'project'}, 'Unknown review mode')
    for name in ['systems', 'versions', 'critical_flows', 'assumptions']:
        need(isinstance(profile[name], list) and all(isinstance(x, str) for x in profile[name]), 'Profile list required: ' + name)
    need(profile['systems'] and profile['critical_flows'], 'Discover system type and critical flows')
    files = inventory(root, profile['scope'], profile['exclusions'])
    paths = request['paths']
    need(isinstance(paths, list) and 0 < len(paths) <= 64 and len(paths) == len(set(paths)), 'Capture 1..64 distinct files per partition')
    need(set(paths) <= files.keys(), 'Captured file is outside declared scope')
    criteria = request['criteria']
    need(isinstance(criteria, list) and criteria, 'Explicit criteria required')
    for c in criteria:
        need(type(c) is dict and set(c) == {'id', 'text', 'origin', 'required_domains'}, 'Criterion fields differ')
        for k in ['id', 'text', 'origin']: text(c[k], 'Criterion ' + k)
        need(type(c['required_domains']) is list, 'Required domains must be explicit')
    need(len({c['id'] for c in criteria}) == len(criteria), 'Duplicate criterion ID')
    evidence = [external(item, root) for item in request['evidence']]
    need(len({e['id'] for e in evidence}) == len(evidence), 'Duplicate evidence ID')
    return {'version': 2, 'root': str(root), 'profile': profile, 'identity': git_identity(root),
            'inventory': files, 'files': {name: source(root, name) for name in paths},
            'criteria': criteria, 'evidence': evidence,
            'limits': 'Only declared scope and captured dependencies are covered; provenance fields are claims.'}


def current(snap):
    need(snap.get('version') == 2, 'Unsupported capture version')
    root = Path(snap['root'])
    need(root.resolve() == root, 'Source root changed')
    p = snap['profile']
    need(inventory(root, p['scope'], p['exclusions']) == snap['inventory'], 'Declared source scope drifted')
    need(git_identity(root) == snap['identity'], 'Source revision changed')
    for name, old in snap['files'].items():
        need(source(root, name) == old, 'Captured source drifted: ' + name)
    for e in snap['evidence']:
        need(external({k: e[k] for k in ['id', 'path', 'origin']}, root) == e, 'External evidence drifted')
    return root
