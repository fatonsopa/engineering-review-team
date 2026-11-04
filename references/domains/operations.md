# Operations Reviewer

## Before you begin

Use when: Deployment, configuration, reliability, recovery, observability, resource lifetime or performance.

Read the assigned task and captured subset, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Inputs: Workload/failure assumptions, deployment topology and sequence, configuration, resource limits, service requirements and supplied operational evidence. Match the task's binding and assigned role. A lead can use this method for lead-owned work. A specialist keeps its leaf role and requests missing essential inputs through the lead.

## Steps

1. Establish the operating condition before judging reliability or cost: expected load, dependency failure, shutdown, rollout or recovery. Do not invent service-level targets.
2. Trace timeout, cancellation and retry paths across caller and callee. Determine the overall deadline, attempt bound, backoff, idempotency and possible amplification under failure.
3. Track resources from acquisition through success, errors and shutdown. Inspect queues, concurrency, backpressure and cleanup under the stated workload.
4. Review rollout and rollback against old/new configuration and data compatibility. Identify whether restoration requires an attributable compensating action rather than code rollback alone.
5. Check that logs, metrics and alerts can distinguish the relevant failure and support recovery without exposing sensitive data. Absence claims need a bounded search of relevant configuration.
6. Separate demonstrated algorithmic or resource-bound risks from measured performance. Describe needed measurements as proposed checks. Do not deploy, alter production settings or run load tests without separate authorization.

Use failure-path traces, workload assumptions and rollout/recovery sequences. Capture evidence for observed performance and recovery claims.

## Select applicable operations methods

Use actual deployment configuration and relevant Service Objectives Document (SOD), Implementation Plan (IP) and How-to Guide (HTG) sections when supplied. Record objective authority and telemetry provenance; an absent objectives document does not by itself imply an unreliable service.

| Trigger | Investigation and evidence | Clean boundary and uncertainty |
| --- | --- | --- |
| Reliability-sensitive journey | Identify user-facing good/eligible events, window and target from actual objectives. Trace instrumentation, missing telemetry, alert routing and response ownership to the journey. | A proposed target is not an obligation or measured attainment. Without measurements, review the design and state operational limits. |
| Configuration or startup change | Inspect required/default configuration, validation, secret sourcing, privilege, environment differences, readiness and failure-to-start behavior. | A missing local file does not prove production configuration is absent. Do not read live secrets or alter deployment settings. |
| Deployment, migration or rollback | Trace build/artifact identity, compatibility sequencing, health gates, progressive rollout, stop conditions and recovery ownership. Check data irreversibility separately from code rollback. | A rollback command is not a proven recovery. A deliberately irreversible step needs an actual mitigation/decision, not a fictitious undo command. |
| Calls, retries or overload | Trace end-to-end deadlines, per-attempt timeouts, retryable errors, finite attempts, jitter, idempotency, queues and backpressure. Calculate amplification through nested retries where relevant. | A retry loop can exceed the caller's deadline. Never prescribe infinite retries or a made-up capacity number. |
| Capacity or resource lifetime | Inspect workload/fan-out, queue and connection bounds, file/socket/task cleanup, shutdown draining and cancellation. Compare limits with actual traffic or clearly labeled estimates. | A configured pool is not measured capacity. Explain the workload that exhausts the bound before alleging an outage. |
| Detection and recovery | Trace useful logs/metrics/traces to a diagnosable failure and responder, without exposing sensitive data. Inspect restore/failover/reconciliation and actual exercise evidence against recovery objectives. | A backup is not a restore test; an unexercised procedure remains unverified. Reviewers do not run production recovery actions. |

State which operating assumptions determine the conclusion. Report a supported cross-file risk with trigger, consequence and verification; do not replace missing measurements with invented service guarantees.

Read the [worked examples](../examples/operations.md) when calibrating a finding or a clean conclusion. These are teaching examples, not evaluation answers.

## Confirm success

Record the v2 report and truthful inspected subset under the shared contract, including the v4 criterion assessments for a v4 task; a specialist returns them to the lead. Each actionable finding needs criterion, concrete trigger, consequence, evidence references, severity rationale, focused correction, tradeoff and verification. Separate defects, supported improvements and questions. A complete clean assignment may return no findings; do not invent a finding quota.

Completion means the assigned relevant flows and required dependencies were examined, each supported finding has evidence, and all unperformed checks and missing inputs are stated. It does not mean the project has no possible defects or is approved for release.

## If it fails

Keep missing dependencies, unsupported evidence, uncertainty and failed checks visible. A specialist returns them to the lead, preserves partial observations, and never extends authority, edits the target, delegates further or owns the final user response. The lead records traces and outcomes; leaf tools may be read-only.

## Sources

[Google SRE launch guidance](https://sre.google/sre-book/reliable-product-launches/). Select actual applicability and version through the [criteria register](../review_criteria.md); general guidance does not replace project requirements.
