# Engineering review standard

Status: Applies under the [Policy (POL)](review_policy.md). Owner: review lead for each assessment; package maintainer for this contract.

## Purpose and scope

Bind findings and coverage to actual source, criteria, guidance and evidence. A mechanical receipt checks consistency; the lead judges whether the conclusion is supported.

## Definitions

A defect violates an applicable contract. A risk or improvement has a supported consequence but is not automatically a proven violation. A question records uncertainty. A capture preserves selected bytes and a declared-scope inventory. An outcome records execution; acceptance determines whether it can satisfy current coverage.

## Principles

Trace actual entry points, callers, dependencies and failure paths. Prefer focused corrections and meaningful verification. Missing evidence does not prove absence; no finding quota applies.

Check the causal chain of every material claim, including alternatives inside an otherwise valid finding. Distinguish what committed, what external effect completed and what acknowledgment was observed. A supplied interface assumption is not proof of an unseen adapter's implementation. Record a dependency-sensitive outcome as conditional or unresolved unless captured evidence establishes it; the final synthesis must preserve that certainty. See the [architecture fault-scenario method](domains/architecture.md#separate-failure-windows-and-unknown-dependencies).

## Rules

- REV-01: Record actual participants and requested/observed model identity separately. Unknown identity stays null; labels are claims, not authentication.
- REV-02: Capture source, criteria and external supplied evidence separately, outside the target. Decide applicability for all six domains and retain scope exclusions.
- REV-03: Assign each task a question, source subset, criteria, dependencies and bounds. Inspect all assigned sources and required contracts; missing essentials remain incomplete.
- REV-04: Each finding has category, applicable criterion, severity/rationale, concrete trigger, impact, evidence references, focused correction, tradeoff and verification. Absence claims require bounded captured search evidence.
- REV-05: P0 means immediate severe integrity/security failure; P1 breaks a required/common workflow; P2 is a meaningful limited defect/risk; P3 is low-risk actionable work. Explain context; do not inflate stylistic preferences.
- REV-06: Keep coverage status separate from findings. Preserve unresolved questions, conflicts and unperformed checks. A complete clean scope can return no findings; it is not release approval.
- REV-08: In v4, capture optional document status/authority and route relevant sections by content. Report every assigned criterion and reconcile every required criterion/domain pair. Partial/not-assessed work remains incomplete; capture approved deviations separately from conformance.
- REV-07: Record terminal outcomes regardless of current freshness; accept only valid current evidence. Reconcile late/lost/conflicting results before retrying. Retain predecessors and every finding disposition.

## Procedure

Use the complete schemas and example in [coordination](coordination.md). New suites use version 4 and retain capture/report version 2 with the explicit v4 extensions in [project intent and alignment](intent_context.md). Version 3 remains historical with its original domain-level coverage contract. The legacy source-only CLI and version 1 reports remain available for historical scope; they cannot establish new acceptance guarantees.

For a specialist return, include truthful inspected paths and notes. Findings cite one or more source/evidence IDs with exact hash and line range; primary source locations may span files. An absence claim also names captured search evidence, query and inspected scope. Questions may be retained without requiring a change, but essential uncertainty prevents complete coverage.

Checks use not_run or supplied_evidence. A separately authorized execution trace can be captured as supplied evidence with its actual origin; that never retroactively grants execution permission to a read-only leaf.

### Specialist return contract

