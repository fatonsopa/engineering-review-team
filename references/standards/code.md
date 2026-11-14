# Code review technical standard

## Purpose and scope

The Code Reviewer examines whether assigned code implements the intended behavior correctly and remains understandable, compatible and safe to change. Use behavior tracing, boundary analysis, concurrency schedules and resource ownership methods. A short role guide should load this detailed Technical Standard (STD) only for applicable control families.

These controls are package defaults, not universal legal obligations or proof of certification. The project supplies intended behavior, supported platforms, release compatibility, workload limits and approved exceptions. External publications explain relevant mechanisms; they do not create product requirements. Source-specific examples below apply only to the identified platform or contract. All examples are illustrative, not findings about an inspected application.

For every applicable control, record the selected criterion, inspected code and dependencies, expected versus observed behavior, evidence type, and remaining limits. Reading a source, inspecting code, receiving a test result and executing a test are distinct evidence states. A suspected defect requires a concrete trigger and consequence. Missing evidence is not proof of failure. Use the shared finding guidance and the user’s requested format.

## Definitions

A **control** is a conditional review rule with an inspection method; it is not proof that a particular technology is mandatory. An **invariant** is a property that must remain true across the operation. A **safe counterpart** satisfies the stated boundary under its assumptions; it is not certified secure in every context. A **project parameter** is an actual limit, supported version, business rule or operating condition needed to evaluate a control. Unknown parameters stay unknown.

## Principles

Assess observable consequences and accepted obligations. Match language and provider semantics to the deployed versions. Use realistic failing and safe paths to distinguish defects from preferences. Preserve missing evidence and scope limits. Apply phase and independent risk together, without imposing future architecture on a bounded application.

## Applicability and phases

Select controls by code behavior and exposure first. The phase describes depth and evidence needs; it cannot waive an active risk.

| Phase | Code review depth |
| --- | --- |
| Foundation | Trace changed behavior, edge values, contracts, state, relevant resources, errors and tests. An isolated prototype need not acquire queues, distributed locks or multi-region services. Real credentials, shared tenants, payments or durable effects still activate their controls. |
| Production launch | Verify actual user and tenant boundaries, external failures, deployed compatibility, recoverable persistent effects and diagnostic behavior. Confirm the limits and error outcomes users encounter. |
| Growth | Extend the same controls across larger inputs, overlapping requests, mixed deployed versions, repeated deliveries, capacity limits and competing tenants. Require workload evidence for performance conclusions. |
| Advanced scale or criticality | Examine the assigned code’s behavior under documented partition, replay, failover or consistency conditions when those mechanisms exist. Specialized system analysis remains a handoff, not an automatic requirement to adopt distributed architecture. |

Payments, sensitive data, external exposure, tenancy, irreversible actions and contractual availability activate relevant checks at any phase. SaaS delivery does not imply shared-table multitenancy or a particular scale. Each control below identifies its trigger; phase alone never activates a technology that the project does not use.

## Rules

For each applicable control, the reviewer must perform its method or report the precise unperformed work. A compliant result satisfies the recorded contract and invariant on the inspected scope, supported by the specified evidence; a safe example illustrates one way, not the only permitted implementation. Every control inherits the Code Policy (POL) and its approved alternatives and exceptions.

## Verification

The methods, evidence and safe counterparts below define the check for each rule. Use these together with the parameter table; annotate unperformed checks and unresolved parameters in the shared report. A syntactically valid report does not prove the assessment is correct.

### Control parameters and ownership

The Code Reviewer owns the application-code assessment for every row below. Contributors provide specialist evidence through the lead; their availability does not erase an uncovered dependency. These are required input categories, not a mandate to create a separate document for each.

