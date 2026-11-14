# Project context

Establish only the context needed for the review, using the request and available project material. Keep it in the assignment or review notes; no separate profile file is required.

- What is being reviewed: change, component or broader project; important entry points, callers and exclusions.
- Expected behavior and authority: user requirements, accepted decisions, applicable policies, overrides and unresolved conflicts.
- Technology: actual languages, frameworks, runtime/library versions and deployment environment where they affect behavior.
- Consequences: users, trust boundaries, sensitive or valuable data, critical flows, workload and recovery needs.
- Available evidence: source, tests, observations, optional documents and any access or execution limits.

Scale the method to the project. Size alone does not determine risk; a small system may handle consequential data. Do not require documents, infrastructure or test layers unrelated to the task. Explain essential unknowns and continue supported work.

## Phase and SaaS context

Use phase as context for selecting relevant controls, not as a mandatory architecture roadmap:

- Foundation or experiment: establish actual exposure and data; retain applicable correctness, security, dependency and licensing checks.
- Production launch: real users or valuable data trigger relevant isolation, persistence, deployment, observability, recovery, accessibility and privacy checks, with service expectations proportional to risk.
- Growth: increasing workload, tenants or change frequency may require capacity evidence, resource fairness, backpressure, compatible changes and operational automation.
- Advanced scale or criticality: assess failure domains, replication, failover and regional commitments when consequences or architecture justify them; do not mandate microservices, sharding or multiple regions.

Phase, exposure, sensitivity and criticality are independent. Low traffic or a prototype label does not waive applicable protections, and missing facts do not justify assigning a lower phase. Use actual commitments rather than invented numeric targets.

For SaaS, distinguish the delivery/business model from tenant architecture and workload scale. Establish relevant tenant onboarding, switching and deletion; isolation and propagated tenant context; roles, entitlements and billing; background jobs; tenant-aware observability; and resource fairness. Route applicable questions to existing standards: Architecture for boundaries, Code for context and job behavior, Security for authorization, Database for storage and lifecycle, DevOps for delivery and recovery, Performance for workload and fairness, Design/Localization for user journeys and recipient context, Testing for verification, and Compliance for established obligations. Select only relevant controls; SaaS alone does not require every role or a particular tenancy model. Discover governing sections through [project intent](intent_context.md), keeping actual facts and unknowns in the assignment.
