# Architecture review technical standard

Package default under the Architecture Policy (POL).

## Purpose and scope

The Architecture Reviewer examines component responsibilities, dependency and integration boundaries, shared rules, runtime interactions, evolution and quality tradeoffs. Apply this Technical Standard (STD) to the assigned flows and applicable controls. It applies to a module, modular monolith or distributed system without preferring one deployment style.

These are package-designed review controls. External publications support the mechanisms and methods identified in the research record; they do not establish this project's requirements or adopt a vendor's architecture. The project supplies actual behavior, supported consumers, workload, isolation, availability and lifecycle commitments. All examples are illustrative. A safe counterpart satisfies its stated assumptions, not every possible requirement.

Use the [Architecture Policy (POL)](../policies/architecture.md) for the effective review criteria and exceptions, the shared [Policy (POL)](../review_policy.md) for authority, the shared [Technical Standard (STD)](../review_standard.md) for evidence and findings, and [project intent and implementation alignment](../intent_context.md) for assigned source sections. These controls do not change team routing, report fields, review permissions or acceptance statuses.

## Definitions

- A **component** is an identified unit with responsibilities and interfaces. Its source, runtime and deployment boundaries can differ.
- A **boundary** separates responsibilities, permitted dependencies, state ownership, trust or failure propagation. A directory or process name alone does not prove that boundary is enforced.
- A **rule owner** is the component or established authority responsible for a business decision. Several physical implementations can be valid if their consistency and change contract is explicit.
- An **integration contract** states the semantics producers and consumers rely on, including success, failure, timing, state, identity, compatibility and recovery when relevant.
- A **quality scenario** identifies a stimulus and its source, operating conditions, affected part of the system, required response and observable response measure. The measure can be a correctness outcome rather than a numeric service target.
- A **sensitivity point** is a decision or parameter that materially affects a quality outcome. A **tradeoff point** affects more than one quality concern, such as reducing waiting while allowing stale reads.
- A **failure window** is a specific interruption point together with durable state, completed effects and possible next actions. An unknown response is not evidence that the effect did not happen.
- A **failure domain** is a set of resources exposed to a common failure. Different instances can share a host, database, region, credential, control service or deployment fault.
- An **authoritative state** is the state designated to decide an invariant. A **projection** or cache derives state for another use and has an explicit freshness and repair contract.
- A **tenant** is the project's isolation and ownership unit. It need not equal one user, customer, deployment, database or subscription.
- A **project parameter** is a real contract, limit, supported version or operating condition needed to assess a control. Unknown values remain unknown.

## Principles

Assess structure through a concrete flow and its consequences. Prefer the simplest arrangement that satisfies actual requirements, including future capabilities that have an established commitment. Distinguish accepted design from observed implementation and inferred conventions.

Inspect both sides of a boundary. Follow the rules, state, resources and failure paths that cross it. A local guarantee does not establish a complete business outcome, and a component name does not establish a provider guarantee.

Evaluate focused alternatives against the same scenario. Include migration work, operational cost and risk transferred to other components. A supported improvement can be useful without being a defect; a pattern preference alone is neither.

Match evidence to the claim. Source inspection supports a bounded structural conclusion. Supplied runtime measurements support their recorded version, environment and workload. A diagram, configuration setting or successful schema check does not establish deployed behavior, reliability attainment or release readiness.

## Applicability and phases

Select controls by the affected behavior and risk. Scale investigation depth with phase and independent risk together.

| Phase | Architecture review depth |
| --- | --- |
| Foundation | Identify the changed flow, its responsibilities, contracts and actual constraints. Check relevant durable effects and boundaries. A small application can have one deployable, one database and manual tenant administration. |
| Production launch | Inspect supported consumers, real tenant and entitlement boundaries, startup/shutdown, external failures, partial effects and relevant lifecycle recovery. Confirm actual commitments and owners. |
| Growth | Extend scenarios to representative workload skew, shared capacity, repeated delivery, projection lag, fleet or tenant variation and mixed versions. Use evidence to distinguish a current bottleneck from a forecast. |
| Advanced scale or criticality | Analyze relevant partitions, correlated failures, failover, replay, migration and consistency tradeoffs where those mechanisms exist or an actual requirement requires them. Do not add distributed mechanisms merely because this phase applies. |