| Control | Required project parameters and reason | Contributor or specific limit |
| --- | --- | --- |
| CODE-01 | Accepted behavior and authorized change scope; prevent silent product drift. | Lead resolves intent and authority. |
| CODE-02 | Types, defaults, ranges, units and compiler settings; preserve valid values. | Static types do not establish runtime data shape. |
| CODE-03 | Format/schema, permitted fields, size and business constraints; reject invalid states before effects. | Security owns attack-class assessment. |
| CODE-04 | Producers, consumers, deployed versions and compatibility window; protect supported clients. | Architecture/Database provide system and schema contracts. |
| CODE-05 | Invariants, effect/commit boundaries and recovery contract; prevent hidden partial outcomes. | Database validates engine guarantees. |
| CODE-06 | Shared state, participating execution contexts and atomicity requirements; prevent conflicting decisions. | Database/Performance assess isolation and contention. |
| CODE-07 | Resource owner, transfer and required lifetime; prevent leaks and premature release. | Framework-managed cleanup can be correct. |
| CODE-08 | Runtime version, child ownership, cancellation API and deadline meaning; avoid orphan work. | Local cancellation does not undo remote effects. |
| CODE-09 | Call deadline, attempts, retryable outcomes and nested client configuration; contain retry load. | Performance/DevOps supply capacity and service evidence. |
| CODE-10 | Business operation identity, provider API, key scope/retention and reconciliation; avoid duplicate effects. | Expired deduplication needs an explicit recovery decision. |
| CODE-11 | Broker/provider delivery contract, durable acceptance and terminal handling; prevent lost or repeated work. | Security verifies authentication/signature design. |
| CODE-12 | Tenant model, trusted context, entitlement authority and caching rules; preserve isolation. | Security owns authorization/threat depth. |
| CODE-13 | Input limits, cost growth and latency/memory budgets where established; detect reachable resource failure. | Performance owns workload-wide measurement. |
| CODE-14 | Queue/worker capacity, admission policy, fairness and overload contract; preserve bounded progress. | Performance/DevOps provide operational limits. |
| CODE-15 | Adopted conventions, responsibility boundaries and supported change scenarios; reduce concrete maintenance risk. | Architecture owns system decomposition. |
| CODE-16 | Changed requirements, test setup, observable outcomes and available results; reject misleading confidence. | Testing owns full verification strategy. |
| CODE-17 | Error/status/payload contract and permitted recovery; preserve honest caller behavior. | No universal exception-swallowing or retry rule. |
| CODE-18 | Permitted fields, event purpose, volume and required audit semantics; preserve diagnosis without prohibited disclosure. | Security/Compliance establish protection/audit obligations. |
| CODE-19 | UI states, lifecycle, support matrix and applicable accessibility requirements; prevent broken interactions. | Design supplies visual and assistive evidence. |
| CODE-20 | Currency/unit, rounding/precision, timezone and calendar rules; preserve business meaning. | Localization owns presentation; example arithmetic is language-specific. |

### CODE-01 — Requirement and change alignment

- Rule: Changed observable behavior must match accepted requirements and authorized supporting scope; unresolved intent must remain explicit.

- Trigger: Any behavior change; all phases.
- Method: Map changed paths to accepted behavior and necessary supporting work. Trace an entry point to its observable outcome; distinguish deliberate scope expansion from necessary refactoring. Ask the lead to resolve conflicting intent.
- Evidence: Requirement or task section, caller and changed path, expected/observed result, unexplained changes.
- Defective example: A rename-only request also changes who can delete a workspace without accepted authorization.
- Safe example: A local helper extraction preserves behavior and enables the requested rename.
- No rule requires every changed line to name a ticket.

### CODE-02 — Values, absence and representation

- Rule: Values and defaults must preserve the contract’s distinctions, ranges and units across producer and consumer boundaries.

- Trigger: Nullable, optional, converted or boundary-valued input/output; all phases.
- Method: Enumerate absent, null, zero, false, empty, minimum, maximum and out-of-range cases allowed by the contract. Follow conversions and defaults into consumers; inspect compiler configuration and unsafe assertions.
- Evidence: Value table, types/configuration, runtime validation and caller behavior.
- Defective example: A failed TypeScript `find` lookup is asserted non-null and dereferenced.
- Safe example: The missing case returns the contracted outcome before dereference.
- Enabling a compiler option is not proof that external data was validated.

