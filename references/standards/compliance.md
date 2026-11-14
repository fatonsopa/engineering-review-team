# Compliance review standard

Package default under the [Compliance Policy (POL)](../policies/compliance.md) and shared authority procedure. The lead selects applicable controls and routes actual project obligations; this document does not assign a jurisdiction or certify compliance.

## Purpose and scope

Assess changed materials and data-handling behavior against established rights, contracts and technical obligations. A small internal tool may need only provenance and notice checks. Real personal data, distribution or a consequential obligation can require deeper review regardless of traffic or project phase.

## Definitions

**Distribution/conveyance** and **network use** follow the actual license terms; they are not interchangeable triggers. A **hold** is an established restriction on disposing of identified records. **Access**, **erasure** and **portability** are distinct requests with applicable scope and exceptions. **Pseudonymization** does not automatically make data anonymous. A **control** is an assessable requirement; evidence of one control does not establish organization-wide compliance.

## Principles

Identify the obligation before judging conformance. Trace actual material, data and side effects. Preserve legitimate alternatives, source terms and authority. Compare correct behavior as well as the suspected failure, and keep missing evidence separate from a demonstrated defect.

## Rules

Read applicable controls in full. Sources, versions and the uploaded-scope mapping are in [Compliance research](../research/compliance.md); ordinary assignments need only the relevant project terms and controls.

