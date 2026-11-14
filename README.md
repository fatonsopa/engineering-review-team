# Engineering Review Team

**Engineering Review Team** — A coordinated team of AI reviewers led by an Engineering Review Lead, with specialists in code, architecture, security, database, testing, DevOps, performance, design, localization, and compliance. Delivered as an agent skill package for Codex and Claude Code.

Review changes or components through ordinary host-native tools. The lead reviews directly or selects specialists, then returns evidence-backed findings and honest limits. The package supplies technical knowledge and instructions; it does not require a review engine, ledger or evaluation matrix.

## Start

Use the skill in your current host and name the target, expected behavior and review scope. Supply relevant requirements or project guidance when available. Review is read-only; corrections and publication need their own authority. See [SKILL.md](SKILL.md) for the workflow.

## Install

Python 3.11+ is needed only for the standalone installer:

```sh
python3 scripts/install_skill.py --host codex --destination /absolute/path/to/engineering-review
```

Use `--host claude-code` for Claude Code. To register optional native roles, run the installed installer with `--source /absolute/path/to/engineering-review --agents-dir /path/to/project/.codex/agents --host codex --preview`; Claude Code uses `.claude/agents` and `--host claude-code`. Remove `--preview` to write after checking the destination. See [host setup](references/host_setup.md) for conflicts, permissions and archive creation. Asset files do not prove actual host execution.

## Reviewers and shared guidance

Every role uses the [shared policy](references/review_policy.md), [evidence and finding standard](references/review_standard.md), and relevant [project intent](references/intent_context.md). The lead also uses [coordination](references/coordination.md) and [project context](references/project_profile.md). Read only the selected role and applicable technical controls; research references are for source verification, not mandatory preload.

| Reviewer | Responsibilities | Policy (POL) | Technical Standard (STD) |
| --- | --- | --- | --- |
| [Engineering Review Lead](references/coordination.md) | Establish scope and authority, inspect evidence, assign selected specialists, check coverage, reconcile findings and deliver the final assessment. A nested read-only lead requests parent assistance when needed. | [Shared Policy (POL)](references/review_policy.md) | [Shared Technical Standard (STD)](references/review_standard.md) |
| [Code Reviewer](references/domains/code.md) | Functional correctness, requirement alignment, contracts, state transitions, errors, concurrency, resource ownership, compatibility or concrete maintainability risks. | [Code Reviewer Policy (POL)](references/policies/code.md) | [Code Reviewer Technical Standard (STD)](references/standards/code.md) |
| [Architecture Reviewer](references/domains/architecture.md) | Component boundaries, rule ownership, dependencies, contracts, compatibility or quality-attribute risks. | [Architecture Reviewer Policy (POL)](references/policies/architecture.md) | [Architecture Reviewer Technical Standard (STD)](references/standards/architecture.md) |
| [Security Reviewer](references/domains/security.md) | Trust boundaries, identity, authorization, secrets, untrusted input, dependency or sensitive-output risks. | [Security Reviewer Policy (POL)](references/policies/security.md) | [Security Reviewer Technical Standard (STD)](references/standards/security.md) |
| [Database Reviewer](references/domains/database.md) | Persistence contracts, schemas, database access, queries, transactions, migrations, retention, maintenance, replication or recovery. | [Database Reviewer Policy (POL)](references/policies/database.md) | [Database Reviewer Technical Standard (STD)](references/standards/database.md) |
| [Testing Reviewer](references/domains/testing.md) | Requirement and risk coverage, test oracles, fixtures and doubles, isolation, concurrency, compatibility, regression quality or execution evidence. | [Testing Reviewer Policy (POL)](references/policies/testing.md) | [Testing Reviewer Technical Standard (STD)](references/standards/testing.md) |
| [DevOps Reviewer](references/domains/devops.md) | CI/CD, build artifacts, infrastructure, identity/configuration, deployment compatibility, production readiness, operational resource bounds, detection or recovery. | [DevOps Reviewer Policy (POL)](references/policies/devops.md) | [DevOps Reviewer Technical Standard (STD)](references/standards/devops.md) |
| [Performance Reviewer](references/domains/performance.md) | Latency, throughput, resource lifetime, algorithmic cost, I/O, caching, concurrency, capacity, fairness, assets, rendering or performance evidence. | [Performance Reviewer Policy (POL)](references/policies/performance.md) | [Performance Reviewer Technical Standard (STD)](references/standards/performance.md) |
| [Design Reviewer](references/domains/design.md) | User journeys, adopted design rules, accessibility, responsive presentation, UI states, interaction and browser evidence. | [Design Reviewer Policy (POL)](references/policies/design.md) | [Design Reviewer Technical Standard (STD)](references/standards/design.md) |
| [Localization Reviewer](references/domains/localization.md) | Locale selection and fallback, translated messages, plural and interpolation rules, locale-sensitive formats, Unicode and bidirectional content, localized UI and delivery evidence. | [Localization Reviewer Policy (POL)](references/policies/localization.md) | [Localization Reviewer Technical Standard (STD)](references/standards/localization.md) |
| [Compliance Reviewer](references/domains/compliance.md) | Applicable adopted obligations, authority and exceptions, policy-to-implementation traceability, data handling, consent, retention, audit evidence and supported compliance claims within the supplied scope. | [Compliance Reviewer Policy (POL)](references/policies/compliance.md) | [Compliance Reviewer Technical Standard (STD)](references/standards/compliance.md) |

