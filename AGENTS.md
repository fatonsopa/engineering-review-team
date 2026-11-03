# Repository instructions

## Test changes

During implementation, use `scripts/run_tests.py --execute` to run only impacted tests. The script derives changes from the last successful checkpoint or Git HEAD and reports why each check was selected. Do not invoke full unittest/pytest discovery or a full-suite helper directly. Unmapped changes must be assigned an impact rule; they must not trigger a full-suite fallback.

Run the full suite only after the user confirms the batch is finished, with an authorization record bound to the current artifact. Do not create that record without the actual user instruction. Final testing does not grant push approval.

## Routine test retries

Routine testing and necessary retries are part of the authorized task. Choose and record bounded batches from task complexity and observed results; do not ask for each extra test or retry. Use scripts/continuation.py for bounded extensions with a concrete reason. Preserve frozen criteria and all attempts. Stop and report when retries stall or their ceiling is reached. Explicit user hard limits, host permissions, scope changes and paid-service restrictions still apply.

## GitHub approval

Do not push to GitHub without the user's explicit approval for the completed changes being published. An earlier approval does not cover later edits. Prepare a concrete, reviewable result, report its validation, and wait for approval before pushing. A request to continue editing is not push approval.

## Shared instructions

Keep repository workflow rules in AGENTS.md. Always provide CLAUDE.md with an @AGENTS.md import so Claude Code uses the same rules. Preserve this pattern in skills created or maintained by Skill Builder.

## Project guidance

The shared testing and approval rules above take precedence over conflicting project notes.

Keep authority in references/review_policy.md and evidence rules in references/review_standard.md. Role assets load those shared owners and their conditional domain references. Keep one root skill and host-specific assets separate.

Change mechanics and affected controls together. Preserve v1 cases as historical scope; expanded coordination criteria live separately. Keep operational evidence outside the repository. Never import application-specific scripts or dependencies. Actual host observations are required for host behavior claims.