### CODE-03 — Parsing and validation boundaries

- Rule: Data used for business effects must satisfy the applicable structural and semantic rules on the representation actually consumed; this does not replace sink-specific security controls.

- Trigger: Data crosses a format or trust boundary; all phases.
- Method: Check parser limits, permitted fields, syntax and cross-field meaning before business effects. Follow the representation actually used after decoding.
- Evidence: Parser settings, schema/business rules, accepted and rejected examples.
- Defective example: Valid dates pass independently although a booking ends before it starts.
- Safe example: Structural checks and ordering rules reject that booking before storage.
- Validation does not establish authorization or replace parameterized SQL/context-specific output encoding. Route concrete injection concerns to Security while retaining located evidence.

### CODE-04 — Interface and version compatibility

- Rule: Changes must preserve the contracts of supported consumers and permitted deployment/version combinations, or use an explicitly accepted migration.

- Trigger: Changed API, message, shared function, serialization or dependency contract; all phases, with mixed-version checks at launch and later.
- Method: Inspect actual producers and consumers, defaults, errors and upgrade/rollback combinations. Separate wire compatibility from application behavior.
- Evidence: Old/new contract, call sites, supported versions and compatibility cases.
- Defective example: Reusing a protobuf field number changes an old field’s meaning for deployed consumers.
- Safe example: Reserve the removed number and use a new field with compatible defaults, after verifying that every supported consumer tolerates the removal or documented fallback.
- Binary protobuf conclusions do not automatically apply to ProtoJSON or other serializers.

### CODE-05 — State invariants and partial effects

- Rule: Each operation must preserve its declared invariants and accurately represent committed, failed, partial and uncertain effects through recovery.

- Trigger: Mutations, multi-step workflows or effects outside one atomic boundary; all phases.
- Method: State the invariant; enumerate failure points before and after each effect. Inspect commit, recovery and reconciliation paths. A timeout does not establish rollback.
- Evidence: State transition table, effect ordering, transaction boundary and recovery outcome.
- Defective example: A payment may succeed remotely, but a lost response causes the application to create a second payment as recovery.
- Safe example: Reconciliation identifies the original operation before deciding whether another effect is needed.
- Database transaction guarantees require Database evidence; this check covers application orchestration.

### CODE-06 — Concurrency and atomic decisions

- Rule: Overlapping executions must preserve shared invariants under reachable event orderings; a guard must cover the complete decision and effect it claims to protect.

- Trigger: Shared state, overlapping requests, callbacks, threads or processes; all phases.
- Method: Write a concrete interleaving. Check whether synchronization protects the complete decision and mutation, including every competing path; inspect lock ordering and reentrancy when present.
- Evidence: Schedule, invariant, participating reads/writes and synchronization scope.
- Defective example: Two requests both observe the last seat as available before either reserves it.
- Safe example: One atomic conditional reservation permits only one success.
- Process-local locks do not establish cross-process exclusion. Database isolation remains a handoff.

### CODE-07 — Resource lifetime and ownership

- Rule: Every acquired resource must remain valid while owned work uses it and be released or transferred according to the required lifetime on every relevant exit.

- Trigger: Acquired streams, handles, connections, locks, subscriptions or tasks; all phases.
- Method: Trace acquisition, ownership transfer and release through success, error, early return and teardown. Inspect retained references and cleanup when ownership changes.
- Evidence: Ownership table, release paths and lifecycle cases.
- Defective example: A React subscription survives dependency replacement and delivers duplicate notifications.
- Safe example: Cleanup releases the old subscription before replacement and at unmount.
- Managed scopes can be sufficient; do not demand manual release where the runtime guarantees the required lifetime.

### CODE-08 — Cancellation and child work

- Rule: Owned child work must reach the required terminal or transferred-ownership state before its resources are released; requesting cancellation alone is insufficient.

