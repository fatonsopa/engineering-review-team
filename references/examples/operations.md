# Operations Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/operations.md) to actual captured inputs.

## How it works and why

Defective case: A worker acknowledges a message before committing the required database update. Termination between those actions loses work. Trace acknowledgement, commit and restart behavior; choose a durable ordering and verify recovery.

Clean counterexample: The worker commits an idempotent update before acknowledgement. A crash may redeliver the message, but the deduplication key prevents duplicate effects. Verify the relevant broker and storage guarantees.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[Google SRE launch guidance](https://sre.google/sre-book/reliable-product-launches/)
