# Repository instructions

## Test changes

During implementation, use `scripts/run_tests.py --execute` to run only impacted tests. The script derives changes from the last successful checkpoint or Git HEAD and reports why each check was selected. Do not invoke full unittest/pytest discovery or a full-suite helper directly. Unmapped changes must be assigned an impact rule; they must not trigger a full-suite fallback.

Run the full suite after the author has verified every planned implementation change is delivered and no implementation work remains. Use an external implementation-completion record bound to the current artifact. User batch approval is not required; final testing and publication follow implementation verification.

## Routine test retries

Routine testing and necessary retries are part of the authorized task. Choose and record bounded batches from task complexity and observed results; do not ask for each extra test or retry. Use scripts/continuation.py for bounded extensions with a concrete reason. Preserve frozen criteria and all attempts. Stop and report when retries stall or their ceiling is reached. Explicit user hard limits, host permissions, scope changes and paid-service restrictions still apply.

## GitHub approval

Publish within the user's existing explicit authority for this deliverable, remote and branch. Preserve that authority across routine edits and retries. When publication is not authorized, prepare the tested deliverable and ask only for that remaining action. Editing/testing alone does not authorize publication or merging.

## Shared instructions

Keep repository workflow rules in AGENTS.md. Always provide CLAUDE.md with an @AGENTS.md import so Claude Code uses the same rules. Preserve this pattern in skills created or maintained by Skill Builder.

## Project guidance

The shared testing and approval rules above take precedence over conflicting project notes.

Keep authority in references/review_policy.md and evidence rules in references/review_standard.md. Role assets load those shared owners and their conditional domain references. Keep one root skill and host-specific assets separate.

Change mechanics and affected controls together. Preserve v1 cases as historical scope; expanded coordination criteria live separately. Keep operational evidence outside the repository. Never import application-specific scripts or dependencies. Actual host observations are required for host behavior claims.
