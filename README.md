# Engineering review

A portable independent review workflow with one shared Technical Standard (STD), a reusable reviewer role and source-bound report checks. AI judges defects; Python checks evidence consistency.

## Requirements

- Python 3 standard library and a tool-enabled host that can read the selected source and write artifacts outside it.
- A lead-supplied candidate scope and reviewer distinct from the implementer. Host permissions and model availability are configured separately.

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

> /engineering-review Review module.py against its stated behavior. Keep the target unchanged and return a source-bound report.

A structured report, capture/inspection artifacts and a mechanical validation receipt, with actual evidence limits.

## Usage scenarios

### Review a bounded change

> /engineering-review Review parser.py and its selected caller against the supplied requirements before integration.

Supported actionable findings or a no-findings result with inspected scope and unrun checks.

### Review changed sources

> /engineering-review Follow up after the selected source changed. Preserve the previous report and review the current bytes.

A fresh capture and affected review; the old source-bound report is not reused as current approval.

## Verification

```sh
python3 scripts/check_review_cases.py all
```

Thirteen authored mechanical controls pass; this does not establish AI review quality or host behavior.

## Evaluate and improve results

Use disposable independent source fixtures and keep evidence outside them. Real behavioral runs need a fresh performing context and captured tool trace.

### Acceptance criteria

- Mechanical contract controls pass on exact package bytes.
- Required actual behavioral cases receive independent source-bound assessment; unrun hosts remain unverified.

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

## Support

Give the maintaining lead the exact package/source hashes, failed control or refusal and redacted evidence. Do not include credentials.

## License

MIT, Manaferra Inc.

<!-- repository:start -->

## Documentation

The repository itself is the installable skill. The agent asset describes a role; host activation and enforcement require separate configuration.

- [Engineering review Technical Standard (STD)](references/review_standard.md)
- [Reviewer agent asset](assets/agents/engineering-reviewer.md)

<!-- repository:end -->

<!-- skill-readme:source -->
