#!/usr/bin/env python3
"""Copy Engineering Review, register its native agents, or create a ZIP (Python 3.11+)."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
import zipfile


HOSTS = {"codex": ("codex", ".toml"), "claude-code": ("claude", ".md")}


def checked_path(value):
    """Reject symlinks before resolving a user-supplied path."""
    path = Path(os.path.abspath(Path(value).expanduser()))
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError(f"Symlink paths are not supported: {path}")
    return path.resolve()


def skill_name(source):
    text = (source / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---\n", 2)
    match = re.search(r"^name:\s*['\"]?([a-z0-9]+(?:-[a-z0-9]+)*)['\"]?\s*$", parts[1], re.M) if len(parts) == 3 and not parts[0] else None
    if not match:
        raise ValueError("SKILL.md needs a valid name in its frontmatter.")
    return match[1]


def package_files(source):
    """Select only the skill, knowledge, native assets and standalone installer."""
    files = []
    for name in ("SKILL.md", "README.md", "LICENSE"):
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Required regular file missing: {path}")
        files.append(path)
    for name in ("references", "assets"):
        directory = source / name
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError(f"Required regular directory missing: {directory}")
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlink in package: {path}")
            if path.name == ".DS_Store" or any(p in {"__pycache__", ".pytest_cache"} for p in path.parts):
                continue
            if path.is_file():
                files.append(path)
            elif not path.is_dir():
                raise ValueError(f"Unsupported package entry: {path}")
    installer = source / "scripts" / "install_skill.py"
    if installer.exists() or installer.is_symlink():
        checked_path(installer)
        if not installer.is_file():
            raise ValueError("Installer must be a regular file.")
        files.append(installer)
    return files


def install(source, host, destination=None):
    if host not in HOSTS:
        raise ValueError("Unknown host.")
    source = checked_path(source)
    name = skill_name(source)
    files = package_files(source)
    default = Path.home() / (".agents" if host == "codex" else ".claude") / "skills" / name
    target = checked_path(destination if destination is not None else default)
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("Source and installation destination must not overlap.")
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise ValueError(f"Installation destination must be absent or empty: {target}")
    target.mkdir(parents=True, exist_ok=True)
    for path in files:
        output = target / path.relative_to(source)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, output)
    return {"destination": str(target), "files": len(files)}


def register_agents(source, host, destination, preview=False):
    if host not in HOSTS:
        raise ValueError("Unknown host.")
    source = checked_path(source)
    skill_name(source)
    subdir, suffix = HOSTS[host]
    directory = checked_path(source / "assets" / subdir)
    assets = sorted(directory.glob(f"engineering-review-*{suffix}"))
    if not assets:
        raise ValueError(f"No native assets found in {directory}")
    target = checked_path(destination)
    if target.exists() and not target.is_dir():
        raise ValueError("Agent destination must be a directory.")
    if target == source or source in target.parents or target in source.parents:
        raise ValueError("Agent destination and source must not overlap.")
    planned = []
    for asset in assets:
        if asset.is_symlink() or not asset.is_file():
            raise ValueError(f"Native asset must be a regular file: {asset}")
        text = asset.read_text(encoding="utf-8").replace("{{SKILL_ROOT}}", str(source))
        if host == "codex":
            import tomllib
            tomllib.loads(text)
        output = checked_path(target / asset.name)
        if output.exists() and (not output.is_file() or output.read_bytes() != text.encode("utf-8")):
            raise ValueError(f"Refusing to replace customized native agent: {output}")
        planned.append((output, text, output.exists()))
    if not preview:
        target.mkdir(parents=True, exist_ok=True)
        for output, text, exists in planned:
            if not exists:
                with output.open("x", encoding="utf-8", newline="") as stream:
                    stream.write(text)
    return {"source": str(source), "agents_dir": str(target), "preview": preview,
            "agents": [{"path": str(path), "status": "unchanged" if exists else "planned" if preview else "created"}
                       for path, _, exists in planned]}


def make_archive(source, output):
    source = checked_path(source)
    name = skill_name(source)
    files = package_files(source)
    output = checked_path(output)
    if output == source or source in output.parents:
        raise ValueError("Archive must be outside the source package.")
    if output.exists():
        raise ValueError(f"Archive already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        try:
            with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
                for path in files:
                    archive.write(path, str(Path(name) / path.relative_to(source)))
        except Exception:
            output.unlink()
            raise
    return {"archive": str(output), "files": len(files)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--host", choices=HOSTS)
    parser.add_argument("--destination", type=Path, help="Exact skill installation directory")
    parser.add_argument("--agents-dir", type=Path, help="Register native agents referencing --source")
    parser.add_argument("--preview", action="store_true", help="Preview agent registration without writing")
    parser.add_argument("--archive", type=Path, help="Create a ZIP instead of installing")
    args = parser.parse_args(argv)
    if args.archive:
        if args.host or args.destination or args.agents_dir or args.preview:
            parser.error("--archive cannot be combined with installation or registration options")
    elif not args.host:
        parser.error("--host is required for installation or registration")
    elif args.agents_dir and args.destination:
        parser.error("--agents-dir cannot be combined with --destination")
    elif args.preview and not args.agents_dir:
        parser.error("--preview requires --agents-dir")
    try:
        if args.archive:
            result = make_archive(args.source, args.archive)
        elif args.agents_dir:
            result = register_agents(args.source, args.host, args.agents_dir, args.preview)
        else:
            result = install(args.source, args.host, args.destination)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
