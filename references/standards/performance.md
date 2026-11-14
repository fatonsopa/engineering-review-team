# Performance review technical standard

## Purpose and scope

The Performance Reviewer assesses latency, throughput, resource efficiency and the evidence supporting them across the assigned user journey or workload. Scope includes algorithmic cost, resource lifetime, I/O, caches, concurrency, overload, shared-resource fairness, frontend delivery and rendering. It inspects captured implementation, configuration, profiles and measurements; it does not execute the target, collect profiles or run benchmarks.

The [Performance Policy (POL)](../policies/performance.md) governs judgment. Team-owned [Review scope and criteria](../intent_context.md#review-scope-and-criteria) determines effective project criteria, replacements and waivers. The shared [Review Technical Standard (STD)](../review_standard.md) owns evidence, findings and coverage records. These controls add no separate authority process or report schema.

`PERF-01`–`PERF-12` are package controls. Their examples are hypothetical, and a safe counterpart is safe only for its stated conditions. Check actual runtime, library, browser, provider and tool versions before relying on their behavior.

## Definitions

- A **workload** specifies the work presented to a system: operation mix, inputs, arrival pattern, concurrency and duration, with relevant users, tenants and environments.
- **Latency** measures elapsed time between identified start and end events. **Throughput** measures completed work per unit time; distinguish successful useful work from attempts, errors and rejections.
- A **performance budget** is an adopted limit with a metric, unit, population and applicable conditions. A recommendation or tool score is not automatically a project budget.
- A **percentile** describes a point in a measured distribution. A **tail** is its slow end; neither an average nor an average of instance percentiles establishes the combined tail.
- **Saturation** occurs when demand approaches or exceeds a constraining resource's usable capacity. **Headroom** is capacity available beyond the stated demand under the relevant operating conditions.
- **Backpressure** slows or limits producers when consumers cannot keep up. **Fairness** preserves the project's intended allocation and progress among competing workloads; it does not necessarily mean equal shares.

## Principles

Start with the affected outcome and reachable workload. Preserve correctness, authorization, freshness, durability and accessibility while assessing speed or cost. An optimization that violates those properties is not an acceptable performance improvement.

Separate measured results, analytical bounds and hypotheses. Source inspection can demonstrate an unbounded retention path or deadlock schedule without establishing elapsed time. A profile can locate work without proving that it causes the reported delay. Unknown workloads, budgets and environments remain unknown.

Assess the complete relevant path. Moving work to a queue, worker, client or dependency may shift latency and cost rather than remove them. Prefer a bounded design that meets actual needs over extra caching, parallelism or infrastructure without a supported benefit.

## Applicability and phases

Select controls by the changed behavior, workload and consequences. Read each selected control in full; retain material exclusions and missing inputs through the shared contract. A narrow change need not become an audit of every performance mechanism.

| Phase | Relevant depth |
| --- | --- |
| Foundation | Inspect reachable cost, resource ownership and responsiveness for actual inputs. A bounded local utility may need no service telemetry, tenant quotas, cache, CDN or load exercise. |
| Production launch | Assess affected user journeys, supported environments, dependencies and resource bounds against established expectations. Seek focused evidence where an important conclusion depends on measurement. |
| Growth | Examine changing input sizes, operation mix, bursts, tails, contention, queues, tenant competition and capacity where relevant. |
| Advanced scale or criticality | Extend analysis to degraded capacity, failure overlap, long-running workloads and stronger assurance when the architecture or consequences require it. |

Small size does not waive an active risk. A low-volume service handling sensitive exports still needs bounded work and protected caches. A local script reading a small trusted file synchronously may be suitable. No phase creates a universal latency target, bundle limit, benchmark suite, distributed cache, autoscaler or dedicated performance document.

## Rules

### PERF-01 — Workload and performance criteria

Performance judgments must identify the operation, relevant workload and effective criterion before claiming a regression or sufficient capacity.

- Establish input sizes, data distribution, operation mix, arrival pattern, concurrency, duration and relevant bursts. Include large tenants, cold starts or background work when they affect the changed path.
- Locate adopted latency, throughput, memory, transfer or cost budgets and their units, population, percentile and window. Distinguish an end-to-end budget from one component's allowance.
- Match the environment to the conclusion: hardware or resource allocation, runtime/build, dependency placement, browser/device, network and cache state as relevant.
- When essential facts are missing, identify the conclusion they prevent and request focused evidence through the lead. A missing budget does not erase a demonstrated leak or progress failure, and it does not authorize an invented target.

A single small-input timing cannot establish capacity for an import whose supported population is much larger. An explicitly bounded local operation can be assessed within that bound without extrapolating to a public service.

### PERF-02 — Profiles, measurements and comparisons

Measured claims about a bottleneck, improvement or regression must identify observations that represent the claim and distinguish material differences from measurement artifacts. Source analysis may establish structural cost or progress risks without claiming observed timing.

- Inspect supplied artifact/revision identity, inputs, configuration, tool/version, timing boundaries, warm-up, cache state, run duration and repetitions. Check whether compared runs perform equivalent useful work and include relevant setup or completion costs.
- Read the appropriate evidence for CPU work, allocation/retention, waiting, locks, I/O and end-to-end time. A CPU profile does not measure time spent waiting; sampling gaps and instrumentation overhead can change the interpretation.
- Check offered versus achieved load, generator capacity, failures, timeouts, dropped work and queued work. A closed workload that waits for completion can reduce arrivals when the service slows; it cannot by itself establish behavior under independently arriving traffic.
- Inspect distributions, sample counts, variability and aggregation. Do not average per-instance percentiles into a service percentile; histogram boundaries, sampling and the represented window limit precision.
- For regression evidence, preserve the baseline and changed result under comparable conditions. Microbenchmarks and synthetic tests establish their measured scope, not whole-system or real-user performance.

Calling a release faster because its reported requests omit timed-out operations is misleading. A comparison with the same workload, disclosed failures and variability, and an appropriate measurement boundary can support a bounded improvement claim. In Go, CPU, heap and blocking profiles answer different questions and simultaneous diagnostics can interfere; select evidence for the actual runtime and collection mode.

### PERF-03 — Algorithmic cost and input growth

Reachable computation and intermediate state must fit the supported input range and relevant resource constraints.

- Identify the variables that grow: records, bytes, nesting, graph edges, candidates, fan-out and repeated passes. Trace work across helpers, serializers and callbacks rather than counting visible loop nesting alone.
- Derive time and space growth where possible, including recursion depth, copying, repeated sorting/scanning, conversions and materialized results. Relate the result to reachable inputs and the affected execution context.
- Examine repeated subproblems before proposing memoization. Account for cache keys, invalidation, memory retention and the cost of maintaining an index or lookup structure.
- Preserve result ordering, duplicates, precision and other required semantics when comparing alternatives. Identify the needed measurement when constant factors or practical input sizes determine the choice.

Repeatedly scanning a growing catalogue for each imported record can create multiplicative work. Building a correctly keyed lookup once may reduce that work at a memory cost. Two bounded loops over a tiny fixed domain, or recursion that visits each tree node once with acceptable depth, do not require a rewrite or memoization merely because of their syntax.

### PERF-04 — Allocation, retention and resource lifetime

Resources must have an owner and a bounded useful lifetime through normal completion, failure, cancellation and shutdown.

- Trace allocation/acquisition, ownership transfer and release for memory, files, sockets, streams, connections, subscriptions, event listeners, timers and asynchronous tasks. Check repeat mount/reconnect/retry paths that can accumulate retained objects or continuing work.
- Inspect framework-managed lifetimes before demanding explicit cleanup. Garbage collection can reclaim unreachable managed objects; it does not guarantee timely release of every external resource or stop a still-referenced timer/task.
- Distinguish retained live data, peak buffers, allocation churn, garbage-collection cost and process memory. A rising process-memory sample alone does not prove a leak; compare repeated completed lifecycles and retaining paths where supplied evidence permits.
- Account for concurrent operations, copies, buffered results and cache entries when assessing peak memory. A per-item limit or bounded worker count need not bound all pending work.

A component that registers another recurring listener on each visit while a long-lived emitter retains every old listener can accumulate work and memory. A framework subscription disposed at the correct lifecycle boundary, with no surviving owner, can satisfy the check without manual deallocation. Code owns implementation-level cleanup correctness; Performance retains the resource and workload consequence.

### PERF-05 — I/O and transferred data

I/O and payload handling must avoid supported resource or responsiveness failures while preserving the required data and completion semantics.

- Trace blocking file, network and storage calls in their execution context. Blocking on a shared event loop or UI thread differs from bounded synchronous work in a dedicated batch process.
- Inspect request counts, serialized dependency calls, connection reuse, payload projection, pagination, batching and streaming. Include serialization/parsing, buffering, connection setup and transfer costs where relevant.
- Check whether batching or parallel requests reduce round trips at the expense of memory, first-result latency, downstream load or correctness. Route database query plans and index choices to Database while retaining end-to-end costs.
- For compression, inspect actual content negotiation and response encoding, intermediary behavior, compressibility, CPU cost and compatibility. Already-compressed or very small responses may not benefit. Sensitive dynamic responses need Security assessment of compression-related exposure.

Buffering an unbounded export before sending its first byte can exhaust memory; a bounded stream that respects its consumer and closes on failure can avoid that failure. Missing application compression middleware is not proof of uncompressed delivery when a proxy handles it. In Node.js, an asynchronous function can still perform blocking CPU work, and some asynchronous APIs share a worker pool; inspect the actual API and runtime version.

### PERF-06 — Caching and invalidation

Where a cache exists or is proposed, its benefit must be weighed against freshness, isolation, memory and dependency behavior on misses or failure.

- Trace keys through tenant/user identity, authorization-sensitive state, representation, locale and relevant version/input dimensions. Verify hits preserve the required visibility and freshness semantics; a high hit rate cannot justify wrong results.
- Inspect invalidation, expiry, revalidation, negative results, write/read races and mixed-version values. Establish which stale results are permitted and for how long from the actual contract.
- Check size/eviction bounds, hot keys, simultaneous refresh, cold start and unavailable-cache behavior. Include miss amplification and backend protection when the service depends on a warm cache.
- For HTTP, inspect effective origin, browser and intermediary directives, validators and `Vary` behavior. An unqualified `no-cache` response directive requires successful validation before reuse; it does not prohibit storage. An unqualified `private` response directive prohibits shared-cache storage and does not itself encrypt content. Field-qualified directives have narrower semantics; inspect the actual header.
- Compare hit rate, lookup/serialization cost and invalidation complexity with the uncached path where evidence is available. Do not require a cache when reuse is negligible or freshness requirements make it unsuitable.

A cache keyed only by object ID can return another tenant's representation, and concurrent misses can overwhelm the source despite good steady-state timings. Correctly scoped keys and an appropriate refresh/admission mechanism can preserve the contract. A deliberate uncached path can also be suitable. Python's `lru_cache` retains arguments and results until eviction or clearing; thread-safe cache bookkeeping does not guarantee only one execution for simultaneous misses.

### PERF-07 — Concurrency, locks and progress

Concurrency must preserve required correctness and progress within the available execution and dependency capacity.

- Trace tasks/threads, shared state, locks, pool acquisition and blocking waits. Construct a relevant schedule for races, cyclic waits, pool exhaustion, starvation or a task waiting on work that needs its occupied executor.
- Inspect lock scope/order, time spent holding locks, I/O under locks and competing priorities. Necessary synchronization is not a defect; connect contention to the workload and consequence before recommending a change.
- Compare worker/pool counts with CPU, memory, downstream connections and scheduling overhead. More parallelism can increase contention, context switching, copying or dependency pressure.
- Check task cancellation and completion ownership; timing out a caller does not establish that the worker or remote operation stopped. Coordinate correctness findings with Code and database locks with Database.

A Python `ThreadPoolExecutor` worker waiting synchronously for a child submitted to the same single-worker pool cannot make progress. A design that leaves execution capacity for dependencies or composes completion without that wait can avoid this schedule. Match executor/runtime semantics to the installed version; do not infer application atomicity or performance from a language's global lock or an `async` declaration.

### PERF-08 — Queues, backpressure and repeated work

Accepted and repeated work must remain bounded enough to preserve the required progress and recovery behavior under slow consumers or dependencies.

- Follow admission through active work, waiting queues and buffers. Inspect bounds in items and bytes where item sizes vary, queue age, producer behavior, rejection and the required handling of rejected or expired work.
- Trace stream demand and cancellation across all stages, including hidden buffering and a slow or disconnected consumer. For Node.js streams, `highWaterMark` is a buffering threshold, not a strict total-memory limit; respect the selected implementation's backpressure behavior.
- Trace the end-to-end deadline, timeout coverage, retryable outcomes, attempt limits, backoff and jitter. Account for retries at multiple layers, fan-out and work that continues after its result is no longer useful.
- Check overload recovery, not only initial acceptance. A bounded queue can still be too slow for its contract; a durable backlog may be appropriate for work that can wait. Shedding or degradation must preserve the actual work contract.

Putting every input into an unbounded pending-future list while limiting active workers does not bound retained work. A bounded producer/consumer path with accepted rejection or deferral behavior can. Python 3.14 added `Executor.map(buffersize=...)`; older versions and the default unbounded collection behavior need another assessment. No retry or cancellation setting proves that a remote side effect was undone.

### PERF-09 — Saturation, tails and capacity

Capacity conclusions must connect usable resources, demand and service outcomes under the operating conditions represented by the evidence.

- Inspect latency distributions alongside useful throughput, errors, queue age and constrained resources. Consider CPU, memory, I/O, bandwidth, handles, pool slots and provider quotas as relevant; low average CPU does not exclude a saturated single thread or dependency.
- Examine bursts, hot partitions, long-running work, cold caches/startup and degraded capacity when the actual operating requirement includes them. Do not extrapolate linear scaling through a shared bottleneck without evidence.
- Compare configured resource limits with observed throttling, termination, waits or other effective constraints. Distinguish reserved resources and nominal pool size from demonstrated capacity.
- Where capacity or cost planning is relevant, state headroom assumptions, growth evidence, scale-out delay and downstream ceilings. Request representative evidence for an unsupported commitment; do not invent a fixed utilization or spare-capacity percentage.

A service can have acceptable average latency while a large export occupies the only execution slot and stalls interactive work. A bounded workload with evidence for its relevant tail and recovery behavior can meet its contract without autoscaling. DevOps owns deployment/autoscaling settings and operating actions; Performance assesses the workload and measurement argument.

### PERF-10 — Tenant fairness and attributable cost

Where workloads share finite resources, review whether one tenant, request class or background job can prevent the intended progress of others.

- Identify trusted workload identity and shared bottlenecks, including caches, queues, connection pools, storage and external quotas. Inspect enforcement across replicas and background paths, not just one ingress handler.
- Compare request counts with actual cost: input/output bytes, CPU time, execution duration, fan-out or paid operations as relevant. Equal request rates do not imply equal resource use.
- Inspect admission, scheduling, quotas, isolation or other protections for the project's fairness contract. Include legitimate bursts, large tenants and lower-priority work that must eventually progress; no particular quota algorithm or dedicated infrastructure is universal.
- Where per-tenant efficiency or cost claims matter, inspect the allocation method and its uncertainty. Control telemetry cardinality and sensitive identifiers rather than prescribing an unbounded metric label for every tenant.

A bulk tenant able to occupy every shared worker indefinitely can starve an otherwise legitimate small tenant even when total average utilization appears low. Bounded work with scheduling or isolation that preserves the stated allocation can be suitable. Rate limits alone do not prove fairness when operation costs differ. Security owns identity and abuse judgments; financial billing correctness remains with its application and domain owners.

### PERF-11 — Frontend assets and delivery

For affected browser journeys, delivered resources must support the required content and interactions within adopted budgets and supported environments.

- Inspect actual production output and supplied network evidence for initial and later-route JavaScript/CSS, duplicate dependencies, fonts, images, media and third-party code. Distinguish source size, compressed transfer size and parse/execute cost.
- Trace resource discovery, priorities and dependency waterfalls. Evaluate dynamic imports and lazy loading at the point users need the feature; extra chunks can move delay to a later interaction.
- Check image dimensions/formats, responsive selection, font loading and delivery cache behavior against intended quality and supported clients. A CDN, particular format or universal bundle threshold is not mandatory.
- Compare initial and repeat visits, device/network conditions and route coverage with the actual budget. Missing bundle or waterfall evidence limits a measured-size or loading claim.

Deferring the page's main image until lazy-loading checks run can worsen Largest Contentful Paint even if it lowers initial request counts. Keeping the critical resource discoverable while deferring a nonessential editor until needed can be appropriate. Check the real dependency graph: a dynamic import does not establish that shared eager code was removed.

### PERF-12 — Rendering and interaction

Frontend performance review must cover the work between a user's action and a usable visible result, including relevant behavior after initial load.

- Trace event handling, state updates, expensive computation, hydration, rendering, layout and paint in supplied profiles. Inspect repeated work, long tasks, synchronous layout reads after writes, large DOM updates and unnecessary retained UI state where they affect the journey.
- Assess proposed scheduling, workers, memoization or virtualization for total work, communication cost, stale results, focus/keyboard behavior and accessible content. Faster rendering cannot justify breaking the interaction contract.
- Interpret loading, interaction and visual-stability metrics according to their definitions and collection version. For Core Web Vitals, distinguish LCP, INP and CLS; older FID evidence is not equivalent to INP, and a navigation-only Lighthouse TBT result is a diagnostic proxy rather than a measured INP value.
- Keep lab and field populations separate, including page versus origin, devices, networks, visits and interactions. A trace from one desktop session does not prove all supported devices are responsive; unavailable field data does not by itself establish poor performance.

A loop that alternates style writes and layout reads across a growing list can repeatedly force layout. Grouping reads and writes may remove that repetition when it preserves the required result. A short static page without interactive controls need not acquire virtualization or a worker. Design owns interaction/accessibility requirements; Performance supplies timing and rendering evidence.

## Verification

Apply the checks beside each selected rule to located code, configuration and supplied evidence. Relate any failure to a concrete reachable condition and consequence, and consider a legitimate case that should remain valid. A missing measurement can prevent a capacity conclusion while a demonstrated retention or wait cycle still supports a defect.

Use captured profiles, traces, build reports, request/queue measurements and existing benchmark or field results. Identify their provenance and limits. Request additional collection or execution through the lead; this reviewer does not launch applications, run benchmarks/load tests, attach profilers, query live telemetry or alter settings. A proposed experiment, hypothetical example or document check is not a runtime result.

## Responsibilities and exceptions

Performance owns workload-wide efficiency, bottleneck and measurement interpretation. Code owns application correctness and resource/concurrency mechanisms; Database owns query-plan, index and database-lock analysis; DevOps owns deployment and operational configuration; Testing owns verification quality; Architecture owns structural tradeoffs. Preserve the observed consequence and use the lead for cross-domain coordination rather than claiming an unperformed specialist assessment.

The lead resolves effective criteria, missing material context, conflicts and exceptions under team-owned guidance. Apply an authorized replacement or waiver within its actual scope and retain unresolved consequences. Vendor advice does not establish project approval, and a faster result cannot silently replace a correctness, security or accessibility requirement.

## Ownership, review, and related policy

The Engineering Review Team maintains this Technical Standard (STD) under the [Performance Policy (POL)](../policies/performance.md). Review affected controls when supported runtime/tool semantics, project needs, false positives or newly demonstrated failure modes change. Preserve stable control identities and record material scope changes in package maintenance.

## Research reference

[Sources and control mappings](../research/performance.md) support source verification and maintenance. Load that record only when needed; keep behavior-affecting qualifications beside the checks used during routine review.
