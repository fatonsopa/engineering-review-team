# Coordinate an engineering review

## Before you begin

Use Python 3.11+ and a Unix-like host for file locking. Keep the host-provided workspace as the working directory. The installed skill and review target are independent paths; a skill alias may resolve outside the workspace. Resolve only the supplied skill location, without listing its ancestors or searching sibling directories. Use the supplied absolute target and evidence paths. If a required path is missing, request it through the lead.

For shell calls, set `REVIEW_SKILL_ROOT` to the absolute resolved skill path and invoke `python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py"`. Repeat that assignment when the host does not preserve shell variables between calls. Do not change into the skill directory or use `..` from a skill alias to find workspace files. Read named role definitions from the host-provided workspace or registration record. The [Policy (POL)](review_policy.md) owns access boundaries; these path steps do not grant additional access or enforce a filesystem sandbox.

Keep state, criteria, reports and traces in the authorized evidence directory outside the target. The examples below are illustrative; replace `EXTERNAL` with that absolute directory and use actual identities. Scripts never launch workers or execute target code.

## Current v4 review

New reviews use `--v4`. Read [project intent and alignment](intent_context.md) before preparing or assigning work. The complete base request, task, outcome and assessment below retain their fields. For v4 add the following exact extensions:

1. Request: `alignment` with `documents`, `criterion_sources` and `deviations`; criteria have nonempty required domains.
2. Task: `documents`, the exact relevant captured section tokens selected by content and criterion/domain recipients.
3. V2 report inside each outcome: `criterion_assessments`, one evidence-backed row per assigned criterion.
4. Final assessment: `criterion_dispositions`, one row per criterion and required domain, tied to the last accepted task for that pair.

Use `--v4` for every lifecycle command; do not mix ledger versions. Empty document/deviation lists are valid. For example, the one-criterion base request below adds `"alignment": {"documents": [], "criterion_sources": {"C1": null}, "deviations": []}` and its task adds `"documents": []`. Its report adds a satisfied/contradicted/partial/not-assessed row with actual evidence for C1; its final assessment adds the matching implementation-domain disposition. The intent guide provides exact fields, a document-routing example and deviation rules.

The base schemas and existing v3 example below remain useful for their unchanged fields and historical replay. Their v3 command and report alone do not satisfy a v4 review. Preserve the historical specialist-return example for v3 controls; a current leaf receives the v4 extension with its actual assignment from the lead.

## Steps

### 1. Prepare source and criteria

Save an external request matching this example. Its criteria text may come directly from the conversation without writing into the target. Add external logs as evidence entries with id, absolute path and origin.

```json
{
  "root": "/absolute/target",
  "profile": {
    "mode": "component",
    "scope": [
      "module.py",
      "caller.py"
    ],
    "exclusions": [],
    "systems": [
      "Python library"
    ],
    "versions": [
      "Python 3"
    ],
    "critical_flows": [
      "clamp boundary"
    ],
    "assumptions": []
  },
  "paths": [
    "module.py",
    "caller.py"
  ],
  "criteria": [
    {
      "id": "C1",
      "text": "Clamp integers to 0..10; independently inspect the boundary",
      "origin": "User conversation copied outside target",
      "required_domains": [
        "implementation"
      ]
    }
  ],
  "evidence": [],
  "coverage": {
    "implementation": {
      "status": "applicable",
      "owner": "lead",
      "reason": "Required input/output flow",
      "evidence": [
        "C1"
      ]
    },
    "architecture": {
      "status": "not_applicable",
      "owner": null,
      "reason": "No relevant flow in this bounded control",
      "evidence": [
        "C1"
      ]
    },
    "security": {
      "status": "not_applicable",
      "owner": null,
      "reason": "No relevant flow in this bounded control",
      "evidence": [
        "C1"
      ]
    },
    "data": {
      "status": "not_applicable",
      "owner": null,
      "reason": "No relevant flow in this bounded control",
      "evidence": [
        "C1"
      ]
    },
    "testing": {
      "status": "not_applicable",
      "owner": null,
      "reason": "No relevant flow in this bounded control",
      "evidence": [
        "C1"
      ]
    },
    "operations": {
      "status": "not_applicable",
      "owner": null,
      "reason": "No relevant flow in this bounded control",
      "evidence": [
        "C1"
      ]
    }
  },
  "participants": {
    "implementer": "author-context",
    "lead": "review-context",
    "requested_model": null,
    "observed_model": null
  },
  "bounds": {
    "max_calls": 4,
    "max_seconds": 600,
    "max_concurrent": 2
  },
  "capabilities": {
    "direct": true,
    "parent": true
  },
  "predecessor": null
}
```

```sh
python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 prepare --state EXTERNAL/state.json --input EXTERNAL/request.json
```

