# Engineering review standard

## Purpose and scope

Connect each conclusion to applicable requirements and actual evidence. Use ordinary prose, tables or the user's requested format; no package-specific JSON or review-state record is required.

## Evidence and loading

Read the shared policy, your role guide and policy, and relevant technical controls. Select controls by the actual task, stack and risk; do not preload every domain or research catalogue. Reuse unchanged guidance already available in context. Read selected controls with their conditions and exceptions. If a relevant passage is truncated or omitted, retrieve that passage with a bounded read or state the limitation. A search snippet is not a substitute for the required clause.

Inspect actual sources and relevant callers, tests or supplied observations. Cite file paths and useful line ranges, document sections, or image regions. Identify the revision or environment when it affects the claim; ordinary Git references and task context are sufficient. Do not require hash manifests. Check current changes before reusing earlier conclusions.

State the trigger, expected behavior, observed behavior and supported consequence. Separate established defects from risks, improvements and questions. Account for defenses and legitimate behavior. Unseen adapters, unavailable tests and unverified runtime behavior remain explicit dependencies, not invented guarantees. A successful command does not prove the desired behavior; supplied results retain their provenance and limits.

Check proposed triggers and verification expectations against the actual requirement, including at-most, at-least and exact relations and legitimate boundary cases. Do not make a check reject behavior the requirement permits.

## Findings

For each actionable finding, include a concise title, priority with context, location, causal explanation, consequence, focused correction and useful verification. Mention tradeoffs when material. Use the project's priorities; otherwise P0 means immediate severe harm, P1 a required/common workflow failure, P2 a meaningful limited defect or risk, and P3 low-risk actionable work. Do not inflate style preferences or force a finding quota. Base severity on supported consequences and exposure, not a threat category, control count or workflow phase alone. P0 requires evidence of immediate severe harm in the actual scope; distinguish a synthetic example from an observed live incident.

Give findings stable identifiers and retain them through handoff, developer response and re-review; link newly discovered findings separately. Use ordinary prose or the project format, without a mandatory schema. Account for each assigned requirement using the [scope and criteria guidance](intent_context.md#compare-and-report), and state what remains unassessed.

### Consolidating findings

Combine reports of the same underlying failure while preserving relevant consequences and verification obligations. Different severities or requirement labels do not alone create separate defects. A shared correction alone does not make distinct faulty mechanisms or independently affected paths duplicates. Preserve original evidence and explain material disagreement; do not hide a serious supported finding through voting.

## Specialist return

Return findings, inspected scope and important limitations to the lead in a concise message. Report useful partial findings even when another question is blocked. Distinguish a source defect from a missing input, denied tool or unperformed check. Do not invent a successful inspection, alter sources or take over the final user response.

## Developer handoff and response contract

Give the developer the retained findings, reviewed source, suggested corrections, verification needs and unresolved decisions. The optional [handoff template](templates/review-handoff.md) can be included in the review itself.

The developer responds per finding with what changed or why it remains disputed, deferred or blocked; relevant files/revision; actual checks and results; and remaining risks or decisions. One shared fix can reference several findings. Partial fixes and omitted responses remain visible. Do not demand commits or pre-fix execution logs that do not exist; use the working tree and explain evidence limits. See the optional [response template](templates/developer-response.md).

Re-review the actual changed source against the original failure and relevant valid paths. Apply the [independence policy](review_policy.md#evidence-and-judgment). Confirm source and governing-requirement freshness, inspect affected changes and new risks, and report fixed, partially fixed, unresolved or withdrawn findings under their original identifiers with reasons. Qualify obsolete evidence rather than using it to close current work. A developer's claim or passing test alone does not close a finding. Final coverage can remain incomplete while supported findings and corrections are reported.
