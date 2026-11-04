# Project intent and implementation alignment

Use this guide for a v4 review. Project documents can supply acceptance criteria, context or observed evidence. They are optional inputs. Technical Writer's format references teach how to write documents; they do not supply the project's requirements or become a runtime dependency of Engineering Review.

## Establish authority before comparison

Ask what the user wants reviewed, then inspect supplied requirements, contracts and plans. Record each source's origin, version, status, authority and relevant sections. An available agreed requirement can bind the review. A proposal, stale design, superseded decision or unresolved conflict remains context until the user or actual decision authority resolves it. A filename, recent timestamp or document type does not establish approval. Test plans describe intent; test results describe observations.

When a document is missing, continue the technical review against explicit task criteria and verified contracts. State which intent comparisons could not be performed. Do not report a code defect solely because a project lacks a plan, threat model or service-objectives file. An explicitly required but missing deliverable can be a finding against that actual requirement.

## Route sections by content

The lead reads relevant supplied documents and assigns section recipients using this map. Small projects can keep several subjects in one issue or file; a section can have several recipients. Give each worker the exact assigned source subset, criterion IDs, question, binding and relevant section text with its metadata and hash. Do not send a filename alone or require leaf roles to discover documents across the filesystem.

| Content and common document types | Primary recipients and comparison |
| --- | --- |
| Observable behavior in Product Requirements Document (PRD), Issue, User Story (US), Spec Driven Development document (SDD) | Lead, implementation and testing; route domain constraints to the responsible specialist. Compare delivered behavior and acceptance coverage. |
| Boundaries, quality scenarios and choices in High Level Document (HLD), Decision Record (DR) | Architecture, plus affected security, data and operations. Compare responsibilities, interactions and accepted tradeoffs. |
| Internal detail, operations and data definitions in Low Level Design (LLD), Interface Contract (IC) | Implementation and architecture; security for access/trust, data for invariants/transactions, testing for observable contracts. |
| Work and verification in Implementation Plan (IP) | Lead and implementation; testing receives verification, data receives migration/backfill, operations receives rollout/recovery. Check promised deliverables as well as functioning code. |
| Test Plan (TP), Test Specification (TS), Test Status Report (TSR), Test Completion Report (TCR) | Testing and affected domains. Keep planned checks, actual results, skips and unrun work distinct. |
| Threats and controls in Threat Model (TM) | Security, with architecture, data and operations for their boundaries/controls. Keep residual-risk decisions and implemented/tested status distinct. |
| Objectives and response in Service Objectives Document (SOD) | Operations, architecture and relevant testing. Compare agreed measurement/response contracts; proposed targets do not establish violations or measured attainment. |
| Applicable Policy (POL), Technical Standard (STD), operational How-to Guide (HTG) | All affected domains by subject. Verify actual applicability, authority, operating prerequisites and recovery limits. |

## Capture the optional context

Add an `alignment` object to the existing complete request in [coordination](coordination.md). With no documents, use `documents: []`, map every explicit criterion to null, and use `deviations: []`. Every v4 criterion has at least one distinct required domain; criterion IDs and domains must already exist in the request.

This illustrative addition assumes criteria `AUTH-1` and `SESSION-1`, both required for security, and a supplied external file whose first two lines state the agreed intent. Replace the path, metadata, line ranges and IDs with actual captured input.

```json
{
  "alignment": {
    "documents": [{
      "id": "INTENT",
      "path": "/absolute/supplied/requirements.md",
      "origin": "Project owner supplied revision 7",
      "version": "revision 7",
      "status": "available",
      "authority": "agreed",
      "reason": "Owner identifies these requirements as current acceptance criteria",
      "sections": [{
        "id": "access-and-session",
        "start_line": 1,
        "end_line": 2,
        "criteria": ["AUTH-1", "SESSION-1"],
        "domains": ["security"]
      }]
    }],
    "criterion_sources": {
      "AUTH-1": "INTENT:access-and-session",
      "SESSION-1": "INTENT:access-and-session"
    },
    "deviations": []
  }
}
```

Each document has exactly the fields shown. `status` is `available`, `missing`, `stale`, `conflicting` or `not_applicable`; `authority` is `agreed`, `proposed`, `unknown` or `superseded`. Missing/not-applicable documents use null `path` and empty `sections`, with a reason and an honest version such as `unknown`. Other statuses capture real UTF-8 bytes from an absolute non-symlink path. A document inside the target must also be among the captured source paths. Captures retain hashes and text; a changed document invalidates acceptance.