| Control | Subject | Control | Subject |
| --- | --- | --- | --- |
| [CMP-01](#cmp-01-applicability-and-authority) | Applicability | [CMP-08](#cmp-08-retention-deletion-and-holds) | Retention and holds |
| [CMP-02](#cmp-02-material-inventory-and-provenance) | Provenance | [CMP-09](#cmp-09-rights-and-exports) | Rights and exports |
| [CMP-03](#cmp-03-license-obligations) | License terms | [CMP-10](#cmp-10-processors-transfers-and-location) | Recipients and location |
| [CMP-04](#cmp-04-notices-and-headers) | Notices | [CMP-11](#cmp-11-audit-records) | Audit records |
| [CMP-05](#cmp-05-data-and-purposes) | Data and purposes | [CMP-12](#cmp-12-required-security-controls) | Security linkage |
| [CMP-06](#cmp-06-minimization-and-sensitive-outputs) | Minimization | [CMP-13](#cmp-13-framework-specific-controls) | Framework scope |
| [CMP-07](#cmp-07-choices-and-permissions) | Choices | [CMP-14](#cmp-14-evidence-and-claims) | Evidence limits |

### CMP-01: Applicability and authority

- Identify the actual entity role, users/data, processing purposes, use/distribution, contracts and jurisdiction/framework determination relevant to the change. Retain unknown or disputed facts.
- Bind each obligation to its exact applicable source, version/effective period and captured interpretation. Distinguish adopted rules, proposals, historical decisions and package defaults.
- Trace replacements and exceptions through shared authority rules. Internal approval cannot establish release from an independent license, contract or statutory duty.
- Check that exclusions have supporting scope facts. Neither a prototype label nor a framework name decides applicability.

A supplied contractual ban on storing payment credentials is reviewable without asserting that every other PCI DSS requirement applies.

### CMP-02: Material inventory and provenance

- Identify affected direct/transitive dependencies, copied code, fonts, images, datasets and other delivered assets, including vendored or generated contents that a lockfile omits.
- Compare actual versions, origin, license text, notices, chosen dual-license option and exceptions with the inventory and shipped artifact.
- Treat scan results, package metadata and Software Bill of Materials entries as evidence to reconcile. Missing or ambiguous terms remain unresolved; public availability is not permission.
- Preserve origin and ownership claims. Do not assume AI-generated or copied material has cleared third-party rights merely from how it was acquired.

A correct dependency list can still omit a bundled font. An unchanged company-authored file with established provenance need not acquire an external license review service.

### CMP-03: License obligations

- Read the exact terms and actual use: modification, linking/combination, redistribution, source/binary delivery, network interaction and recipients where relevant.
- Verify required license copies, attribution, modification notices, corresponding source or offers, and permitted licensing of covered material in the actual delivery path.
- Distinguish GPL conveyance conditions, AGPL network conditions and other licenses' scopes or exceptions. Do not infer that every copyleft dependency requires publication of the entire surrounding system.
- Evaluate an authorized dual-license selection or exception against its actual scope. Resolve uncertain derivative-work or compatibility questions through the lead rather than guessing.

Preserving a permissive license's required notice may satisfy the affected obligation. An internal “accept risk” label cannot replace a missing licensor permission.

### CMP-04: Notices and headers

- Compare required attribution, license text, upstream NOTICE contents and modification statements with source, bundled output, installer/download and other relevant delivery surfaces.
- Apply corporate headers or ownership metadata only where established policy requires them. Check permitted identifiers, sidecars or repository notices rather than imposing one universal header format.
- Preserve required upstream notices and truthful attribution; a corporate copyright statement cannot replace them. Do not fabricate authorship or update years without a governing rule.
- Check packaging filters, minifiers, generated assets and export paths that can remove required content despite correct source files.

A project may replace repeated internal boilerplate with an agreed identifier and attribution file while still preserving an upstream MIT notice.

### CMP-05: Data and purposes

- Trace affected data from collection through enrichment, storage, recipients and disposal; include identifiers, device/activity data, telemetry and derived profiles when relevant.
- Compare each actual purpose and recipient with the captured lawful-basis determination, contract and user-facing commitments. A privacy notice alone does not establish that processing is permitted.
- Check additional conditions for sensitive categories where applicable. Do not require consent universally or infer anonymity from hashing, masking or removal of one identifier.
- Identify a new use, recipient or data category that falls outside the established assessment, and state the specific unresolved obligation.

An account-service purpose and optional advertising can have different rules. One general acceptance flag does not automatically authorize both.

### CMP-06: Minimization and sensitive outputs

- Compare collected, persisted, logged, exported and transmitted fields with the actual purpose and permitted field set. Include error paths, traces, analytics, support payloads and test fixtures.
- Inspect required masking/redaction in the actual serialization path and for nested or unexpected fields. A masked UI does not establish that logs or storage omit the original value.
- Check access and retention of necessary sensitive output; avoid over-redaction that removes evidence explicitly required by a legitimate contract.
- Distinguish pseudonymized from anonymous output and identify residual linkability where it affects the obligation.

An allowlisted audit event may correctly retain an internal subject ID while excluding the email address and full request body.

### CMP-07: Choices and permissions

- Establish the actual purpose, basis, choice/permission semantics, defaults and effective point. Consent, withdrawal, objection, opt-out and an application permission are not interchangeable.
- Where consent is required, compare collection and withdrawal behavior with the applicable requirements; do not silently repurpose consent or change its basis after withdrawal.
- Trace changes through APIs, persisted state, caches, queues, retries and recipients. Check whether prohibited work is still collected or delivered after the contract's effective point.
- Preserve independently authorized processing and required audit evidence. A withdrawn marketing preference need not prohibit an unrelated necessary service notice.

A toggle saved correctly but ignored by a delivery worker violates a no-marketing-after-withdrawal contract. Its existence alone proves neither compliant choice nor a universal consent requirement.

### CMP-08: Retention, deletion and holds

- Establish actual retention triggers, periods, scope and disposal/restriction rules for each affected record category. Do not invent a global duration.
- Trace expiry/deletion through primary and secondary stores, caches, indexes, replicas, processors and backups where relevant; inspect failed jobs, retries and restore behavior.
- Apply a valid hold only to its covered records and permitted uses, with its actual release/review conditions. Continue required disposal for independent unheld records.
- Distinguish deletion, irreversible anonymization, restricted retention and delayed backup expiry. Verify the adopted guarantee and honest completion status rather than promising immediate physical erasure or an unlimited backup exemption.

A scoped invoice hold need not retain unrelated tracking events. Deleting a primary row while restoring it from an unmanaged backup may contradict the adopted lifecycle.

### CMP-09: Rights and exports

- Establish the applicable request type, subject/tenant, eligible information, identity checks, time limits and exceptions. Access and portability need not include identical data or use identical formats.
- Trace retrieval, correction, restriction, erasure or export across the stores and recipients within the actual promise. Protect other people's data and preserve justified exclusions explicitly.
- Inspect authorization, secure delivery, pagination/completeness, partial failure and repeated requests where affected. A successful download does not establish that its contents are complete or belong to the requester.
- Keep request status and explanations truthful. Distinguish unavailable evidence, a valid exception and unfinished processing.

A scoped export can correctly omit another tenant's records and protected third-party data; silently omitting the requester's eligible second page is different.

### CMP-10: Processors, transfers and location

- Identify actual recipients, processor/subprocessor roles, agreements, approved purposes and permitted instructions where relevant. A vendor name alone does not establish its role or approval.
- Trace hosting, backup, support access, telemetry and onward transfers against established location and transfer commitments. Storage region alone does not prove compliance with all transfer obligations.
- Inspect required deletion/return, assistance, incident notification and subprocessor-change mechanisms in the affected integration and supplied evidence.
- Preserve unresolved contractual or transfer interpretations; do not prescribe one mechanism for every jurisdiction or treat encryption as automatic legal authorization.

A region-pinned database can still send support payloads elsewhere. A wholly local utility with no recipient need not invent a processor agreement.

### CMP-11: Audit records

- Identify the required events, including relevant permission or tracking-choice changes. Verify actor/service identity, subject/resource, action, time, relevant change/outcome and correlation as required.
- Trace attempted, committed, failed and partially completed operations into truthful records. Check duplicates, retries and concurrent changes against the adopted guarantee.
- Inspect failure handling, delivery/reconciliation, alteration resistance, access and retention where relevant. A transactional outbox or another justified mechanism can satisfy the contract; no universal synchronous-write design applies.
- Exclude prohibited secrets and unnecessary personal payloads while retaining required evidence. A log file's existence does not prove event completeness or ongoing operation.

A success event emitted before a rejected update misstates the result. A retry-safe outbox recording the committed change may be valid without a direct remote log call.

### CMP-12: Required security controls

- Map established confidentiality, access, protection, incident and evidence-integrity obligations to the affected technical controls and their actual scope.
- Route threat analysis and implementation weaknesses to Security; storage and recovery mechanisms to Database/DevOps. Preserve the compliance criterion and evidence through the lead.
- Compare configuration, implementation and supplied operational evidence separately. Do not infer continuous control operation or compliance from a declaration or passing scan.
- Retain a supported technical defect even when broader legal applicability is unresolved; describe the authority for the finding honestly.

An unauthorized cross-tenant export can violate a captured access contract without a reviewer making an unsupported regulatory determination.

### CMP-13: Framework-specific controls

- Apply only established framework/version and system scope, with relevant roles and exclusions. Review current adopted requirements rather than draft or historical rules.
- For GDPR-related work, use the actual processing scope and captured obligations for purposes, rights, safeguards and recipients; do not turn it into a universal consent checklist.
- For HIPAA-related work, establish covered-entity/business-associate scope and relevant agreements before applying the assigned privacy/security controls. Health-related content alone does not settle applicability.
- For PCI DSS-related work, consider actual storage, processing, transmission and systems affecting account-data security. Distinguish display masking from stored-data protection; under the applicable requirements, inspect prohibited post-authorization sensitive-authentication-data storage, including card verification values. Outsourcing payment collection does not automatically remove every responsibility.
- For another established regime or customer control, obtain its exact relevant terms and assess the implementation/evidence; do not claim coverage of uninspected clauses or invent certification.

A declared HIPAA boundary does not prove every system belongs inside it. A supplied payment contract can prohibit retaining verification values even in a low-volume service.

### CMP-14: Evidence and claims

- Bind each conclusion to the actual obligation, source revision, inspected artifacts, method, observation and limits. Retain missing, stale, contradictory and unperformed evidence.
- Compare inventories and attestations with their scope, period, issuer, exceptions and affected system. A policy, scanner result or vendor certificate is not a complete product assessment.
- Preserve technical failures and historical exceptions without fabricating renewed approval. A developer response does not close its own finding.
- Separate a supported technical contradiction, an unresolved interpretation and a recommendation. Do not announce legal advice, certification, full compliance or release approval from this review.

A test can establish that a notice survives packaging for its inputs; it cannot establish every dependency's licensing status.

## Verification

For each selected control, retain the governing criterion, applicable facts, exact source/evidence, expected behavior, actual observation or supported analysis, consequence and limits. Use the control's distinguishing checks and legitimate counterexamples. Preserve source terms, data, decisions and prior results during verification.

The leaf recommends checks and inspects supplied results; it does not execute targets, collect live personal data or alter approvals. The lead may obtain separately authorized observations and qualified interpretation. Record material exclusions and incomplete comparisons without erasing independently supported findings.

## Responsibilities and exceptions

The lead establishes scope, authority and evidence; Compliance assesses assigned obligations; developers implement and verify corrections. Use the shared customization procedure for supplements, replacements and waivers. Preserve independent obligations, expired history and evidence honesty. A waived unmet requirement remains unmet.

## Ownership, review, and related policy

The package maintainer owns defaults and validation. Revisit affected checks when relevant terms, obligations, data flows, shared contracts or demonstrated missed defects/false positives change. Follow the [Compliance Policy (POL)](../policies/compliance.md), [procedure](../domains/compliance.md) and shared [Review Technical Standard (STD)](../review_standard.md).