Payments, shared tenants, sensitive or durable data, irreversible actions, external dependencies and contractual reliability activate their relevant controls at any phase. SaaS delivery does not imply pooled storage, automated provisioning or multi-region operation. Missing optional architecture documents do not constitute a defect; reconstruct bounded views from captured code and configuration and state remaining deployment uncertainty.

## Rules

For each applicable control, perform the inspection or report the unperformed work and its effect on coverage. Explain the applicable requirement and relevant `ARCH-xx` control when useful. A defect requires an applicable contract, a reachable trigger and a supported consequence. Record supported risks or improvements and unresolved questions separately.

### ARCH-01 — Quality scenarios and architectural intent

- Rule and rationale: Evaluate a material architectural choice against the affected behavior and quality scenario. This prevents a structural preference from becoming a product requirement or an unsupported guarantee.
- Trigger; phase/risk: Changed responsibilities, dependencies, topology, capacity or quality commitments; all phases. High-impact effects require the relevant failure scenario even in a prototype.
- Parameters: Accepted behavior and constraints; affected users/consumers; stimulus, operating conditions, required response and measure; actual source authority. Record unknown objectives rather than selecting a numeric target.
- Inspection: Trace one critical flow across participating components. Identify its important quality concerns and the decisions that affect them. Compare normal, changed and relevant failed conditions; identify sensitivity and tradeoff points. Use supplied design sections or reconstruct the necessary view. Ask the lead to resolve material intent conflicts while continuing independent work.
- Expected evidence: Located flow and requirement, scenario with observable outcome, component responsibilities, assumptions and evidence supporting each conclusion. A satisfied assessment explains how the inspected design meets the recorded scenario; analysis alone does not prove measured attainment.
- Defective example: The supplied checkout contract requires order acceptance during a notification-provider outage, but accepting an order always waits for that provider and returns failure when it is unavailable.
- Safe counterpart: The chosen design preserves accepted orders and records notification progress under the agreed delivery contract; the reviewer identifies its remaining delivery delay and recovery costs.
- Limits: No prescribed uptime, latency, formal ATAM workshop or architecture-document set. A missing objective limits that comparison; it does not prove an outage.
- Owner/contributors: Architecture owns scenario analysis; the lead resolves intent, affected specialists supply evidence.

### ARCH-02 — Modular boundaries and rule ownership

- Rule and rationale: Components must preserve their established responsibility boundaries and produce consistent decisions for shared rules where the contract requires consistency. Uncoordinated rule ownership causes divergent outcomes and costly changes.
- Trigger; phase/risk: A rule moves, is copied, gains a new caller, or crosses an established layer, module, service or bounded context; all phases.
- Parameters: Rule semantics, intended owners, permitted dependencies, consumer differences and accepted consistency requirements.
- Inspection: Follow the same business decision from each affected entry point to its implementation and authoritative inputs. Locate bypasses, duplicated policy and writes across ownership boundaries. Determine whether similar code implements the same rule or different contextual rules. Check the actual exports, calls and write paths rather than directory names.
- Expected evidence: Responsibility/rule map, affected consumers, located decision paths and a concrete change or input exposing divergence. A compliant result preserves the rule across the inspected consumers, through one owner or an explicitly coordinated alternative.
- Defective example: Web checkout uses the current shared surcharge rule while batch checkout retains an older copied rate, despite an agreed identical pricing contract.
- Safe counterpart: Both paths invoke the same domain operation inside a modular monolith. Alternatively, distinct customer contexts intentionally use different approved pricing rules with separate ownership.
- Limits: Shared helpers, replicated rules and shared databases are not intrinsically defects. Require the actual consistency or encapsulation obligation and consequence; do not demand service extraction.
- Owner/contributors: Architecture owns system responsibility; Code checks local implementation and Database supplies write-boundary evidence.

### ARCH-03 — Dependency direction and coupling