## Project documents and roles

The lead finds relevant project guidance and passes the useful sections to reviewers. Combined documents and direct task requirements are sufficient; the table describes content, not mandatory paperwork.

| Document/content | What to compare | Reviewers |
| --- | --- | --- |
| Product Requirements Document (PRD), Spec Driven Development document (SDD), Issue, User Story (US), behavioral requirements | Observable behavior, actors, permissions, boundaries, failures and acceptance criteria | Lead accounts for scope; Code traces implementation; Testing checks verification. Route domain constraints to the relevant specialist. |
| High Level Document (HLD), Decision Record (DR) | Boundaries, dependencies, quality scenarios, accepted choices and tradeoffs | Architecture assesses structure; Code checks local adherence; Security, Database, DevOps and Performance receive affected constraints; Testing receives quality scenarios and accepted compatibility or failure expectations. A decision's rationale is not proof of implementation. |
| Low Level Design (LLD), Interface Contract (IC) | Types, nullability, units, validation, errors, ordering, state transitions, serialization, compatibility, idempotence, persistence invariants and consistency guarantees | Code and Architecture compare producers/consumers; Security receives access/trust rules; Database receives persistence invariants; Testing receives observable contracts; Performance receives latency, payload, allocation and concurrency constraints; Localization receives text identity, serialization, currency and temporal semantics. Unknown dependency behavior remains unresolved. |
| Implementation Plan (IP) | Accepted deliverables, dependencies, implementation constraints, verification, mixed-version sequencing and rollout/recovery steps | Lead checks whole-plan coverage; Code checks assigned code deliverables; Testing receives verification; Database receives migration/backfill; DevOps receives rollout/recovery; Performance receives accepted efficiency work, workload assumptions and performance verification. Superseded approaches are context. |
| Test Plan (TP), Test Specification (TS) | Cases, expected outcomes, fixtures, boundary/failure scenarios and exit criteria | Testing assesses coverage, meaningful expected results, test selection, fixtures and exit criteria; Code and affected specialists check relevant assertions and behaviors. Proposed cases remain proposed; adopted test gates retain their authority, and no universal requirement for all test layers applies. |
| Test Status Report (TSR), Test Completion Report (TCR) | Actual commands and selection, source revision, environment, dependencies, results, failures, timeouts, retries, skips and limitations | Lead, Testing and affected reviewers assess observed evidence. Results are observations, not normative behavior; stale results do not prove the current code passed. |
| Organization Policy (POL), project Technical Standard (STD), coding guidelines | Applicable obligations, adopted conventions, named controls, scope and approved exceptions | Lead establishes authority and routes by subject. Code receives naming, file organization, patterns, errors, logging and compatibility rules; other domains receive their actual obligations. Conflicts require resolution. |
| Threat Model (TM) | Assets, trust boundaries, assumptions, abuse scenarios, controls and accepted residual risks | Security owns threat assessment; Architecture, Database and DevOps assess affected mechanisms; Code checks assigned validation, tenant context and output-handling paths. Testing checks whether verification exercises relevant denied and legitimate behavior. Missing documentation does not suppress applicable technical checks. |
| Service Objectives Document (SOD), operational How-to Guide (HTG) | Agreed indicators/objectives, deadlines, retry/resource limits, deployment/stop/recovery procedures, dependencies and response responsibilities | DevOps and Architecture assess operational contracts; Database checks storage durability, consistency, backup scope and restore evidence against applicable recovery objectives; Testing assesses evidence; Code traces applicable timeout, cancellation, retry and recovery behavior. Performance receives workload shapes, latency/throughput percentiles, resource budgets, capacity limits, tenant fairness and cost constraints. Source inspection alone does not establish measured attainment. |
| Design specifications/design system | Required UI states, validation, interactions, accessibility semantics and support matrix | Code checks implementation behavior; Testing assesses the required interaction, browser and accessibility verification and its limits. Design assesses user journeys, adopted design rules, accessible operation, UI states and visual/browser evidence; the lead supplies exact relevant sections and captured image/context evidence. Localization receives script, expansion, direction and localized-state expectations. Unperformed browser or assistive-technology checks stay visible. |
| Supported-locale requirements | Encoding, timezone/currency meaning, locale formatting, direction, fallback and language requirements | Localization compares supported languages/scripts/channels, message behavior, user/tenant preferences, Unicode, currency/time-zone meaning, formatting, plural rules, fallback, direction, sorting and recipient context. Code checks boundary integration; Design checks presentation; Testing assesses the supplied verification. Route relevant terminology, runtime/catalog versions and linguistic evidence; no standalone locale matrix is mandatory. Technical checks do not establish linguistic approval. |
| Established licensing/privacy/compliance obligations | Applicable licenses/notices, source headers, sensitive data handling, audit/output and retention requirements | The lead captures the actual scope and authority. Compliance compares exact license/asset terms, distribution or network use, notices and required headers; data categories/purposes, lifecycle, preference and rights contracts; applicable audit, processor, residency and retention requirements. Route dependency inventories, license texts, notices, data maps, retention schedules and actual decisions by content; separate files are optional. Security/Database assess their technical controls; Testing assesses verification. Preserve unresolved legal applicability and obtain qualified interpretation when necessary; do not infer a universal license ban or regulatory regime. |
| Performance evidence and budgets, including supplied profiles, load results and asset reports | Workload shape and volume, concurrency, duration, environment/version, distributions, resource limits, baseline and changed revision | Performance compares adopted budgets and representative observations; Testing assesses measurement validity; Database receives query/engine evidence; DevOps receives saturation and operational limits; Architecture receives structural constraints. Measurements remain observations, missing workloads remain unknown and proposed targets cannot become obligations. |

