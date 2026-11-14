# Testing review technical standard

## Contents

- [Purpose and scope](#purpose-and-scope)
- [Definitions](#definitions)
- [Principles](#principles)
- [Applicability and phases](#applicability-and-phases)
- [Rules](#rules)
- [TEST-01 — Scope, risks and criteria](#test-01--scope-risks-and-criteria)
- [TEST-02 — Meaningful oracles and assertions](#test-02--meaningful-oracles-and-assertions)
- [TEST-03 — Inputs, decisions and state transitions](#test-03--inputs-decisions-and-state-transitions)
- [TEST-04 — Test levels and integration contracts](#test-04--test-levels-and-integration-contracts)
- [TEST-05 — Test doubles and environment fidelity](#test-05--test-doubles-and-environment-fidelity)
- [TEST-06 — Fixtures, isolation and cleanup](#test-06--fixtures-isolation-and-cleanup)
- [TEST-07 — Time, randomness and asynchronous completion](#test-07--time-randomness-and-asynchronous-completion)
- [TEST-08 — Concurrency, retries and partial effects](#test-08--concurrency-retries-and-partial-effects)
- [TEST-09 — Security, tenant and privacy verification](#test-09--security-tenant-and-privacy-verification)
- [TEST-10 — Data changes and version compatibility](#test-10--data-changes-and-version-compatibility)
- [TEST-11 — Resilience, performance and resources](#test-11--resilience-performance-and-resources)
- [TEST-12 — User interfaces, accessibility and locales](#test-12--user-interfaces-accessibility-and-locales)
- [TEST-13 — Test selection and execution evidence](#test-13--test-selection-and-execution-evidence)
- [TEST-14 — Flakiness, retries and quarantine](#test-14--flakiness-retries-and-quarantine)
- [TEST-15 — Metrics, regressions and maintainability](#test-15--metrics-regressions-and-maintainability)
- [Verification](#verification)
- [Responsibilities and exceptions](#responsibilities-and-exceptions)
- [Ownership, review, and related policy](#ownership-review-and-related-policy)

## Purpose and scope

The Testing Reviewer assesses whether the assigned verification can distinguish required behavior from relevant failures, and whether execution claims match the supplied evidence. Scope includes test code, selected implementation paths, fixtures, configuration, planned checks and actual results. It does not replace domain review, execute the target's tests or approve release.

The [Testing Policy (POL)](../policies/testing.md) governs judgment. Team-owned [Review scope and criteria](../intent_context.md#review-scope-and-criteria) establishes applicable project rules, defaults, replacements and waivers. The shared [Review Technical Standard (STD)](../review_standard.md) owns evidence, findings and return fields. This standard introduces no separate document catalog or report schema.

`TEST-01`–`TEST-15` are package-designed controls. Primary sources support selected methods and framework behavior; they do not mandate this control list or a universal testing architecture. Examples are hypothetical. Use the target's actual language, framework, runner, dependency versions and declared behavior before applying them.

## Definitions

- A **test oracle** decides whether an observed result satisfies the expected behavior. It may be an assertion, reference result, invariant or qualified human assessment.
- **Coverage** needs a named subject: requirements, states, risks, code execution or environments. These measures are not interchangeable.
- A **test double** replaces a dependency in a test. Its **fidelity** is how accurately it represents the behavior relevant to that test.
- A **fixture** establishes test state and dependencies; its lifecycle includes setup, cleanup and failed setup.
- **Flakiness** is inconsistent outcome under conditions intended to be equivalent. An unexplained failure alone does not establish flakiness.
- **Execution evidence** records an actual attempt and its conditions. Authored or planned tests are not execution evidence; missing evidence does not establish that no attempt occurred.

## Principles

Begin with the required behavior and a plausible wrong result the test should reject. Trace what actually executes and what the oracle observes. A test name, mock call, status code or green summary can conceal an unexamined behavior.

Scale verification to risk and change. Account for new and changed decisions, outcomes and significant dependencies, with reasons for material exclusions. Preserve explicitly adopted coverage or release gates. Without such a requirement, do not prescribe one test per syntactic branch, a fixed testing pyramid ratio, every test level, or an arbitrary percentage.

Keep authored coverage, observed execution and confidence distinct. Preserve failures, timeouts, skips, partial results and limitations. Recommend a focused discriminating check, not extra tests whose expected result simply repeats the implementation.

## Applicability and phases

Read the control list, select relevant controls and read them in full. A narrow change needs its affected behavior and dependencies assessed; it need not trigger a new audit of the entire test estate. The lead routes actual requirement, design, threat, service and verification sections through the shared map. Optional standalone documents are not prerequisites.

| Phase | Relevant depth |
| --- | --- |
| Foundation | Meaningful checks for important behavior, input boundaries and recoverable local state. Use simple fixtures and test levels that expose actual risks. |
| Production launch | Include real access/tenant boundaries, persistence, supported integrations, failure behavior and trustworthy release evidence where affected. |
| Growth | Extend to representative populations, concurrency, overload, parallel-test isolation, resource behavior and supported version combinations. |
| Advanced scale or criticality | Require the evidence warranted by actual recovery, availability, privacy or compatibility commitments; examine fault and recovery scenarios within separately authorized bounds. |

Real users, sensitive data, irreversible effects and shared resources can require deeper checks at any phase. A prototype label cannot waive an applicable obligation. Fuzzing, property-based testing, mutation testing and fault injection are options when they address a concrete gap, not mandatory tools for every change.

## Rules

### TEST-01 — Scope, risks and criteria

Verification coverage must account for the assigned requirements, changed behavior and material failure risks.

- Map each important criterion to its test or other verification, exercised path and observable assertion. Include new/changed branches, error outcomes and accepted plan deliverables; explain exclusions or missing evidence.
- Establish the real input revision, dependency scope and relevant project decisions. A stale expected result or proposed requirement cannot silently become the oracle.
- Distinguish an absent test found through a bounded search from a file or result that was not supplied. Record search limits and request essential dependencies through the lead.
- Inspect accepted manual or observational checks on their merits. An automation gap and a complete lack of verification are different conclusions.

For example, a migration deliverable omitted from the implementation remains uncovered even if all supplied API tests pass. Conversely, a focused test can cover several decision outcomes without one test function per branch.

### TEST-02 — Meaningful oracles and assertions

A test must reject the relevant incorrect behavior while permitting legitimate behavior within its contract.

- Trace the actual implementation, adapters, helpers and assertions. Identify a concrete wrong result that would still pass; avoid judging only names or test counts.
- Check observable values, state changes, absence of forbidden effects and relevant error/log behavior. A successful status or “did not throw” can be sufficient for that narrow contract, but not for an unasserted data effect.
- Inspect assertions hidden in callbacks, broad exception handlers, empty collections or conditional branches. Ensure the expected failure path cannot succeed without checking anything.
- Check tolerances, ordering and snapshot expectations against the required behavior. Keep nondeterministic incidental data out of the oracle without hiding meaningful differences; review updated expected outputs rather than automatically accepting them.

A serializer test that mocks the serializer and checks only a call cannot establish escaping. Mocking the network while running the real serializer and checking its output can be appropriate. A model-generated or human-written test needs the same review.

### TEST-03 — Inputs, decisions and state transitions

Selected cases must exercise the meaningful partitions and transitions that can change the required result.

- Inspect valid, invalid, empty, null/absent, minimum/maximum and just-outside values where the contract distinguishes them. Include malformed encodings, precision or size limits when relevant.
- Trace decision combinations, state transitions, repeated operations and invalid sequences. Check entry preconditions and the state left after rejection, cancellation or partial failure.
- For generated/property-based or fuzz tests, inspect input domains, constraints, assertions, replay information and failure reduction. A large run count does not compensate for a generator that excludes the risky values.
- Keep expected results independent enough to expose the error. Round-trip and differential checks need care when both paths share the same defect or the comparison implementation has different semantics.

For example, testing only “below limit” and “well above limit” can miss an off-by-one error at the actual boundary. Stateful generation can explore operation sequences, but a simple example table may be sufficient.

### TEST-04 — Test levels and integration contracts

The selected test level must exercise the boundary on which the claim depends.

- Determine which logic is isolated and which components, processes or real dependencies participate. Test labels alone do not establish unit, integration, contract or end-to-end coverage.
- Inspect producer and consumer agreement on serialization, required/optional fields, errors, permissions, ordering and version compatibility as applicable.
- Check that consumer expectations are verified against a relevant provider implementation and state when contract testing is claimed. A mock response or schema check alone does not establish deployed interoperability.
- Use broader tests for risks that narrower tests cannot expose, balancing diagnosis, cost and reliability. Do not demand every layer for every rule or treat end-to-end tests as a universal substitute.

Pact checks selected request/response interactions; that does not prove the provider's unasserted side effects, performance or entire business workflow. A real integration test remains appropriate where it observes the required boundary directly.

### TEST-05 — Test doubles and environment fidelity

A substitute or test environment must preserve the semantics needed for the claim, with material differences disclosed.

- Identify replaced components and compare their behavior with relevant production contracts: errors, timeouts, consistency, validation, serialization, transactions and permissions.
- Check that mocks do not bypass the behavior under review. Interaction assertions are useful when the interaction itself is the contract; they do not prove an unexecuted dependency's behavior.
- Inspect actual engine/runtime versions, feature flags, configuration and permissions relevant to the test. A container, emulator or staging label does not establish parity.
- Look for complementary real-boundary evidence where a double cannot represent the risk. Do not ban mocks or require a complete production clone for every unit test.

For example, Django's transaction-wrapped `TestCase` can conceal whether code establishes a required transaction; its documented `TransactionTestCase` supports observing commit/rollback behavior. The actual backend still matters. These examples do not mandate Django or a particular testing framework.

### TEST-06 — Fixtures, isolation and cleanup

Fixtures must establish the intended state and leave unrelated tests and resources unaffected, including failed setup.

- Trace fixture scope, creation order and cleanup through success, exception, cancellation and partial setup. Check database rows, files, ports, accounts, environment variables, patched functions and background workers.
- Inspect shared mutable state and ordering assumptions, including parallel workers and repeated runs. Shared immutable setup can be legitimate; mutable state needs isolation or controlled serialization.
- Check realistic keys, tenant ownership, existing records and exceptional populations selected from the risk. Keep sensitive production data and credentials out of unsafe fixtures and artifacts.
- Verify teardown targets only owned test resources. Cleanup must not erase the evidence needed to diagnose the attempt or affect production/shared external resources.

In pytest, code after a fixture's `yield` does not run if that fixture raises before yielding. A compact setup that allocates two resources and then fails can therefore leak the first unless cleanup was arranged safely. Inspect the actual lifecycle rather than counting teardown methods.

### TEST-07 — Time, randomness and asynchronous completion

Tests must control or observe nondeterminism sufficiently to make their assertions meaningful and their failures diagnosable.

- Inspect clocks, dates/timezones, random inputs, identifiers and external state. Record or preserve values needed to reproduce failures; a fixed seed does not control unrelated concurrency or service state.
- Ensure the runner waits for relevant asynchronous work and propagates rejection, timeout and callback failures. Check that a test cannot finish before its assertion executes.
- Prefer condition-based waits or explicit synchronization over unexplained sleeps. Keep real timeout limits appropriate to the contract and environment; simulated time cannot prove real scheduler or network behavior.
- Inspect clock advancement, pending timers, cancellation and cleanup when fake time is used. Verify the code actually reads the substituted clock and that the substitution is restored.

For example, failing to await or return an asynchronous assertion’s promise can let a Jest test finish before that assertion settles. Either correctly awaiting or returning the promise avoids that specific gap without requiring arbitrary sleeps.

### TEST-08 — Concurrency, retries and partial effects

Tests for concurrent or repeated operations must reach the relevant interleaving and observe the invariant after the operation completes or fails.

- Match the fixture to a concrete schedule: competing readers/writers, duplicate delivery, out-of-order completion, cancellation or retry. Use barriers, controlled dependencies or equivalent evidence that the critical overlap occurred.
- Distinguish definite rejection from a lost response after possible commit. Check repeat effects, durable identity, partial progress and reconciliation when the contract requires them.
- Inspect assertions on final state, forbidden intermediate effects and resource cleanup. Concurrent requests that happen to run sequentially do not establish race coverage.
- Treat runtime race detectors and stress runs as evidence for exercised conditions. A clean run cannot establish every schedule, distributed invariant or deadlock property.

A retry test that fails before every write misses duplicate effects after a lost commit acknowledgment. A controlled post-commit response loss plus a stored-state assertion can expose that risk.

### TEST-09 — Security, tenant and privacy verification

Where security or privacy behavior is in scope, verification must exercise the real enforcement path and distinguish denied operations from permitted ones.

- Map relevant Security criteria to identities, roles/permissions, tenants, object ownership, trusted/untrusted inputs and affected surfaces. Include both legitimate requests and unauthorized alternatives where applicable.
- Check that denial asserts the protected effect did not occur, rather than only checking an error response. Inspect alternate APIs, jobs, cache paths and changed privileges relevant to the assigned boundary.
- Review regression evidence for assigned injection, session, secret, sensitive-output, abuse or resource-limit concerns. A broad scanner result cannot substitute for the application's specific authorization or business-rule oracle.
- Inspect safe test identities, synthetic data, isolated targets and artifact redaction. A test definition does not authorize exploitation, traffic generation or production access by this reviewer.

For example, a tenant-isolation test that uses an administrator fixture with bypass privileges may never exercise the ordinary-user boundary. The same privileged fixture can be correct for an explicitly administrative operation. Security defines the threat/control judgment; Testing assesses whether the checks demonstrate it. This does not claim full WSTG coverage.

### TEST-10 — Data changes and version compatibility

Verification of persistence or interface changes must cover the supported starting states, callers and transition guarantees relevant to the change.

- Inspect fresh setup and upgrades from populated supported versions, including legacy nulls, duplicates, keys, seeds and retained historical dependencies.
- Check old/new readers and writers across intermediate schema/message states when versions coexist. A new-version-only test cannot establish rolling compatibility.
- Inspect failure, restart, partial backfill, reconciliation and duplicate-processing assertions. Validate identities, values and invariants where counts alone could conceal corruption.
- Evaluate the promised rollback, forward repair or restore route using relevant post-change data. An irreversible migration needs honest recovery evidence; an inverse schema operation does not prove value recovery.

For example, Django migrations depend on historical models and retained references; testing only the current model state misses a broken clean installation. Database establishes engine guarantees and compatibility risks; Testing checks whether fixtures and assertions expose them.

### TEST-11 — Resilience, performance and resources

Tests supporting service or capacity claims must represent the relevant failure/workload conditions and measure the promised outcome.

- Inspect dependency timeout/unavailability, partial responses, overload, cancellation and recovery checks where applicable. Verify degraded behavior, bounded retries, cleanup and restored correctness rather than process survival alone.
- For load/benchmark evidence, establish workload shape, arrival/concurrency model, duration, data size/skew, cache/warmup conditions, environment and measurement scope. Check generator saturation or omitted work that can invalidate a capacity claim.
- Compare relevant latency distributions, errors, throughput and resource behavior with actual objectives. No universal target, soak duration or user count follows from the SaaS label.
- For fault/recovery exercises, inspect scenario, injected fault, stop conditions, protected data and recovery/invariant checks. Controlled execution requires separate authorization; this reviewer only assesses supplied evidence.

In k6, failed `check` calls do not by themselves fail the run; configured thresholds can make those results affect its exit status. A zero exit code therefore cannot establish a stated error-rate objective without inspecting the test configuration.

### TEST-12 — User interfaces, accessibility and locales

Verification of user-facing behavior must match the supported interaction and environment requirements.

- Inspect meaningful UI outcomes and states: loading, empty, error, disabled, focus and successful completion. Check keyboard interaction and semantics where relevant, not only screenshots or element existence.
- Check the actual browser/device/viewport support matrix, responsive content and visual baselines. Emulation and a screenshot prove only the exercised conditions; review baseline changes for unintended differences.
- Where supported, inspect locale/timezone, number/date/currency formats, plural cases, text expansion, right-to-left layouts and fallback behavior. A browser locale setting alone does not validate translations or the runner's timezone.
- Distinguish automated accessibility findings from manual/assistive-technology and inclusive-user evidence. A clean automated scan does not establish complete accessibility conformance.

Playwright supports browser locale/timezone emulation while the test runner can retain another timezone. Its accessibility guidance explicitly identifies limits of automation. Design and Localization supply their adopted expectations; Testing checks coverage and evidence without inventing a universal device or locale matrix.

### TEST-13 — Test selection and execution evidence

Reported results must identify what actually ran, against which artifact, and what remained uncovered.

- Inspect command, working directory, revision/build, relevant environment/configuration, collected tests, filters, shards and selected matrix entries. Check changed-path selection and dependency coverage, including zero-test outcomes.
- Compare raw results and logs with exit status and summaries. Preserve failures, timeouts, cancellations, collection/setup errors, skips, expected failures and uncompleted work according to their observed status.
- Inspect CI conditions, failure propagation, early termination, retries and allowed failures. A green aggregate can coexist with failed optional jobs or cancelled required coverage.
- Identify stale or mismatched results, missing artifacts and supplied versus reviewer-generated evidence. “Not supplied” or “unverified” does not mean “never ran”; an observed timeout must not be relabeled unrun.

Pytest assigns a distinct exit status to empty collection. GitHub Actions can allow a failed step/job without failing its aggregate, and matrix fail-fast can cancel other work. These mechanisms require outcome-level evidence, not a dashboard color.

### TEST-14 — Flakiness, retries and quarantine

Intermittent outcomes must remain visible, with a supported diagnosis and bounded mitigation rather than silent conversion to success.

- Compare attempts under their actual revision, environment, order, worker and input conditions. Investigate uncontrolled state, timing, external dependencies and overstrict assertions; do not label a deterministic failure flaky.
- Preserve the initial failure and later attempts, including changes between them. A pass after retry can support a narrower observation, not proof that the original failure was harmless or fixed.
- Inspect retry scope and fixture reset. Retrying one test, a worker or a whole job can exercise different starting states and leave earlier side effects.
- For quarantined or skipped checks, record the actual reason, responsible follow-up and affected verification gap under project rules. A justified known skip is not automatically a new product defect; it also cannot count as a pass.

Playwright distinguishes first-attempt passes, flaky tests that pass on retry, and persistent failures. Quarantine can reduce disruption while leaving a risk unresolved. No fixed retry or flakiness threshold is imposed.

### TEST-15 — Metrics, regressions and maintainability

Testing metrics and maintenance changes must preserve evidence about real behavior rather than merely improve reported numbers.

- Identify coverage type, scope, denominator, exclusions and revision. Inspect uncovered relevant decisions and meaningful assertions in covered paths; line or branch execution is not requirement satisfaction.
- Honor adopted coverage gates and exceptions. Without them, justify missing verification by risk and behavior instead of inventing a target or demanding tests for every trivial implementation detail.
- Where mutation evidence is supplied, inspect relevant survivors, equivalent mutants, timeouts, compile failures and excluded code. A mutation score is useful evidence about the chosen transformations, not proof of all correctness.
- Check that regression tests expose the original failure and preserve legitimate behavior. Inspect deleted/disabled tests, broadened tolerances and updated snapshots against an actual changed contract.
- Keep test names, fixtures and helpers understandable enough to diagnose failures. Avoid unnecessary coupling to incidental implementation details or generated tests with duplicated logic and no independent oracle.

For example, 100% branch coverage can coexist with a test that never checks the returned amount. A surviving equivalent mutant need not represent a missing behavioral test.

## Verification

For each selected control, connect the assigned criterion to the actual test path, oracle and relevant execution evidence. Explain a plausible faulty implementation the test would reject and a legitimate case it must permit. Use compact requirement-to-test maps, schedules or compatibility matrices when they clarify the gap; do not require a new project document for every review.

Inspect captured source and supplied results only. Do not run target tests, install dependencies, change test data, execute scanners, load/fault tools or production checks through this leaf role. The lead may arrange separately authorized verification. Proposed tests and hypothetical outcomes remain proposals.

A supported test finding identifies the undetected behavior, why the current check misses it, its consequence and a focused correction/verification. A test defect can be established from source without proving the application currently fails. Missing execution evidence limits runtime claims; it does not erase observed failures or establish missing implementation. Return all assigned criterion assessments, truthful inspected scope and limitations through the shared contract.

## Responsibilities and exceptions

Testing owns verification selection, oracle quality, fixture fidelity and execution-evidence assessment. Code owns functional implementation; Security threat and authorization analysis; Database persistence guarantees; Architecture system contracts; Performance workload interpretation; DevOps delivery and exercise execution; Design and Localization their experience requirements; Compliance established obligations. The lead routes precise questions, resolves overlaps and preserves missing expertise as a limit.

Project supplements, mapped scoped/whole-standard replacements and waivers use [Review scope and criteria](../intent_context.md#review-scope-and-criteria). Preserve actual authority, scope, remaining consequences and expiry. A valid waiver retains the contradicted criterion; a changed review threshold cannot rewrite observed results. No independent obligation disappears merely because a package default is replaced.

## Ownership, review, and related policy

The Engineering Review Team maintains this standard under the [Testing Policy (POL)](../policies/testing.md). Revisit affected controls when runner/framework behavior, supported environments, shared contracts or observed false positives/missed risks change. Keep `TEST-xx` identifiers stable through refinements and record material scope changes.

## Research reference

[Sources and control mappings](../research/testing.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