- Rule and rationale: Dependencies must respect applicable boundary contracts and preserve the required ability to change, initialize, isolate or exercise affected components. Judge cycles by their consequences and adopted rules, not their mere shape.
- Trigger; phase/risk: Added imports, runtime calls, shared mutable state, shared libraries, initialization dependencies or coordinated deployments; all phases, with larger consumer/deployment matrices at growth.
- Parameters: Allowed dependency direction; relevant build/runtime graph; component change and initialization requirements; ownership and mutability of shared state.
- Inspection: Distinguish compile-time, runtime, data and deployment dependencies. Follow an edge through actual call sites and configuration; trace any cycle to a concrete change, startup, lock or failure scenario. Check whether testing one boundary requires unrelated live dependencies and whether that contradicts an actual requirement. Examine hidden coupling through a shared schema, singleton, SDK or configuration value.
- Expected evidence: Bounded graph or table with located edges and edge types, reachable consequence, applicable constraint and focused alternative. A compliant result demonstrates the required change/isolation scenario without an unacknowledged dependency.
- Defective example: Components A and B each refuse startup until the other's readiness endpoint succeeds; the captured startup contract permits both to start together, producing a reachable startup deadlock.
- Safe counterpart: A and B exchange requests in both directions after independent startup, with bounded failure handling and no prohibited source dependency. A bidirectional interaction alone is not reported as a cycle defect.
- Limits: Test doubles are not mandatory, and a mock-friendly interface does not prove production decoupling. Uncaptured runtime bindings remain unknown.
- Owner/contributors: Architecture owns dependency analysis; Code, Testing and DevOps contribute local, isolation and startup evidence.

### ARCH-04 — Pattern applicability and abstraction cost

- Rule and rationale: An adopted structural pattern must be followed within its actual scope or assessed against an authorized alternative. New abstractions and pattern changes must be evaluated for the requirement they serve and the complexity they introduce.
- Trigger; phase/risk: New layer, interface, framework, service extraction, generic extension mechanism or pattern deviation; all phases. Future scalability alone does not establish applicability.
- Parameters: Adopted pattern and authority, specific variation/change scenario, present and committed consumers, operating constraints and supported alternatives.
- Inspection: Identify the problem the structure solves. Trace responsibilities and dependencies through a representative extension or change; compare a smaller correction with the proposed design under the same scenario. Check whether Factory, Repository, Clean Architecture, CQRS or another named pattern is actually adopted and what it means in this codebase. Record additional consistency, deployment, debugging, ownership and migration costs where relevant.
- Expected evidence: Applicable convention/decision, concrete consumer or change scenario, structural behavior, alternatives and consequences. A recommendation identifies a real benefit and cost; a defect identifies a violated obligation or demonstrated hazard.
- Defective example: An adopted domain boundary excludes persistence-specific types, but a new public domain operation exposes the concrete storage session and forces every caller to manage its transaction semantics.
- Safe counterpart: A small CRUD module uses its framework's ordinary persistence API within the accepted boundary and has no established need for a new repository layer or separate read store.
- Limits: One implementation does not make an interface useless; a stable external boundary or meaningful test seam can justify it. CQRS need not include messaging, event sourcing or two databases. No fixed service, layer or abstraction count applies.
- Owner/contributors: Architecture owns structural tradeoffs; Code and affected specialists contribute concrete costs. Requiring a focused comparison is a package default, not a mandate for a separate Decision Record (DR).

### ARCH-05 — Owned integration contracts

- Rule and rationale: Each affected integration must have compatible producer/consumer expectations and identifiable responsibility for authoritative decisions and failures. Transport success must not be mistaken for the promised business outcome.
- Trigger; phase/risk: New or changed synchronous API, asynchronous message, external adapter, shared library or cross-component operation; all phases.
- Parameters: Producer/consumer and deployed binding; payload meaning, identity, error and acceptance semantics; timing, ordering, delivery and recovery guarantees where relevant; supported versions and actual contract owner.
- Inspection: Compare the two sides on success, rejection, partial completion and uncertain response. Locate the concrete adapter and configuration that supply any claimed retry, durability or idempotency guarantee. Trace protocol-to-domain translation and clarify which component decides the final outcome. Carry compatibility analysis to ARCH-13 and state sequencing to ARCH-08/09.
- Expected evidence: Contract sections or verified behavior, actual producer/consumer call sites and binding, ownership and failure-response table. Compliance requires agreement on the relevant outcomes, not merely matching field names.
- Defective example: An API promises a completed export after a queue acknowledges acceptance, while the captured worker can later reject that export and no completion result is exposed.
- Safe counterpart: The API promises accepted work, provides a stable operation identity and exposes eventual completion or failure through the agreed mechanism.
- Limits: A signature, interface name or illustrative storage contract does not establish the injected adapter's implementation. If essential semantics are uncaptured, return a conditional risk or question and incomplete affected coverage.
- Owner/contributors: Architecture owns boundary semantics; Code checks adapters, Database storage guarantees, Security trust boundaries and DevOps provider configuration.

