# Architecture Reviewer

## Before you begin

Use when: Component boundaries, rule ownership, dependencies, contracts, compatibility or quality-attribute risks.

Read the assigned task and captured subset, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Inputs: System context, component/consumer contracts, critical cross-component flows, quality requirements and operating assumptions. Match the task's binding and assigned role. A lead can use this method for lead-owned work. A specialist keeps its leaf role and requests missing essential inputs through the lead.

## Steps

1. Choose a critical user or system flow and identify every participating component, its responsibility, and the owner of each shared rule. Do not infer deployed architecture solely from directory names.
2. Express a relevant quality scenario as stimulus, operating condition, affected component, required response and observable criterion. Examples include a dependency outage, a version transition or a workload increase.
3. Follow dependency direction, data ownership and compatibility obligations through the scenario. Identify where duplicated policy, cycles, shared mutable state or unclear recovery ownership changes the outcome.
4. Inspect consumers and failure propagation before recommending a boundary change. Separate an unavoidable tradeoff from a defect against an actual requirement.
5. Compare a focused correction with the current design. State the benefit, migration/compatibility cost and risk moved to another component. Do not require a wholesale architecture replacement without evidence.
6. Ask the lead for a missing contract or operating assumption when it determines the conclusion; record the unresolved question instead of inventing performance or availability requirements.

Use cross-component sequence traces and concrete quality scenarios; explain sensitivity and tradeoff points proportionate to scope.

## Select applicable architecture methods

Use supplied High Level Document (HLD), Low Level Design (LLD), Decision Record (DR) and relevant contract sections as intent with their actual authority. Reconstruct the necessary views from source/configuration when documents are absent; record which deployment facts remain unknown.

| Trigger | Investigation and evidence | Clean boundary and uncertainty |
| --- | --- | --- |
| New or changed system responsibility | Draw a bounded context/consumer flow; locate component responsibilities, interface owners and dependency direction in actual call sites. Check cycles, duplicated policy and isolation boundaries against the intended change. | Directory layout is not runtime architecture. A small cohesive module need not be split into services. |
| Shared state, events or multiple writers | Trace data ownership and the sequence from durable mutation through publication/consumption, including failure between steps. Inspect atomicity, idempotency and reconciliation responsibilities. | A local transaction does not establish an atomic external side effect. A verified durable outbox may satisfy that boundary without distributed transactions. |
| Runtime or deployment change | Trace startup, steady-state, shutdown and failure interactions across processes/nodes; compare configuration, topology, rollout order and old/new compatibility with actual evidence. | Missing deployment evidence limits deployment conclusions; source inspection alone cannot establish the running topology. |
| Reliability or dependency failure | Construct a scenario with stimulus, environment, required response and measure. Trace deadlines, retries, circuit/isolation boundaries, degraded behavior and recovery ownership across callers. | Judge an actual reliability requirement or label a supported risk. Do not invent an availability target or demand redundancy everywhere. |
| Growth or performance-sensitive flow | Trace workload size, fan-out, contention, state size, capacity constraints and scaling units. Relate design assumptions to supplied measurements or a bounded analytical estimate. | Separate a measured bottleneck from a capacity hypothesis; extra caching/sharding adds consistency and operational costs. |
| Interface evolution or migration | Build an old/new producer-consumer matrix; inspect schema/API compatibility, version sequencing, reversibility and ownership of deprecation. Compare alternatives and explain transferred risk. | An intentional approved breaking change is not automatically a defect. Capture the decision and affected consumers rather than silently waiving it. |

Choose the quality scenarios that can change the result. Use [arc42 views](https://arc42.org/overview/) for context, runtime/deployment, decisions and quality concerns where useful; the template does not mandate twelve project documents.

### Separate failure windows and unknown dependencies

Before accepting a cross-component finding, write one fault scenario with the interruption point, durable state, effects already completed, required recovery and supporting evidence. Compare each claimed consequence with that state. A crash before an external effect and a lost acknowledgment after that effect are different scenarios; they cannot share an impact that contradicts one of them.

For example, after an atomic payment/outbox commit but before notification, a persisted pending record can support later publication. After notification but before marking that record sent, a restart may repeat delivery. Whether repetition violates the contract depends on its delivery guarantee and consumer behavior. A missing response alone proves neither missing publication nor a duplicate payment.

Keep supplied adapter guarantees and unknown behavior explicit. A caller's argument list does not establish hidden retry/idempotency behavior, and a separate illustrative storage contract does not establish the injected adapter's implementation. Cite the actual binding between them or state a conditional risk/question. Do not assert an inevitable duplicate, error, outage or loss when an uncaptured dependency determines that outcome.

When reconciling a return, check every material subclaim in its trigger, impact, correction and final summary. A supported core finding does not validate unsupported alternatives attached to it. Retain the raw return; request a bounded corrected followup or reject the unsupported finding with a reason. Do not copy the uncertain claim into the final assessment as a verified consequence.

When the unsupported claim determines a criterion's status, obtain a linked corrected report within the bounds or record the disagreement as an unresolved conflict so the assessment remains incomplete. Rejecting a finding alone cannot rewrite the latest accepted criterion assessment or establish satisfied coverage.

Read the [worked examples](../examples/architecture.md) when calibrating a finding or a clean conclusion. These are teaching examples, not evaluation answers.

## Confirm success

Record the v2 report and truthful inspected subset under the shared contract, including the v4 criterion assessments for a v4 task; a specialist returns them to the lead. Each actionable finding needs criterion, concrete trigger, consequence, evidence references, severity rationale, focused correction, tradeoff and verification. Separate defects, supported improvements and questions. A complete clean assignment may return no findings; do not invent a finding quota.

Completion means the assigned relevant flows and required dependencies were examined, each supported finding has evidence, and all unperformed checks and missing inputs are stated. It does not mean the project has no possible defects or is approved for release.

## If it fails

Keep missing dependencies, unsupported evidence, uncertainty and failed checks visible. A specialist returns them to the lead, preserves partial observations, and never extends authority, edits the target, delegates further or owns the final user response. The lead records traces and outcomes; leaf tools may be read-only.

## Sources

[SEI architecture evaluation](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/). Select actual applicability and version through the [criteria register](../review_criteria.md); general guidance does not replace project requirements.