- Trigger: Asynchronous children, cancellation or scoped deadlines; all phases.
- Method: Determine who owns child completion, cleanup and exception observation. Inspect cancellation propagation and post-cancellation effects using the actual library version.
- Evidence: Parent/child lifecycle trace and failure/cancellation outcomes.
- Defective example: Python code assumes `gather` cancels other tasks after one ordinary exception, then closes resources they still use.
- Safe example: It requests cancellation where needed and awaits/joins owned tasks through completion and cleanup before release, or uses a structured-concurrency scope that guarantees that completion. A task that suppresses cancellation still needs explicit handling.
- For Python 3.11.18, `TaskGroup` and `gather` differ; neither local cancellation nor timeout proves remote work stopped.

### CODE-09 — Timeouts and retry amplification

- Rule: Remote work and retries must obey applicable total deadlines and bounded attempt policies, without unintended multiplicative retry behavior or unowned work after caller completion.

- Trigger: Remote calls or retrying dependencies; all phases, expanded capacity checks at growth.
- Method: Trace total deadline, connection/request coverage, retryable failures, attempts and delays across nested clients. Inspect whether retries outlive the caller or multiply at several layers.
- Evidence: Effective client configuration, attempt timeline and failure outcomes.
- Defective example: Three retrying layers each multiply attempts during one downstream failure.
- Safe example: A designated retry owner observes the remaining deadline and bounded attempts with suitable backoff/jitter.
- Numeric budgets come from the project and dependency behavior, not an invented universal timeout.

### CODE-10 — Idempotent business operations

- Rule: Retries of one logical operation must preserve its intended effect under the actual deduplication/reconciliation contract, including concurrency and retention limits.

- Trigger: A side effect can be retried or resubmitted; all phases.
- Method: Trace operation identity, parameter binding, deduplication scope, concurrent attempts, retention and recovery after an uncertain response.
- Evidence: Key lifecycle, effect boundary, duplicate/retry cases and provider version.
- Defective example: Each retry generates a new payment operation key.
- Safe example: Retries of the same intended operation reuse its key under the provider’s contract; a new purchase gets a distinct identity.
- HTTP idempotence concerns intended effect, not identical responses. Stripe API v1 and v2 differ; never universalize their behavior.

### CODE-11 — Webhooks and background delivery

- Rule: Accepted asynchronous work must preserve the documented delivery/effect contract through crashes, duplicates and ordering changes; success must not promise durability that was not achieved.

- Trigger: Events, jobs or webhook handlers; all phases where present.
- Method: Inspect duplicate/out-of-order delivery, authentication integration, durable acceptance, acknowledgement, retries and terminal failures. Trace the gap between recording delivery and committing its effect.
- Evidence: Delivery contract, acknowledgement/effect sequence and replay/failure cases.
- Defective example: A handler returns success, stores work only in memory, then loses it on process exit.
- Safe example: It acknowledges after durable acceptance and processes an idempotent job under documented recovery behavior.
- Durability sequencing is a package review rule, not a quoted Stripe requirement. Verify the actual broker/provider; do not assume universal delivery guarantees.

### CODE-12 — Tenant context and entitlements

- Rule: Tenant-specific reads, writes, caches and jobs must use the correct trusted tenant and entitlement context wherever the contract requires isolation or access control.

- Trigger: Tenant-scoped data, caches, jobs or plan-dependent behavior; any phase with these features.
- Method: Follow trusted tenant identity and entitlement decisions through entry point, lookup, cache key, queued work and response. Distinguish user authentication from permission to access a particular tenant resource.
- Evidence: Context provenance, enforcement call sites and cross-tenant/denied cases.
- Defective example: A shared cache key contains only a tenant-local document ID.
- Safe example: The cache’s isolation design prevents one tenant’s entry from satisfying another tenant’s request.
- This control checks integration correctness; Security owns threat coverage and authorization design assessment.

