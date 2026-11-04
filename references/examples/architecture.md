# Architecture Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/architecture.md) to actual captured inputs.

## How it works and why

Defective case: A payment service calls its notification provider inside the database transaction. Provider latency holds database locks and prevents payment completion, contrary to a supplied availability requirement. Record the failure scenario and compare an outbox against a bounded synchronous path.

Clean counterexample: A small internal tool intentionally sends a bounded notification synchronously after committing its data. Its documented latency and delivery requirements permit that tradeoff; service extraction alone is not an improvement.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[SEI architecture evaluation](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/)