## Findings and corrections

Findings explain the location, triggering behavior, supported consequence and focused correction. The final response also states inspected scope and important limits. Valid partial findings remain useful when another question is unresolved. The optional [handoff](references/templates/review-handoff.md) and [developer response](references/templates/developer-response.md) outlines keep follow-up concise; re-review actual changes without manufacturing missing evidence.

## Maintain the package

See [AGENTS.md](AGENTS.md). Run `python3 -B -m unittest discover -s tests -p test_package.py -v` for installer and asset checks. Inspect affected links and instruction meaning. These checks do not prove domain expertise or native-host execution; use a bounded host smoke only when the changed behavior warrants one.

### Behavioral regression trials

[The retained cases](tests/review_cases.json) include the original pair for each of ten reviewers and additional finite scenarios with maintainer-only expectations. Preparation defaults to the pair; use `--cases SCENARIO_ID ...` to select existing extended scenarios. Run the preparation checks with `python3 -B -m unittest discover -s tests -p test_review_cases.py -v`, then prepare a disposable workspace from the repository root:

```sh
python3 -B tests/test_review_cases.py --prepare code --destination /absolute/disposable/code --host claude-code
cd /absolute/disposable/code
claude -p --agent engineering-review-implementation --permission-mode dontAsk --tools Read,Glob,Grep --allowedTools Read,Glob,Grep < prompt.txt
```

The expected checklist is for the maintainer and is not staged. Assess the actual output against it and verify source preservation; preparation and unit checks are not behavioral passes. For Codex, use `--host codex` with the same [preparation module](tests/test_review_cases.py), follow the [native binding guidance](references/host_setup.md#register-optional-agents), then dispatch the prepared native reviewer from the main context.

Use `--prepare lifecycle` to stage the initial shared-workflow fixture. Keep the expected checklist in [tests/lifecycle_case.json](tests/lifecycle_case.json) outside the model workspace. After the initial review, apply only its `follow_up_files` and provide the developer response using the actual initial finding identifiers, then request re-review in the same host conversation. Assess each stage against the maintainer checklist. The same helper accepts `--prepare TEAM-DISCOVERY`, `TEAM-LEAD-BOUNDARIES` or `TEAM-RESPONSE`; use their retained operator stages and follow-ups, including same-conversation discovery refresh, without exposing expected outcomes. Record the actual host/model and available tools. These bounded cases and host profiles do not certify every technical control or every host configuration.

## License

MIT; see [LICENSE](LICENSE).