### CODE-13 — Bounded work and algorithmic cost

- Rule: Reachable input-driven work must remain within established resource constraints; material unknown bounds must remain an assessment limit, not an invented performance result.

- Trigger: Input-dependent loops, recursion, parsing, buffering, fan-out or large payloads; all exposed phases, deeper measurement at growth.
- Method: Identify actual maximum input, work and allocation growth. Inspect pre-processing limits and blocking work on shared execution paths. Explain consequences with a reachable input and runtime evidence where needed.
- Evidence: Input bounds, complexity trace and appropriately scoped measurement.
- Defective example: A Node request synchronously parses an unbounded payload on the shared event loop.
- Safe example: Bounded accepted input fits a demonstrated budget, or suitable streaming/offload preserves limits.
- Nested loops and recursion are not automatically defects; Performance owns workload-wide measurement.

### CODE-14 — Backpressure and resource fairness

- Rule: Admission, queued and concurrent work must preserve the project’s resource and overload contract, including tenant fairness where promised.

- Trigger: Shared queues, worker pools, parallel calls or competing tenant workloads; any phase with the risk, expanded at growth.
- Method: Trace admission, queue growth, concurrency limits and overload outcomes; examine whether one input/tenant consumes all workers. Follow the error/degraded result back to callers.
- Evidence: Capacity configuration, bounded queue/worker behavior, overload scenario and caller handling.
- Defective example: A bulk request starts one remote task per unbounded item and exhausts shared connections.
- Safe example: Bounded admission and work scheduling preserve a documented overload outcome.
- Quotas and fairness depend on resources and commitments; do not invent a standard requests-per-second limit.

### CODE-15 — Maintainability and useful abstractions

- Rule: Code must follow applicable conventions and keep implemented rules coherent; a maintainability finding requires an actual convention violation or concrete change/error consequence.

- Trigger: New or changed structure, duplication or conventions; all phases.
- Method: Identify a concrete maintenance hazard, conflicting duplicated rule or unreadable responsibility boundary. Check adopted naming/style rules, misleading comments, obsolete paths and changed public behavior that requires documentation. Explain the concrete consequence rather than prescribing a preferred style.
- Evidence: Affected call sites and a plausible maintenance/error consequence.
- Defective example: Two discount implementations diverge for the same accepted rule.
- Safe example: Shared business logic preserves intentionally distinct presentation paths.
- No arbitrary function-length maximum, compulsory pattern or mandatory abstraction. Pure preferences are optional comments, not defects.

### CODE-15 fallback when project structure guidance is missing

This is part of the same Technical Standard (STD), not an additional standard. Apply it only to gaps left by established project rules, and select methods compatible with the actual language and framework. The project's approved Technical Standard (STD) may specialize or explicitly replace these defaults through the shared authority procedure.

| Default | Inspection and acceptable result | Defective example / safe counterpart |
| --- | --- | --- |
| CODE-15.F1 — Cohesive responsibilities | Trace why a module changes and which callers depend on it. Responsibilities can share a file when that keeps one coherent operation understandable. No universal line count applies. | An email-format helper also mutates billing state unexpectedly / a cohesive billing operation uses explicit collaborators with visible effects. |
| CODE-15.F2 — Understandable interfaces and names | Compare names, visibility and exposed operations with actual meaning and language conventions. Distinguish misleading behavior from a preferred spelling. | `isEligible()` charges a card despite a predicate contract / an explicitly named charge operation declares its effect. |
| CODE-15.F3 — Coherent business rules | Compare duplicated logic for contradictory outcomes and identify its authoritative owner. Similar text with different domain meaning need not be merged. | Two tax paths implement different rates for the same rule / one owned calculation or deliberately separate rules with distinct contracts. |
| CODE-15.F4 — Controlled dependencies | Follow dependencies and initialization/call paths. Establish an accepted boundary violation or concrete coupling/initialization failure; a cycle alone is insufficient. | A module cycle reads uninitialized state on a reachable startup path / a supported cycle is safe under the actual runtime semantics and project constraints. |
| CODE-15.F5 — Navigable file organization | Compare related files and locate public interfaces, tests and implementation ownership. Respect framework discovery, generated files and established component conventions. | A misplaced auto-discovered handler silently bypasses required middleware / a framework-compatible layout has clear ownership even without a preferred `services/` directory. |
| CODE-15.F6 — Useful abstractions | Trace whether an abstraction clarifies a real contract or creates duplicated configuration and hidden behavior. Accept direct code for a bounded operation. | A nominally generic wrapper discards required error distinctions / a small direct call preserves the contract, or an abstraction encapsulates a real shared invariant. |

