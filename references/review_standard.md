# Engineering review standard

Status: Applies under the [Policy (POL)](review_policy.md).
Owner: Engineering Review Lead for each assessment; package maintainer for this standard.

## Purpose and scope

Review consequential correctness, regression and maintainability risks against exact selected source and criteria. The policy owns authority; this standard owns evidence and reporting.

## Definitions

A finding is an actionable defect supported by source and requirements. A limitation is an unanswered question or unperformed check. A capture preserves selected UTF-8 bytes, hashes and line counts. A mechanically valid report has consistent structure and citations; its engineering conclusion still needs judgment.

## Principles

Follow the actual consumer flow and its boundaries. Prefer a focused correction over needless machinery. Distinguish observations, hypotheses and missing evidence. No finding quota applies.

## Rules

- REV-01: Record actual implementer and reviewer identities. Use a distinct reviewer for an independent review. Record requested model/effort separately from observed values; unknown values stay null. A stronger configured model may help when available, but a name or requested profile proves neither independence nor quality.
- REV-02: Capture explicit files and applicable criteria before inspecting. Keep evidence outside the target and apply the policy's authority limits.
- REV-03: Inspect required entry points, callers and dependent contracts. Follow resource ownership, lifetime, error/recovery paths and the real test oracle. Missing essential sources prevent a complete conclusion.
- REV-04: Each finding names severity, captured path/hash and exact lines, triggering flow, consequence, focused correction and verification. Complexity criticism needs a concrete duplicated rule, coupling, cost or failure risk.
- REV-05: Use P0 for immediate severe integrity/security failure, P1 for a broken required or common workflow, P2 for a meaningful limited defect and P3 for a low-risk actionable issue.
- REV-06: A source report uses `needs_changes`, `no_findings` or `blocked`. A suite assessment uses `incomplete` for missing required coverage or unresolved conflicts. Supplied evidence stays labeled supplied; source inspection does not establish live execution.
- REV-07: Validate source, inspection and report consistency. Preserve prior evidence on source/criteria change or revocation; review current bytes before reuse. The lead reviews semantics and the requesting owner decides integration.

## Source report procedure

Run commands from the installed package root. Replace uppercase placeholders with explicit values; outputs must be new paths outside the target.

```sh
python3 scripts/review_contract.py capture --root TARGET --paths module.py requirements.txt --implementer IMPLEMENTER --reviewer REVIEWER --output EVIDENCE/capture.json
python3 scripts/review_contract.py inspect --capture EVIDENCE/capture.json --paths module.py requirements.txt --notes "Actual inspected flow and limits" --output EVIDENCE/inspection.json
python3 scripts/review_contract.py report --capture EVIDENCE/capture.json --inspection EVIDENCE/inspection.json --report EVIDENCE/report.json --output EVIDENCE/receipt.json
```

Read the captured files before recording inspection. The report has exactly `capture_id`, `reviewer`, `decision`, `summary`, `findings`, `limitations`, `observed_model`, `observed_effort`, `actions`, `checks` and `source_instructions_followed`. Set the last field to false. Source-only actions are `read_source`, `capture`, `inspect` and `report`.

Each finding has `title`, `severity`, `path`, `sha256`, `start_line`, `end_line`, `evidence`, `impact`, `correction` and `verification`. Each check has `name`, `status` (`not_run` or `supplied_evidence`) and `source` (null or a captured evidence path). The v1 validator intentionally accepts source-only reports. A separately authorized test trace can be captured and reported as supplied evidence; it does not turn the v1 action list into a target execution permission.

For suite results, use the suite capture ID and task actor as reviewer. Supply an inspection with `capture_id`, `reviewer`, all `inspected` paths and meaningful `notes`. The lead or authorized parent records returned JSON; read-only leaf agents need not write files.

## Verification

| Rules | Check |
| --- | --- |
| REV-01 | Inspect actual participant provenance and requested/observed identity |
| REV-02 | Capture controls and actual host trace establish selected sources and actions |
| REV-03–05 | Review actual flow, consequence, evidence and correction; schema alone cannot establish quality |
| REV-06 | Validate decision/coverage consistency and inspect the semantic conclusion |
| REV-07 | Reject drift, revoked evidence and mismatched returns; retain historical attempts |

## Responsibilities and exceptions

The lead owns the final assessment. Specialists return findings and limitations. The policy owns test exceptions and authority. Host enforcement must be verified separately from instructions.

## Ownership, review, and related policy

Change the affected controls with this standard. The [Policy (POL)](review_policy.md) and [coordination procedure](coordination.md) are its related contracts. The existing thirteen v1 controls test source-report mechanics; expanded suite cases test additional coordination behavior.
