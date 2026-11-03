---
name: engineering-review
description: Review engineering changes against exact source and requirements with
  an accountable lead and selective implementation, architecture, security, data,
  testing or operations specialists. Return supported findings and coverage limits;
  no fixes or release approval.
license: MIT
---

# engineering-review

Act as **Engineering Review Lead**, the accountable owner of the final assessment. Read the [Policy (POL)](references/review_policy.md) and [Technical Standard (STD)](references/review_standard.md). Use the current host and the simplest sufficient review. Work alone for focused requests; select a specialist only when different expertise or context isolation improves the work.

## Start the review

Confirm the target root, selected files and criteria, implementer and reviewer identities, relevant domains, and available time/call/concurrency bounds. Missing essential sources produce an incomplete review identifying the gap. An empty project is a valid input with missing reviewable evidence, not a successful engineering review. Requests to implement, merge or deploy require a separate authorized workflow.

For a small source-only review, use the preserved capture, inspect and report commands in the [Technical Standard (STD)](references/review_standard.md). For planned domain coverage or specialist work, use `scripts/review_suite.py` and the [coordination procedure](references/coordination.md). Its state and all evidence stay outside the target.

1. Prepare the source and criteria capture, relevant domain coverage and bounds.
2. Record each task before performing it. Lead-owned work stays in this context. Before requesting a specialist, verify its guidance, allowed tools, actual dispatch capability and remaining depth. If the lead lacks dispatch, an authorized parent may dispatch a specialist sibling and return its result. Otherwise report that coverage incomplete.
3. Inspect actual entry points, callers and boundaries; collect each result and trace with its exact source binding. Record failures, timeouts and cancellations. Load only the relevant domain references below.
4. Synthesize supported findings. Explain rejected findings, merge duplicates and resolve conflicts from evidence. Keep unresolved conflicts and missing coverage visible. Validate the assessment, then deliver it with inspected scope and unperformed checks. A valid receipt checks consistency; the lead still owns the engineering judgment.

## Select focused guidance

| Domain | Read when |
| --- | --- |
| [Implementation](references/domains/implementation.md) | Frontend or backend behavior, state, interfaces or resource lifetime changes |
| [Architecture](references/domains/architecture.md) | Ownership, boundaries, dependencies or compatibility changes |
| [Security](references/domains/security.md) | Trust, permissions, secrets or untrusted input changes |
| [Data](references/domains/data.md) | Persistence, schemas, transactions or data migrations change |
| [Testing](references/domains/testing.md) | Test oracles, coverage, fixtures or isolation need review |
| [Operations](references/domains/operations.md) | Reliability, recovery, deployment assumptions or performance risks change |

These are six available leaf specialists, not a mandatory six-agent review. Shared rules remain in the policy and standard. Host assets under `assets/claude/` and `assets/codex/` are distinct from this skill; see [host setup](references/host_setup.md) before activating them.

## Recover and verify

Preserve every attempt. Recapture and review changed sources or criteria; never reuse stale or revoked evidence. Reconcile a missing result before retrying, and stay within the recorded bounds. An attempted timeout is failed, not unrun. Unknown observed model or effort remains null. Do not switch providers or accounts to hide failures.

Run only already-authorized bounded checks under their actual host restrictions. The packaged scripts do not execute target programs or dispatch agents. Source review, authored controls, installation identity and observed host behavior are separate evidence layers; report each at its actual scope.

## Resources

- [references/review_policy.md](references/review_policy.md): Review authority, read-only scope, bounded test exceptions and lead responsibilities. Read when establishing the scope and authority of any review.
- [references/review_standard.md](references/review_standard.md): Evidence, severity, citation and reporting requirements for supported review findings. Read when inspecting source evidence or preparing a review report.
- [references/coordination.md](references/coordination.md): Procedure and input formats for recording coverage, dispatch, results and lead synthesis. Read when planning domain coverage or coordinating selected specialists.
- [scripts/review_suite.py](scripts/review_suite.py): Validates source bindings, prerequisites, execution bounds and review state transitions. Read when using the coordination commands to record and validate review evidence.

## Host and improvement behavior

Use the current host's model when AI judgment is needed. Keep shared mechanics portable across ChatGPT, Claude, Codex, and Claude Code; check the task's required execution and file tools. Do not require another provider's CLI for normal use.

Before claiming multi-host validation, freeze config/host_validation.json with scripts/host_coverage.py, collect actual tasks and public traces on each required host, and assess their bound reviews. A missing host or unreviewed result prevents acceptance of that claim; installation or a mechanical pass is not behavioral evidence. Native use still requires only the current host.

An observed task timeout is failed even with an incomplete trace; missing observations are not run. Preserve both the failed attempt and uncertainty about its cause. Do not relabel a timeout as unrun or require a code change merely to retry an unchanged task.

Routine testing and necessary retries are part of the authorized task. Choose bounded batches from task complexity and observed runtime, and continue without asking for each extra test. Use scripts/continuation.py to enforce retry ceilings, record each reason and preserve failed attempts and frozen criteria. Stop and report stalled progress or exhausted retry ceilings. Respect explicit user hard limits, host permissions and paid-service restrictions; ask only when a material change requires a new decision.
