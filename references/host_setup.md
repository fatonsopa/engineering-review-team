# Set up host roles

## Before you begin

Host role templates are in `assets/claude/` and `assets/codex/`. Registration resolves their resource paths to the installed package.

Engineering Review is one skill with seven optional role assets. Start with the current host as lead. Host definitions are configuration, not proof of discovery, execution or permission enforcement. Normal review requires only the current host; Codex and Claude Code are separate validation targets.

## Steps

1. Install the repository using `python3 scripts/install_skill.py --host codex --destination INSTALL/engineering-review` (or --host claude-code). Use a separate disposable destination for validation. The installed repository includes its public resources; no Builder checkout is required.
2. Preview role registration from the installed package: `python3 scripts/install_skill.py --host codex --source INSTALL/engineering-review --agents-dir PROJECT/.codex/agents --preview`. For Claude Code use --host claude-code and PROJECT/.claude/agents.
3. Remove --preview to register after the destinations are within the authorized setup. Conflicting existing files are refused, not overwritten. Back up customized roles outside discovery directories and reconcile them explicitly. Registration replaces the asset's {{SKILL_ROOT}} marker with the actual installed root.
4. Invoke Engineering Review in the host's main context. Discover actual agent tool availability, depth, permissions and remaining bounds. Main-context lead dispatches selectively; bundled nested lead uses authorized parent-dispatched siblings and retains synthesis. Leaf roles never delegate.
5. Inspect the effective instructions: role asset, inherited/preloaded content, shared policy/standard, domain guide and task. Claude leaves do not preload lead orchestration. Codex roles preserve their assignment if the host exposes inherited skills. Separate contexts can share filesystem/account access; use actual host restrictions and inspect traces.

## Confirm success

Verify discovery or explicit loading, correct resource reads, separate performers, selective dispatch, result return, lead final ownership and target preservation. Record actual host/version, requested/observed model and effort, tool/permission configuration and source hashes. Unknown values remain unknown. Test direct, parent fallback and denied-dispatch outcomes. Run scripts/review_eval.py --preflight before freezing the required host matrix. Missing host observations remain unrun and cannot establish support.

## If it fails

Report exact missing capability or loading conflict. Do not imply an agent ran because its file exists. Preserve timeouts as failures and incomplete returns as evidence limits. A direct-loading test is not a registered-agent discovery test. Restore previous customized installation files from their backup if setup fails; preserve review histories outside the installation.

## Sources

[Claude Code subagents](https://code.claude.com/docs/en/sub-agents) and [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) explain host-specific formats and controls. Recheck actual supported behavior before claiming a new host profile.
