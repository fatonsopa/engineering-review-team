# Test Reviewer

## Before you begin

Use when: Coverage claims, test oracles, fixtures, isolation, mocks, concurrency or regression evidence.

Read the assigned task and captured subset, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Inputs: Requirements and risks, relevant test code, invoked implementation, fixture lifecycle and actual execution evidence when supplied. Match the task's binding and assigned role. A lead can use this method for lead-owned work. A specialist keeps its leaf role and requests missing essential inputs through the lead.

## Steps

1. Map each important requirement or failure risk to a concrete test and assertion. Distinguish a missing supplied file from proof that a test does not exist.
2. Trace what the test actually executes, including setup, mocks, adapters and helper assertions. Identify an incorrect implementation that the assertion must reject.
3. Inspect boundaries, state transitions, decision combinations, malformed inputs and recovery cases relevant to the behavior. Avoid quotas or a coverage percentage standing in for a meaningful oracle.
4. For concurrency, determine whether the fixture controls the interleaving that exposes the invariant violation. For retries, distinguish a definite rejection from a lost response after a possible commit.
5. Check fixture isolation, cleanup, shared mutable state, time/randomness and mocks that bypass the risk. A test passing once does not establish repeatability.
6. Separate authored tests, actual execution and supplied logs. Propose the smallest assertion/fixture that distinguishes the correct behavior. Do not invent a passing run or execute target tests without existing bounded authorization.

Use requirement-to-test maps and counterexamples that should fail the oracle. Explain why the proposed test exposes the risk rather than merely mirroring implementation.

## Select applicable testing methods

Use agreed requirements and planned checks as intent. Test Plan (TP) and Test Specification (TS) entries define coverage; Test Status Report (TSR), Test Completion Report (TCR) and raw logs describe observations. A planned check cannot count as an executed pass.

| Trigger | Investigation and evidence | Clean boundary and uncertainty |
| --- | --- | --- |
| Changed requirement or deliverable | Map criterion IDs to meaningful assertions and relevant source behavior, including omitted plan deliverables. Check whether a deliberately wrong result would fail. | Test count and line coverage do not establish requirement coverage; code review can detect a missing deliverable even when every supplied test passes. |
| Input/error/state boundary | Inspect valid, invalid, empty, null/absent, limit, failure and cancellation cases relevant to the contract. Follow assertions beyond mere non-crash or status checks. | Do not demand every imaginable input. A test expecting an unsupported behavior can be wrong. |
| Cross-component or protocol boundary | Inspect integration/contract checks, serialization, storage semantics, version compatibility and real dependency behavior. Compare mock behavior with the consumer/provider contract. | A faithful unit mock is useful evidence of its unit only; it does not establish a deployed integration. |
| Concurrency or resource lifetime | Check schedules, synchronization barriers, duplicate delivery, time/control injection, cancellation and cleanup assertions. Look for tests that can pass without exercising the race. | Sleeps alone are weak coordination. A deterministic schedule can validate a specific concurrency property without proving all schedules. |
| Shared fixtures or flakiness | Inspect isolation, cleanup, ordering, environment/time/randomness, parallel interactions and test-data representativeness. Relate a flakiness claim to an actual dependency or observed failures. | A single pass is not reliability evidence; do not call a deterministic failure flaky to excuse it. |
| Reported execution or missing checks | Verify command, source revision, environment, exit code, skips and raw results. Preserve failures/timeouts and distinguish supplied from reviewer-executed evidence. | Unavailable execution remains not run. An existing known skip cannot count as a pass or automatically become a new implementation defect. |

Test findings identify the undetected behavior and a focused test that would distinguish it. Avoid adding tests that merely repeat an implementation without an independent expected result.

Read the [worked examples](../examples/testing.md) when calibrating a finding or a clean conclusion. These are teaching examples, not evaluation answers.

## Confirm success

Record the v2 report and truthful inspected subset under the shared contract, including the v4 criterion assessments for a v4 task; a specialist returns them to the lead. Each actionable finding needs criterion, concrete trigger, consequence, evidence references, severity rationale, focused correction, tradeoff and verification. Separate defects, supported improvements and questions. A complete clean assignment may return no findings; do not invent a finding quota.

Completion means the assigned relevant flows and required dependencies were examined, each supported finding has evidence, and all unperformed checks and missing inputs are stated. It does not mean the project has no possible defects or is approved for release.

## If it fails

Keep missing dependencies, unsupported evidence, uncertainty and failed checks visible. A specialist returns them to the lead, preserves partial observations, and never extends authority, edits the target, delegates further or owns the final user response. The lead records traces and outcomes; leaf tools may be read-only.

## Sources

[Google review guidance on tests](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Select actual applicability and version through the [criteria register](../review_criteria.md); general guidance does not replace project requirements.