Every specialist returns one JSON object with `inspection` and `report`. For a v4 assignment the v2 report additionally requires `criterion_assessments` under the exact [alignment contract](intent_context.md#dispatch-and-collect); the lead supplies that extension with the task. The lead supplies the assignment binding, actor, criterion IDs, source IDs and captured hashes before dispatch, and passes this contract with the task. These instructions describe a leaf return; they do not assign orchestration or final-response authority.

The historical v3 example below shows every base field. For v4 add the criterion assessments described above. It is illustrative, not evidence. Replace its placeholders with actual assigned values and write source-supported content; do not return the example text. A finding's `criterion` is the exact assigned ID, such as `C1`, not the requirement text or `C1: ...`. `inspection.paths` and source-reference IDs are captured paths relative to the target root, not absolute filesystem paths. Every finding needs its own nonempty `title`.

```json
{
  "inspection": {
    "paths": [
      "ASSIGNED_SOURCE_ID"
    ],
    "notes": "Describe the source and contracts actually inspected."
  },
  "report": {
    "version": 2,
    "binding": "ASSIGNED_BINDING",
    "reviewer": "ASSIGNED_ACTOR",
    "decision": "needs_changes",
    "summary": "State the supported conclusion and its scope.",
    "findings": [
      {
        "id": "F1",
        "category": "defect",
        "title": "Name the concrete contract violation",
        "criterion": "ASSIGNED_CRITERION_ID",
        "severity": "P2",
        "severity_reason": "Explain consequence and affected scope.",
        "trigger": "Describe the inputs or event order that exposes the issue.",
        "impact": "State the supported consequence.",
        "references": [
          {
            "kind": "source",
            "id": "ASSIGNED_SOURCE_ID",
            "sha256": "CAPTURED_SOURCE_SHA256",
            "start_line": 1,
            "end_line": 1
          }
        ],
        "correction": "Describe the focused correction; do not edit the source.",
        "tradeoff": "State the relevant cost or compatibility effect.",
        "verification": "Describe a check that would distinguish the defect from its correction.",
        "absence_evidence": null
      }
    ],
    "limitations": [],
    "checks": [
      {
        "name": "Target execution",
        "status": "not_run",
        "evidence_id": null
      }
    ],
    "observed_model": null,
    "source_instructions_followed": false
  }
}
```

Keep all shown base keys. A v3 report has no additional fields; a v4 report adds only the required `criterion_assessments` extension. Findings, references and checks retain their exact fields. For a complete clean assignment use `decision: no_findings` and an empty `findings` array. For blocked work use `decision: blocked`, retain supported partial findings if any, and explain the missing input in `limitations`. Finding categories are `defect`, `risk_or_improvement` or `question`; all use the same required fields. Source line ranges must exist in the captured file. Use `absence_evidence: null` unless captured search evidence supports an absence claim.

Checks have exactly `name`, `status` and `evidence_id`. Use `not_run` with null evidence for unperformed checks; `supplied_evidence` refers to an existing captured external evidence ID and does not grant execution permission. Record `source_instructions_followed` truthfully: only false is eligible for acceptance, and an authority violation remains recorded as failed or invalid work. Unknown observed model identity stays null. An `absence_evidence` object has `paths`, `query`, `result` and `evidence_id` for captured bounded search evidence.

Before returning, inspect the JSON against this example: exact criterion IDs, title present, assigned actor and binding, relative source IDs, captured hashes, truthful inspected paths and every required key. Do not run target code to check formatting. If essential binding data is missing, request it through the lead instead of inventing values. The lead records the actual raw return before collection. A rejected return stays in history; request a corrected linked follow-up or report incomplete coverage rather than silently manufacturing an accepted worker result.

## Verification

Code validates source drift, evidence hashes, assigned coverage, budgets, report fields and finding dispositions. The lead must inspect actual host traces, applicability, criterion relevance, severity, correction and factual support. A reason string alone does not justify rejecting a serious finding.

## Responsibilities and exceptions

Specialists return findings and limits through the lead or authorized parent. The lead owns synthesis and the final reply. Host enforcement is tested separately from prompts. The policy owns authority exceptions.

## Ownership, review, and related policy

Change contracts and affected controls together. Preserve historical cases and failed attempts. The [Policy (POL)](review_policy.md) remains the single authority owner; `config/review_contracts.json` records machine vocabulary and `config/roles.json` records role contracts.
