# Testing review research references

Consult this record when verifying a source, checking a version-dependent claim or maintaining the reviewer. Do not load it automatically for routine reviews. The technical standard owns the controls; these references do not independently create project obligations.

## Domains references

[Google's review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html) supports selecting appropriate test levels and checking whether assertions detect broken behavior. [pytest's flaky-test guidance](https://docs.pytest.org/en/stable/explanation/flaky.html) supports examining state, isolation and causes rather than trusting a retry. These method sources do not establish the target's stack or requirements. Control-specific sources and version qualifications are recorded in the [source table](#standards-references) below.

## Standards references

These primary pages were opened on **2026-11-04**. Versioned sources are reference baselines, not project version requirements. Living documentation and displayed versions must be checked against the actual installation. The controls combine source-supported mechanisms with package-designed review methods; they do not claim complete certification against any testing standard.

| ID | Primary source and reference baseline | Controls |
| --- | --- | --- |
| S1 | Google Engineering Practices, living guide: [Tests in code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html#tests) | TEST-01–02 |
| S2 | Software Engineering at Google, 2020: [Testing overview](https://abseil.io/resources/swe-book/html/ch11.html) | TEST-01, TEST-04 |
| S3 | Software Engineering at Google, 2020: [Test doubles](https://abseil.io/resources/swe-book/html/ch13.html) | TEST-02, TEST-05 |
| S4 | Hypothesis living docs, displayed 6.170.14: [Stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html) | TEST-03 |
| S5 | Pact living docs: [When to use Pact and its limits](https://docs.pact.io/getting_started/what_is_pact_good_for) | TEST-04 |
| S6 | pytest stable/living docs: [Fixtures and safe teardown](https://docs.pytest.org/en/stable/how-to/fixtures.html#safe-teardowns) | TEST-06 |
| S7 | pytest stable/living docs: [Flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html) | TEST-06–07, TEST-14 |
| S8 | Playwright living docs: [Best practices](https://playwright.dev/docs/best-practices) | TEST-12 |
| S9 | Jest living docs, displayed 30.5: [Asynchronous code](https://jestjs.io/docs/asynchronous) | TEST-07 |
| S10 | Go living docs: [Data race detector](https://go.dev/doc/articles/race_detector) | TEST-08 |
| S11 | OWASP WSTG v4.2: [Testing framework](https://wstg.owasp.org/v4.2/3-The_OWASP_Testing_Framework/0-The_Web_Security_Testing_Framework/) | TEST-09 |
| S12 | Django 5.2: [Testing tools and transaction test cases](https://docs.djangoproject.com/en/5.2/topics/testing/tools/#transactiontestcase) | TEST-05, TEST-10 |
| S13 | Django 5.2: [Migrations and historical models](https://docs.djangoproject.com/en/5.2/topics/migrations/#historical-models) | TEST-10 |
| S14 | Google SRE book, 2016: [Testing for reliability](https://sre.google/sre-book/testing-reliability/) | TEST-11 |
| S15 | Grafana k6 living docs, displayed v2.3.x: [Thresholds and checks](https://grafana.com/docs/k6/latest/using-k6/thresholds/) | TEST-11 |
| S16 | Playwright living docs: [Accessibility testing](https://playwright.dev/docs/accessibility-testing) | TEST-12 |
| S17 | Playwright living docs: [Emulation, locale and timezone](https://playwright.dev/docs/emulation) | TEST-12 |
| S18 | pytest stable/living docs: [Exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) | TEST-13 |
| S19 | GitHub Actions living docs: [Workflow syntax, allowed failures and matrix cancellation](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | TEST-13 |
| S20 | Playwright living docs: [Retries and result categories](https://playwright.dev/docs/test-retries) | TEST-14 |
| S21 | Google Testing Blog, 2020-08-07: [Code coverage best practices](https://testing.googleblog.com/2020/08/code-coverage-best-practices.html) | TEST-15 |
| S22 | Stryker living docs: [Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) | TEST-15 |
| S23 | Stryker living docs: [Equivalent mutants](https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/) | TEST-15 |

## Control-to-source mapping

The entries below preserve the source associations and qualifications used when authoring the controls. They are research evidence, not additional review instructions.

- **TEST-01 — Scope, risks and criteria:** For example, a migration deliverable omitted from the implementation remains uncovered even if all supplied API tests pass. Conversely, a focused test can cover several decision outcomes without one test function per branch. S1–S2 support useful, proportionate testing; the criterion map is the package's review method.
- **TEST-02 — Meaningful oracles and assertions:** A serializer test that mocks the serializer and checks only a call cannot establish escaping. Mocking the network while running the real serializer and checking its output can be appropriate. A model-generated or human-written test needs the same review. S1 and S3 support these distinctions.
- **TEST-03 — Inputs, decisions and state transitions:** For example, testing only “below limit” and “well above limit” can miss an off-by-one error at the actual boundary. Stateful generation can explore operation sequences, but a simple example table may be sufficient. S4 supports the conditional use of generated stateful tests; boundary selection is a review judgment.
- **TEST-04 — Test levels and integration contracts:** Pact checks selected request/response interactions; that does not prove the provider's unasserted side effects, performance or entire business workflow. A real integration test remains appropriate where it observes the required boundary directly. S2 and S5.
- **TEST-05 — Test doubles and environment fidelity:** For example, Django's transaction-wrapped `TestCase` can conceal whether code establishes a required transaction; its documented `TransactionTestCase` supports observing commit/rollback behavior. The actual backend still matters. S3 and S12 support fidelity checks, not a mandate to use those frameworks.
- **TEST-06 — Fixtures, isolation and cleanup:** In pytest, code after a fixture's `yield` does not run if that fixture raises before yielding. A compact setup that allocates two resources and then fails can therefore leak the first unless cleanup was arranged safely. Inspect the actual lifecycle rather than counting teardown methods. S6; cross-test state concerns are also described in S7.
- **TEST-07 — Time, randomness and asynchronous completion:** For example, failing to await or return an asynchronous assertion’s promise can let a Jest test finish before that assertion settles. Either correctly awaiting or returning the promise avoids that specific gap without requiring arbitrary sleeps. S9 supports asynchronous completion; S7 supports controlling environmental causes of intermittent outcomes.
- **TEST-08 — Concurrency, retries and partial effects:** A retry test that fails before every write misses duplicate effects after a lost commit acknowledgment. A controlled post-commit response loss plus a stored-state assertion can expose that risk. S10 documents the runtime coverage limits of Go's race detector; the schedule and uncertain-outcome method is package design.
- **TEST-09 — Security, tenant and privacy verification:** For example, a tenant-isolation test that uses an administrator fixture with bypass privileges may never exercise the ordinary-user boundary. The same privileged fixture can be correct for an explicitly administrative operation. Security defines the threat/control judgment; Testing assesses whether the checks demonstrate it. S11 supports security verification across the lifecycle; this does not claim full WSTG coverage.
- **TEST-10 — Data changes and version compatibility:** For example, Django migrations depend on historical models and retained references; testing only the current model state misses a broken clean installation. Database establishes engine guarantees and compatibility risks; Testing checks whether fixtures and assertions expose them. S12–S13 support the framework examples; the transition matrix is package design.
- **TEST-11 — Resilience, performance and resources:** In k6, failed `check` calls do not by themselves fail the run; configured thresholds can make those results affect its exit status. A zero exit code therefore cannot establish a stated error-rate objective without inspecting the test configuration. S14 supports requirement-shaped resilience testing; S15 supports this runner distinction.
- **TEST-12 — User interfaces, accessibility and locales:** Playwright supports browser locale/timezone emulation while the test runner can retain another timezone. Its accessibility guidance explicitly identifies limits of automation. Design and Localization supply their adopted expectations; Testing checks coverage and evidence without inventing a universal device or locale matrix. S8, S16–S17.
- **TEST-13 — Test selection and execution evidence:** Pytest assigns a distinct exit status to empty collection. GitHub Actions can allow a failed step/job without failing its aggregate, and matrix fail-fast can cancel other work. These mechanisms require outcome-level evidence, not a dashboard color. S18–S19; the provenance comparison is package method.
- **TEST-14 — Flakiness, retries and quarantine:** Playwright distinguishes first-attempt passes, flaky tests that pass on retry, and persistent failures. Quarantine can reduce disruption while leaving a risk unresolved. S7 and S20 support these distinctions; no fixed retry or flakiness threshold is imposed.
- **TEST-15 — Metrics, regressions and maintainability:** For example, 100% branch coverage can coexist with a test that never checks the returned amount. A surviving equivalent mutant need not represent a missing behavioral test. S21–S23 support metric limits; test maintenance remains ordinary engineering judgment under the applicable contract.