### ARCH-06 — Runtime and deployment lifecycle

- Rule and rationale: The participating components must preserve required behavior through startup, steady operation, replacement, shutdown and restart. Static structure alone cannot show lifecycle safety.
- Trigger; phase/risk: Changed process topology, hosting, dependency initialization, readiness, shutdown, local state or deployment unit; all phases where deployed behavior is relevant, deeper at launch/growth.
- Parameters: Actual runtime/deployment topology and versions; traffic admission, initialization and termination behavior; owned in-flight work; persistence and recovery obligations; permitted interruption window.
- Inspection: Trace who starts first, when traffic/work is admitted, and how dependencies become usable. Follow draining and termination while work is active, including forced termination and restart. Check ephemeral state and ownership transfer. Compare configured behavior with supplied observed deployment evidence; distinguish the two.
- Expected evidence: Relevant manifests/configuration and process bindings, lifecycle sequence, in-flight-work fate, state lifetime and available runtime observations. A compliant design finishes, rejects or durably transfers work according to its contract at each inspected transition.
- Defective example: A worker acknowledges a durable job before placing its only completion state in an ephemeral process cache; replacement loses the accepted job despite a no-loss contract.
- Safe counterpart: The worker's durable claim and completion protocol allows another worker to recover unfinished accepted work; shutdown behavior matches that protocol.
- Limits: Kubernetes is not required. Kubernetes 1.34 documentation supplies one platform example of readiness and termination, not a guarantee for other versions or an application's correctness. Configuration alone does not prove deployed topology or shutdown success.
- Owner/contributors: Architecture owns interactions and state lifetimes; DevOps supplies platform/release evidence, Code worker behavior and Database durability.

### ARCH-07 — End-to-end failure isolation

- Rule and rationale: A dependency failure, delay or overload must not propagate beyond the allowed impact or consume resources beyond the recorded end-to-end contract. Local retry or timeout settings are insufficient when their composition changes the result.
- Trigger; phase/risk: Remote dependencies, shared pools, fan-out, retries, degraded modes or availability commitments; all relevant phases, expanded workload/recovery analysis at growth or high criticality.
- Parameters: Critical/optional dependencies; total user-operation deadline and attempts where specified; shared resources and capacity; allowed degraded behavior; recovery owner and common failure assumptions.
- Inspection: Trace a slow, unavailable and recovering dependency through all affected callers. Identify waiting resources, nested retries, cancellation limits, queue growth and shared failure paths. Check whether a proposed fallback is independent and preserves required correctness, tenant context and capacity. Assess recovery load as well as steady-state failure. Use measured data or state a bounded hypothesis.
- Expected evidence: Call/failure sequence, effective retry and deadline ownership, shared-resource map, permitted degradation, capacity assumptions and supplied observations. A compliant result contains the selected failure within the required scope and has a supported recovery path.
- Defective example: Optional recommendations share the entire request pool with checkout; a captured prolonged recommendation outage consumes that pool and prevents checkout, violating the supplied isolation requirement.
- Safe counterpart: Recommendations have bounded use of shared capacity and a permitted omission path, while checkout retains the resources needed for its recorded workload.
- Limits: A circuit breaker, separate process or redundant endpoint is not universally required or sufficient. Timeout does not undo remote effects. An unknown provider determines conditional outcomes; do not report inevitable loss or duplication.
- Owner/contributors: Architecture owns failure propagation; Code retry/cancellation correctness, Performance capacity and DevOps operational recovery contribute. Numeric budgets remain project parameters.

### ARCH-08 — Atomicity and recoverable multi-component effects

