# Devops review research references

Consult this record when verifying a source, checking a version-dependent claim or maintaining the reviewer. Do not load it automatically for routine reviews. The technical standard owns the controls; these references do not independently create project obligations.

## Domains references

[Google's production-readiness discussion](https://sre.google/sre-book/evolving-sre-engagement-model/) supports examining service-specific operational needs; it does not mandate Google's staffing model. [GitHub's secure workflow guidance](https://docs.github.com/en/actions/reference/security/secure-use) supports examining pipeline trust and permissions. The [DevOps Technical Standard (STD)](../standards/devops.md) owns controls and applicability. Source versions and control mappings are recorded below; use the target’s actual platform and operating context.

## Standards references

Sources checked 2026-11-04. Product documentation is living guidance; use the target's actual supported version. SLSA references v1.2. Google book/workbook references are the 2016/2018 editions. These references explain mechanisms and methods, not universal project obligations.

| Source | Primary reference and use |
| --- | --- |
| S1 | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use): pipeline input, checkout, token and runner trust. |
| S2 | [GitHub Actions OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) and [Google deployment-pipeline federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation-with-deployment-pipelines): short-lived credentials, issuer/audience checks and provider-supported workload restrictions. |
| S3 | [GitHub dependency caching](https://docs.github.com/en/actions/concepts/workflows-and-actions/dependency-caching): cache access and artifact distinction. |
| S4 | [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): dependency, concurrency and failure semantics. |
| S5 | SLSA v1.2 [build track](https://slsa.dev/spec/v1.2/build-track-basics) and [build requirements](https://slsa.dev/spec/v1.2/build-requirements): provenance and assurance levels. |
| S6 | [Docker build best practices](https://docs.docker.com/build/building/best-practices/): image inputs, pinning and refresh. |
| S7 | [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking): backend-dependent coordination. |
| S8 | [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data): state/plan exposure and redaction limits. |
| S9 | [Terraform drift management](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift): configuration, state and observed infrastructure. |
| S10 | [Google SRE configuration design](https://sre.google/workbook/configuration-design/): safe configuration and operator interaction. |
| S11 | [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html): scoped access and credential lifecycle. |
| S12 | [Kubernetes network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/): enforcement dependencies. |
| S13 | [Docker rootless mode](https://docs.docker.com/engine/security/rootless/): daemon/container isolation distinctions. |
| S14 | [Kubernetes resource management](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/): requests, limits and failure behavior. |
| S15 | [Google SRE canarying releases](https://sre.google/workbook/canarying-releases/): staged release evaluation. |
| S16 | [Google SRE implementing objectives](https://sre.google/workbook/implementing-slos/): user outcomes and measurement. |
| S17 | [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/): liveness, readiness and startup distinctions. |
| S18 | [Kubernetes pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/): termination and grace periods. |
| S19 | [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/): useful signals and actionable alerts. |
| S20 | [AWS timeouts, retries and jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): deadline coverage, repeat effects and amplification. |
| S21 | [Google SRE overload handling](https://sre.google/sre-book/handling-overload/): resource-sensitive overload behavior. |
| S22 | [AWS recovery validation](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_backing_up_data_periodic_recovery_testing_data.html): usable restores against recovery objectives. |
| S23 | [Google SRE incident management](https://sre.google/sre-book/managing-incidents/): preparation, coordination and recovery. |
| S24 | [Google SRE eliminating toil](https://sre.google/sre-book/eliminating-toil/): repetition and growth as reasons for automation. |

## Control-to-source mapping

The entries below preserve the source associations and qualifications used when authoring the controls. They are research evidence, not additional review instructions.

- **DEVOPS-01 — Pipeline trust and privileges:** For example, executing a fork's code in a job with production credentials crosses the boundary. A privileged job that processes only constrained trusted inputs needs a different assessment. GitHub describes these hazards and OIDC mechanisms in S1–S2; analogous controls apply to the actual platform.
- **DEVOPS-02 — Pipeline execution and caches:** An intentionally optional experimental job may fail without blocking release. A required security check hidden behind unconditional success cannot support the gate. S3 explains GitHub cache boundaries; S4 distinguishes failure and parallelism settings.
- **DEVOPS-03 — Artifact identity and provenance:** A digest-pinned image with a reviewed refresh process can preserve identity without freezing updates indefinitely. Do not require a SLSA level for every local build. S5 defines build assurance levels; S6 explains image pinning and updates.
- **DEVOPS-04 — Infrastructure state and drift:** Protected local state can be suitable for an isolated single-operator workflow. Shared writers and sensitive production state need stronger coordination and protection. This reviewer inspects supplied evidence and does not run a plan, refresh or state command. S7–S9 document the Terraform mechanisms and their limits.
- **DEVOPS-05 — Configuration and secrets:** Environment variables are one configuration mechanism, not a secret boundary by themselves. A secret store also needs appropriate access and retrieval behavior. S1 and S8 support exposure checks; S10 explains configuration's effect on safe operations.
- **DEVOPS-06 — Identity and network access:** A public API is not a defect merely because it is a backend. Unrestricted administrative access can be a defect even in a small service. S11 supports least privilege and access review; S12 establishes Kubernetes network-policy enforcement conditions. Security owns threat/exploit judgments when deeper assessment is required.
- **DEVOPS-07 — Container isolation and resources:** A Kubernetes CPU request influences placement; a CPU limit can throttle, while memory enforcement has different failure behavior. Neither proves capacity. S6, S13 and S14 explain build, isolation and resource mechanisms; the selected limits remain project-specific.
- **DEVOPS-08 — Release compatibility and recovery:** A canary with no relevant signal cannot establish safe expansion. A planned maintenance release can be appropriate when its interruption is explicitly accepted. S15 supports staged evaluation; compatibility and recovery checks here are the package's cross-domain review method.
- **DEVOPS-09 — Operating needs and service objectives:** A one-person local utility needs different operating evidence from a public payment service, even if both have little traffic. S16 supports user-centered objectives; proportional applicability and reporting uncertainty are package rules.
- **DEVOPS-10 — Startup, readiness and shutdown:** A process may not need a liveness probe if it reliably exits on the relevant fatal failure. A readiness check does not prove graceful shutdown. S17–S18 define Kubernetes lifecycle behavior; apply the corresponding lifecycle for other runtimes.
- **DEVOPS-11 — Telemetry and actionable alerts:** A small tool can surface actionable failure to its operator without a pager service. An alert with no reachable owner cannot support a promised response. S19 supports actionable, user-relevant monitoring; exact tools and support hours come from project criteria.
- **DEVOPS-12 — Dependency failures and job delivery:** Acknowledging a job before its required durable commit can lose work on termination. Committing an idempotent update before acknowledgement can tolerate redelivery only when broker/storage guarantees support it. S20 supports deadline and retry reasoning; the worker example preserves the existing Operations review method.
- **DEVOPS-13 — Capacity, backpressure and resource lifecycle:** An unbounded queue in a constrained service can exhaust memory even at modest traffic. Fixed concurrency with a bounded queue and accepted rejection behavior can be sufficient without autoscaling. S21 supports overload and resource-cost reasoning; no benchmark result may be inferred from configuration.
- **DEVOPS-14 — Backup, restoration and failover:** A disposable local cache may need regeneration rather than backup. A backup requiring a key lost with the failed environment may be unusable. S22 supports validation of actual recovery against objectives; the broader dependency sequence is the package's review method.
- **DEVOPS-15 — Incident and recovery ownership:** One accountable maintainer and a usable recovery procedure may suffice for a limited-hours application. A promised continuous response without an available responder does not. S23 supports prepared, scalable incident coordination; exact staffing and response periods belong to the project.
- **DEVOPS-16 — Fleet and maintenance automation:** A script that restarts every tenant after one failed target needs review of scope and failure handling. A bounded single-instance update does not need a fleet controller. S24 explains growth-related operational repetition; these automation checks are package-designed applications of the preceding controls.
