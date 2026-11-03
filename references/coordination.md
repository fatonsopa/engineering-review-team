# Coordinate an engineering review

Use this procedure when the review has explicit domain coverage or selected specialists. Python 3 on a Unix-like host is required for the state lock. The script performs no provider calls or target execution. It records claims and validates consistency; inspect actual host traces separately.

## Prepare

Save a request JSON outside the target. The example uses illustrative paths and must be adapted to actual files and identities:

```json
{
  "root": "/absolute/project",
  "paths": ["handler.py", "requirements.txt"],
  "criteria": ["requirements.txt"],
  "implementer": "actual-implementer",
  "lead": "actual-reviewer",
  "coverage": {"implementation": {"owner": "lead", "reason": "One bounded caller flow"}},
  "bounds": {"max_calls": 0, "max_seconds": 600, "max_concurrent": 1},
  "capabilities": {"lead_dispatch": false, "parent_dispatch": false}
}
```

Select only relevant domains from `config/roles.json`. An owner is `lead` or `specialist`; record why. Capabilities report what this host context can actually do, not what a vendor page recommends. Put requirements in a captured file if they were supplied in the conversation, preserving their wording and origin.

```sh
python3 scripts/review_suite.py prepare --state EVIDENCE/state.json --input EVIDENCE/request.json
```

The state captures source and criteria, coverage, bounds and a binding digest. Empty sources or missing criteria are refused; explain the missing input to the user. Keep the state protected and outside the target. The local ledger is not a tamper-proof audit service.

## Dispatch and collect

Record a task with `id`, `domain`, `actor`, `route` and `depends_on`. Use `lead` for work in the lead context, `nested` only when the lead can dispatch, or `sibling` when an authorized parent dispatches for the lead. Dependencies are completed task IDs. Each domain has one active or completed task; failed attempts remain and a new ID can retry within bounds.

```sh
python3 scripts/review_suite.py dispatch --state EVIDENCE/state.json --input EVIDENCE/task.json
python3 scripts/review_suite.py collect --state EVIDENCE/state.json --input EVIDENCE/result.json
```

Dispatch records eligibility before a host call; it does not launch a worker. Give a worker its task, exact capture, policy, standard, relevant domain reference and limits. Ask for a result with exactly `task_id`, `binding`, `actor`, `status`, `inspection`, `report`, `trace` and `limitations`. Status is `completed`, `failed`, `timeout` or `cancelled`. Completed results carry the standard's inspection and source report. Other outcomes may have null inspection/report and must explain limitations. The trace is an object with `path` (an absolute external file path) and `sha256` (its exact digest). The file must exist, be nonempty and remain unchanged through synthesis and reuse. It identifies the actual host record, not an invented receipt; the lead still checks its provenance. A blocked source report cannot count as completed coverage.

Parallelize independent reads only. Leaf roles return JSON to the lead or dispatching parent, which records it. A parent must return sibling results to the lead before synthesis. If dispatch is denied, record the actual failure and incomplete domain; do not claim the intended specialist ran. Timeouts remain failures even with partial output. Do not retry a still-running task until its outcome is reconciled.

## Synthesize

Save an assessment with `lead`, `decision`, `summary`, `dispositions`, `conflicts` and `limitations`. Reference findings as `TASK_ID:ZERO_BASED_INDEX`. Each disposition has `finding`, `action` (`retain`, `reject` or `duplicate`), `reason` and `duplicate_of` (a retained finding ID for duplicates, otherwise null). Include every completed result's finding once. Explain rejection from evidence, not preference.

Each conflict has `finding_ids`, `resolution` and boolean `resolved`. Resolve substantive disagreements by inspecting the applicable source and criteria. Unresolved conflicts remain incomplete. The script checks declared consistency; it cannot discover an omitted semantic conflict.

```sh
python3 scripts/review_suite.py synthesize --state EVIDENCE/state.json --input EVIDENCE/assessment.json
```

The decision is `incomplete` for missing domains or unresolved conflicts, otherwise `needs_changes` for retained findings or `no_findings`. A review must have terminal task records before synthesis. Deliver the lead's findings, coverage and limitations; the final receipt is not release approval.

## Revoke or reuse

```sh
python3 scripts/review_suite.py revoke --state EVIDENCE/state.json
python3 scripts/review_suite.py reuse --state EVIDENCE/fresh-state.json --previous EVIDENCE/previous-state.json
```

Revocation prevents reuse and further accepted work. Reuse eligibility requires unchanged source, criteria and coverage plus an unrevoked complete prior assessment. Eligibility does not copy acceptance into the new review: the lead must inspect provenance and continued authority. Preserve changed-source failures and prepare a new capture. Never edit state to erase a failed attempt.

## Check the outcome

A refusal exits with code 2 and a JSON reason. Correct the missing input or report the gap; do not bypass a refusal by editing the ledger. The [Technical Standard (STD)](review_standard.md) owns source reports and the [Policy (POL)](review_policy.md) owns authority.
