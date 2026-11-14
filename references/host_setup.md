# Set up host roles

Engineering Review Team is one skill with an optional lead and ten native specialist definitions. Normal review uses the current host. Registration makes roles discoverable; it does not prove they ran or enforce permissions beyond the host's controls.

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

Invoke the skill in the host's main context and use the available native agent tools. Inspect actual role discovery and instructions when troubleshooting. The main-context lead may dispatch; the bundled nested lead asks its parent for actions unavailable to it. Read-only leaves return to the lead and never delegate or execute target programs. Permission labels in prose are not a host sandbox.

## Package or troubleshoot

Create an archive with `python3 scripts/install_skill.py --source /path/to/package --archive /path/to/package.zip`. Keep the archive outside the source. For a loading or tool failure, report the actual missing capability and continue only supported review work; do not claim native activation from asset parsing alone.

See the official [Codex subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents) and [Claude Code subagent documentation](https://code.claude.com/docs/en/sub-agents) for host behavior.