Record which evidence established the conclusion. A proposed organizational improvement with no demonstrated defect remains advice. Missing guidance alone is neither a code defect nor permission to redesign the project. When an architectural choice is necessary to judge correctness, the lead seeks a decision or records the affected criterion incomplete; Code does not silently choose it.

Language-neutral outcomes do not imply language-neutral implementations. Match resource, dependency, naming and module checks to actual Rust ownership, Go packages, Python modules, Java/.NET conventions, JavaScript/TypeScript modules or framework behavior as applicable. These examples identify selection dimensions, not newly researched control libraries for those stacks. Use existing version-matched official guidance or report the specific gap.

### CODE-16 — Changed-code test integrity

- Rule: Verification relied on for changed behavior must assert meaningful observable outcomes and exercise relevant risks with valid setup; test count or coverage percentage alone does not establish adequacy.

- Trigger: Changed logic or tests; all phases, depth proportional to consequence.
- Method: Check whether assertions distinguish intended behavior from a plausible failure. Inspect mocks, fixtures, awaited work and boundary cases relevant to changed logic.
- Evidence: Requirement-to-assertion mapping; supplied versus executed result clearly labeled.
- Defective example: A cancellation test asserts only that the mock was called, never that cleanup happened.
- Safe example: It observes the required resource/behavior outcome after cancellation.
- No automatic 100% coverage or separate test per branch requirement. Testing owns overall verification strategy and suite adequacy.

### CODE-17 — Error contracts and recovery behavior

- Rule: Error propagation and recovery must preserve the interface’s failure meaning and must not report a failed or uncertain effect as confirmed success.

- Trigger: Exceptions, rejection, partial results or translated service errors; all phases.
- Method: Follow failures through caller handling; compare status, type, payload and retry meaning with the actual interface. Check that failure does not masquerade as successful business output.
- Evidence: Failure path, public contract, observed caller behavior.
- Defective example: A failed update is caught and returned as an empty successful result, so the UI says it saved.
- Safe example: A stable error outcome reaches the caller with the recovery action permitted by the contract.
- Catching every exception is not inherently graceful handling.

### CODE-18 — Diagnostic and audit events

- Rule: Diagnostic and required audit events must preserve their agreed outcome, context and protection requirements without prohibited sensitive content or uncontrolled resource consumption.

- Trigger: Logs, exceptions, telemetry or business audit events change; all phases with those outputs.
- Method: Inspect allowed fields, contextual identifiers, log volume, untrusted formatting and logging failures. Verify required audit events at the actual outcome boundary.
- Evidence: Event schema/sample with sensitive values removed, call sites and failure behavior.
- Defective example: An authentication error logs the complete request including its token.
- Safe example: A bounded structured event records outcome and permitted correlation context without the credential.
- Security/Compliance determine sensitive-data and audit obligations; Code checks the implementation. Required audit durability can differ from optional diagnostic logging.

### CODE-19 — UI asynchronous and lifecycle behavior

- Rule: User-facing state transitions and lifecycle behavior must preserve current intent and applicable interaction contracts, including failures, stale responses and accessible control semantics.

