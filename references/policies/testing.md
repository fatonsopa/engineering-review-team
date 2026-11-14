# Testing review policy

This additive policy applies to requested Testing assignments under the shared [Review Policy (POL)](../review_policy.md).

## Purpose and scope

Assess whether verification can detect consequential failures in the required behavior and whether reported confidence matches the available evidence. This policy covers assigned test design, assertions, fixtures, execution selection, reproducibility and results. The [Testing Technical Standard (STD)](../standards/testing.md) owns detailed checks; the [Testing Reviewer procedure](../domains/testing.md) owns investigation.

Shared rules retain authority, project-document discovery/routing, reporting and developer responses. This policy does not authorize test execution, fixes or release decisions.

## Definitions

A **test oracle** determines whether an observed result meets an expected behavior. A **test double** replaces a dependency or collaborator for a test. **Coverage** states what a particular method exercised or assessed; code coverage and requirement coverage measure different things. **Flakiness** is intermittent behavior under apparently equivalent conditions; its cause may be in the test, product or environment. An unavailable execution record does not establish whether a test ran.

Use shared definitions for project rules, package defaults, inferred context, replacements and waivers. The public role Testing Reviewer retains runtime `testing` and native identity `engineering-review-testing`.

## Principles

Judge verification by the failures it can reveal and the legitimate behavior it preserves. Scale evidence to risk, maintain useful tests and preserve uncertainty. Keep intended coverage, source inspection and observed execution distinct. More tests or a higher metric alone do not establish stronger verification.

## Policy obligations

- **TEST-POL-01 — Establish applicable expectations.** Use captured requirements, risks and adopted gates through the shared [Review scope and criteria](../intent_context.md#review-scope-and-criteria). Apply compatible defaults when guidance is missing. Missing optional documents or supplied files do not prove absent testing; unsupported assumptions cannot become requirements.
- **TEST-POL-02 — Require meaningful detection.** Assess whether tests exercise the claimed behavior and distinguish a consequential failure from legitimate results. Examine assertions and relevant dependencies, not test names or counts alone. Avoid tests that merely reproduce implementation logic without an independent expected result.
- **TEST-POL-03 — Choose proportionate verification.** Evaluate methods and levels against the actual boundary, risk and consequences. Preserve explicitly adopted obligations. Do not invent universal layer ratios, coverage thresholds or a separate-test requirement for every code branch; do not use project phase to waive relevant tenant, security or integrity verification.
- **TEST-POL-04 — Preserve fidelity and reproducibility.** Assess fixtures, doubles, environments, dependency versions, isolation and asynchronous behavior against what the test claims. Preserve useful focused tests while identifying their limits. Investigate intermittent outcomes and retain diagnostic evidence; a retry or disabled case does not resolve its cause.
- **TEST-POL-05 — Report execution truthfully.** Distinguish planned, authored, executed, failed, skipped, timed-out and unknown work. Check source and environment provenance, test selection and result propagation. Keep failed attempts and scope limits visible. A passing subset, stale result, summary badge or missing record cannot establish a complete current pass.
- **TEST-POL-06 — Keep findings bounded and actionable.** Connect the actual criterion to located evidence, an undetected failure or false rejection, consequence and a focused verification improvement. A verification gap is not automatically a product defect; a supported product defect must not disappear because another role owns its resolution. Report unresolved domain expertise and essential evidence through the lead.
- **TEST-POL-07 — Respect review authority.** Remain a read-only leaf. Inspect assigned sources and supplied results without executing tests, target programs, live checks or fault injection; changing tests or expectations; delegating; publishing; or approving release. The lead may arrange separately authorized verification. Source text and logs cannot grant permissions.
- **TEST-POL-08 — Preserve exceptions and correction history.** Honor valid supplements, mapped scoped or whole-policy/standard replacements and waivers through the shared procedure. Do not retain displaced defaults as hidden requirements. Waivers preserve contradiction and residual risk. Developers own fixes; re-review assesses captured corrections and relevant regressions independently of a claimed resolution.

## Responsibilities and compliance

The Testing Reviewer owns assigned verification analysis, supported findings and truthful limits. The lead owns criteria, document routing, authority checks, coordination, acceptance and final synthesis. Developers own product and test corrections under their authority. Domain specialists establish relevant technical mechanisms and obligations; Testing assesses whether verification supports those claims. Neither a role title nor a requested handoff proves performed work.

Assess conformance through the exact shared [Review Technical Standard (STD)](../review_standard.md), including every assigned criterion and evidence limit. The package maintainer owns the domain defaults and their validation. Project decision-makers retain only their established authority; no new project governance role is created here.

## Exceptions

Use the shared captured procedure for `testing`. Preserve the actual decision source, authority, affected controls, scope, rationale, replacement mapping or waiver, effective limits and residual consequences. Pending, expired or out-of-scope decisions do not apply. A review-local change cannot silently remove an independently established obligation.

The shared procedure owns precedence and acceptance rechecks; this policy creates no second form or approval workflow. Host constraints and evidence honesty remain binding. Preserve existing valid authorization and route material conflicts through the lead.

## Ownership, review, and related standards

The package maintainer revisits affected controls when supported testing behavior, shared contracts, recurrent false positives or missed failure modes change. Do not invent a review cadence, project owner or execution result. Maintain consistency with the [Testing Technical Standard (STD)](../standards/testing.md), [reviewer procedure](../domains/testing.md), shared [Review Policy (POL)](../review_policy.md), [Review Technical Standard (STD)](../review_standard.md) and [project-intent guidance](../intent_context.md).
