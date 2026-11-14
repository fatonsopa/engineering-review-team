# Database review research references

Consult this record when verifying a source, checking a version-dependent claim or maintaining the reviewer. Do not load it automatically for routine reviews. The technical standard owns the controls; these references do not independently create project obligations.

## Domains references

Version-specific engine references and their control mappings are in the [source table](#standards-references) and [control-to-source mapping](#control-to-source-mapping) below. [PostgreSQL transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html) and [MongoDB atomicity](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/) support examining actual operation boundaries. [MySQL online DDL limitations](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-limitations.html) and [PostgreSQL query-plan guidance](https://www.postgresql.org/docs/18/using-explain.html) support conditional migration and performance judgment. These are method sources, not evidence of the target's engine or adopted requirements.

## Standards references

Official primary sources below were opened on **2026-11-04**. Versioned pages are reference baselines, not requirements to use those releases. Living pages lack a fixed release contract; confirm the actual engine/service/driver version and relevant configuration before relying on their behavior. Sources establish mechanisms, not complete industry certification or applicability to every database. The mapped controls combine those mechanisms with explicitly identified package review methods.

| ID | Primary source and reference baseline | Controls |
| --- | --- | --- |
| S1 | PostgreSQL 18: [Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html) | DB-02, DB-08 |
| S2 | PostgreSQL 18: [Row security policies](https://www.postgresql.org/docs/18/ddl-rowsecurity.html) | DB-03 |
| S3 | PostgreSQL 18: [CREATE FUNCTION; security-definer guidance](https://www.postgresql.org/docs/18/sql-createfunction.html) | DB-03 |
| S4 | PostgreSQL 18: [Transaction isolation](https://www.postgresql.org/docs/18/transaction-iso.html) | DB-04–05 |
| S5 | PostgreSQL 18: [Explicit locking](https://www.postgresql.org/docs/18/explicit-locking.html) | DB-06 |
| S6 | PostgreSQL 18: [Using EXPLAIN](https://www.postgresql.org/docs/18/using-explain.html) | DB-08; Verification |
| S7 | PostgreSQL 18: [LIMIT and OFFSET](https://www.postgresql.org/docs/18/queries-limit.html) | DB-07 |
| S8 | PostgreSQL 18: [CREATE INDEX](https://www.postgresql.org/docs/18/sql-createindex.html) | DB-08–09 |
| S9 | MySQL 8.4: [Foreign-key constraints](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html) | DB-08 |
| S10 | MongoDB 8.0: [Atomicity and transactions](https://www.mongodb.com/docs/v8.0/core/write-operations-atomicity/) | DB-04–05, DB-10 |
| S11 | MongoDB 8.0: [Schema validation](https://www.mongodb.com/docs/v8.0/core/schema-validation/) | DB-02 |
| S12 | MongoDB 8.0: [Read isolation, consistency and recency](https://www.mongodb.com/docs/v8.0/core/read-isolation-consistency-recency/) | DB-14 |
| S13 | PgBouncer living documentation: [Pooling feature compatibility](https://www.pgbouncer.org/features.html) | DB-06 |
| S14 | PgBouncer living documentation: [Connection limits and configuration](https://www.pgbouncer.org/config.html) | DB-06 |
| S15 | SQLite living documentation: [Foreign-key support](https://www.sqlite.org/foreignkeys.html) | DB-02, DB-11 |
| S16 | SQLite living documentation: [Isolation](https://www.sqlite.org/isolation.html) | DB-06, DB-11 |
| S17 | Redis living documentation: [Transactions and command errors](https://redis.io/docs/latest/develop/using-commands/transactions/) | DB-04 |
| S18 | Redis living documentation: [Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) | DB-01, DB-15 |
| S19 | Redis living documentation: [Key eviction](https://redis.io/docs/latest/develop/reference/eviction/) | DB-01, DB-13 |
| S20 | Django 5.2: [Database access optimization](https://docs.djangoproject.com/en/5.2/topics/db/optimization/) | DB-08 |
| S21 | MySQL 8.4: [Statements causing implicit commit](https://dev.mysql.com/doc/refman/8.4/en/implicit-commit.html) | DB-04, DB-09 |
| S22 | PostgreSQL 18: [ALTER TABLE; constraint validation and locking](https://www.postgresql.org/docs/18/sql-altertable.html) | DB-09–10 |
| S23 | MySQL 8.4: [Online DDL limitations](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-limitations.html) | DB-09 |
| S24 | Django 5.2: [Migrations; historical models and reversibility](https://docs.djangoproject.com/en/5.2/topics/migrations/) | DB-11 |
| S25 | DynamoDB living service documentation: [Time to live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) | DB-12 |
| S26 | PostgreSQL 18: [Routine vacuuming](https://www.postgresql.org/docs/18/routine-vacuuming.html) | DB-13 |
| S27 | PostgreSQL 18: [Table partitioning](https://www.postgresql.org/docs/18/ddl-partitioning.html) | DB-13 |
| S28 | PostgreSQL 18: [Standby servers and replication](https://www.postgresql.org/docs/18/warm-standby.html) | DB-14 |
| S29 | DynamoDB living service documentation: [Read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) | DB-14 |
| S30 | PostgreSQL 18: [Continuous archiving and point-in-time recovery](https://www.postgresql.org/docs/18/continuous-archiving.html) | DB-15 |

## Control-to-source mapping

The entries below preserve the source associations and qualifications used when authoring the controls. They are research evidence, not additional review instructions.

- **DB-01 — Storage contracts and invariants:** For example, an evictable Redis cache and Redis used as the sole store have different consequences when keys disappear. Review persistence and eviction choices against that role; do not require a cache to preserve reconstructible data indefinitely. S18–S19 support these mechanisms; the inventory method is package design.
- **DB-02 — Types, constraints and representation:** PostgreSQL `CHECK` can accept null, and its unique constraints have explicit null semantics. MongoDB validation can be configured to warn instead of reject; validation settings affect existing records. Neither a constraint name nor a validator's presence proves the intended invariant. S1, S11 and S15 support these checks.
- **DB-03 — Tenant keys, database access and stored routines:** For example, PostgreSQL table owners normally bypass row security; a policy tested only under an ordinary role does not establish the owner's behavior. Definer routines need safe object resolution and execution grants. Supply this database evidence to Security for exploitation and authorization judgment; do not duplicate its threat catalogue. S2–S3.
- **DB-04 — Atomicity, isolation and concurrent changes:** For example, two requests can both observe a free slot before either inserts. A transaction keyword or application precheck does not resolve that schedule. A correctly scoped uniqueness constraint with conflict handling may do so without imposing serializable isolation on the whole application. S4, S10, S17 and S21.
- **DB-05 — Uncertain outcomes, retries and deduplication:** A new identifier on every retry cannot deduplicate the same logical operation. Conversely, a repeated request with the same durable identity and confirmed stored result need not create another effect. Storage atomicity is Database's responsibility; Code owns caller retry behavior and Architecture owns the cross-system coordination choice. S4 and S10 support transaction boundaries; this outcome-tracing method is package design.
- **DB-06 — Locks, deadlocks and connection pools:** PgBouncer transaction pooling does not preserve arbitrary session features; prepared-statement support depends on mechanism and configuration. SQLite's writer concurrency also differs from server databases. Compare the actual mode with its callers instead of demanding a universal pool size or lock-free writes. S5, S13–S14 and S16.
- **DB-07 — Query results and pagination:** For example, ordering only by a nonunique creation time cannot define a stable page boundary among ties. PostgreSQL documents the need for unique ordering with `LIMIT`/`OFFSET`; source S7 does not establish the application's cross-request snapshot contract.
- **DB-08 — Query cost, indexes and statistics:** A full scan can be appropriate for a small table or a query reading most rows. Foreign-key indexing is engine-specific: PostgreSQL does not automatically index referencing columns; MySQL/InnoDB creates a required suitable referencing index if missing. Inspect actual metadata before recommending another index. S1, S6, S8–S9 and S20.
- **DB-09 — Mixed-version migrations and DDL:** Adding a required column can break an old writer even after existing rows are backfilled. “Online” DDL does not mean no blocking: MySQL online operations still need metadata locks. PostgreSQL concurrent index creation has failure states and transaction restrictions. Use exact-version evidence; do not promise zero downtime from a keyword. S8, S21–S23.
- **DB-10 — Backfills and reconciliation:** For example, a backfill that blindly copies an old value over a newer user edit can finish every batch successfully and still be wrong. Conditional writes, ordering or another documented coordination method must preserve the intended winner. S10 and S22 support conditional enforcement/validation mechanisms; checkpoint and reconciliation review is package design.
- **DB-11 — Seeds, mocks and migration verification:** For example, SQLite foreign-key declarations need enforcement enabled for the connection. A passing test with enforcement disabled cannot demonstrate production referential integrity. Django data migrations use historical models; importing only current models can break a future clean installation. S15, S16 and S24.
- **DB-12 — Retention and deletion:** Compliance owns the applicable legal/contractual obligation; Security owns exposure and access judgments. Database supplies lifecycle semantics and evidence, including copies not inspected. S25 supports the TTL distinction; the lifecycle tracing method is package design.
- **DB-13 — Maintenance, partitioning and storage capacity:** PostgreSQL maintenance prevents specific storage/transaction-age problems, and partitioned uniqueness has key restrictions. These do not justify prescribing partitions, manual vacuum schedules or a database-per-tenant design for every SaaS application. S19, S26–S27.
- **DB-14 — Replication, read consistency and failover:** For example, DynamoDB global secondary index reads are eventually consistent. PostgreSQL streaming replication is asynchronous by default; MongoDB guarantees depend on read/write concerns and routing. No generic “replicated” label proves zero data loss or immediate read visibility. Database establishes storage effects; DevOps reviews failover execution and Architecture the topology. S12, S28–S29.
- **DB-15 — Backup, restore and rebuilding:** PostgreSQL point-in-time recovery needs an appropriate base backup and continuous required WAL history; a logical dump cannot substitute in that chain. Redis recovery depends on its selected persistence mode. These are examples, not a mandate that every project use point-in-time recovery. The reviewer inspects evidence and requests missing verification through the lead; it does not restore a database. S18 and S30.
- **Verification:** Consume supplied schema/configuration captures, query plans, migration output, representative measurements and test/restore records. Record their environment, version, population and limitations. Do not execute SQL, `EXPLAIN`, migrations, maintenance, load tests or restoration through the reviewer role. In particular, PostgreSQL `EXPLAIN ANALYZE` executes the statement; a diagnostic label does not make it read-only (S6).
