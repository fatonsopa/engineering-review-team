# Engineering Review

One Engineering Review installation with an accountable lead and six optional specialists: implementation, architecture, security, data, testing and operations. The lead selects useful specialists and owns the final assessment; Python checks evidence consistency.

## Requirements

- Python 3 standard library; Unix file locking for suite coordination.
- Explicit source files, criteria and actual implementer/reviewer identities.
- Host-native file access; no application credentials or another provider CLI required for normal use.

## Installation

### Get the skill

Download and extract the skill ZIP. Open the folder containing `SKILL.md`.

### ChatGPT desktop and Codex

For a filesystem-enabled ChatGPT desktop/Codex workspace, run:

```sh
python3 scripts/install_skill.py --host codex
```

The installer copies the repository files to `~/.agents/skills/engineering-review/`. Start a new chat and select `@engineering-review` in ChatGPT desktop or invoke `$engineering-review` in Codex. In the desktop app, Skills is available from the sidebar. This installation uses local skill support; it does not install a browser or mobile add-on.

### Claude Code

```sh
python3 scripts/install_skill.py --host claude-code
```

The destination is `~/.claude/skills/engineering-review/`. Start a new Claude Code session and invoke `/engineering-review`.

### Claude

Download the repository ZIP, extract it, and use the folder containing SKILL.md as the skill. For a custom-skill upload, compress that folder with your archive tool. [Claude upload instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Quick start

Explicitly invoke the skill before giving it a task. Examples below use `/engineering-review`. Use `@engineering-review` in ChatGPT desktop and `$engineering-review` in Codex.

> /engineering-review Review handler.py and requirements.txt in the supplied project. Keep source unchanged. Use the lead alone unless a specialist materially improves the review. Return supported findings and uncovered work.

Exact source capture, located findings or supported no-findings, and explicit coverage limits. Missing essential input yields an incomplete review.

## Usage scenarios

### Review one function

> /engineering-review Review parser.py, its caller and criteria.txt; keep the target unchanged.

Lead-owned implementation review with exact citations and unrun checks.

### Review a tenant-sensitive storage change

> /engineering-review Review handler.py, storage.py and tenant criteria. Select security/data review only when useful.

Source-bound specialist results returned to the lead for deduplication, conflict resolution and coverage assessment.

## Verification

```sh
python3 scripts/check_suite_cases.py success
```

The authored coordination control records prepare, dispatch, collect and synthesize. This is not an actual host or model-quality result.

## Evaluate and improve results

Keep private evidence outside source. Preserve the original 13 v1 controls and cases under evals/v1_cases.json. Freeze current evals/cases.json and evals/suite_cases.json before performing tasks. Actual observations, discovery and specialist returns remain separate from controls.

### Acceptance criteria

- Current mechanical suite passes; v1 preservation controls remain separately auditable.
- Fresh performing tasks and public traces establish selected specialist behavior and lead synthesis.
- Actual Claude Code and Codex runs are required before two-host acceptance; missing coverage stays incomplete.

### Run the evaluations

Use the evaluation command below. Replace named placeholders with the paths returned by the skill.

```sh
python3 scripts/evaluate.py --package . --allow-exec
```

### Read the results

| Result field | Meaning |
| --- | --- |
| `task_success_percent` | Accepted task attempts ÷ evaluated attempts × 100 |
| `coverage_percent` | Evaluated attempts ÷ planned attempts × 100 |
| `critical_failures` | Failed non-negotiable requirements; these block acceptance |
| `pending_review` | Outputs that still need a semantic judgment |

For example, 8 accepted attempts out of 10 evaluated attempts gives 80% task success. If 12 attempts were planned, coverage is 83.3%. A missing denominator is reported as not measured. Wrong or malformed task outputs count as failed attempts. Infrastructure gaps reduce coverage. A quality rubric score is reported separately from truth-based accuracy.

A candidate is accepted only when its declared target, coverage, critical checks, and required reviews pass. An installation self-check is not a complete quality assessment of a generated skill.

Missing actual AI observations remain unrun. Import the captured results with `--observations PATH` on the evaluation command and review the refreshed evidence before acceptance. Generated maintenance sessions report incomplete coverage as `awaiting_observations`; refreshing the unchanged candidate retains earlier reports without spending another tuning experiment. Complete failures and runtime limits still apply.

### Improve and retest

1. Locate a concrete failure, preserve its evidence and change only the responsible code or instruction.
2. Repeat affected controls and the same frozen behavioral task within the configured bounds.

## Models and run limits

AI work uses the model already available in the current host. The skill records an unknown model identity rather than guessing one. Mechanical operations run through the packaged scripts.

Routine testing includes necessary bounded retries without approval for each extra test. The skill records the reason, preserves earlier attempts and stops when progress stalls or retry ceilings are reached. Explicit user hard limits still apply. Requirements and scoring stay fixed.

## Troubleshooting

### The report is refused after a source change.

Preserve the old artifacts, capture current selected bytes and review the affected change before validating again.

### The host cannot expose its exact model identity.

Record the requested profile and keep observed_model null; do not infer provider identity or switch accounts.

### A nested lead has no dispatch tool or sufficient depth.

Use an authorized parent to dispatch selected specialist siblings and return results to the lead, or mark uncovered work incomplete. See references/host_setup.md.

## Support

Give the maintaining lead the exact package/source hashes, failed control or refusal and redacted evidence. Do not include credentials.

## License

MIT, Manaferra Inc.

<!-- repository:start -->

## Documentation

One root skill with optional Claude Markdown and Codex TOML role assets. Host activation requires actual evidence.

- [Policy (POL)](references/review_policy.md)
- [Technical Standard (STD)](references/review_standard.md)
- [Coordination](references/coordination.md)
- [Host setup](references/host_setup.md)

<!-- repository:end -->

<!-- skill-readme:source -->