- Rule and rationale: Operations spanning state owners or external effects must preserve their declared invariant and expose a recoverable, truthful outcome at each relevant interruption point. A transaction in one component does not make another component's effect atomic.
- Trigger; phase/risk: Dual writes, shared mutable state, multiple writers, event publication following mutation, or multi-step business effects; all phases where present, with heightened scrutiny for irreversible actions.
- Parameters: Invariant and authoritative writer(s); actual transaction boundary; effect/acknowledgment order; operation identity; delivery/deduplication guarantees; reconciliation or compensation responsibilities and allowed terminal states.
- Inspection: Write separate failure windows before and after each commit, publication and acknowledgment. For each, record durable state, effects already completed and required next action. Examine concurrent writers and retry/compensation paths, including compensation failure. Verify adapter bindings before using their guarantees. Compare one local transaction, durable publication, reconciliation or compensation according to the actual invariant; no mechanism is prescribed in advance.
- Expected evidence: Located state/effect sequence, fault-window table, provider/store contract, writer and recovery ownership, and distinguishing cases. A compliant result can recover each required outcome without falsely reporting rollback, completion or absence of an effect.
- Defective example: A committed booking requires a durable fulfillment request, but the captured path crashes after commit and before an in-memory-only publication; no persisted intent or reconstruction path exists in the bounded inspected scope.
- Safe counterpart: Booking and publication intent commit atomically, and recovery republishes pending intent under a verified duplicate-tolerant consumer contract. This protects the inspected gap; it does not establish global exactly-once effects.
- Limits: An outbox preserves intent, not automatic external atomicity. Compensation may preserve business meaning without restoring original state and may need owned manual recovery. Engine isolation and delivery guarantees require version-specific evidence.
- Owner/contributors: Architecture owns cross-component invariants; Code orchestration, Database transactions and DevOps recovery contribute.

### ARCH-09 — Asynchronous consistency and derived state

- Rule and rationale: Events, projections, replicas and caches must preserve the consistency and lifecycle contract of the decisions that consume them. A readable projection is not necessarily current enough to authorize a business effect.
- Trigger; phase/risk: Asynchronous communication, replay, multiple read models, replicated state or caching; all phases where present, deeper lag/skew/rebuild analysis at growth.
- Parameters: Authoritative state; acceptable freshness and ordering scope; event identity, retention and replay behavior; duplicate handling; rebuild/reconciliation owner; consumer decisions and applicable deletion/retention rules.
- Inspection: Trace mutation through publication, consumption and visible state. Examine duplicate, out-of-order, delayed and missing delivery using the actual contract. Follow a consumer acting on stale data, a restarted projector, and a rebuild alongside live updates. For caches, inspect identity scope, invalidation/expiry and the consequences of a miss or stale entry. Check whether replay can repeat effects or reintroduce data that should remain unavailable.
- Expected evidence: State lineage, consistency contract, event/projection sequence, repair/rebuild rules and observed or proposed distinguishing cases. Compliance preserves the required business invariant despite the allowed lag and replay behavior.
- Defective example: An eventually updated inventory projection is the sole authority for accepting a limited-stock sale even though the contract prohibits overselling and concurrent authoritative reservations are not checked.
- Safe counterpart: The projection supports browsing, while the authoritative reservation operation decides stock availability; the interface represents its result honestly.
- Limits: Eventual consistency is not automatically defective, and immediate consistency is not universally required. A local broker guarantee does not establish exactly-once business effects. Event sourcing, CQRS and caching remain optional.
- Owner/contributors: Architecture owns consistency across consumers; Code delivery logic, Database persistent semantics, Performance cache costs and Compliance established lifecycle obligations contribute.

### ARCH-10 — Tenancy model and context boundaries

- Rule and rationale: The selected tenancy model must preserve the established isolation, ownership and resource-sharing contract across the complete affected flow. Authentication alone does not establish tenant isolation.
- Trigger; phase/risk: Tenant-scoped resources, shared hosting, tenant routing or changed tenancy model; any phase with those features.
- Parameters: Meaning of tenant, user/customer relationships, tenant-to-deployment/storage mapping, trusted context source, shared resources, permitted cross-tenant operations and actual isolation/residency commitments.
- Inspection: Map the tenant through entry point, service call, queue/job, cache, storage and returned artifact. Identify where context is established, translated or lost. Inspect shared administration and background paths. Compare pooled, dedicated or hybrid choices only against the affected commitments; include noisy-neighbor and fleet costs where relevant.
- Expected evidence: Tenant/resource map, context boundaries and actual consumers, responsibility for tenant-aware routing/enforcement, relevant cross-tenant and capacity evidence. Compliance requires the selected mechanism to preserve the recorded boundary, not a particular physical layout.
- Defective example: Tenant-local report IDs cross a shared worker boundary without tenant context, so a captured worker lookup can select another tenant's report.
- Safe counterpart: The worker receives verified tenant context and resolves report identity within the correct scope, or the verified deployment binding makes that scope unambiguous.
- Limits: Security owns exploitation and authorization depth; Architecture must not imply security certification from this trace. One database per tenant, shared tables and separate services are all conditional choices.
- Owner/contributors: Architecture owns the model and cross-component context; Security, Code, Database and DevOps supply enforcement and placement evidence.

