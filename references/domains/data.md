# Data Reviewer

## Before you begin

Use when: Schemas, persistence, queries, migrations, transactions, isolation, retention or recovery.

Read the assigned task and captured subset, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Inputs: Data invariants, existing populations, schema/migration chain, old and new callers, storage engine/version and recovery evidence. Match the task's binding and assigned role. A lead can use this method for lead-owned work. A specialist keeps its leaf role and requests missing essential inputs through the lead.

## Steps

1. Write the invariant before evaluating code: uniqueness, ownership, allowed nulls, precision, referential integrity, retention or ordering. Identify every writer and the population the rule must cover.
2. Trace reads and writes through transaction boundaries, constraints and error paths. Use the actual engine/version semantics; application checks are not automatically equivalent to storage constraints.
3. Construct a two-operation schedule for concurrency risks. Identify isolation, locking, retries and idempotency keys; determine whether an acknowledged or uncertain outcome can be duplicated.
4. For migrations, examine existing rows and the period when old and new callers coexist. Check backfill/default assumptions, constraint validation, lock/workload effects and deployment order.
5. Inspect query populations, joins, ordering and pagination against requirements. Separate a measured query problem from an unmeasured capacity hypothesis.
6. Inspect rollback and restoration evidence without assuming a successful restore or inevitable data loss. Do not execute SQL, migrations or production queries through the reviewer role.

Use invariant tables, transaction schedules and old/new caller compatibility matrices. Cite versioned engine documentation for behavior that controls the result.

## Select applicable data methods

Start with data definitions and invariants in agreed Low Level Design (LLD), Interface Contract (IC) or relevant project sections. Use the actual storage engine/version; database guarantees differ. Missing documents do not establish missing constraints.

| Trigger | Investigation and evidence | Clean boundary and uncertainty |
| --- | --- | --- |
| Schema or representation | Inventory types, units, null/default semantics, key/ownership constraints, precision and referential rules. Trace all writers and storage-level enforcement for each invariant. | An application precheck may race; a correctly scoped unique constraint can be clean. Do not coerce opaque identifiers such as `0087` to numbers. |
| Transactions or concurrency | Construct two-operation schedules and uncertain commit cases. Inspect isolation, locks, optimistic versions, retries, idempotency and atomic publication relative to the invariant. | State which engine guarantee prevents the proposed failure. Do not claim serializability from a transaction keyword alone. |
| Migration or backfill | Inspect existing populations, defaults, expand/contract sequencing, resumable batches, checkpoints, reconciliation, locking and old/new compatibility. Connect each step to a validation and stop condition. | A new column's non-null constraint does not prove old rows were populated. Distinguish code rollback from irreversible data transformation. |
| Query or pagination change | Check joins, filters, tenant boundaries, ordering/tie-breakers, pagination stability, N+1 effects and index support with actual predicates and populations. | A potential slow query is a risk until measured or analytically supported; an index name alone proves little. |
| Retention or deletion | Trace sensitive-data retention, logical/physical deletion, derived copies, audit needs and backup behavior against actual obligations. | Do not invent a retention duration or claim all copies are erased when backups were not examined. |
| Restore or reconciliation | Compare backup scope, integrity checks, replay/rebuild steps, recovery objectives and actual restore evidence. Follow partial failures and authoritative-source reconciliation. | A configured backup is not a demonstrated restore. Unrun recovery checks remain limitations, not fabricated data loss. |

Use invariant-to-writer/constraint tables and old/new compatibility matrices for applicable flows. Missing authority or production evidence stays explicit; reviewer tools do not execute migrations or live queries.

Read the [worked examples](../examples/data.md) when calibrating a finding or a clean conclusion. These are teaching examples, not evaluation answers.

## Confirm success

Record the v2 report and truthful inspected subset under the shared contract, including the v4 criterion assessments for a v4 task; a specialist returns them to the lead. Each actionable finding needs criterion, concrete trigger, consequence, evidence references, severity rationale, focused correction, tradeoff and verification. Separate defects, supported improvements and questions. A complete clean assignment may return no findings; do not invent a finding quota.

Completion means the assigned relevant flows and required dependencies were examined, each supported finding has evidence, and all unperformed checks and missing inputs are stated. It does not mean the project has no possible defects or is approved for release.

## If it fails

Keep missing dependencies, unsupported evidence, uncertainty and failed checks visible. A specialist returns them to the lead, preserves partial observations, and never extends authority, edits the target, delegates further or owns the final user response. The lead records traces and outcomes; leaf tools may be read-only.

## Sources

[PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), when PostgreSQL is the actual engine. Select actual applicability and version through the [criteria register](../review_criteria.md); general guidance does not replace project requirements.
