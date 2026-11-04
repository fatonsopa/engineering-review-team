# Engineering review criteria

## Context

Project requirements and verified contracts define acceptance. General engineering guidance informs the review but is not automatically a mandatory compliance obligation. Capture exact applied rules and versions with the review.

## How it works and why

| Source | Applicability | Evidence and review trigger |
| --- | --- | --- |
| [Google code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Design, behavior, complexity and tests | Caller flows and test oracles; revisit when review methods change. |
| [arc42 architecture views](https://arc42.org/overview/) | Context, runtime/deployment, decisions and quality scenarios | Use relevant views as an inspection aid, not a requirement to create twelve documents. |
| [SEI architecture evaluation](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Cross-component quality scenarios | Operating scenario, required response and tradeoffs; scale the method to scope. |
| [OWASP ASVS 5.0.0](https://asvs.owasp.org/) | Applicable web applications/services | Selected versioned control IDs, trust boundary and enforcement evidence; do not impose every control on unrelated projects. |
| [Google SRE launch practices](https://sre.google/sre-book/reliable-product-launches/) | Relevant rollout/reliability risks | Workload, deployment and recovery evidence; adapt to actual operating requirements. |
| Actual storage/framework documentation, e.g. [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | Only the engine/version used by the target | Record a version-specific source and concrete invariant/transaction assumption before relying on it. |

For each applied criterion retain ID, exact text or captured excerpt, source origin, version/date, applicability and expected verification. External source references must be checked when they affect a conclusion; unavailable references remain a limitation. Google code review, OWASP ASVS 5.0.0, arc42 and the Google SRE launch chapter were opened for the 4 November 2026 follow-up. The retained SEI and storage references still require version/applicability checks when they control a conclusion; this register does not establish future freshness.

## Tradeoffs and limits

No finding quota or universal checklist applies. Separate defects against a contract, justified risks/improvements and unresolved questions. A preferred design, absent attachment or unmeasured performance claim is insufficient evidence. Update affected cases when a justified criterion changes, retaining earlier results under their original version.

## Related sources

The [shared evidence rules](review_standard.md) own finding fields and severity; each [domain method](domains/implementation.md) supplies the relevant procedure. Source selection is a lead judgment, not a claim that this skill certifies regulatory compliance.

For optional project intent and precise per-criterion coverage use [project intent and alignment](intent_context.md). A wider topic inventory guides applicability discovery; it is not proof that any family was inspected or every possible requirement was captured.