- Trigger: User-facing state, effects or asynchronous requests; all phases where present.
- Method: Trace initial, pending, empty, success, error, disabled and replacement states. Examine stale results, cleanup, keyboard/focus behavior, accessible names and semantic controls against actual UI requirements. Retain the current guide’s contrast and assistive-technology checks when relevant and assigned; request Design evidence for checks beyond available source or interaction evidence.
- Evidence: State table, event ordering and interaction results; visual/assistive checks labeled if unperformed.
- Defective example: A slow old search response overwrites a newer query’s results.
- Safe example: The component or data layer prevents superseded results from committing and clears pending state correctly.
- Design owns visual/accessibility depth; source inspection alone does not prove browser or assistive-technology behavior.

### CODE-20 — Money, time and precision-sensitive semantics

- Rule: Arithmetic and time transformations must preserve accepted units, precision, rounding and calendar/instant meaning through relevant boundaries.

- Trigger: Prices, billing, rounding, durations, expiry or calendar rules; any phase with the behavior.
- Method: Follow units, representation, rounding point and timezone meaning across storage and interfaces. Construct fractional, boundary and timezone-transition cases from the business contract.
- Evidence: Unit/rounding/time rules and exact expected values.
- Defective example: A billing calculation uses binary float equality where the contract requires exact decimal totals, or treats an unspecified local timestamp as a unique instant.
- Safe example: The chosen arithmetic and time representation preserve the specified invariant, including explicit rounding and zone interpretation.
- Decimal still needs precision/rounding decisions; calendar dates are not automatically UTC instants. Localization owns presentation conventions.

## Version and language limits

Before using a language/framework rule, obtain the actual language, runtime, framework, compiler options and deployed provider/API versions from the assigned evidence. Match official documentation to them. The selected examples demonstrate the method; they are not exhaustive language standards.

- TypeScript static null checking cannot certify runtime JSON shape, especially through `any`, assertions or unchecked deserialization.
- Python 3.11 cancellation behavior and structured concurrency must not be copied onto earlier Python or another task library. Cancellation has cleanup and ownership semantics, not automatic transactional rollback.
- React effect replacement/unmount behavior does not describe every UI framework. Framework-managed fetching can already handle stale requests; inspect it before alleging missing manual cleanup.
- Go’s memory model is language-specific. A Go synchronization argument cannot establish C/C++ undefined-behavior safety or prove atomicity across services.
- Match blocking-API checks to the installed Node.js version; an older API list is not complete coverage for a newer runtime.
- Protobuf binary compatibility, application compatibility and ProtoJSON compatibility differ.
- Stripe API v1 replay responses and API v2 recovery behavior differ. Provider semantics and key retention must be selected explicitly.

This catalogue does not provide dedicated C/C++, Rust, JVM, .NET, mobile or database-driver rule libraries. A review of those stacks must select their primary versioned sources before claiming those checks complete. This is a controlled applicability limit, not permission to skip general behavior tracing.

## Responsibilities and exceptions

The Code Reviewer selects and applies these controls within assigned scope. The lead verifies applicability, project authority, selected document sections, exceptions and unresolved specialist dependencies. The package maintainer owns the control catalogue and revisits affected entries when sources, runtime semantics or recurring failures change. Do not invent an organization approver or a review schedule.

Use `references/policies/code.md` for defaults, supplements, replacements and waivers. Record control IDs and the actual effective criteria. A valid waiver preserves the observed contradiction; a replacement identifies displaced criteria and resulting coverage. Shared report and authority rules remain in `references/review_standard.md` and `references/review_policy.md`.

Bind each control and source record to the package version used for the review. Preserve earlier accepted versions when rules change. Do not claim new language/framework coverage without its actual versioned evidence and behavioral evaluation.

## Ownership, review, and related policy

The package maintainer maintains this catalogue under `references/policies/code.md`. Review changes when supported semantics, actual defects, adopted requirements or authority handling change. Keep version-bound source, control and evaluation evidence in maintenance records. Shared finding guidance and permission boundaries remain in their existing owners.

## Research reference

[Sources and control mappings](../research/code.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
