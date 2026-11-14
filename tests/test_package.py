"""Small installation safety and shipped-document checks; no model calls."""
import importlib.util
from pathlib import Path
import re
import tempfile
import tomllib
import unittest
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts/install_skill.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / "source"
        for directory in ("references", "assets/codex", "assets/claude", "scripts", "config"):
            (self.source / directory).mkdir(parents=True, exist_ok=True)
        for name, text in {
            "SKILL.md": "---\nname: engineering-review\n---\n# Review\n",
            "README.md": "# Install\n", "LICENSE": "license\n",
            "references/policy.md": "policy\n", "scripts/install_skill.py": "# installer\n",
            "scripts/check_review.py": "# acceptance checker\n",
            "config/obsolete.json": "{}",
        }.items():
            (self.source / name).write_text(text)
        for role in ("lead", "implementation"):
            name = f"engineering-review-{role}"
            (self.source / f"assets/codex/{name}.toml").write_text(
                f'name = "{name}"\ndescription = "Authored native review fixture"\ndeveloper_instructions = "Read {{{{SKILL_ROOT}}}}/references/policy.md"\n')
            (self.source / f"assets/claude/{name}.md").write_text(
                f"---\nname: {name}\ntools: Read, Glob, Grep\n---\nRead {{{{SKILL_ROOT}}}}/references/policy.md\n")

    def test_install_selection_and_nonempty_refusal(self):
        target = self.base / "installed"
        installer.install(self.source, "codex", target)
        self.assertEqual((target / "SKILL.md").read_bytes(), (self.source / "SKILL.md").read_bytes())
        self.assertTrue((target / "scripts/install_skill.py").is_file())
        self.assertEqual((target / "scripts/check_review.py").read_bytes(),
                         (self.source / "scripts/check_review.py").read_bytes())
        self.assertFalse((target / "config").exists())
        with self.assertRaises(ValueError):
            installer.install(self.source, "codex", target)
        with self.assertRaises(ValueError):
            installer.install(self.source, "codex", self.source / "nested")
        with self.assertRaises(ValueError):
            installer.install(self.source, "codex", self.base)
        self.assertFalse((self.source / "nested").exists())

    def test_registration_preview_render_and_idempotence(self):
        for host, suffix in (("codex", ".toml"), ("claude-code", ".md")):
            target = self.base / host
            result = installer.register_agents(self.source, host, target, preview=True)
            self.assertEqual(len(result["agents"]), 2)
            if host == "codex":
                bindings = tomllib.loads(result["codex_configuration"])["agents"]
                for name, binding in bindings.items():
                    self.assertEqual(binding["config_file"], str(target / (name + suffix)))
                    self.assertEqual(binding["description"], "Authored native review fixture")
            self.assertFalse(target.exists())
            installer.register_agents(self.source, host, target)
            paths = sorted(target.glob("*"))
            before = [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths]
            self.assertTrue(all(str(self.source) in p.read_text() for p in paths))
            self.assertTrue(all(p.suffix == suffix for p in paths))
            result = installer.register_agents(self.source, host, target)
            self.assertTrue(all(a["status"] == "unchanged" for a in result["agents"]))
            self.assertEqual(before, [(p.read_bytes(), p.stat().st_mtime_ns) for p in paths])

    def test_conflict_preflight_writes_nothing(self):
        target = self.base / "agents"
        target.mkdir()
        conflict = target / "engineering-review-lead.toml"
        conflict.write_text("custom")
        with self.assertRaises(ValueError):
            installer.register_agents(self.source, "codex", target)
        self.assertEqual([p.name for p in target.iterdir()], [conflict.name])
        self.assertEqual(conflict.read_text(), "custom")

    def test_incomplete_codex_metadata_is_rejected_before_registration(self):
        asset = self.source / "assets/codex/engineering-review-lead.toml"
        asset.write_text('name = "engineering-review-lead"\ndeveloper_instructions = "Read sources"\n')
        target = self.base / "agents"
        with self.assertRaisesRegex(ValueError, "metadata is incomplete"):
            installer.register_agents(self.source, "codex", target)
        self.assertFalse(target.exists())

    def test_symlinks_refused(self):
        alias = self.base / "alias"
        alias.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError):
            installer.install(alias, "codex", self.base / "installed")
        (self.source / "references/linked.md").symlink_to(self.source / "README.md")
        with self.assertRaises(ValueError):
            installer.install(self.source, "codex", self.base / "installed")
        target = self.base / "agents"
        target.mkdir()
        (target / "engineering-review-lead.toml").symlink_to(self.source / "README.md")
        with self.assertRaises(ValueError):
            installer.register_agents(self.source, "codex", target)
        self.assertEqual(len(list(target.iterdir())), 1)

    def test_archive_selection_and_conflict(self):
        output = self.base / "skill.zip"
        installer.make_archive(self.source, output)
        with zipfile.ZipFile(output) as archive:
            self.assertIn("engineering-review/SKILL.md", archive.namelist())
            self.assertIn("engineering-review/scripts/install_skill.py", archive.namelist())
            self.assertFalse(any("config/" in p for p in archive.namelist()))
            self.assertEqual(archive.read("engineering-review/SKILL.md"), (self.source / "SKILL.md").read_bytes())
        with self.assertRaises(ValueError):
            installer.make_archive(self.source, output)
        with self.assertRaises(ValueError):
            installer.make_archive(self.source, self.source / "skill.zip")


class PackageTests(unittest.TestCase):
    def test_native_assets(self):
        codex = sorted((ROOT / "assets/codex").glob("*.toml"))
        claude = sorted((ROOT / "assets/claude").glob("*.md"))
        self.assertEqual(len(codex), 11)
        self.assertEqual({p.stem for p in codex}, {p.stem for p in claude})
        for path in codex:
            data = tomllib.loads(path.read_text())
            self.assertEqual(data["name"], path.stem)
            self.assertTrue(data["description"])
            self.assertTrue(data["developer_instructions"])
        for path in claude:
            parts = path.read_text().split("---\n", 2)
            self.assertEqual(parts[0], "")
            self.assertEqual(len(parts), 3)
            fields = dict(line.split(": ", 1) for line in parts[1].splitlines() if ": " in line)
            self.assertEqual(fields["name"], path.stem)
            self.assertTrue(fields["description"])
            self.assertEqual(fields["tools"], "Read, Glob, Grep")
            self.assertTrue(parts[2].strip())
            heading, _, instructions = parts[2].strip().partition("\n")
            self.assertTrue(heading.startswith("# "))
            counterpart = tomllib.loads((ROOT / "assets/codex" / (path.stem + ".toml")).read_text())
            self.assertEqual(instructions.strip(), counterpart["developer_instructions"].strip())

    def test_local_links_and_native_resource_paths(self):
        files = list(ROOT.glob("*.md")) + list((ROOT / "references").rglob("*.md"))
        files += list((ROOT / "assets").rglob("*.md")) + list((ROOT / "assets").rglob("*.toml"))
        for path in files:
            text = path.read_text()
            for link in re.findall(r"\]\(([^)]+)\)", text):
                target = link.split("#", 1)[0].strip("<>")
                if not target or re.match(r"[a-zA-Z][\w+.-]*:", target):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), link=link):
                    self.assertTrue((path.parent / unquote(target)).exists(), f"Missing local link: {target}")
            for resource in re.findall(r"\{\{SKILL_ROOT\}\}/([\w./-]+)", text):
                with self.subTest(file=str(path.relative_to(ROOT)), resource=resource):
                    self.assertTrue((ROOT / resource.rstrip(".")).is_file())


if __name__ == "__main__":
    unittest.main()
