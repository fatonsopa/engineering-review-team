# Test Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/testing.md) to actual captured inputs.

## How it works and why

Defective case: A mock replaces the serializer whose escaping behavior the test claims to cover. The test verifies only that the mock was called, so malformed output cannot fail it. Use the real serializer at that boundary and compare externally visible bytes.

Clean counterexample: A focused unit test mocks the network but exercises the real serializer and checks the required output, including special characters. Mocking an unrelated dependency does not invalidate the oracle.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[Google review guidance on tests](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
