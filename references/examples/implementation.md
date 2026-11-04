# Implementation Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/implementation.md) to actual captured inputs.

## How it works and why

Defective case: A search UI accepts a late response for query A after query B has already completed. The old response overwrites the current results. Record the request sequence and commit only a response whose generation matches the active query.

Clean counterexample: A response carries a generation token checked before updating state. Cancellation is an optimization; the generation guard preserves correctness even when cancellation races.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[Google review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
