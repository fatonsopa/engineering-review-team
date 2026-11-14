# DevOps review technical standard

## Contents

- [Purpose and scope](#purpose-and-scope)
- [Definitions](#definitions)
- [Principles](#principles)
- [Applicability and phases](#applicability-and-phases)
- [Rules](#rules)
- [Delivery and infrastructure](#delivery-and-infrastructure)
- [DEVOPS-01 — Pipeline trust and privileges](#devops-01--pipeline-trust-and-privileges)
- [DEVOPS-02 — Pipeline execution and caches](#devops-02--pipeline-execution-and-caches)
- [DEVOPS-03 — Artifact identity and provenance](#devops-03--artifact-identity-and-provenance)
- [DEVOPS-04 — Infrastructure state and drift](#devops-04--infrastructure-state-and-drift)
- [DEVOPS-05 — Configuration and secrets](#devops-05--configuration-and-secrets)
- [DEVOPS-06 — Identity and network access](#devops-06--identity-and-network-access)
- [DEVOPS-07 — Container isolation and resources](#devops-07--container-isolation-and-resources)
- [DEVOPS-08 — Release compatibility and recovery](#devops-08--release-compatibility-and-recovery)
- [Production readiness](#production-readiness)
- [DEVOPS-09 — Operating needs and service objectives](#devops-09--operating-needs-and-service-objectives)
- [DEVOPS-10 — Startup, readiness and shutdown](#devops-10--startup-readiness-and-shutdown)
- [DEVOPS-11 — Telemetry and actionable alerts](#devops-11--telemetry-and-actionable-alerts)
- [DEVOPS-12 — Dependency failures and job delivery](#devops-12--dependency-failures-and-job-delivery)
- [DEVOPS-13 — Capacity, backpressure and resource lifecycle](#devops-13--capacity-backpressure-and-resource-lifecycle)
- [DEVOPS-14 — Backup, restoration and failover](#devops-14--backup-restoration-and-failover)
- [DEVOPS-15 — Incident and recovery ownership](#devops-15--incident-and-recovery-ownership)
- [DEVOPS-16 — Fleet and maintenance automation](#devops-16--fleet-and-maintenance-automation)
- [Verification](#verification)
- [Responsibilities and exceptions](#responsibilities-and-exceptions)
- [Ownership, review, and related policy](#ownership-review-and-related-policy)

## Purpose and scope

The DevOps Reviewer assesses delivery, infrastructure and the ability to operate and recover the assigned system. It inspects supplied configuration, scripts, implementation paths and evidence. Delivery/infrastructure and production readiness are distinct work areas; a valid configuration does not establish that a service can detect or recover from failure.

The [DevOps Policy (POL)](../policies/devops.md) governs judgment. Team-owned [Review scope and criteria](../intent_context.md#review-scope-and-criteria) establishes applicable project rules, defaults, replacements and waivers. The shared [Review Technical Standard (STD)](../review_standard.md) owns evidence and findings. This document adds no separate document catalog or report schema.

`DEVOPS-01`–`DEVOPS-16` are package-designed controls. Sources support selected engineering methods and product behavior; they do not prescribe this reviewer organization or certify a project. Examples are hypothetical. Check the actual provider, runtime, deployment model and versions before applying vendor-specific mechanisms.

## Definitions

- An **artifact** is an identified build output. **Provenance** records how it was produced; neither a signature nor provenance establishes that its contents are safe.
- **Infrastructure state** records managed resources. **Drift** is a relevant difference between intended configuration, recorded state and the actual environment.
- **Readiness** means able to perform the required work. **Liveness** determines whether restarting a process is an appropriate response; **startup** covers initialization.
- A **service level indicator** measures a service outcome. A **service level objective** sets its target and measurement window.
- A **recovery time objective** bounds acceptable recovery time. A **recovery point objective** bounds acceptable data loss measured in time.
- **Backpressure** limits accepted work when downstream capacity is insufficient. **Idempotency** permits repetition without repeating the protected effect.

## Principles

Start with the operating condition: users and workload, exposure, sensitive or durable state, dependencies, deployment sequence and failure consequences. Do not invent traffic, availability, recovery or cost targets. A platform feature, checked configuration or successful build is evidence for its own claim, not proof of production readiness.

Trace failure through boundaries: a build into its release artifact, a request through its dependencies, a worker through durable completion, and an incident through usable recovery. Assess explicit limits and recovery behavior before proposing additional infrastructure.

Review only the assigned scope and relevant dependencies. Missing information stays unknown; absence requires a bounded search. A tool's presence cannot substitute for checking its effective configuration and evidence.

## Applicability and phases

Read the control list, select relevant controls and read them in full. Record brief reasons for material exclusions in the shared return. Do not expand every narrow change into a complete platform audit. The lead supplies relevant project criteria through the shared document map; a standalone service, threat, deployment or recovery document is not a prerequisite.

| Phase | Relevant depth |
| --- | --- |
| Foundation | Trustworthy builds and access, understandable configuration, recoverable local state and failure handling where present. A local tool may need no hosted infrastructure or continuous monitoring. |
| Production launch | Assess actual exposure, deployment compatibility, service detection, recovery and accountable support for affected user journeys. |
| Growth | Add shared-resource limits, operational capacity, tenant/fleet consistency and automation where workload or repeated changes warrant them. |
| Advanced scale or criticality | Examine regional recovery, failure isolation and stronger assurance when the topology, exposure or adopted commitments require them. |

Phase names guide depth; they do not waive obligations. A small service processing sensitive records needs access protection and appropriate recovery. A local disposable-data utility may reasonably exclude regional failover, on-call rotations and backup infrastructure. Neither Kubernetes nor a separate service-objective document, 24/7 support, distributed deployment or load exercise is a universal requirement. Explicitly adopted obligations remain binding at any size.

For managed, serverless or platform-hosted services, establish which controls the provider owns and which remain with the project. Review the actual configuration, guarantees and supplied evidence; do not require customer-managed host or orchestration controls that the service does not expose.

## Rules

Use the controls below to assess the relevant work areas separately. Keep supported defects, unresolved criteria, evidence limits and optional improvements distinct. A shorter design that satisfies the actual requirement is acceptable.

## Delivery and infrastructure

### DEVOPS-01 — Pipeline trust and privileges

Untrusted inputs and execution must not gain release authority or access beyond the pipeline's intended trust boundary.

- Trace triggers, checked-out revisions, reusable workflows, scripts and runner reuse. Inspect pull-request code and metadata, downloaded content and artifacts that cross into privileged jobs.
- Check token permissions, environment gates and cloud trust conditions for the actual job, repository and destination. Verify issuer/audience validation and restrict the authorized workload through provider-supported subject claims or equivalent claim/attribute conditions. Short-lived credentials alone do not establish the correct scope.
- Inspect interpolation of untrusted strings into shell or generated code. Keep data separate from executable syntax, including in scripts invoked by actions.
- Check whether a compromised job can retain access through a self-hosted runner, shared workspace, credential or downstream artifact. Verify restrictions from supplied configuration; do not assume runner isolation.

For example, executing a fork's code in a job with production credentials crosses the boundary. A privileged job that processes only constrained trusted inputs needs a different assessment. Apply the corresponding trust controls to the actual platform.

### DEVOPS-02 — Pipeline execution and caches

Required checks must govern the correct artifact, and failure or cancellation must not silently become release success.

- Trace job dependencies, conditions, change filters, exit handling and required gates. Inspect optional/experimental jobs separately from mandatory checks; review skipped, timed-out and cancelled outcomes.
- Check concurrency controls for conflicting deployments, resource use and cleanup. Parallelize only independent work when the benefit and isolation justify it; sequential pipelines are not inherently defective.
- When caching is used, inspect keys, inputs, tool versions, trust boundaries, invalidation and behavior without a cache. Keep secrets out of caches; do not trust restored executable content solely because a cache hit occurred.
- Distinguish reusable caches from outputs retained for release or evidence. Evaluate pipeline duration and resource waste against an actual concern; caching and maximum parallelism are not universal gates.

An intentionally optional experimental job may fail without blocking release. A required security check hidden behind unconditional success cannot support the gate.

### DEVOPS-03 — Artifact identity and provenance

The release must identify its actual inputs and output, with integrity evidence proportionate to its trust boundary.

- Trace source revision, dependencies, toolchain and build parameters to the artifact tested and promoted. Detect mutable references or rebuilding between approval and deployment that can change the result.
- Inspect dependency/action/base-image references and their update process. A pinned digest identifies content; it neither removes vulnerabilities nor supplies future fixes.
- Where provenance, signatures or attestations are required, inspect the recorded digest, trusted issuer/build identity and verification at consumption. A generated statement without enforced verification does not establish the claimed boundary.
- Check artifact storage permissions, retention and access to a usable prior release. Assess reproducibility or stronger build isolation only when required or material to the identified risk.

A digest-pinned image with a reviewed refresh process can preserve identity without freezing updates indefinitely. Do not require a SLSA level for every local build.

### DEVOPS-04 — Infrastructure state and drift

Infrastructure changes must preserve the correct state, coordination and intended environment.

- Inspect resource ownership, account/region/workspace selection, provider versions and destructive/replacement effects in supplied changes and existing plan evidence. Check that the reviewed inputs correspond to the proposed deployment.
- For stateful infrastructure tools, inspect access, encryption, retention/recovery and sensitive values in state or saved plans. Output redaction alone does not protect stored secrets.
- Check how competing writers are prevented and stale locks recovered. Verify the selected backend's actual locking support; remote storage alone does not establish locking or security.
- Inspect evidence of drift detection and reconciliation, including emergency changes. Distinguish accepting observed state from restoring intended configuration; require an explicit decision where the difference matters.

Protected local state can be suitable for an isolated single-operator workflow. Shared writers and sensitive production state need stronger coordination and protection. This reviewer inspects supplied evidence and does not run a plan, refresh or state command.

### DEVOPS-05 — Configuration and secrets

Configuration must select the intended environment, reject unsafe values and protect sensitive material throughout its lifecycle.

- Trace defaults, precedence, generated values and overrides into the running application. Check required values, types, ranges and startup behavior when configuration is missing or invalid.
- Keep environment-specific values configurable where needed for deployment. Inspect meaningful differences between environments; identical files do not establish equivalent behavior, and deliberate size differences are not defects by themselves.
- Trace secrets through storage, delivery, rotation, expiry and revocation. Inspect repository history supplied for the task, logs, build arguments, layers, artifacts and diagnostic output for exposure; avoid reproducing secret values in findings.
- Check whether live configuration changes are atomic or compatible with active work and whether a failed change can be understood and reversed safely.

Environment variables are one configuration mechanism, not a secret boundary by themselves. A secret store also needs appropriate access and retrieval behavior.

### DEVOPS-06 — Identity and network access

Infrastructure access and connectivity must match the intended principals, resources and traffic paths.

- Inspect cloud roles, service accounts, human access and delegated trust for necessary actions, resource scope and conditions. Examine unused privileges and credential lifetime where relevant; identify the actual excessive access rather than demanding an unexplained role redesign.
- Trace public entry points, administrative interfaces, storage, internal services and outbound dependencies through routing, security groups, peering, firewalls and ingress/egress rules.
- Check transport protection and effective enforcement at the affected boundary. For orchestrated networks, inspect whether the deployed network implementation supports the declared policy.
- Distinguish intentional public service endpoints from unintended exposure of management or private data paths. Inspect dependency traffic and recovery access so restrictions do not make the service or its recovery unusable.

A public API is not a defect merely because it is a backend. Unrestricted administrative access can be a defect even in a small service. Security owns threat/exploit judgments when deeper assessment is required.

### DEVOPS-07 — Container isolation and resources

Container settings must provide appropriate isolation and resource behavior for the actual runtime and workload.

- Inspect image contents, runtime identity, capabilities, host mounts, privileged modes, writable paths and access to the container engine. Identify the privilege required by the workload before recommending a restriction.
- Distinguish a non-root process from a rootless daemon and user-namespace isolation. Assess supported alternatives and compensating controls; do not require a particular container platform or mode universally.
- For scheduled workloads, inspect CPU/memory requests, limits, storage and process constraints against realistic use. Check throttling, out-of-memory termination, scheduling and restart consequences; arbitrary exact limits can harm availability.
- Check image lifecycle and runtime compatibility, including supplied evidence for the actual platform. Route image identity to DEVOPS-03 and health/shutdown behavior to DEVOPS-10.

A Kubernetes CPU request influences placement; a CPU limit can throttle, while memory enforcement has different failure behavior. Neither proves capacity. Selected limits remain project-specific.

### DEVOPS-08 — Release compatibility and recovery

A release must account for mixed versions, partial completion and the path to a usable service after failure.

- Trace code, configuration, database/schema, message and external-contract changes through old/new version overlap. Check migration order, locks, compatibility windows and irreversible effects with the relevant owners.
- Inspect release gates, artifact identity, destination, health evaluation and stop conditions. Where progressive rollout is used, check whether the exposed population and observation period can reveal the relevant failure.
- Assess rollback, roll-forward, compensation or reconciliation against the resulting state. A previous binary does not undo destructive data changes or already-issued external effects.
- Inspect ownership and usable evidence for release failure, including interrupted deployment and concurrent changes. A manual reversible procedure can suffice for a small system when it meets the actual requirement.

A canary with no relevant signal cannot establish safe expansion. A planned maintenance release can be appropriate when its interruption is explicitly accepted.

## Production readiness

### DEVOPS-09 — Operating needs and service objectives

Readiness judgments must use the actual service outcomes and operating conditions.

- Establish user journeys, operating hours, workload shape, dependency assumptions and tolerated interruption or data loss from supplied criteria. Preserve unknowns instead of inventing targets.
- Where objectives are adopted, check the event population, success definition, measurement window, target and owner. Inspect whether instrumentation covers the user outcome rather than only a healthy internal component.
- Compare readiness evidence with those commitments and the changed behavior. A provider's availability claim does not establish the application's result.
- If formal objectives are absent, assess concrete risks supported by the scope and evidence. A missing standalone document is not automatically a defect; request essential ambiguity through the lead.

A one-person local utility needs different operating evidence from a public payment service, even if both have little traffic.

### DEVOPS-10 — Startup, readiness and shutdown

The service lifecycle must admit work only when it can handle it and stop without violating its work or state contract.

- Trace initialization, required dependencies, invalid configuration and readiness into traffic or job admission. Check warm-up and recovery behavior after startup failure.
- Inspect health checks for what they observe and what failure triggers. Do not treat liveness, readiness and startup checks as interchangeable or require all three when the runtime does not need them.
- Trace termination signals, grace periods, draining, in-flight work and final cleanup. Inspect whether rollout/restart timing can interrupt protected completion or leave stale ownership.
- Check that an unavailable dependency does not create an inappropriate restart loop or admit work that cannot succeed. Evaluate the actual service behavior; not every dependency failure requires stopping all traffic.

A process may not need a liveness probe if it reliably exits on the relevant fatal failure. A readiness check does not prove graceful shutdown. Apply the corresponding lifecycle for other runtimes.

### DEVOPS-11 — Telemetry and actionable alerts

The service must expose enough evidence to detect and diagnose material failures within its support commitments.

- Trace important outcomes and failure paths to useful logs, metrics or traces. Inspect correlation, timestamps, version/context and relevant latency, error, demand and saturation signals without requiring every telemetry type.
- Check sensitive-data redaction, access, retention, sampling and cardinality where they affect privacy, diagnosis or cost. A log statement alone does not establish that a responder can retrieve it.
- Inspect alert conditions, routing, response ownership and expected action. Distinguish urgent user impact from information that can wait; evaluate duplicate or noisy pages against their actual consequence.
- Check monitoring gaps during deployment, dependency failure and recovery, including whether the monitoring path depends on the failed service.

A small tool can surface actionable failure to its operator without a pager service. An alert with no reachable owner cannot support a promised response. Exact tools and support hours come from project criteria.

### DEVOPS-12 — Dependency failures and job delivery

Dependency handling must bound failure amplification and preserve the required work outcome.

- Trace deadlines, connection/request timeouts and cancellation across caller, proxy, worker and dependency. Check actual coverage of connection setup and queued work, not merely the presence of a timeout option.
- Inspect retryable failures, total attempts, backoff, jitter and combined retry layers. Assess side effects and idempotency before treating a timeout as safe to retry.
- Trace job acceptance, durable progress, acknowledgement, redelivery and reconciliation through termination and dependency failure. Inspect poison-message handling or dead-letter ownership when relevant.
- Check fallback and degraded behavior against the contract, including stale data and partial success. Route application retry/cancellation correctness to Code and persistence/transaction guarantees to Database; retain the operational failure finding and handoff.

Acknowledging a job before its required durable commit can lose work on termination. Committing an idempotent update before acknowledgement can tolerate redelivery only when broker/storage guarantees support it.

### DEVOPS-13 — Capacity, backpressure and resource lifecycle

Accepted work and resource use must remain bounded enough to meet the actual operating requirement and recover from overload.

- Inspect queues, admission, concurrency, connection pools and dependency quotas against workload shape and fan-out. Check rejection, shedding, fairness and recovery when bounds are reached.
- Trace files, sockets, connections, tasks and other acquired resources through success, failure, cancellation and shutdown. Request Code review for implementation-level ownership or cleanup defects; preserve their operational consequence.
- Check capacity assumptions, autoscaling signals, startup delay and downstream limits where present. Scaling workers can overload storage or another dependency instead of restoring service.
- Distinguish measured performance from an analytical risk. Route workload measurement, bottleneck analysis and algorithmic efficiency to Performance, and query/locking behavior to Database. Recommend focused evidence without running a load exercise.

An unbounded queue in a constrained service can exhaust memory even at modest traffic. Fixed concurrency with a bounded queue and accepted rejection behavior can be sufficient without autoscaling. No benchmark result may be inferred from configuration.

### DEVOPS-14 — Backup, restoration and failover

Recovery must restore the required service and usable state within adopted loss and interruption limits.

- Establish which durable data and configuration need backup, retention or reproducibility. Inspect access, encryption keys, deletion protection and failure-domain independence according to the actual loss scenario.
- Examine supplied restore evidence for data usability, dependencies and elapsed recovery, not only a successful backup or completed restore job. Keep missing execution evidence distinct from a demonstrated failed restore.
- Where failover is part of the design, inspect capacity, routing, credentials, replication lag, write ownership, reconciliation and return to normal operation. Regional redundancy is conditional, not a universal requirement.
- Coordinate data integrity, engine recovery and database backup mechanics with Database; DevOps owns the service recovery sequence and operational access. Record an unresolved handoff rather than assuming storage availability establishes recovery.

A disposable local cache may need regeneration rather than backup. A backup requiring a key lost with the failed environment may be unusable.

### DEVOPS-15 — Incident and recovery ownership

Material operational failures need a response that the responsible people can perform under the actual support arrangement.

- Identify who detects, triages, mitigates and communicates each relevant failure, including escalation and unavailable primary responders when required by support commitments.
- Inspect recovery instructions for prerequisites, access, decision points, verification and stop conditions. Check dependencies on unavailable infrastructure and dangerous or irreversible actions.
- Examine supplied exercises or incident evidence where justified by risk or commitments. Keep written procedures, completed exercises and observed recovery distinct; propose missing checks without executing them.
- Inspect how material incidents feed necessary corrections into delivery, detection and recovery. Avoid requiring a large incident organization or ceremony for a small operator-run service.

One accountable maintainer and a usable recovery procedure may suffice for a limited-hours application. A promised continuous response without an available responder does not. Exact staffing and response periods belong to the project.

### DEVOPS-16 — Fleet and maintenance automation

Recurring maintenance must preserve service operation, including for a single instance. Where automation affects multiple tenants, instances or regions, it must also preserve those boundaries and make partial progress recoverable.

- Inspect target selection, tenant/environment identity, permissions and blast radius for provisioning, upgrades, configuration changes and decommissioning.
- Check checkpoints, retry safety, stop/resume behavior, version compatibility and reconciliation after partial completion. Coordinate tenant/data consequences with Security and Database.
- Inspect scheduled maintenance, certificate/credential expiry and dependency/runtime updates where the service relies on them. Check ownership, detection and recovery when renewal or maintenance fails, including provider-managed or controlled manual renewal.
- Evaluate automation against actual repetition, error risk and growth. A controlled manual operation can be appropriate; speculative fleet management is not required for a single instance.

A script that restarts every tenant after one failed target needs review of scope and failure handling. A bounded single-instance update does not need a fleet controller.

## Verification

Inspect supplied repository files and evidence read-only. Do not execute target scripts, CI jobs, infrastructure plans, cloud commands, probes, tests, load generators, restores or deployments. Recommend a discriminating check and route any execution need to the lead and authorized implementer.

For each applicable criterion, connect the control to the actual file/path, mechanism and supplied evidence using the shared report. Explain the trigger, consequence and missing protection for a finding; give enough context to distinguish an acceptable alternative. Record assessment limits, material exclusions and cross-domain handoffs. Do not infer absence from missing files, measurement from analysis, or live enforcement from declared configuration.

The lead must receive a conclusion for each relevant work area within the existing shared report fields, not separate reports or a new schema. No findings means only that the bounded inspection found none; it is not release approval or proof that recovery was exercised.

## Responsibilities and exceptions

The lead owns assignment, document routing and reconciliation. The DevOps Reviewer owns these assessments and supported handoffs. Developers and service owners implement changes and supply execution evidence. Reviewers do not fix infrastructure or authorize release.

Code owns application correctness, including retry/cancellation and resource ownership. Architecture owns structural boundaries and failure isolation. Security owns threat and exploit analysis. Database owns storage/query/integrity mechanisms. Performance owns measurement, bottlenecks and algorithmic cost. Testing owns verification quality. DevOps retains deployment and operational consequences; if another reviewer is unavailable, disclose the unresolved assessment rather than dropping it or claiming specialist coverage.

Use the policy and team authority procedure for explicit project overrides, replacements and waivers. Preserve their scope, approver, rationale, conditions and review/expiry terms where supplied. Do not silently substitute the newest or strictest external rule. Unresolved conflicts return to the lead.

## Ownership, review, and related policy

The Engineering Review Team package maintainer owns this default standard. Review it when an approved scope changes, a control proves ambiguous, a supported platform changes materially or a missed/false finding exposes a gap. The [DevOps Policy (POL)](../policies/devops.md) owns judgment rules; shared criteria and reporting remain team-owned.

## Research reference

[Sources and control mappings](../research/devops.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