### ARCH-11 — Tenant lifecycle and data disposition

- Rule and rationale: Supported tenant transitions must preserve coherent ownership, access and data disposition through partial progress and recovery. Deactivation, offboarding and deletion have different meanings and must not be conflated.
- Trigger; phase/risk: Onboarding, trial conversion, suspension/reactivation, offboarding, relocation, or supported tenant merge/split; any phase implementing the transition. Growth increases concurrency and fleet variation, not the set of promised features.
- Parameters: Supported states/transitions; activation prerequisites; tenant/resource ownership; handling of in-flight work; established export, retention, deletion, reactivation and residency requirements; owner of residual resources and recovery.
- Inspection: Trace the transition through tenant metadata, routing, credentials/access, resources, jobs and data copies. Interrupt provisioning or cleanup after each material step; inspect retry and partial status. For offboarding, follow applicable derived data, provider copies and backups to their actual disposition policy and restoration behavior. For moves, inspect authoritative routing and writers before/during/after cutover. Check only supported merge/split behavior.
- Expected evidence: Lifecycle/state table, affected resource/data inventory, partial-progress and recovery paths, accepted disposition rules and relevant observations. Compliance means the requested state is reached truthfully or remains explicitly incomplete with owned recovery.
- Defective example: Offboarding reports deletion complete after removing the tenant row while a captured queued export can still recreate and expose tenant files, contrary to the supplied deletion contract.
- Safe counterpart: The lifecycle prevents new work, accounts for in-flight work and removes or retains each copy according to the established policy, reporting pending disposition accurately.
- Limits: No universal retention duration, deletion law, instant backup erasure or automated provisioning requirement. A controlled manual process can satisfy a small deployment. Compliance supplies obligations; Database/DevOps establish storage and recovery facts.
- Owner/contributors: Architecture owns lifecycle coordination; Code, Security, Database, DevOps and Compliance contribute their affected controls.

### ARCH-12 — Entitlement ownership and propagation

- Rule and rationale: Plan- or subscription-dependent behavior must use a coherent entitlement authority and a defined propagation/failure contract. A payment event, account role and feature entitlement need not mean the same thing.
- Trigger; phase/risk: Paid features, plans, quotas, subscription events, grace periods or entitlement caches; any phase implementing these features.
- Parameters: Tenant/customer/account mapping; authoritative feature rules; grant/revoke effective time; permitted grace and provider-outage behavior; cache freshness; handling of provider event order, completeness and reconciliation; in-flight work rules.
- Inspection: Trace a grant, downgrade and revocation from authority through API, workers and relevant UI decisions. Identify duplicated pricing/entitlement rules and conflicting caches. Inspect missed/delayed notifications and re-fetch/reconciliation behavior using the actual provider version. Determine whether an existing job may finish after a change under the recorded policy.
- Expected evidence: Authority and consumer map, transition/propagation table, provider binding, stale/outage outcome and reconciliation ownership. Compliance preserves the actual feature-access and quota contract across all inspected consumers.
- Defective example: A synchronous API stops allowing a paid export after revocation, while a separate worker treats an old purchase event as perpetual permission despite an immediate-revocation requirement.
- Safe counterpart: Both use the established effective entitlement policy; queued work observes the recorded revocation or permitted completion rule and can reconcile stale state.
- Limits: No universal billing provider, immediate revocation, grace interval or fail-open/fail-closed choice. Stripe's product-feature mapping is a provider example; its event and API behavior must not be assumed for another provider or unverified version.
- Owner/contributors: Architecture owns authority/propagation design; Code implementation, Security access enforcement and Performance cache behavior contribute.

### ARCH-13 — Compatibility and migration

