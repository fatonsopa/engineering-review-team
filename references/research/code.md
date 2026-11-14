# Code review research references

Consult this record when verifying a source, checking a version-dependent claim or maintaining the reviewer. Do not load it automatically for routine reviews. The technical standard owns the controls; these references do not independently create project obligations.

## Standards references

All links below were opened and relevant content read on 2026-11-04. Living documentation has no asserted immutable revision unless stated. These are technical evidence sources; package-default authority comes from user agreement, and product criteria come from the project.

| ID | Source and version | What it supports |
| --- | --- | --- |
| S1 | [Google — What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html), living guidance | Functional intent, relevant context and useful tests. CODE-01/16 are operational procedures adapted to this package. |
| S2 | [Google — The standard of code review](https://google.github.io/eng-practices/review/reviewer/standard.html), living guidance | Technical facts, adopted style and nonblocking preference comments; supports CODE-15. |
| S3 | [TypeScript — strictNullChecks](https://www.typescriptlang.org/tsconfig/strictNullChecks.html), living compiler documentation | Null/undefined analysis depends on configuration; supports CODE-02. |
| S4 | [OWASP — Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html), living guidance | Parse limits, structure/meaning, decoding consistency and separation from authorization/injection defenses; supports CODE-03. |
| S5 | [Protocol Buffers — proto3 language guide](https://protobuf.dev/programming-guides/proto3/), living proto3 guide, Updating a message type | Wire/application distinction, unsafe field-number changes, default handling and rollout constraints; supports CODE-04. |
| S6 | [AWS — Timeouts, retries, and backoff with jitter](https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter), Marc Brooker, 2019-12-05 | Uncertain effects, retry overload, deadline selection and jitter; supports CODE-05/09. |
| S7 | [Go Memory Model](https://go.dev/ref/mem), 2022-06-06 | Synchronization and language-specific shared-memory reasoning; supports CODE-06. |
| S8 | [React — useEffect](https://react.dev/reference/react/useEffect), page displays v19.3 | Setup/cleanup dependencies and stale response suppression; supports CODE-07/19. |
| S9 | [Python — Coroutines and Tasks](https://docs.python.org/3.11/library/asyncio-task.html), 3.11.18 documentation | Ownership of tasks, cancellation cleanup, TaskGroup/gather differences; supports CODE-08. |
| S10 | [Stripe — Idempotent requests](https://docs.stripe.com/api/idempotent_requests), living API documentation | Current API v1/v2 distinctions, parameter/key behavior and retention caveats; supports CODE-10. |
| S11 | [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), June 2022, especially §9.2 | Method idempotence and retry interpretation; HTTP-specific basis for CODE-10/17. |
| S12 | [Stripe — Webhooks](https://docs.stripe.com/webhooks), living documentation | Duplicates, unordered events, signatures and timely acknowledgement; supports CODE-11. |
| S13 | [AWS SaaS Lens — General design principles](https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/general-design-principles.html), living guidance | Tenant context, isolation across layers and variation in SaaS architectures; supports CODE-12. |
| S14 | [Node.js — Don’t Block the Event Loop](https://nodejs.org/learn/asynchronous-work/dont-block-the-event-loop), living guidance with historical API-list caveat | Input-size cost, shared event-loop blocking and bounded work; supports CODE-13. |
| S15 | [Google SRE — Handling Overload](https://sre.google/sre-book/handling-overload/), book chapter 21 | Resource-sensitive limits, customer isolation and explicit overload behavior; supports CODE-14. |
| S16 | [OWASP — Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html), living guidance | Appropriate events/context, excluded sensitive data, encoding and logging failures; supports CODE-18. |
| S17 | [Python — decimal](https://docs.python.org/3.11/library/decimal.html), 3.11.18 documentation | Decimal representation, precision and rounding controls; supports CODE-20. |
| S18 | [Python — datetime](https://docs.python.org/3.11/library/datetime.html), 3.11.18 documentation | Aware/naive time semantics and ambiguity; supports CODE-20. |

## Control-to-source mapping

The entries below preserve the source associations and qualifications used when authoring the controls. They are research evidence, not additional review instructions.

- **CODE-01 — Requirement and change alignment:** Basis: Code review procedure; [S1]. No rule requires every changed line to name a ticket.
- **CODE-02 — Values, absence and representation:** Basis: Code review procedure; [S3]. Enabling a compiler option is not proof that external data was validated.
- **CODE-03 — Parsing and validation boundaries:** Basis: [S4]. Validation does not establish authorization or replace parameterized SQL/context-specific output encoding. Route concrete injection concerns to Security while retaining located evidence.
- **CODE-04 — Interface and version compatibility:** Basis: Code review procedure; [S5]. Binary protobuf conclusions do not automatically apply to ProtoJSON or other serializers.
- **CODE-05 — State invariants and partial effects:** Basis: Code review procedure; [S6]. Database transaction guarantees require Database evidence; this check covers application orchestration.
- **CODE-06 — Concurrency and atomic decisions:** Basis: Code review procedure; [S7] for Go synchronization semantics. Process-local locks do not establish cross-process exclusion. Database isolation remains a handoff.
- **CODE-07 — Resource lifetime and ownership:** Basis: Code review procedure; [S8] for React effects. Managed scopes can be sufficient; do not demand manual release where the runtime guarantees the required lifetime.
- **CODE-08 — Cancellation and child work:** Basis: [S9], Python 3.11.18. `TaskGroup` and `gather` differ; neither local cancellation nor timeout proves remote work stopped.
- **CODE-09 — Timeouts and retry amplification:** Basis: [S6]. Numeric budgets come from the project and dependency behavior, not an invented universal timeout.
- **CODE-10 — Idempotent business operations:** Basis: [S10] and [S11]. HTTP idempotence concerns intended effect, not identical responses. Stripe API v1 and v2 differ; never universalize their behavior.
- **CODE-11 — Webhooks and background delivery:** Basis: [S12]; durability sequencing is a package review rule, not a quoted Stripe requirement. Verify the actual broker/provider; do not assume universal delivery guarantees.
- **CODE-12 — Tenant context and entitlements:** Basis: [S13]. This control checks integration correctness; Security owns threat coverage and authorization design assessment.
- **CODE-13 — Bounded work and algorithmic cost:** Basis: [S14]. Nested loops and recursion are not automatically defects; Performance owns workload-wide measurement.
- **CODE-14 — Backpressure and resource fairness:** Basis: [S15]. Quotas and fairness depend on resources and commitments; do not invent a standard requests-per-second limit.
- **CODE-15 — Maintainability and useful abstractions:** Basis: [S2]; Code review scope. No arbitrary function-length maximum, compulsory pattern or mandatory abstraction. Pure preferences are optional comments, not defects.
- **CODE-16 — Changed-code test integrity:** Basis: [S1]; requirement-to-assertion review. No automatic 100% coverage or separate test per branch requirement. Testing owns overall verification strategy and suite adequacy.
- **CODE-17 — Error contracts and recovery behavior:** Basis: Code review procedure and [S11] for HTTP semantics only. Catching every exception is not inherently graceful handling.
- **CODE-18 — Diagnostic and audit events:** Basis: [S16]. Security/Compliance determine sensitive-data and audit obligations; Code checks the implementation. Required audit durability can differ from optional diagnostic logging.
- **CODE-19 — UI asynchronous and lifecycle behavior:** Basis: Code review procedure; [S8]. Design owns visual/accessibility depth; source inspection alone does not prove browser or assistive-technology behavior.
- **CODE-20 — Money, time and precision-sensitive semantics:** Basis: [S17], [S18]. Decimal still needs precision/rounding decisions; calendar dates are not automatically UTC instants. Localization owns presentation conventions.
- **Version and language limits:** TypeScript static null checking cannot certify runtime JSON shape, especially through `any`, assertions or unchecked deserialization [S3, S4].
- **Version and language limits:** Python 3.11 cancellation behavior and structured concurrency must not be copied onto earlier Python or another task library. Cancellation has cleanup and ownership semantics, not automatic transactional rollback [S9].
- **Version and language limits:** React effect replacement/unmount behavior does not describe every UI framework. Framework-managed fetching can already handle stale requests; inspect it before alleging missing manual cleanup [S8].
- **Version and language limits:** Go’s memory model is language-specific. A Go synchronization argument cannot establish C/C++ undefined-behavior safety or prove atomicity across services [S7].
- **Version and language limits:** The Node guidance’s synchronous-API list explicitly dates its completeness to Node v9. Use the mechanism and recheck the actual installed version, rather than copying that historical list as current coverage [S14].
- **Version and language limits:** Protobuf binary compatibility, application compatibility and ProtoJSON compatibility differ [S5].
- **Version and language limits:** Stripe’s current page distinguishes API v1 replay responses from API v2 recovery behavior. Provider semantics and key retention must be selected explicitly [S10].
