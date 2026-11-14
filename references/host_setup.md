# Set up host roles

Engineering Review Team is one skill with an optional lead and ten native specialist definitions. Normal review uses the current host. Registration writes role definitions; it does not prove which definition the host selected or that a role ran. Permission enforcement remains with the host.

## Install the skill

The standalone installer uses Python 3.11+ and the standard library:

```sh
python3 scripts/install_skill.py --host codex --destination /absolute/path/to/engineering-review
```

Use `--host claude-code` for Claude Code. An explicit `--source /path/to/package` selects another package source. The installer refuses a nonempty destination. It copies the skill, references, assets and installer without a Builder dependency.

## Register optional agents

From the installed skill, preview registration into your project's native agent directory:

```sh
python3 scripts/install_skill.py --host codex --source /absolute/path/to/engineering-review --agents-dir /path/to/project/.codex/agents --preview
python3 scripts/install_skill.py --host claude-code --source /absolute/path/to/engineering-review --agents-dir /path/to/project/.claude/agents --preview
```

Remove `--preview` to register. Existing identical files are retained; conflicts and symlinks are refused. The installer replaces `{{SKILL_ROOT}}` with the canonical source root. Ensure that root is readable under the host's actual permissions. Do not widen access by inventing an alias or editing unrelated global configuration. Restart the Claude Code session if needed after creating its agents directory.

For Codex, the installer's `codex_configuration` return field contains a native TOML snippet generated from the registered paths and descriptions; the installer does not edit user configuration. Merge those entries into the intended trusted native configuration, or pass the same `agents.NAME.config_file` and `agents.NAME.description` entries through CLI `-c` overrides. For example, replace the absolute placeholder with the registered file:

```toml
[agents.engineering-review-implementation]
config_file = "/absolute/path/to/project/.codex/agents/engineering-review-implementation.toml"
description = "Review code implementation against applicable requirements."
```

Explicit bindings avoid selecting an older same-name profile. Verify the selected definition in the actual session; this does not imply that directory discovery fails on every host version. Bindings retain parent permissions and inherited sandbox limits; they do not grant additional access.

Invoke the skill in the host's main context and use the available native agent tools. Inspect actual role discovery and instructions when troubleshooting. The main-context lead may dispatch; the bundled nested lead asks its parent for actions unavailable to it. Read-only leaves return to the lead and never delegate or execute target programs. Permission labels in prose are not a host sandbox.

## Package or troubleshoot

Create an archive with `python3 scripts/install_skill.py --source /path/to/package --archive /path/to/package.zip`. Keep the archive outside the source. For a loading or tool failure, report the actual missing capability and continue only supported review work; do not claim native activation from asset parsing alone.

See the official [Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents) for host behavior.
