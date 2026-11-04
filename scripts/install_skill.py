#!/usr/bin/env python3
"""Install the skill repository or make a host-upload ZIP."""
import argparse
import json
from pathlib import Path
import re
import sys
import os
import tempfile
import zipfile

from evaluate import copy_package, hash_tree


def skill_name(source):
    source = Path(source).resolve()
    text = (source / "SKILL.md").read_text()
    header = text.split("---\n", 2)
    match = re.search(r"^name:\s*['\"]?([a-z0-9]+(?:-[a-z0-9]+)*)['\"]?\s*$", header[1], re.M) if len(header) == 3 and not header[0] else None
    if not match:
        raise ValueError("The source needs valid SKILL.md name metadata.")
    return match[1]


def install(source, host, destination=None):
    source = Path(source).resolve()
    name = skill_name(source)
    base = Path.home() / (".agents/skills" if host == "codex" else ".claude/skills")
    destination = Path(destination).expanduser().resolve() if destination else base / name
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("Installation destination must be separate from the source.")
    files = copy_package(source, destination, profile="runtime")
    return {"status": "installed", "name": name, "host": host, "destination": str(destination), "files": len(files)}


def make_archive(source, output):
    source, output = Path(source).resolve(), Path(output).expanduser().resolve()
    name = skill_name(source)
    if output.is_relative_to(source):
        raise ValueError("Write the upload ZIP outside the source folder.")
    before = hash_tree(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="skill-upload-") as folder:
        stage = Path(folder) / name
        copy_package(source, stage, profile="runtime")
        files = hash_tree(stage)
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(descriptor, "wb") as stream, zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
                for relative in sorted(files):
                    archive.write(stage / relative, f"{name}/{relative}")
            if hash_tree(source) != before:
                raise ValueError("Source changed during packaging.")
        except Exception:
            output.unlink(missing_ok=True)
            raise
    return {"status": "packaged", "name": name, "path": str(output), "files": len(files)}


def register_agents(source, host, destination, preview=False):
    """Register selected package roles without overwriting customized host files."""
    source=Path(source).resolve();destination=Path(destination).absolute()
    if destination.resolve().is_relative_to(source) or destination.is_symlink():
        raise ValueError('Agent directory must be separate from package and not symlinked.')
    folder='codex' if host=='codex' else 'claude'
    roles=json.loads((source/'config/roles.json').read_text())
    extension='toml' if host=='codex' else 'md'
    files={}
    for role in ['lead',*roles['specialists']]:
        name=f'engineering-review-{role}.{extension}'
        content=(source/'assets'/folder/name).read_text().replace('{{SKILL_ROOT}}',str(source))
        target=destination/name
        if target.is_symlink() or target.exists() and target.read_text()!=content:
            raise ValueError('Preserve customized agent; conflicting destination: '+str(target))
        files[name]=content
    if not preview:
        destination.mkdir(parents=True,exist_ok=True)
        for name,content in files.items():
            target=destination/name
            if not target.exists():
                with target.open('x') as stream:stream.write(content)
    return {'status':'preview' if preview else 'registered','host':host,'skill_root':str(source),'destination':str(destination),'files':list(files),'limits':'Registration is not proof of host loading or behavior.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--host", choices=["codex", "claude-code"])
    action.add_argument("--archive", type=Path, help="Create an upload ZIP outside the source folder.")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--agents-dir',type=Path,help='Register role assets from an already installed --source; no skill copy.')
    parser.add_argument('--preview',action='store_true',help='Preview role registration without writing.')
    args = parser.parse_args()
    if args.archive and args.destination:
        parser.error("--destination is only used with --host.")
    try:
        if args.agents_dir:
            if not args.host or args.destination or args.archive:parser.error('--agents-dir requires --host and an already installed --source, without --destination/--archive')
            result=register_agents(args.source,args.host,args.agents_dir,args.preview)
        else:
            if args.preview:parser.error('--preview applies to --agents-dir')
            result = make_archive(args.source, args.archive) if args.archive else install(args.source, args.host, args.destination)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