Each section has exactly `id`, inclusive `start_line`/`end_line`, `criteria` and nonempty `domains`. IDs cannot contain colons. An empty criterion list marks contextual material for all tasks in those recipient domains. Other sections reach tasks whose criteria intersect their IDs. Section routing must cover every required domain when the section supplies normative intent.

`criterion_sources` contains every criterion exactly once. Null means an explicit task criterion whose origin is recorded in the existing criterion object. A `DOCUMENT:SECTION` value must identify available agreed intent containing that criterion and all its required domains. Stale/proposed/conflicting documents can be routed as context, but cannot occupy this normative source slot. The lead must check source meaning; declaring null is not permission to silently copy a proposal into a binding requirement.

## Dispatch and collect

A v4 task retains all existing fields and adds `documents`, an exact list of its relevant `DOCUMENT:SECTION` tokens. `review_alignment.routes(state['alignment'], task)` computes that list; it does not select semantic recipients for the lead. Dispatch rejects missing, extra, duplicate or unrelated tokens. The worker receives the actual content and capture hash of each assigned section, with status and authority preserved.

The shared v2 report fields remain intact. Under a v4 ledger the report also requires `criterion_assessments`, exactly one row per assigned criterion. This illustrative row belongs to a security task assigned `SESSION-1`; fill the hash and source range from its actual capture.

```json
{
  "criterion": "SESSION-1",
  "status": "satisfied",
  "rationale": "The verifier rejects expired credentials before performing the operation; relevant callers use this verifier",
  "references": [{"kind": "source", "id": "session.py", "sha256": "ACTUAL_CAPTURE_HASH", "start_line": 12, "end_line": 18}],
  "findings": [],
  "deviation_id": null
}
```

The allowed statuses are `satisfied`, `contradicted`, `partially_satisfied` and `not_assessed`. Explain the evidence and limits per criterion. Every assessed row needs references. A not-assessed row can lack references but must explain its limitation. Partial/not-assessed rows require report limitations and cannot establish complete coverage. Include every related finding ID exactly once. A contradiction needs a defect finding or a separately captured approved deviation; satisfied cannot conceal a returned defect.

References retain the existing exact fields `kind`, `id`, `sha256`, `start_line`, `end_line`. `source` and `evidence` work as before. V4 also permits `document`, where `id` is the document ID and the range must fall within an assigned section. A document proves intent or supplied observation; it does not by itself prove the implementation satisfies it. The lead judges whether cited evidence supports the claimed result.

## Reconcile complete coverage and deviations

The v4 final assessment adds `criterion_dispositions`, exactly one row for every criterion and required-domain pair. Each row has `criterion`, `domain`, `status`, `task`, `rationale` and `deviation_id`. The last accepted task assessing that pair supplies its status and deviation. An unassigned pair uses `not_assessed`, null `task` and null `deviation_id`. A domain having another accepted task cannot fill that gap. Use an accepted followup to resolve competing conclusions; do not silently rewrite a worker's result.

All finding dispositions and conflict reconciliation still apply. Contradicted intent without an approved deviation yields `needs_changes`, even if the lead rejected its returned finding. Partial/not-assessed criteria yield `incomplete`, with visible limitations. Complete coverage means the declared criteria were assessed, not that all were satisfied or the release is approved. Inspect the full criterion inventory against the user's request: code cannot detect a requirement the lead never captured.

An approved deviation is a separate request row with exactly `id`, `criterion`, `domain`, `evidence_id` and `reason`. The evidence ID must identify captured external decision evidence. The lead verifies actual approval authority, scope and continued applicability; the script authenticates neither a person nor a decision. The report uses that deviation ID only with `contradicted`, preserving the difference from conformance. Final output retains approved-deviation records separately. An invented waiver or an unrelated criterion/domain cannot satisfy the contract.

## Verify and recover

Use `--v4` consistently for prepare, dispatch, collect, synthesize, show, revoke and reuse. A CLI flag/ledger version mismatch is refused. Document drift, changed source/guidance, revocation and late/failed outcomes follow the existing ledger rules: history is retained, current acceptance is separate. Create a successor scope when inputs or intent need to change. State and lock paths must remain outside the target and cannot alias captured external evidence or documents.

Run the authored alignment controls through the impacted runner. They demonstrate deterministic rejection and coverage behavior, not fresh reviewer performance or actual risk approval. Actual host trials assess whether reviewers choose useful criteria, route content, inspect code and reach supported conclusions. Historical v3 records remain readable with `--v3` and retain their original domain-level coverage limits.
