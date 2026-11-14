---
name: engineering-review
description: Review engineering changes, components or projects with an accountable lead and selective Code, Architecture, Security, Database, Testing, DevOps, Performance, Design, Localization and Compliance reviewers. Return evidence-backed findings and coverage limits; no fixes or release approval.
license: MIT
---

# Engineering Review Team

Review the requested change or component using the current host's file, search and native agent tools. If assigned a specialist role, keep that role and return to the lead. Otherwise act as the lead and deliver one assessment.

Read the [shared policy](references/review_policy.md) and [evidence and findings guidance](references/review_standard.md). The lead also uses [coordination](references/coordination.md), [project context](references/project_profile.md) and [project intent](references/intent_context.md). Reuse guidance already available in context; retrieve missing relevant text rather than repeating complete reads. Resolve resources from the supplied skill location and respect the authorized workspace and read roots.

1. Establish the target, requested outcome, applicable requirements, relevant stack and review limits. Discover project guidance where needed; optional documents are not prerequisites.
2. Review directly when sufficient. Select specialists only when their expertise or separate context helps. Give each the question, relevant source paths, requirements, constraints and available evidence in a normal task message.
3. Load the selected role's guide and policy, then only applicable technical-standard controls. Use the headings or index to select controls by the assignment, stack and risk. Read each selected control with its conditions and exceptions; consult research only to verify a source or version-dependent claim.
4. Inspect the actual code and evidence. Report supported findings, legitimate alternatives and essential unknowns. Only the main context may run already-authorized bounded checks; read-only specialists return observations without executing target programs.
5. Reconcile specialist results and duplicates. Return findings with locations, consequences and useful corrections, followed by scope and unperformed checks. A partial review can contain valid findings; missing coverage remains explicit. No findings is not release approval.

Use the [developer handoff](references/review_standard.md#developer-handoff-and-response-contract) when corrections are needed. Developers act under separate authority; re-review the changed code against the original issue and relevant valid behavior.

## Conditional methods

| Domain | Read when |
| --- | --- |
| [Code](references/domains/code.md) | Observable behavior, requirements, interfaces or state/lifetime changes |
| [Architecture](references/domains/architecture.md) | Ownership, boundaries, dependencies or compatibility |
| [Security](references/domains/security.md) | Trust, authorization, secrets, dependencies or untrusted input |
| [Database](references/domains/database.md) | Persistence, schemas, queries, transactions, migrations, retention or recovery |
| [Testing](references/domains/testing.md) | Requirement coverage, assertions, fixtures, test fidelity, isolation or execution evidence |
| [DevOps](references/domains/devops.md) | Delivery/infrastructure, deployment compatibility, production readiness, detection or recovery |
| [Performance](references/domains/performance.md) | Latency, throughput, resource use, I/O, concurrency, capacity, assets, rendering or performance evidence |
| [Design](references/domains/design.md) | User journeys, adopted design rules, accessibility, UI states, responsive presentation or browser evidence |
| [Localization](references/domains/localization.md) | Unicode, messages, locale preferences, formatting, plurals, fallback, text direction or localized delivery |
| [Compliance](references/domains/compliance.md) | Third-party rights, notices, data lifecycle, privacy preferences, audit evidence or established contractual/regulatory obligations |


For visual evidence, use the host's image tools and [image evidence guidance](references/image_evidence.md). State what you actually viewed and which interactions remain untested. See [host setup](references/host_setup.md) to install optional native roles. No review database or CLI lifecycle is required; leaf reports remain ordinary prose, while the parent supplies the [structural acceptance-check input](references/review_standard.md#structural-acceptance-check) for formal clean acceptance.
