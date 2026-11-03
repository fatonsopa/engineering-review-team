# Set up host roles

Engineering Review is one skill installation. Agent files are optional host assets bundled inside it; they do not create seven independent skills. Start with the current host acting as lead. Activate separate roles only when the review benefits from them and the host supports the required controls.

## Install the skill

From the repository root, `python3 scripts/install_skill.py --host codex` installs to `~/.agents/skills/engineering-review/`. For Claude Code, use `--host claude-code`, which installs to `~/.claude/skills/engineering-review/`. These commands change the user's skill directory; invoke them only when installation is authorized. Use `--help` for explicit target options.

For a disposable test, copy the root skill to the test project's `.agents/skills/engineering-review/` for Codex or `.claude/skills/engineering-review/` for Claude Code. Keep evaluation answers and private run evidence outside the performing context. Confirm actual discovery in a fresh session. Copy identity establishes installation bytes, not activation.

## Activate optional agents

Claude Code reads Markdown/YAML agent definitions. Copy selected files from `assets/claude/` into the test project's `.claude/agents/`. Their `skills` field explicitly preloads Engineering Review; the skill must be discoverable. Their tools are limited to Read, Glob and Grep. The parent records evidence using the package scripts.

Codex reads standalone TOML agent definitions. Copy selected files from `assets/codex/` into `.codex/agents/`. Each has `name`, `description` and `developer_instructions`. Codex agents inherit parent permissions and provider configuration; these files do not create a sandbox. Configure the parent for the narrowest permitted access and inspect the actual trace.

The bundled lead uses a parent-dispatched arrangement: it returns specialist requests to its authorized parent, which starts selected sibling specialists and supplies results back to the lead. Leaf roles do not delegate. A main-context lead may use direct dispatch when actually available. Do not assume that a nested lead has an Agent tool or sufficient depth.

## Verify the chosen arrangement

Record exact package hashes, host/version, requested and observed model/effort, permission configuration, and available account/workspace identity without secrets. Test discovery or explicit loading, source reads, result return, denied dispatch/depth and incomplete coverage. Unknown identity remains null. Native collaboration and static file validation do not establish actual Claude Code or Codex acceptance.

Host/model acceptance is unverified until a fresh performing task and its public trace are reviewed against frozen criteria. Preserve timeouts as failed attempts and report unattempted cases separately. The existing `scripts/host_coverage.py` supports source-bound host evidence; its v1 case contract does not automatically cover the expanded suite.

## Sources

Opened on 2026-11-03. These pages support format and design choices; they do not prove the installed host's capabilities.

- [OpenAI orchestration](https://developers.openai.com/api/docs/guides/agents/orchestration): manager retains final response and selects specialists when useful.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): standalone TOML and inherited permissions.
- [Codex skills](https://learn.chatgpt.com/docs/build-skills): skill discovery and progressive disclosure.
- [Anthropic workflow principles](https://www.anthropic.com/research/building-effective-agents): use a simple sufficient workflow; tooling details in this 2024 article have changed.
- [Claude skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): concise entrypoints and conditional resources.
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents): Markdown frontmatter, skill preloading and host-specific nested dispatch.
- [Agent Skills specification](https://agentskills.io/specification): portable skill metadata and directory contract.