- Rule and rationale: Architecture changes must preserve supported producer/consumer and deployment combinations or follow an explicitly accepted transition. A reversible routing change does not imply reversible data changes.
- Trigger; phase/risk: API/event/schema evolution, service or storage moves, adapter replacement, rollout order, rollback or deprecation; all phases with existing consumers, expanded mixed-version analysis at launch/growth.
- Parameters: Supported old/new producers, consumers, schemas and stored events; compatibility window; sequencing and traffic routing; source of truth during transition; downtime allowance; rollback/roll-forward limits and deprecation owner.
- Inspection: Build an old/new matrix for source, wire and behavioral expectations. Trace deployment and rollback in allowed orders, including delayed jobs and persisted messages. Inspect data transfer, concurrent writes, reconciliation and cutover. Identify the point after which reverting code is insufficient. Compare incremental migration with bounded replacement using the actual project constraints.
- Expected evidence: Version/consumer matrix, contract changes, deployment and state-transition sequence, recovery limits and accepted breaking-change decision if relevant. Compliance requires every supported combination or its agreed exclusion to be accounted for.
- Defective example: A producer deploys a new event meaning before old consumers retire; parsing succeeds, but the old consumer applies the amount in the wrong unit.
- Safe counterpart: The transition preserves old semantics for old consumers or gates the accepted cutover until their retirement; replay and rollback remain compatible with stored records.
- Limits: Google AIP-180 is scoped API guidance, not a universal versioning rule. A deliberate approved breaking change can be valid. Zero downtime, indefinite backward compatibility and a strangler migration are not universal requirements.
- Owner/contributors: Architecture owns system transition; Code API/message behavior, Database migration integrity and DevOps rollout/recovery contribute.

### ARCH-14 — Workload scaling and capacity constraints

- Rule and rationale: A structural scaling claim must account for the actual workload, limiting resources and scaling unit. A reachable capacity risk must be explained with evidence or a bounded estimate rather than an assumed future size.
- Trigger; phase/risk: Growth commitment, fan-out, large state or payloads, shared resources, asynchronous backlog, concurrency or performance-sensitive flow; all phases with a reachable limit, wider workload analysis at growth/criticality.
- Parameters: Arrival and service rates where known; input/state size; peak and tenant skew; fan-out; resource/pool/provider limits; latency/throughput objectives; allowed rejection/degradation; scaling and recovery times; cost constraints when established.
- Inspection: Trace work and resource use per operation and per tenant. Identify serial work, contention, shared bottlenecks and what adding an instance can actually increase. Examine sustained and burst load, backlog draining, admission/backpressure, scale-in and a large tenant. Compare local optimization, bounded admission, larger units, replication, caching or partitioning only when they address the identified constraint; carry consistency changes to ARCH-09/15.
- Expected evidence: Workload assumptions, bounded calculation or supplied measurement with conditions, bottleneck/scaling-unit map and tradeoffs. Compliance supports the stated workload or explicitly records the remaining capacity uncertainty.
- Defective example: Doubling stateless workers doubles connections against an already saturated fixed-size database pool, while the proposed capacity claim assumes throughput doubles and supplies no change to that limiting resource.
- Safe counterpart: The design identifies the limiting resource, bounds worker admission and supports its capacity claim with the relevant measurements or clearly labeled estimate.
- Limits: An estimate is not a benchmark. Average latency hides tail or tenant-specific behavior. No universal utilization target, cache, shard count or service split follows from this control.
- Owner/contributors: Architecture owns structural limits and scaling tradeoffs; Performance owns measurement, Database store bottlenecks and DevOps provisioning limits.

### ARCH-15 — Partition and failure-domain tradeoffs

- Rule and rationale: Existing or required partitioning, replication and failover must preserve the recorded ownership, consistency and recovery contract under the failures they claim to tolerate. Additional copies do not by themselves establish independent failure domains or safe authority transfer.
- Trigger; phase/risk: Shards, cells/stamps, replicas, leader/lease ownership, regional failover, or an explicit requirement to survive an identified shared failure; any phase using them, usually deeper at growth or high criticality.
- Parameters: Partition key/routing and skew; transaction boundaries; replica and writer authority; common dependencies; tolerated failures; consistency during partition; recovery time/data-loss objectives if established; rejoin, rebalance and failback behavior.
- Inspection: Map common failure causes and surviving capacity. Trace an isolated partition, authority transfer, stale route, unavailable shard and recovery/rejoin as applicable. For sharding, inspect cross-partition operations and movement while writes occur. For failover, identify how old and new writers are prevented from violating the invariant. Compare the proposed benefit with coordination, latency, migration and operational costs; verify the actual mechanism through specialist evidence.
- Expected evidence: Failure-domain and authority map, partition/failover sequence, actual store/provider semantics, recovery assumptions and supplied relevant observations. Compliance supports the exact tolerated scenario and states unproven recovery objectives.
- Defective example: Two application replicas are described as surviving database-node failure, but both require the same single database node and no permitted degraded path exists.
- Safe counterpart: The claim is narrowed to application-process failure, which the inspected topology supports. If database-failure tolerance is required, the chosen recovery design and evidence address that separate requirement.
- Limits: No mandatory multi-region deployment, disaster recovery platform, consensus implementation or sharding. A backup setting does not prove restoration; a consensus label does not prove application-effect correctness. Database and DevOps own detailed storage/recovery verification.
- Owner/contributors: Architecture owns common dependencies and system tradeoffs; Database, DevOps, Performance and Security contribute actual storage, recovery, capacity and boundary evidence.