All six applicability decisions are mandatory. Use an evidence reference to a captured path, criterion ID or supplied-evidence ID. Explicitly required domains must be applicable. Unknown versions/assumptions remain visible. Source scope inventories are bounded to 4,096 supported files and each capture to 64 files; partition larger reviews and state aggregate scope. Binary, oversized or symlinked essential evidence requires an explicitly designed adapter or incomplete conclusion.

### 2. Record and perform assignments

A task has exactly: id, domain, actor, route, question, paths, criteria, depends_on, kind, predecessor. Routes are lead, direct or parent. Kinds are initial, retry or followup. Initial predecessor is null; later tasks link a terminal predecessor. Paths are the assigned captured subset; criteria are applicable IDs; depends_on lists accepted task IDs.

```json
{
  "id": "T1",
  "domain": "implementation",
  "actor": "review-context",
  "route": "lead",
  "question": "Does clamp preserve the boundary contract?",
  "paths": [
    "module.py"
  ],
  "criteria": [
    "C1"
  ],
  "depends_on": [],
  "kind": "initial",
  "predecessor": null
}
```

```sh
python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 dispatch --state EXTERNAL/state.json --input EXTERNAL/task.json
```

Only after recording eligibility, use native host tools to start the actual worker. Supply the task, binding, captured subset, shared rules and domain guide. Include the complete [specialist return contract](review_standard.md#specialist-return-contract), the exact criterion IDs, actor and source IDs/hashes in the assignment; do not ask a leaf to infer the JSON shape from a role name. A parent can dispatch siblings and return their results to the lead. A script dispatch receipt records an assignment; it does not prove that a worker ran. Read-only leaves return JSON; the lead records it.

### 3. Collect real outcomes

An outcome has exactly event_id, task_id, binding, actor, status, inspection, report, trace, limitations. Status is completed, failed, timeout or cancelled. Trace is {path, sha256} for an external nonempty captured host record, bounded to 2 MiB. Inspection is {paths, notes}; list the assigned subset truthfully. Preserve raw failed/malformed returns with a terminal envelope and actual limits; do not invent a trace if unavailable.

The [Technical Standard (STD)](review_standard.md#specialist-return-contract) owns the complete leaf return shape and field rules. Use it for both specialist and lead-owned inspections. The lead wraps the returned `inspection` and `report` in the outcome envelope above and attaches the actual trace. `criterion` holds an assigned ID, never its full text; `title` is mandatory. Preserve raw malformed returns and use linked correction work after rejection. Do not rewrite a worker's substantive claim to obtain acceptance.

```sh
python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 collect --state EXTERNAL/state.json --input EXTERNAL/outcome.json
```

The result distinguishes recorded from accepted. Drift, revocation, lateness, malformed fields and missing trace do not erase history, but prevent completed coverage. Identical event replay is idempotent; conflicting returns create a discrepancy and invalidate task acceptance. Record failed attempts before retries; reconcile running work before a new attempt.

### 4. Synthesize and return one assessment

An assessment has lead, decision, summary, dispositions, conflicts, limitations. Each disposition is {finding, action, reason, duplicate_of}; finding IDs are TASK_ID:FINDING_ID. Action is retain, reject or duplicate; duplicate_of points to a retained finding, otherwise null. Every accepted task finding gets a disposition, including prior findings after follow-up.

Each conflict has finding_ids, resolution and boolean resolved. Inspect source/criteria to resolve disagreement; votes are not evidence. Decision is incomplete if required coverage, freshness or conflicts remain unresolved; otherwise needs_changes for retained actionable findings, or no_findings. Questions remain separately classified. Include limitations for incomplete outcomes.

```sh
python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 synthesize --state EXTERNAL/state.json --input EXTERNAL/assessment.json
```

Deliver the lead's findings, actual coverage, relevant questions, uncertainty and unperformed checks. The receipt is not release approval. Review provenance and semantics separately from mechanical validity.

## Confirm success

All required domain work has valid accepted evidence; history retains every dispatched attempt; findings are source-bound and actionable; the lead owns the final reply. Successful controls establish contract behavior only. Actual host execution and reviewer competence need separate observations.

## If it fails

A refusal exits 2 with a JSON reason. Correct inputs or report the limitation; never edit ledger state. To revoke use `python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 revoke --state EXTERNAL/state.json`. Revocation permits terminal outcome recording while stopping new work/acceptance. To inspect use show with the same --state.

Changed source, criteria or dependency scope requires a successor request with predecessor set to the previous review ID. Preserve old states. Reuse only checks eligibility: `python3 "$REVIEW_SKILL_ROOT/scripts/review_suite.py" --v3 reuse --state EXTERNAL/fresh.json --previous EXTERNAL/previous.json`; it never copies acceptance. The lead must recheck authority, provenance and semantics.

For legacy reviews omit --v3 and use the historical request/report formats. Do not convert old receipts into v3 passes. Legacy formats are retained for their original scope.

Legacy validation remains in `scripts/check_suite_cases.py` and `scripts/evaluate.py`; the original 13 v1 controls retain their historical scope. Use `scripts/review_eval.py` for the v3 corpus.
