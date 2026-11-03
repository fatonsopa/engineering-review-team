---
name: engineering-review
description: Independently review engineering changes against exact sources and constraints;
  capture evidence and return actionable findings, no-findings or blocked results
  before integration.
license: MIT
---

# engineering-review

Use this skill for an independent engineering review before integration. Read [Engineering review Technical Standard (STD)](references/review_standard.md) first; it owns the review rules. The reusable role is assets/agents/engineering-reviewer.md.

Confirm the exact root, selected paths, requirements/constraints, implementer and independent reviewer identity. The lead selects and records the reviewer profile; this skill does not spawn a model or prove its quality. Run only this package's evidence scripts, never target programs.

1. Capture selected files with `python3 scripts/review_contract.py capture --root TARGET --paths module.py --implementer IMPLEMENTER --reviewer REVIEWER --output OUTSIDE_TARGET/capture.json`. Optional `--requested-model` and `--requested-effort` record the lead's request. Replace uppercase placeholders with supplied values.
2. Read the captured text and necessary caller/requirement context. If more source is needed, obtain a new explicit capture. Record inspection with `python3 scripts/review_contract.py inspect --capture OUTSIDE_TARGET/capture.json --paths module.py --notes "Scope, actual flow and limitations" --output OUTSIDE_TARGET/inspection.json`.
3. Write a report JSON with capture_id, reviewer, decision, summary, findings, limitations, observed_model, observed_effort, actions, checks and source_instructions_followed. Use null for unexposed model/effort. Set source_instructions_followed to false. Findings contain title, severity, path, sha256, start_line, end_line, evidence, impact, correction and verification. Each check contains name, status (not_run or supplied_evidence) and source (null or a captured path). Use the shared standard's decision/severity rules.
4. Validate using `python3 scripts/review_contract.py report --capture OUTSIDE_TARGET/capture.json --inspection OUTSIDE_TARGET/inspection.json --report OUTSIDE_TARGET/report.json --output OUTSIDE_TARGET/receipt.json`. Deliver the report and its limitations to the lead. A valid receipt establishes structural/source consistency, not semantic correctness or integration approval.

The scripts reject stale or out-of-scope citations. On refusal, preserve artifacts and correct the supported problem or obtain the missing source; do not edit receipts or claim success. If Python/file tools are unavailable, return the review with validation explicitly unperformed. Do not execute target code as a fallback.

## Resources

- [references/review_standard.md](references/review_standard.md): Shared Technical Standard (STD) for engineering reviews. Read when performing or assessing a review.
- [assets/agents/engineering-reviewer.md](assets/agents/engineering-reviewer.md): Reviewer role that loads this skill and its shared standard. Read when configuring an independent reviewer role.
- [scripts/review_contract.py](scripts/review_contract.py): Source capture and report validation. Read when capturing source and delivering a report.

## Host and improvement behavior

Use the current host's model when AI judgment is needed. Keep shared mechanics portable across ChatGPT, Claude, Codex, and Claude Code; check the task's required execution and file tools. Do not require another provider's CLI for normal use.

Before claiming multi-host validation, freeze config/host_validation.json with scripts/host_coverage.py, collect actual tasks and public traces on each required host, and assess their bound reviews. A missing host or unreviewed result prevents acceptance of that claim; installation or a mechanical pass is not behavioral evidence. Native use still requires only the current host.

An observed task timeout is failed even with an incomplete trace; missing observations are not run. Preserve both the failed attempt and uncertainty about its cause. Do not relabel a timeout as unrun or require a code change merely to retry an unchanged task.

Routine testing and necessary retries are part of the authorized task. Choose bounded batches from task complexity and observed runtime, and continue without asking for each extra test. Use scripts/continuation.py to enforce retry ceilings, record each reason and preserve failed attempts and frozen criteria. Stop and report stalled progress or exhausted retry ceilings. Respect explicit user hard limits, host permissions and paid-service restrictions; ask only when a material change requires a new decision.
