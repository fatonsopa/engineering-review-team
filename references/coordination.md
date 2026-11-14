# Review coordination

## Before you begin

Use the current workspace and supplied skill location. Keep target paths distinct from installed guidance and respect their permissions. Read the shared [policy](review_policy.md), [standard](review_standard.md), [project context](project_profile.md) and relevant [intent guidance](intent_context.md). Reuse guidance already present; resolve missing relevant sections as needed.

## Scope and selection

Identify the requested change/component, important behavior, relevant requirements, stack and constraints. Inspect the diff and surrounding consumers when reviewing a change. Choose applicable review areas proportionately; a small local tool does not need enterprise architecture, but consequential data still needs appropriate safeguards.

The lead can review directly or ask relevant specialists using the host's native agent tools. Assign only work that benefits from expertise or context isolation. Give each specialist a concrete question, source paths, effective rules, relevant project-document sections and limits. Request a concise evidence-backed return. No separate task files or state commands are required.

A main-context lead may dispatch when supported. A nested read-only lead asks its authorized parent to dispatch specialist siblings or run permitted checks. Leaves do not delegate. If dispatch is unavailable, perform only work the lead can support and disclose the gap. Role files alone do not prove an agent ran.

## Collect and synthesize

Inspect specialist evidence and clarify material disagreements. Keep useful partial findings and distinguish blocked investigation from a clean result. Report failures, timeouts and unperformed checks honestly. Avoid repeating unchanged work; a follow-up should address the missing evidence or correction. Do not silently broaden scope or switch accounts to conceal a failure.

Consolidate duplicate failures according to the shared standard, preserve distinct mechanisms and return one final assessment. Lead with actionable findings, then summarize inspected scope, missing inputs and unperformed checks. Use the user's format if specified; otherwise concise Markdown is sufficient.

## Handoff for corrections and re-review

Developers make changes under separate authority. Use the [shared handoff guidance](review_standard.md#developer-handoff-and-response-contract) to retain finding identity, actual changes and verification. Re-review affected code and relevant valid behavior; reuse unaffected conclusions when their source and assumptions still hold. Report remaining concerns without a release-approval claim.
