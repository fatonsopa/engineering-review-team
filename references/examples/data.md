# Data Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/data.md) to actual captured inputs.

## How it works and why

Defective case: Two concurrent purchases both read stock=1 and each commits a decrement and reservation without an atomic availability condition. State the transaction schedule and engine assumptions; enforce the invariant in one guarded update or appropriate lock.

Clean counterexample: A guarded update reserves stock only when the remaining quantity is sufficient, and the reservation commits in the same transaction. Verify affected-row handling and rollback under the actual engine semantics.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), when PostgreSQL is the actual engine
