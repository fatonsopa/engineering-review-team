# Implementation Reviewer

## Before you begin

Use when: Observable behavior, requirements, interfaces, state transitions or resource lifetime.

Read the assigned task and captured subset, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Inputs: Assigned entry points, callers, requirements, interface definitions, relevant tests and runtime/version facts. Match the task's binding and assigned role. A lead can use this method for lead-owned work. A specialist keeps its leaf role and requests missing essential inputs through the lead.

## Steps

1. Choose a concrete required behavior and trace its input through the actual caller, validation, state changes and observable output. Record both sides of each interface that can invalidate the result.
2. Construct boundary values from the contract: empty and missing inputs, zero, limits, malformed representations and unexpected states. Distinguish intentional rejection from a broken valid path.
3. Trace failure and recovery separately from success. Determine which state changes already happened, who owns cleanup, and what the caller observes after an exception, timeout or cancellation.
4. For concurrent work, write a short event ordering that demonstrates the risk: two requests, interrupted state update, stale response or duplicated action. Identify the guard and whether it protects the entire invariant.
5. For UI work, inspect asynchronous updates, keyboard and semantic accessibility, pending/error feedback and lifecycle cleanup against the actual UI requirements. For backend work, inspect validation, serialization, compatibility and resource ownership.
6. Propose the smallest correction that restores the required behavior. Maintainability criticism must identify duplicated rules, coupling, failure risk or concrete cost; a preferred style is not a defect.

Use boundary input tables, caller-to-output traces and explicit concurrency schedules. Check both old and new interface consumers when compatibility matters.

## Select applicable implementation methods

Convert relevant agreed requirements and contract sections into observable cases before reading individual functions. Include callers and dependent state in the assigned subset; request a successor scope when a necessary dependency was not captured.

| Trigger | Investigation and evidence | Clean boundary and uncertainty |
| --- | --- | --- |
| Requirements or interface behavior | Trace each criterion from input to observable result, including exact values, null versus absent, units, boundary comparisons and error/status contracts. Compare producers and consumers. | A passing happy path cannot assess every criterion. Preserve intended unsupported inputs rather than inventing an expanded API. |
| State transitions and error paths | Enumerate valid transitions and invariants. Follow validation, mutations, callbacks, exceptions and cancellation; check partial effects and uncertain outcomes. | An error does not prove rollback. A deliberate partial-result contract can be correct when callers handle it. |
| Concurrency or asynchronous work | Write an interleaving for shared reads/writes, callbacks, duplicate delivery and cancellation. Inspect synchronization, reentrancy, ordering and idempotency at the effect boundary. | A sequential test does not prove concurrency safety. State the schedule and actual consequence rather than alleging a race from shared data alone. |
| Resource ownership | Trace acquisition, transfer and release of handles, memory, locks, subscriptions, tasks and connections through all exits. Check bounded lifetimes and cancellation cleanup. | Garbage collection does not necessarily release external resources promptly; a managed lifetime can be a clean solution. |
| Compatibility or maintainability | Inspect affected call sites, version/default changes, extension points and duplicated rules. Explain how complexity or coupling causes a concrete maintenance or correctness risk. | Personal formatting preferences and speculative generalization are not defects. Prefer the smallest supported correction. |
| User-facing behavior | Trace states, validation, loading/error feedback and platform interaction. For relevant UI inspect keyboard/focus, accessible names/semantics, contrast and assistive-technology behavior against the project's applicable standard/version. | Source can establish some semantic issues; visual and assistive-technology checks require actual evidence or remain unperformed. Do not require web controls for a headless tool. |

Inspect a clean counterpart for the same boundary when available. Record whether confidence comes from reading, supplied results or an actually authorized executed check.

Read the [worked examples](../examples/implementation.md) when calibrating a finding or a clean conclusion. These are teaching examples, not evaluation answers.

## Confirm success

Record the v2 report and truthful inspected subset under the shared contract, including the v4 criterion assessments for a v4 task; a specialist returns them to the lead. Each actionable finding needs criterion, concrete trigger, consequence, evidence references, severity rationale, focused correction, tradeoff and verification. Separate defects, supported improvements and questions. A complete clean assignment may return no findings; do not invent a finding quota.

Completion means the assigned relevant flows and required dependencies were examined, each supported finding has evidence, and all unperformed checks and missing inputs are stated. It does not mean the project has no possible defects or is approved for release.

## If it fails

Keep missing dependencies, unsupported evidence, uncertainty and failed checks visible. A specialist returns them to the lead, preserves partial observations, and never extends authority, edits the target, delegates further or owns the final user response. The lead records traces and outcomes; leaf tools may be read-only.

## Sources

[Google review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Select actual applicability and version through the [criteria register](../review_criteria.md); general guidance does not replace project requirements.
