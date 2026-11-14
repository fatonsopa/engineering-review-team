# Database review technical standard

## Contents

- [Purpose and scope](#purpose-and-scope)
- [Definitions](#definitions)
- [Principles](#principles)
- [Applicability and phases](#applicability-and-phases)
- [Rules](#rules)
- [DB-01 — Storage contracts and invariants](#db-01--storage-contracts-and-invariants)
- [DB-02 — Types, constraints and representation](#db-02--types-constraints-and-representation)
- [DB-03 — Tenant keys, database access and stored routines](#db-03--tenant-keys-database-access-and-stored-routines)
- [DB-04 — Atomicity, isolation and concurrent changes](#db-04--atomicity-isolation-and-concurrent-changes)
- [DB-05 — Uncertain outcomes, retries and deduplication](#db-05--uncertain-outcomes-retries-and-deduplication)
- [DB-06 — Locks, deadlocks and connection pools](#db-06--locks-deadlocks-and-connection-pools)
- [DB-07 — Query results and pagination](#db-07--query-results-and-pagination)
- [DB-08 — Query cost, indexes and statistics](#db-08--query-cost-indexes-and-statistics)
- [DB-09 — Mixed-version migrations and DDL](#db-09--mixed-version-migrations-and-ddl)
- [DB-10 — Backfills and reconciliation](#db-10--backfills-and-reconciliation)
- [DB-11 — Seeds, mocks and migration verification](#db-11--seeds-mocks-and-migration-verification)
- [DB-12 — Retention and deletion](#db-12--retention-and-deletion)
- [DB-13 — Maintenance, partitioning and storage capacity](#db-13--maintenance-partitioning-and-storage-capacity)
- [DB-14 — Replication, read consistency and failover](#db-14--replication-read-consistency-and-failover)
- [DB-15 — Backup, restore and rebuilding](#db-15--backup-restore-and-rebuilding)
- [Verification](#verification)
- [Responsibilities and exceptions](#responsibilities-and-exceptions)
- [Ownership, review, and related policy](#ownership-review-and-related-policy)

## Purpose and scope

The Database Reviewer assesses whether assigned persistence changes preserve valid data, return the required results and meet applicable compatibility, performance and recovery criteria. Scope includes relational and nonrelational stores, their callers, migrations, stored routines and supplied configuration or execution evidence. It is a bounded engineering review, not database administration or certification.

The [Database Policy (POL)](../policies/database.md) governs judgment. Team-owned [Review scope and criteria](../intent_context.md#review-scope-and-criteria) establishes project authority, document selection, package defaults, replacements and waivers. The shared [Review Technical Standard (STD)](../review_standard.md) owns evidence and findings. Reuse those procedures; this file adds no document-routing map or report schema.

`DB-01`–`DB-15` are package-designed review controls. Sources support particular engine mechanisms; they do not prescribe a project's architecture, limits or obligations. The methods and hypothetical examples below are review guidance, not claims that tests ran or a system failed. Assess the actual engine, version, driver, configuration and population before applying an example.

## Definitions

- An **invariant** is a property that must remain true for the relevant data and operations, including failure and recovery paths.
- A **writer** is any application, job, migration, import, routine or administrative path that can change the relevant data.
- **Atomicity** concerns whether an operation's changes take effect together. **Isolation** concerns interference between concurrent operations. **Durability** concerns preservation of acknowledged changes under specified failures. None establishes the other two.
- A **backfill** populates or transforms an existing population. **Reconciliation** compares actual records with an identified authoritative source and resolves or reports discrepancies.
- An **uncertain outcome** means the caller cannot establish whether the operation committed. A lost response is not proof of rollback.
- **Recovery point objective (RPO)** bounds acceptable data loss; **recovery time objective (RTO)** bounds acceptable recovery time. Use project definitions and targets; unknown targets stay unknown.

## Principles

Write the invariant before inspecting its enforcement. Trace all relevant writers and readers, including historical data, alternative entry points and partial failures. Application prechecks, ORM declarations and successful happy-path tests are evidence about a layer, not proof of every database guarantee.

Use actual engine semantics. SQL isolation names, document atomicity, transaction errors, constraints, indexes and durability settings differ. A missing project document does not stop compatible technical checks or prove that enforcement is absent.

Preserve correctness while evaluating cost. A scan, lock, join, denormalized record or absent index is not inherently a defect. Explain a concrete failure or workload consequence, and distinguish measured behavior, supported analysis and missing evidence. Do not invent latency, pool, batch, retention or recovery targets.

## Applicability and phases

Read the control list, select relevant entries and record material exclusions or unknowns in the assigned review. Read those entries in full. A narrow query change does not require a fresh audit of every backup system; include dependencies that determine its result.

| Phase | Investigation depth |
| --- | --- |
| Foundation | Establish representations, invariants, query semantics and actual engine behavior. Review concurrency whenever concurrent writers exist. A disposable prototype does not need an invented replication topology. |
| Production launch | Include retained user data, real privileges and tenants, active caller versions, migration failure paths and recovery evidence relevant to the change. |
| Growth | Extend evidence to representative populations, contention, pool demand, maintenance, large backfills, retention workload and replica lag when present. |
| Advanced scale or criticality | Examine partition/shard boundaries, consequential data loss, recovery dependencies, failover and stronger evidence required by actual commitments. |

Phase does not waive an applicable invariant or obligation. Multiple tenants, sensitive data, money, concurrent writes, destructive transformations and irreversible effects activate relevant checks at any phase. For an unfamiliar engine or data platform, identify the unanswered semantic question and ask the lead for qualified coverage; do not silently substitute PostgreSQL behavior.

## Rules

### DB-01 — Storage contracts and invariants

Establish what the assigned data means, who can change it and which store is authoritative before judging its implementation.

- Identify engine/version, relevant extensions, driver/ORM, transaction defaults, deployment topology and differences between test and production. Distinguish inspected configuration from assumed defaults.
- Map each material invariant to its population, writers and enforcing constraint, conditional write, transaction or other mechanism. Include imports, scheduled jobs and privileged routines that bypass normal application paths.
- Identify authoritative records, derived copies, caches and rebuild sources. For each affected boundary, establish allowed staleness, loss and partial progress from project criteria.
- Record missing engine, population or contract evidence that changes a conclusion. Reconstructed assumptions are not approved project requirements.

For example, an evictable Redis cache and Redis used as the sole store have different consequences when keys disappear. Review persistence and eviction choices against that role; do not require a cache to preserve reconstructible data indefinitely.

### DB-02 — Types, constraints and representation

The persisted representation and enforcement must preserve the applicable invariants for every relevant writer and existing population.

- Check units, numeric precision/range, null versus missing values, defaults, encoding/collation, timestamp meaning and identifier representation. An opaque identifier such as `0087` must not lose significant characters through numeric conversion. Distinguish explicit NULL, an omitted field resolved by a default, and an unknown value across every relevant writer; rejecting NULL does not itself forbid a contract-compatible default for omission.
- Match uniqueness, required values, references, ownership and allowed states to actual enforcement. Inspect composite keys, null semantics, deferred validation, cascade effects and constraint/validator bypass paths.
- Check storage-level enforcement where the engine supports the needed guarantee. If application coordination supplies it instead, trace all writers and concurrency behavior; do not accept an unprotected existence precheck as equivalent.
- Compare declared rules with their enabled, validated state and historical data. Inspect representative invalid and valid values, not only fresh empty schemas.

PostgreSQL `CHECK` can accept null, and its unique constraints have explicit null semantics. MongoDB validation can be configured to warn instead of reject; validation settings affect existing records. Neither a constraint name nor a validator's presence proves the intended invariant.

### DB-03 — Tenant keys, database access and stored routines

Storage paths must enforce the assigned ownership and privilege boundaries under the identities that actually execute them.

- Trace tenant/owner keys through joins, references, unique keys, partition keys, reads and mutations. Where a relationship must remain within one tenant, establish how both identity and tenant membership are enforced.
- Inspect effective runtime, migration, worker and administrative grants, including inheritance, schema creation, default privileges and routine execution. Separate migration authority from ordinary service needs.
- Check views, triggers and stored routines for their execution identity, object resolution, dynamic query construction and transaction side effects. Inspect invoker/definer semantics and untrusted schema resolution when applicable.
- Where row-level security is relied on, verify enabled policies, read/write predicates and bypass behavior using actual roles. Include pooled identity changes and alternate access paths.

For example, PostgreSQL table owners normally bypass row security; a policy tested only under an ordinary role does not establish the owner's behavior. Definer routines need safe object resolution and execution grants. Supply this database evidence to Security for exploitation and authorization judgment; do not duplicate its threat catalogue.

### DB-04 — Atomicity, isolation and concurrent changes

The transaction or conditional-write boundary must preserve the invariant under permitted concurrent operations and failures.

- Identify every read used to decide a write, the affected keys/rows/documents and the actual begin/commit boundary, including ORM autocommit and implicit commits.
- Construct a two-operation schedule for lost updates, write skew, duplicate creation, overselling or stale decisions relevant to the change. Explain which constraint, predicate, lock, version check or isolation guarantee prevents it.
- Inspect failed comparisons, zero affected rows, transaction aborts and errors between related writes. A short transaction can still violate an invariant; shorter duration alone is not a fix.
- Establish atomicity across the actual scope. MongoDB multi-document updates are not one atomic operation merely because each document update is atomic. Redis command errors during execution do not undo other queued commands that execute.

For example, two requests can both observe a free slot before either inserts. A transaction keyword or application precheck does not resolve that schedule. A correctly scoped uniqueness constraint with conflict handling may do so without imposing serializable isolation on the whole application.

### DB-05 — Uncertain outcomes, retries and deduplication

Retry handling must distinguish an aborted operation from an operation whose commit outcome is unknown, and preserve the intended result on repetition.

- Follow connection loss before, during and after commit. Inspect how the caller discovers an authoritative outcome or safely repeats the operation.
- For retryable serialization/deadlock failures, inspect the actual driver's behavior and complete transaction retry boundary. Recompute decisions whose reads became invalid; bound attempts according to the surrounding request/job contract.
- Where deduplication is required, inspect durable key scope, tenant binding, request identity, uniqueness, result storage and retention relative to permitted replay. A key stored separately from the protected effect may leave a crash window.
- Trace persistent publication records or equivalent coordination for database changes coupled to messages/external effects. Identify partial completion and reconciliation; do not assume a local transaction covers another service.

A new identifier on every retry cannot deduplicate the same logical operation. Conversely, a repeated request with the same durable identity and confirmed stored result need not create another effect. Storage atomicity is Database's responsibility; Code owns caller retry behavior and Architecture owns the cross-system coordination choice.

### DB-06 — Locks, deadlocks and connection pools

Coordination and connection use must preserve correctness while fitting the assigned workload and availability criteria.

- Inspect lock acquisition order, conflicting modes, touched keys, wait/statement/transaction limits and handling of deadlock or timeout errors. Identify external calls or idle time that unnecessarily prolong transactions and retained locks.
- Use supplied wait graphs, transaction traces or a concrete conflicting schedule to locate contention. Necessary locks and brief contention are not defects; establish their consequence before proposing weaker coordination.
- Account for pool demand across processes, replicas, tenants and jobs. Inspect acquisition timeouts, connection release after exceptions/cancellation and the distinction between waiting clients and active database connections.
- Check pooling mode against session state, tenant context, temporary objects, prepared statements and advisory locks. Verify state reset and driver/version compatibility rather than assuming a reused connection is clean.

PgBouncer transaction pooling does not preserve arbitrary session features; prepared-statement support depends on mechanism and configuration. SQLite's writer concurrency also differs from server databases. Compare the actual mode with its callers instead of demanding a universal pool size or lock-free writes.

### DB-07 — Query results and pagination

Queries must return the required population, values and ordering across relevant states and page boundaries.

- Trace joins, filters, tenant scope, soft-deleted records, aggregation, duplicates and null handling to the expected result. Check whether list, count, export and mutation paths intentionally use the same population.
- Where stable paging is required, inspect a deterministic total order, tie-breakers, cursor predicates and sort direction. Check duplicates/misses across equal sort values and concurrent insert/update/delete behavior against the promised consistency.
- Inspect page/batch limits and deep-offset costs under the supported population. Keyset pagination is an option, not a universal requirement; a tie-breaker alone does not create a snapshot across changing data.
- Verify projections and deserialization preserve required types and precision. Include empty results, boundary values and stale replicas where relevant.

For example, ordering only by a nonunique creation time cannot define a stable page boundary among ties. PostgreSQL documents the need for unique ordering with `LIMIT`/`OFFSET`; ordering alone does not establish the application's cross-request snapshot contract.

### DB-08 — Query cost, indexes and statistics

Query-performance findings must connect an access pattern to relevant data, query behavior and a supported cost or requirement consequence.

- Inspect generated queries and query counts across growing input sizes, including lazy loading and per-record lookups. Compare N+1 behavior with batching/join alternatives and their memory, transfer and consistency costs.
- Read supplied query plans with their exact query, parameters, engine/version, schema/indexes and population. Distinguish estimates from actual execution; assess row estimates, repeated loops, scans, join strategy, sort/spill, I/O and returned data as relevant.
- Check index keys/order, predicates, expressions, collation and included fields against the actual access path. Include write/storage/build costs, invalid or redundant indexes and statistics quality. An index name alone is not evidence of use or benefit.
- Use representative cardinality, skew, tenant size, selectivity and concurrency. State when a toy dataset or missing plan prevents a performance conclusion; supported complexity analysis can still identify a risk.

A full scan can be appropriate for a small table or a query reading most rows. Foreign-key indexing is engine-specific: PostgreSQL does not automatically index referencing columns; MySQL/InnoDB creates a required suitable referencing index if missing. Inspect actual metadata before recommending another index.

### DB-09 — Mixed-version migrations and DDL

Schema changes must preserve the supported callers and data through each deployment state, with a credible response to partial failure.

- Compare old/new readers and writers against the schema before, during and after migration. Include background workers, queued old payloads, rollback binaries and historical records.
- Inspect dependency order for additive changes, compatible reads/writes, backfill, validation and removal. Expand/contract is useful when versions coexist; a justified maintenance window can use another safe sequence.
- Inspect actual DDL operations for lock modes, table rewrite/validation scans, disk/log demand, transaction restrictions and implicit commits. Include how failure, cancellation and partial index/constraint creation are detected before retry.
- State which changes are reversible and what data a reverse operation would discard. Code rollback, schema rollback and recovery of transformed data are distinct. Identify the stop condition and recovery path for destructive steps.

Adding a required column can break an old writer even after existing rows are backfilled. “Online” DDL does not mean no blocking: MySQL online operations still need metadata locks. PostgreSQL concurrent index creation has failure states and transaction restrictions. Use exact-version evidence; do not promise zero downtime from a keyword.

### DB-10 — Backfills and reconciliation

Backfills and repairs must preserve valid concurrent changes, identify partial progress and establish whether the intended population was transformed correctly.

- Identify source of truth, eligible records, transformation rules, malformed/duplicate handling and records written while the job runs. Trace races between backfill writes and live writers.
- Inspect batch boundaries, stable traversal, durable checkpoints and restart behavior. Check a crash before/after checkpoint persistence and repetition of a committed batch; progress reporting must not skip uncommitted work.
- Review resource bounds and pause/stop conditions against supplied lock, log, replica and storage evidence. A fixed batch size is not a universal safety guarantee.
- Reconcile identities, values and invariants, including exceptions and duplicate resolution. Counts alone cannot prove the same records or values were preserved; choose comparisons appropriate to the transformation.
- Check cutover gates and post-cutover writers. Completion requires the relevant existing population and new writes to satisfy the target invariant, or an explicit unresolved exception.

For example, a backfill that blindly copies an old value over a newer user edit can finish every batch successfully and still be wrong. Conditional writes, ordering or another documented coordination method must preserve the intended winner.

### DB-11 — Seeds, mocks and migration verification

Migration and fixture evidence must cover supported starting states and relevant production semantics, including local setup and recovery paths.

- Inspect fresh installation and upgrade from populated supported versions. Include legacy nulls, duplicates, large values, boundary dates and tenant references selected from the affected invariant.
- Check seed order, required reference data, generated identifiers, repeated execution where supported and cleanup. Keep development-only records from unintended production paths.
- Inspect the migration chain's historical dependencies and models. Verify code still needed by old migrations remains available or has an approved replacement.
- Compare mocks and local engines with production for constraints, types, isolation, collation, transactions and DDL. A substitute engine can support fast tests but does not prove incompatible production semantics.
- Check the promised rollback path with written post-migration data and its stated loss limits. An intentionally irreversible migration needs a documented forward repair or restore path, not a fabricated reverse migration.

For example, SQLite foreign-key declarations need enforcement enabled for the connection. A passing test with enforcement disabled cannot demonstrate production referential integrity. Django data migrations use historical models; importing only current models can break a future clean installation.

### DB-12 — Retention and deletion

Persistence behavior must meet established retention, deletion and hold requirements across the affected records and copies.

- Identify the authoritative requirement, eligible population, expiry calculation, clock/unit handling, exceptions and holds. Ask the lead when obligations conflict or are missing; do not invent a retention period.
- Trace logical deletion, physical deletion, cascades, history, derived stores, caches, replicas and backups. Distinguish immediate loss of access from eventual removal and from expiry of retained backups.
- Inspect failed/partial batches, retries and reconciliation. Check that later imports, replay or restoration do not silently resurrect data contrary to the approved requirement.
- Establish actual expiry guarantees. DynamoDB TTL deletes asynchronously; an expiry attribute alone does not prove immediate deletion or exclusion from reads.

Compliance owns the applicable legal/contractual obligation; Security owns exposure and access judgments. Database supplies lifecycle semantics and evidence, including copies not inspected.

### DB-13 — Maintenance, partitioning and storage capacity

For long-lived or growing stores, maintenance and data placement must preserve the required availability and integrity under the actual workload.

- Inspect relevant cleanup, statistics, compaction/vacuum, log retention, index health and disk/memory headroom evidence. Include long-lived transactions, retained replication logs and maintenance competing with normal work.
- Where partitioning/sharding exists or changes, check routing keys, skew/hot keys, missing/future partitions, cross-partition operations and the scope of unique/reference guarantees. Verify pruning or targeted access from relevant evidence.
- Trace partition creation/attachment/removal and data movement through compatible callers, constraints and recovery. Dropping a partition must respect retention and holds.
- For evicting stores, inspect which keys can disappear and how writes behave at capacity. Retaining authoritative state requires a compatible failure/recovery design; changing to `noeviction` introduces write-error handling rather than unlimited capacity.

PostgreSQL maintenance prevents specific storage/transaction-age problems, and partitioned uniqueness has key restrictions. These do not justify prescribing partitions, manual vacuum schedules or a database-per-tenant design for every SaaS application.

### DB-14 — Replication, read consistency and failover

Replication and read routing must provide the consistency and failure guarantees required by the affected operations.

- Identify where reads/writes go and the actual acknowledgment, read concern, write concern or equivalent settings. Separate durable acknowledgment, replica receipt and visibility to readers.
- Trace read-after-write, stale decisions, multi-record snapshots and failover during an uncertain write. Determine whether callers can tolerate the resulting behavior or have a verified coordination mechanism.
- Inspect evidence for replication lag, retained logs, promotion, old-writer exclusion and client reconnection under the documented topology. Identify duplicate/lost work and reconciliation after recovery.
- For managed/nonrelational stores, check guarantees of each access path. A base table's consistency option may not apply to a secondary index; use the selected regional/global configuration rather than general product claims.

For example, DynamoDB global secondary index reads are eventually consistent. PostgreSQL streaming replication is asynchronous by default; MongoDB guarantees depend on read/write concerns and routing. No generic “replicated” label proves zero data loss or immediate read visibility. Database establishes storage effects; DevOps reviews failover execution and Architecture the topology.

### DB-15 — Backup, restore and rebuilding

Recovery claims must be supported by a compatible recovery chain and evidence that the required data and behavior can be restored or rebuilt.

- Identify backup scope, retention, consistency, required logs, engine/version compatibility, encryption keys, configuration and dependencies. Distinguish logical export, physical backup, crash recovery, point-in-time recovery and replica failover.
- Inspect restore/rebuild evidence for the represented version, population, failure scenario and recovery point. Check recovered invariants, tenant boundaries, privileged objects and application usability, not only process exit status.
- Compare observed recovery duration and data loss with established objectives; disclose unmeasured stages and unavailable evidence. A backup setting alone does not demonstrate a restore, while absent exercise evidence does not prove inevitable data loss.
- Trace authoritative-source reconciliation and partial restore effects on derived stores, external side effects and deletion obligations. Confirm the scope of any claimed per-tenant restore; whole-cluster recovery does not establish it.

PostgreSQL point-in-time recovery needs an appropriate base backup and continuous required WAL history; a logical dump cannot substitute in that chain. Redis recovery depends on its selected persistence mode. These are examples, not a mandate that every project use point-in-time recovery. The reviewer inspects evidence and requests missing verification through the lead; it does not restore a database.

## Verification

For each selected control, connect the criterion and invariant to located implementation evidence, a relevant failure case and a legitimate case that must remain valid. Use an invariant-to-writer table, two-operation schedule, caller/schema compatibility matrix or recovery-chain sketch only when it clarifies that assignment. These are methods within the existing report, not mandatory new project documents.

Consume supplied schema/configuration captures, query plans, migration output, representative measurements and test/restore records. Record their environment, version, population and limitations. Do not execute SQL, `EXPLAIN`, migrations, maintenance, load tests or restoration through the reviewer role. In particular, PostgreSQL `EXPLAIN ANALYZE` executes the statement; a diagnostic label does not make it read-only.

Report verified contradictions, supported improvements and unresolved questions separately through the shared contract. Missing measurements may limit a performance claim without hiding an evidenced correctness defect. A clean result covers the inspected paths and chosen criteria only. Test definitions, hypothetical examples and document checks are not runtime results.

## Responsibilities and exceptions

Database owns storage semantics, query-plan/lock analysis, persistence integrity and data-recovery assessment. The lead resolves scope, cross-domain ownership, conflicts and exceptions through shared guidance. Security owns exploitation/authorization judgments, Performance end-to-end performance, DevOps deployment and recovery execution, Architecture structural choices, Code application mechanisms, Testing test quality and Compliance established external obligations.

User/project replacements or waivers follow [Review scope and criteria](../intent_context.md#review-scope-and-criteria). Keep their source, scope and remaining consequences visible. Do not silently substitute stricter defaults, treat vendor documentation as project approval or label an exception technically safe without evidence.

## Ownership, review, and related policy

The Engineering Review Team maintains this Technical Standard (STD) under the [Database Policy (POL)](../policies/database.md). Review affected controls when supported engine semantics, project requirements, recurrent false positives or uncovered failure modes change. Preserve `DB-xx` IDs when refining a rule; record material scope changes in package maintenance.

## Research reference

[Sources and control mappings](../research/database.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
