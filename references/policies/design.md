# Design review policy

This additive policy governs Design assignments under the shared [Review Policy (POL)](../review_policy.md).

## Purpose and scope

Assess required user tasks, accessible operation, coherent presentation and supported environments in relevant user-facing work. The [Design Technical Standard (STD)](../standards/design.md) owns detailed controls; the [reviewer procedure](../domains/design.md) owns investigation. Shared guidance owns authority, document discovery/routing, evidence, findings and developer responses. This policy authorizes no target operation, changes or release decisions.

## Definitions

A **design system** is an adopted set of reusable interface rules and components. A **design token** names a design value or meaning. An **interaction state** affects what a user can perceive or do. A **support commitment** identifies environments, input methods or populations the product undertakes to support. A **rendered observation** records appearance or behavior under identified conditions; a static image does not demonstrate interaction. Use shared definitions for project rules, defaults, inferences, replacements and waivers.

## Principles

Judge the interface against user tasks and applicable obligations, not aesthetic preference. Preserve meaning, operability and recovery when applying visual rules. Scale investigation to risk and scope without treating small size as an accessibility exemption. Distinguish actual evidence, supported analysis and unknowns.

## Policy obligations

- **DES-POL-01 — Establish effective requirements.** Use captured project criteria and applicable package defaults through shared [Review scope and criteria](../intent_context.md#review-scope-and-criteria). Establish the affected journey, states, component/design versions and support conditions. Missing optional guidance is neither a defect nor permission to invent a design requirement.
- **DES-POL-02 — Preserve accessible task completion.** Assess relevant perception, operation, understanding and interface semantics from the first applicable release. Select controls by the actual UI and users. Technical accessibility checks do not establish legal applicability or full-product conformance.
- **DES-POL-03 — Apply design rules proportionately.** Respect adopted tokens/components and scoped alternatives. Literal or dynamic values, native platform differences and an absent corporate library are not automatic defects. A visual concern needs an applicable rule or supported user consequence.
- **DES-POL-04 — Assess states and recovery.** Review the states the interface can enter, including failure and partial outcomes. Feedback and available actions must reflect the supported result and preserve recoverability. Do not require every state on every static element or a confirmation dialog for every action.
- **DES-POL-05 — Assess supported environments.** Preserve access, meaning and task completion across applicable browser, viewport, input and content variation. Use actual commitments and compatible defaults; do not invent all-engine support or require identical pixels without an adopted requirement.
- **DES-POL-06 — Keep evidence and conclusions bounded.** Distinguish source inspection, image viewing, interaction, device and assistive-technology tests. Link each concern to a criterion, trigger, evidence, consequence and useful verification. A screenshot or clean scan cannot establish untested behavior. Preserve incomplete coverage and legitimate safe cases; no finding quota applies.

## Responsibilities and compliance

Design owns its assigned investigation and evidence interpretation. The lead owns capture, criteria, routing, authority, acceptance and synthesis. Developers own corrections and separately authorized verification. The package maintainer owns defaults and their validation; these role names do not appoint project officers.

Use the shared report and criterion-assessment contract. Review only assigned sources and supplied evidence, including bound images through permitted read-only tools. Do not execute target workflows, collect live data, edit or delegate. Route dependencies through the lead and retain independently supported findings.

## Exceptions

Use the shared customization procedure for `design`, including actual authority, scope, mapping, effective period/end conditions and consequences. A valid replacement changes the mapped rule while preserving unrelated obligations. A waiver retains the contradiction and residual risk. Pending, expired or out-of-scope decisions do not apply. An accessibility exception cannot be described as conformance to the unmet criterion.

Add no domain-specific approval form or precedence scheme. Preserve valid user authorization; host restrictions and evidence honesty remain binding. Unresolved conflicts go to the lead.

## Ownership, review, and related standards

Revisit affected controls when platform behavior, applicable standards, shared contracts or observed missed defects/false positives change. Do not invent a review cadence. Keep the [Design Technical Standard (STD)](../standards/design.md), [procedure](../domains/design.md), shared [Review Technical Standard (STD)](../review_standard.md) and [project-intent guidance](../intent_context.md) consistent. Document checks do not prove reviewer effectiveness, native activation or product conformance.