## Verification

The inspection and expected-evidence fields define each control's verification method. Use the defective and safe examples to distinguish conclusions; do not execute examples as though they were project tests. Capture relevant checks as supplied evidence or unperformed work under the shared contract. Review permission does not authorize fault injection, deployment changes or running target code.

### Separate fault windows and unknown adapters

For a cross-component finding, record the interruption point, durable state, effects already completed, required recovery and supporting evidence before asserting impact. Keep the following illustrative payment/outbox windows separate. They assume only an atomic payment-record/outbox commit; the actual notification adapter and consumer contracts still need evidence.

| Interruption point | Established state | Supported conclusion and question |
| --- | --- | --- |
| Before the atomic local commit | Neither local record is committed under the stated transaction guarantee. | This window does not establish a committed local payment. Any earlier external effect must be traced separately. |
| After local commit, before notification | Payment record and pending publication intent are durable. | A verified recovery worker can later publish. The interruption alone does not prove permanent loss, duplicate notification or duplicate payment. |
| After external notification, before marking sent | Local intent remains pending; an external effect has happened if independently established. | A restart may attempt delivery again. Whether a second effect occurs or violates the contract depends on actual adapter/provider deduplication and consumer behavior. |
| After sending, with acknowledgment lost | Local observation is uncertain; external completion may or may not have occurred. | Reconcile under the actual contract. Neither absence nor duplication follows from response loss alone. |

A caller's arguments do not prove a hidden adapter's retries, idempotency or durability. A separate example implementation does not establish the injected implementation. Cite the binding, relevant captured implementation and versioned contract, or state the conditional risk and missing dependency. Never attach an inevitable duplicate payment to a window that establishes only a pending notification.

Before accepting an assessment, compare every material subclaim in its trigger, impact, correction and summary with the established state. A valid core concern does not validate unsupported additional consequences. Retain the raw return; request a bounded corrected follow-up or reject the unsupported finding with a reason through the existing shared process. If the unsupported claim controls a criterion's status, obtain a linked corrected report or retain an unresolved conflict and incomplete coverage. Removing a finding alone cannot rewrite an accepted assessment or establish satisfied coverage.

### Focused corrections and clean conclusions

Compare a correction with the current design using the same scenario. State the expected benefit, compatibility/migration work, operating cost and risk moved elsewhere, plus a check that would distinguish the faulty and corrected behaviors. A whole-system replacement requires evidence beyond the existence of a local defect.

A small internal tool can synchronously send a bounded notification after its data commits when its accepted timing and delivery contract permits that choice. A payment flow that holds database locks while waiting for a provider can violate a different supplied contract. Preserve the different contracts; neither example establishes a universal outbox or service-extraction requirement.

An assignment can return no findings when its applicable scope is supported. State inspected flows, missing consumers/adapters, unperformed checks and unknown deployment facts. Completion of an architecture assignment does not establish overall system correctness or release approval.

## Responsibilities and exceptions

Architecture owns the architectural assessment of these controls. Contributors listed in each control supply evidence through the lead under existing domain responsibilities; these names do not register roles or authorize further delegation. Security owns exploitation/authorization judgment, Database persistence and migration semantics, Code local implementation, Performance measurements, DevOps delivery/readiness/recovery, Testing verification strategy, and Compliance established obligations. Missing specialist evidence remains a coverage limit.

Use the Architecture Policy (POL) for scoped defaults, supplements, replacements and waivers. Record the actual effective criterion and source. A replacement changes the selected rule; a waiver preserves the contradiction and residual consequence. Do not infer exception authority from a comment, filename, source publication or developer response.

## Ownership, review, and related policy

The package maintainer owns this catalogue. Review affected controls when adopted requirements, platform/provider semantics, recurring review failures or accepted domain boundaries change. Keep version-bound source, control and evaluation evidence in maintenance records. Do not invent a recurring review schedule or organization approver.

## Research reference

[Sources and control mappings](../research/architecture.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
