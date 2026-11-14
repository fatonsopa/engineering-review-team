# Security review technical standard

## Contents

- [Purpose and scope](#purpose-and-scope)
- [Definitions](#definitions)
- [Principles](#principles)
- [Applicability and phases](#applicability-and-phases)
- [Rules](#rules)
- [SEC-01 — Assets, threats and trust boundaries](#sec-01--assets-threats-and-trust-boundaries)
- [SEC-02 — Authentication, enrollment and recovery](#sec-02--authentication-enrollment-and-recovery)
- [SEC-03 — Authorization, tenant isolation and delegated access](#sec-03--authorization-tenant-isolation-and-delegated-access)
- [SEC-04 — Sessions, cookies and revocation](#sec-04--sessions-cookies-and-revocation)
- [SEC-05 — Federation, OAuth and token validation](#sec-05--federation-oauth-and-token-validation)
- [SEC-06 — Input meaning, canonicalization and object construction](#sec-06--input-meaning-canonicalization-and-object-construction)
- [SEC-07 — Interpreter and query injection](#sec-07--interpreter-and-query-injection)
- [SEC-08 — Browser output and cross-site scripting](#sec-08--browser-output-and-cross-site-scripting)
- [SEC-09 — Browser origins, CSRF and cross-context access](#sec-09--browser-origins-csrf-and-cross-context-access)
- [SEC-10 — Server-side requests, redirects and egress](#sec-10--server-side-requests-redirects-and-egress)
- [SEC-11 — Parsers, deserialization and XML](#sec-11--parsers-deserialization-and-xml)
- [SEC-12 — Files, paths, uploads and archives](#sec-12--files-paths-uploads-and-archives)
- [SEC-13 — API, proxy and message boundaries](#sec-13--api-proxy-and-message-boundaries)
- [SEC-14 — Secrets and service credentials](#sec-14--secrets-and-service-credentials)
- [SEC-15 — Cryptography, key use and password storage](#sec-15--cryptography-key-use-and-password-storage)
- [SEC-16 — Transport and peer authentication](#sec-16--transport-and-peer-authentication)
- [SEC-17 — Sensitive data and lifecycle exposure](#sec-17--sensitive-data-and-lifecycle-exposure)
- [SEC-18 — Dependencies and supply-chain exposure](#sec-18--dependencies-and-supply-chain-exposure)
- [SEC-19 — Configuration and privileged attack surface](#sec-19--configuration-and-privileged-attack-surface)
- [SEC-20 — Resource exhaustion and denial of service](#sec-20--resource-exhaustion-and-denial-of-service)
- [SEC-21 — Business abuse, concurrency and replay](#sec-21--business-abuse-concurrency-and-replay)
- [SEC-22 — Security events, errors and failed controls](#sec-22--security-events-errors-and-failed-controls)
- [SEC-23 — AI, retrieval and tool authority](#sec-23--ai-retrieval-and-tool-authority)
- [SEC-24 — Native memory and unsafe runtime boundaries](#sec-24--native-memory-and-unsafe-runtime-boundaries)
- [Verification](#verification)
- [Stack-specific reasoning examples](#stack-specific-reasoning-examples)
- [Responsibilities and exceptions](#responsibilities-and-exceptions)
- [Ownership, review, and related policy](#ownership-review-and-related-policy)

## Purpose and scope

The Security Reviewer assesses whether an attacker can cross an intended boundary, disclose or alter protected data, impersonate an actor, misuse a business operation or exhaust a protected resource. Apply this Technical Standard (STD) to assigned components, flows and selected criteria. It supports web applications and services, with conditional methods for native code and AI features. It is not a penetration test, a complete product-security certification or authorization to probe a deployed system.

The [Security Policy (POL)](../policies/security.md) governs judgment and exceptions. The team-owned [Review scope and criteria](../intent_context.md#review-scope-and-criteria) establishes applicable project rules, package defaults, replacements and waivers. The shared [Review Technical Standard (STD)](../review_standard.md) owns evidence, severity, finding guidance and developer responses. This catalogue does not create another routing map or report schema.

The `SEC-01`–`SEC-24` controls are package-designed review obligations. Primary sources support the mechanisms identified below; they do not establish a project's authority, exposure, runtime configuration or numerical limits. The research record maps selected ASVS 5.0.0 requirements; this catalogue does not implement every ASVS requirement or verification level. If the project adopts ASVS, capture the exact requirement text, version and level as criteria; use the shared exception procedure for any departure. All defective and safe examples are hypothetical. A safe example establishes only the stated boundary under its stated assumptions.

## Definitions

- An **asset** is data, capability, identity, money or availability with a protection need.
- An **actor** is a person, service or process with identified capabilities and permissions. An authenticated actor can still be unauthorized for an operation.
- A **trust boundary** is where data, identity or authority moves between differently trusted contexts. A process or directory boundary does not by itself enforce trust.
- A **sensitive operation** reads protected data, changes protected state, executes instructions, invokes another system or spends constrained resources.
- **Attacker control** identifies exactly which bytes, values, timing, identity or repeated actions the actor can influence.
- A **security invariant** is a protection property that must hold through the assigned flow, including applicable error and recovery paths.
- **Validation** checks whether data fits an expected structure or meaning. **Parameter binding**, **output encoding**, **sanitization**, **authorization** and **resource bounds** solve different problems; none is a universal substitute for the others.
- A **package default** is a selected applicable engineering control. A **project parameter** supplies its actual stack/version, contract, trust assumptions, limits or risk conditions. An unknown parameter remains unknown.
- **Reachability** means evidence connects the actor's permitted entry to the affected behavior. A dependency name, scanner label, risky API or matching text alone does not establish reachability or exploitation.

## Principles

Start with the protected operation and the actor's capabilities. Trace actual input, identity and state across boundaries, including alternate callers, asynchronous work and cached results. Inspect where protection is enforced, not merely where an object is created or a check is declared.

Use the actual framework, library, protocol and deployment version. Prefer maintained protection mechanisms used in their documented context. A generic sanitizer, signature, private network, opaque identifier or model instruction does not establish every required property.

Separate an evidenced defect, a supported risk or improvement, and a question whose outcome depends on missing facts. A missing project security document does not excuse relevant technical checks; a missing optional filename is not itself a vulnerability. Unknown global capacity limits do not prevent reporting a captured unbounded operation with a supported exhaustion mechanism.

A defense must preserve intended legitimate behavior. Explain costs such as false rejections, lockout abuse, recovery friction, stale authorization or additional operational work. Do not hide a demonstrated contradiction behind a phase label or an unverified claim that another layer handles it.

## Applicability and phases

Read the complete control list in Contents for an assigned Security scope. Select applicable controls and record reasoned exclusions or needed facts. Review the affected entries in full. A narrow task needs a bounded record, not a mandatory full-system assessment.

| Phase | Investigation depth |
| --- | --- |
| Foundation | Identify actual trust boundaries, protected operations and data. Inspect applicable injection, access, secret, parser and resource protections from their first use. A local library does not acquire web-session requirements merely because this catalogue contains them. |
| Production launch | Include real identities, tenant boundaries, recovery, credential handling, deployment exposure, external dependencies, security events and supported clients. Record unavailable runtime evidence. |
| Growth | Extend to shared quotas, noisy tenants, bulk operations, asynchronous authorization, fleet/version variation, replay, distributed abuse and operational evidence. |
| Advanced scale or criticality | Examine consequential authority changes, correlated failures, high-value transactions, provider compromise, key lifecycle and recovery under the actual threat and commitments. Select stronger assurance where justified; do not impose a universal infrastructure stack. |

Public exposure, multiple tenants, sensitive data, privileged tools, payments, irreversible effects, attacker-controlled files and costly operations activate their relevant checks at any phase. Actual requirements determine authentication strength, retention, availability and quantitative budgets. Phase is not an ASVS level and cannot waive an applicable obligation. Regulatory applicability belongs to established project obligations and the Compliance Reviewer.

## Rules

### SEC-01 — Assets, threats and trust boundaries

Establish protected assets, actors and allowed operations before selecting controls or claiming impact. Deepen analysis when identities, sensitive data, external services or privileged actions change.

- Map actors, actions and objects using actual exposure, trusted components, deployment assumptions and the supplied Threat Model (TM). Include relevant anonymous, cross-user, cross-tenant and service actors.
- Follow changed flows through entries, state, outputs and external calls. Compare supplied threats with those paths; label reconstructed assumptions and route material uncertainty through the lead.
- Cite the flow, asset, trust boundary, selected controls and exact missing facts affecting the comparison. A clean conclusion covers the selected boundary, not every hypothetical attacker.

An export worker's privileged database identity does not authorize tenant-local IDs submitted through its public API. Trace the originating actor, tenant and object through enqueue, execution and download to the access check. Security owns threat applicability; Architecture supplies topology and Compliance established obligations. Reconstruction is not an approved Threat Model (TM).

### SEC-02 — Authentication, enrollment and recovery

Protected operations must use the required authentication and recovery assurance. A weaker alternate route must not grant stronger privileges; intentionally public information endpoints can remain unauthenticated.

- Establish accepted methods/strength, public/protected operations, account lifecycle, recovery authority, provider/library version and abuse limits. Cover registration, invitations, verification, sign-in, password/passkey/MFA changes, recovery, account linking and administrative identity.
- Trace these paths to the resulting identity. Check credential comparison, default accounts, one-time material reuse, enumeration through messages/timing, brute-force defenses and malicious lockout.
- Require applicable existing assurance before changing recovery details. Verify server-side factor/step-up decisions and failure paths.
- Cite identity transitions, verifier calls/configuration and challenge lifecycle, with negative and legitimate recovery cases.

Recovery must not accept an unverified replacement email and issue a full session for an account requiring a second factor. Prove the established account relationship, apply recorded recovery assurance and grant only authorized permissions. Security owns assurance and abuse; Code supplies implementation and Design usability. Do not invent an RBAC model, identity provider or fixed password/session lifetime.

### SEC-03 — Authorization, tenant isolation and delegated access

Every protected function, object and field must enforce the actor's action permission in its current context, including alternate paths.

- Establish tenant membership and its trusted source, actor/action/object/field rules, entitlement timing, delegated authority, revocation and intended cross-tenant administration.
- Trace identity to enforcement before reads/writes, administrative effects, exports and delegated calls. Inspect storage predicates, object retrieval, serializers, writable-field allowlists, mass assignment, tenant switching, cache identity and queued context.
- Check horizontal/vertical privilege changes, stale membership/entitlements and confused-deputy use of service identities. Include direct APIs, alternate versions and workers.
- Cite the access matrix and enforcement locations. Compare denied cross-user/tenant cases with authorized cases, including cache and asynchronous-consumer behavior.

A cache keyed only by `item_id` can return tenant A's bytes to tenant B before a tenant-scoped query runs. Include verified tenant and other required authorization dimensions in the lookup; the returned object must still satisfy action permission. Opaque IDs, UI restrictions and authentication alone are insufficient. Security owns access judgment; Database supplies storage enforcement and Architecture context propagation. RBAC, ABAC and relationship rules depend on the project. Tenant-cache and export cases remain in scope.

### SEC-04 — Sessions, cookies and revocation

Sessions must stay bound to their actor and assurance for the permitted lifetime, then stop granting access under the applicable termination rule.

- Establish token mechanism/entropy, cookie/client storage needs, inactivity/absolute limits, concurrency rules and revocation across consumers. Include refresh/logout, account disablement and privilege changes.
- Trace issuance, fixation resistance, authentication changes, renewal, expiry and invalidation at the verifier. Check refresh replay and lost/disabled accounts, including sockets and jobs authorized by sessions.
- Inspect cookie scope, `Secure`, `HttpOnly` when script access is unnecessary, purpose-appropriate `SameSite`, and exposure in URLs, browser storage or logs.
- Cite lifecycle/verifier paths, token/cookie configuration, lifetime rationale and termination cases.

Deleting a browser cookie does not reject a copied credential. An immediate-logout contract needs enforcement across relevant consumers through server state or the chosen validation mechanism. Security owns session trust; Code implements transitions. Choose supported lifetimes with their usability/recovery costs; do not prescribe JWT or cookies where another mechanism fits.

### SEC-05 — Federation, OAuth and token validation

Before token claims authorize an action, establish issuer, recipient, purpose and transaction. A valid signature alone is insufficient.

- For OAuth/OIDC/SAML, self-contained tokens, multiple providers and external login, establish protocol/profile and library version, client type, issuer/audience, key sources, grant flow, scopes, time/replay checks and linking rules.
- Inspect verification rather than decoding/creation: allowed algorithms, trusted keys, issuer/audience, token type, expiry/not-before and replay defenses.
- For OAuth, check exact redirect registration, transaction-bound PKCE/state/nonce where applicable, code reuse, mix-up defense and refresh replay. Evaluate public-client refresh protection and PKCE under the selected profile.
- Check issuer-plus-subject identity and deliberate linking; an arbitrary provider's email claim does not prove account ownership. Read primary protocol guidance before asserting unexamined SAML or other profile details.
- Cite relying-party/resource-server configuration, key-trust binding, permitted grant and invalid-token cases. Do not assume undocumented library defaults.

An API must not accept an ID token issued for another client merely because its JWT signature verifies. Enforce token class, issuer, audience, time and claims before separate resource authorization. Security owns protocol trust; Code and DevOps supply library/provider settings.

### SEC-06 — Input meaning, canonicalization and object construction

The representation used for a security decision must match the next consumer's interpretation. Untrusted data and object construction must not introduce authority, types or properties beyond the intended contract.

- Establish schema, permitted fields/types/ranges, encoding/normalization, parser limits and framework object semantics.
- Compare parsing, canonicalization, validation and final use. Inspect duplicate-field precedence, missing/null values, numeric boundaries, strict comparisons and unexpected objects/arrays. For JavaScript, check prototype-affecting merges and security-property lookup.
- Reject or safely handle invalid data before it affects the operation. Enforce size/depth limits before expensive parsing, not merely after schema validation.
- Cite transformations, schema and decision use, including malformed/ambiguous input and valid Unicode. Valid identifiers still need authorization; strings still need sink-specific protection.

An object accepted as a username can become a query operator. Require the intended bounded scalar, construct an application-owned query and enforce access separately. Security owns hostile-input consequences; Code contributes type/contract correctness. Do not strip ordinary punctuation or impose one normalization rule on every language/name field.

### SEC-07 — Interpreter and query injection

Untrusted data must not become unintended instructions. Establish the actual interpreter/API, trusted structural tokens, field/operator permissions, encoding context and database/process privileges.

- Trace immediate and stored input to SQL/HQL/NoSQL/Cypher, commands, LDAP, XPath, templates, dynamic code, regex, mail/headers and spreadsheet output wherever used. Verify value binding separately from dynamic structure, including raw ORM paths and stored-procedure SQL.
- Distinguish shell strings from separate arguments; validate executable, options and operands. LDAP filter and distinguished-name contexts require their respective encoding. Keep template data separate from source.
- Assess spreadsheet formula interpretation in the actual consumer, not just CSV syntax. Check regex-data escaping separately from execution cost under SEC-20.
- Cite the input-to-sink path, API/version semantics, permitted structural choices and a distinguishing nonexecuted example. A risky method name without attacker control is not an exploit.

Interpolating user values into SQL before `execute`, or into template source, can cross the instruction boundary. Bind SQL values with trusted structural choices; pass text into fixed templates with appropriate output protection. See the stack examples. Validation, an ORM name or shell escaping alone does not prove safety. Security owns injection; Database supplies stored-language details and Code API use.

### SEC-08 — Browser output and cross-site scripting

Browser output must not grant unintended script or document authority. Match protection to every parser, using the actual framework/version, permitted rich content and supported browsers.

- Trace reflected, stored and DOM-derived data into HTML, attributes, URLs, script/style content, DOM writes, rich text, Markdown/SVG and client templates.
- Inspect framework escape hatches, raw HTML, URL schemes and post-sanitization mutation. Use safe text APIs for text, context-appropriate encoding for syntax and maintained sanitization for permitted markup.
- Check compound HTML/JavaScript contexts. Content Security Policy (CSP) and similar defenses do not replace correction of unsafe sinks.
- Cite rendering paths and encoder/sanitizer configuration with hostile-markup and legitimate-text cases. Distinguish server-side template execution from browser execution.

`element.innerHTML = comment` interprets a comment as markup. An ordinary text element can use `textContent`; permitted HTML needs configured sanitization. `textContent` on a script element is not safe text display. Security owns script-execution risk; Code and Design supply framework/UI behavior.

### SEC-09 — Browser origins, CSRF and cross-context access

An unintended origin must not use browser credentials or cross-origin capabilities to trigger protected actions or read protected results.

- Establish trusted origins, credentials, embedding/messaging permissions, supported clients and CSRF defenses for cookie actions, CORS, embedded content, `postMessage`, redirects and cross-origin loads.
- Trace untrusted-origin requests through credential attachment and server enforcement. Inspect state-changing methods, framework CSRF integration or justified equivalents, Origin/Fetch Metadata handling and fallbacks.
- Check credentialed CORS allowlists, preflight bypasses, exact message-origin checks, frame restrictions and relevant response headers. Distinguish cross-site from same-site subdomain trust.
- Cite request/response flow and origin configuration, including alternate content types and legitimate integrations.

An ordinary cross-origin form must not mutate a cookie-authenticated setting without effective anti-forgery enforcement. Validate context before mutation and permit only intended integrations. Security owns origin trust. CORS is not API authorization; `SameSite` alone does not universally prevent CSRF. Headers depend on the feature/browser contract.

### SEC-10 — Server-side requests, redirects and egress

User-influenced destinations must stay within intended network reach and receive only intended credentials and access.

- For URL fetches, previews, webhooks, imports, identity metadata, proxies and redirects, establish fixed partners versus public-fetch features, schemes/ports, address families, resolver/client behavior, redirects, credentials and permitted internal services.
- Trace parsing, DNS, connection and redirects through actual libraries/proxies. Check IPv4/IPv6 and alternate encodings, resolution changes, loopback/link-local/internal destinations, forwarded credentials and response use.
- Validate fixed partner sets where present. Public-fetch features need suitable isolation and destination/network restrictions. Revalidate redirects or disable them; inspect open redirects affecting phishing or credential flows.
- Cite enforcement across resolution, connection and redirects, a permitted fetch case and sensitive-destination reachability or explicit uncertainty.

A once-checked webhook URL can redirect to a restricted internal endpoint while carrying authorization headers. Enforce destination/credential policy at each connection/redirect, with appropriate egress restrictions. Security owns SSRF and credential exposure; DevOps supplies network evidence. Hostname substrings or initial DNS checks alone are insufficient. Unknown reachability limits impact claims.

### SEC-11 — Parsers, deserialization and XML

Untrusted content must not select executable object behavior, external resources or unsafe features beyond its intended data format.

- For serialization, XML, YAML, document conversion, binary formats and parser chains, establish exact loader/version, permitted types, external-resource needs, schema/transformer settings and resource limits.
- Follow initial and secondary reads. Check object construction/hooks, permitted types and parser inconsistencies. For XML, include entities/DTDs, XInclude, schemas and stylesheets where relevant; unsupported security settings must fail safely.
- Enforce depth, expansion and size limits before and during parsing. Cryptographic authenticity helps only if producer/key authority is trusted for the deserializer's full capability.
- Cite loader/configuration and producer trust, with rejected unsafe features and legitimate-format cases. Distinguish code execution, exhaustion and external-fetch consequences.

Base64 does not make uploads safe for `pickle.loads`. A bounded data-only format with schema validation avoids arbitrary object reconstruction for that input. Likewise, `safe_load` is insufficient if custom constructors restore executable behavior. Security owns parser abuse; Code supplies implementation.

### SEC-12 — Files, paths, uploads and archives

User-controlled files and names must not escape authorized storage, become executable content or expose another actor's data.

- For upload/download, temporary files, archives, document/image processing and filesystem access, establish permitted content, storage roots, owner/tenant rules, serving behavior, privileges, size/expanded-size/count limits and symlink policy.
- Trace names/metadata through canonicalization into actual filesystem operations. Check traversal, absolute paths, relevant symlinks/hard links, overwrite/TOCTOU, archive entries and temporary permissions.
- Compare declared type with inspected content and serving behavior. Check quarantine/scanning where required, failure cleanup, download authorization and safe filename/content response headers. Apply SEC-20 to amplification.
- Cite the effective path/root boundary, access identity and processing/serving configuration, with legitimate and rejected files.

Joining an archive entry to a destination does not constrain the actual write. Enforce entry/link rules there, prevent unauthorized overwrite and process permitted content under bounded privileges. Security owns file abuse; Code and DevOps supply filesystem/runtime semantics. Extensions/MIME alone are insufficient; antivirus does not establish harmlessness.

### SEC-13 — API, proxy and message boundaries

Parsers and intermediaries must agree on message identity, framing and trusted metadata before those values affect protected operations.

- Establish protocol/version, actual proxy chain, trusted forwarded headers, methods/content types, schema and per-message authorization for gateways, proxies, GraphQL, WebSocket, RPC, webhooks and alternate APIs. Deepen analysis with multiple intermediaries.
- Inspect forwarded identity/client addresses, duplicate fields and framing at each hop. Direct backend access must not bypass gateway protection. Include reachable old and administrative APIs.
- Check WebSocket handshake origin/identity and message-level access/limits; GraphQL field/resolver authorization and cost; webhook signatures over correct bytes, trusted keys/sources, replay and event-to-action mapping.
- Cite routing/configuration, parser behavior and message contracts with alternate-hop/version and valid-client cases. Use the other controls for token, input, replay and cost details.

A caller-supplied `X-User-ID` forwarded unchanged is not authenticated identity. Accept trusted metadata only from a verified intermediary, remove untrusted copies and enforce application authorization. Security owns boundary bypass; DevOps supplies deployment paths and Code protocol use. REST guidance does not define every RPC/streaming protocol; read its actual specification.

### SEC-14 — Secrets and service credentials

Credentials must reach only intended holders and work only within their intended scope and lifetime. Deleting a source literal does not complete their lifecycle.

- Establish purpose, consumers, access, exposure, rotation/revocation and recovery for API/database credentials, signing secrets, certificates/private keys, CI variables and service identities.
- Trace provisioning, scoped access, use, rotation, revocation and failures through references, configuration and redacted evidence. Inspect source/build/log/client exposure, environment injection, inherited processes, crash dumps and build-time substitution where relevant.
- Check default/shared privileged credentials and whether short-lived credentials or workload identity fit the integration. Distinguish public certificates from private keys.
- Cite locations, provenance/access metadata, scope, lifecycle and exposure consequences without values. Distinguish known dummy fixtures from apparent credentials using captured provenance; neither infer validity nor test credentials.

CI substitution can put a backend secret into a public frontend bundle. Send browsers only intended public configuration; provision backend credentials with controlled, narrow authority. Security owns misuse; DevOps supplies provisioning and Database permissions. Do not read live secrets. A vault or environment variable alone does not prove secure access.

### SEC-15 — Cryptography, key use and password storage

Use suitable maintained cryptographic implementations to protect the intended property, with correct key, nonce and failure lifecycles.

- For passwords, encryption, signatures/MACs, random tokens, derivation and migrations, establish confidentiality/integrity/authentication needs, data lifetime, algorithm/library version, key source/scope, nonce rules, hash costs and actual compliance constraints.
- Determine what remains exposed. Check ciphertext authentication, nonce/IV use, randomness, key separation/replacement, verification order, timing-sensitive comparisons and error oracles. Protect keys from the threat the encryption addresses.
- Inspect adaptive password hashing, unique salts, parameters and upgrades; distinguish human passwords from high-entropy lookup tokens. Verify current parameters for the selected mechanism.
- Cite primitives/configuration, key/nonce lifecycle, integrity checks and failure paths, with contrasting misuse/safe cases. Configuration alone does not prove production key custody.

Unsalted fast hashes expose passwords to efficient guessing. Reusing a nonce with the same key after a deployment-counter reset is a separate defect when the algorithm requires nonce uniqueness. Use suitable password-hash salts/costs and preserve algorithm-specific nonce requirements across restarts/replicas. Security owns judgment; Code and DevOps supply implementation/custody facts. Do not prescribe custom crypto, arbitrary algorithms or automatic FIPS/post-quantum obligations.

### SEC-16 — Transport and peer authentication

Sensitive communication must preserve confidentiality/integrity against the relevant network attacker and authenticate the intended peer. Encryption alone is insufficient.

- Cover browser/API, service, database, management, monitoring and provider connections carrying protected data or authority. Establish hops/termination, protocol/client/server versions, trust stores, hostname identity, TLS policy and client-authentication needs.
- Trace sender to final consumer, including proxy termination and internal continuation. Check certificates/hostnames, trust sources, downgrade/fallback, obsolete protocols/ciphers, client certificates where used and failure behavior.
- Check whether TLS early data can replay a non-idempotent action. Cite connection/validation settings, intended identity and failure paths; distinguish repository configuration from deployed observations with their environment/time.

Disabling certificate verification can let an untrusted endpoint impersonate a payment provider under the modeled threat. Validate against established trust and reject mismatched/untrusted peers without insecure retry. Security owns peer trust; DevOps supplies termination/network evidence. Private networks alone do not authenticate peers; do not require a universal service mesh or public CA for an intentionally private trust domain.

### SEC-17 — Sensitive data and lifecycle exposure

Data must reach only intended recipients and remain protected through copies, caches, exports, client state and disposition.

- Establish classes, recipients/uses, tenant ownership, permitted fields, retention/deletion obligations and external processors for personal/confidential data, credentials, telemetry, caches, browser storage and backups.
- Trace collection into responses, logs, analytics, browser/server/CDN caches, derived copies and supported deletion/restoration. Inspect excess fields, URL/query leakage, debug/error output, cache keys/policies, metadata and temporary artifacts.
- Compare disclosure/retention with established rules. Coordinate persistence/recovery facts without inventing legal deadlines. Cite bounded data/copy flows, actual recipients/exposure, applicable requirements and legitimate output cases.

A public-profile serializer must not return private recovery fields from the account object. Select permitted fields, preserve recipient boundaries in caches and apply established lifecycle rules to other copies. Security owns exposure; Compliance establishes obligations, Database persistence and Architecture lifecycle coordination. Encryption at rest does not prevent an authorized application disclosing plaintext.

### SEC-18 — Dependencies and supply-chain exposure

Consumed code/artifacts must come from intended sources. Assess known weaknesses against actual versions, configuration and exposure.

- Establish direct/transitive versions or digests, repositories, build/runtime inclusion, update obligations, advisories and integrity/provenance for dependencies, lockfiles, build plugins/actions, images, generated/client assets and registries.
- Resolve actual consumption, including lockfile ranges, vendored code, privileged development tools and downloads. Check dependency confusion, untrusted install/build scripts, artifact substitution and trust in verification keys/identities.
- Read maintainer/CNA advisories for affected ranges, features/configuration and remediation. Trace exposure or retain unknowns; unproven runtime reachability does not waive an applicable vulnerable-version obligation.
- Cite inventory/resolution, advisory/version comparisons, callers/configuration, integrity verification and residual uncertainty.

Executing an untrusted mutable download with release credentials violates a boundary limited to an established publisher. Verify publisher/version through a trusted mechanism, scope build authority and assess applicable advisories. Security owns compromise/exposure judgment; DevOps contributes provenance and Compliance licenses. An old version, CVE label, lockfile or signature alone proves neither exploitability nor trust.

### SEC-19 — Configuration and privileged attack surface

Deployed administration, diagnostics and execution capabilities must be available only to intended actors.

- Establish exposure, administrative identities, environment settings, operating/runtime versions and isolation for production defaults, debug/management endpoints, listeners, containers, filesystem privileges and service permissions.
- Inspect public/internal routes, debug consoles, metrics/docs, source-control/config artifacts, default accounts and privileged operations. Check actual caller access/permissions; a private hostname is insufficient.
- Check threat-relevant sandbox/container/process boundaries, mounts/capabilities/credentials and fail-open settings. Request DevOps deployment evidence when source settings are inconclusive.
- Cite features/configuration, reachability or bounded assumptions, required privileges and unauthorized/legitimate administration cases.

An interactive production debugger reachable by ordinary users can grant privileged execution. Exclude it from production or enforce the actual restricted administrative boundary. Security owns unauthorized exposure; DevOps owns the full infrastructure/release assessment. No universal container platform, private-only backend or network product is required.

### SEC-20 — Resource exhaustion and denial of service

Input, repetition and fan-out must not obtain uncontrolled resources or paid services beyond intended availability/cost boundaries.

- Establish size/expanded-size, depth/cardinality, query cost, execution/wait time, concurrency, queue/storage/provider quotas, trusted identity and workload/availability commitments. Cover public/tenant parsing, uploads, expensive queries/regex, pagination/bulk work, streams, external calls, queues and AI loops.
- Trace single and repeated/concurrent requests through buffering, parsing, CPU, allocation, database/network work, retries/fan-out and retained state. Check pre-allocation and streaming/decompression limits, regex worst cases, image dimensions, GraphQL depth/amount/cost, pagination and batches.
- Inspect per-actor/tenant and shared limits, distributed counters, cancellation, cleanup, backpressure and recovery. Rejection can itself produce costly work/logs; rate limiting cannot cure one unbounded request.
- Cite amplification/resource paths, enforced bounds and provenance, attacker capability and supported consequences. Quantitative outage claims need measurements; bounded reasoning can establish an unbounded mechanism.

An archive can pass an upload limit yet exhaust storage during expansion. Enforce expanded-byte/count/time budgets while extracting, clean partial state and bound concurrent work under actual tenant/shared policy. Security owns adversarial availability; Performance supplies measurements, DevOps volumetric/network mitigation and Architecture isolation. Do not invent requests-per-second targets, mandate universal CAPTCHA or run DoS probes.

### SEC-21 — Business abuse, concurrency and replay

Permitted individual actions must not combine into unauthorized economic, entitlement or state outcomes through repetition, reordering or concurrency.

- For payments, refunds, coupons, invitations, quotas, transitions, approvals, webhooks and retries, establish authoritative values, sequence, actor/tenant/operation binding, one-time/repeated semantics, concurrency guarantees and permitted recovery outcomes.
- Reconstruct server invariants. Check skipped steps, manipulated price/role/state, reused proofs, check-and-write races and replayed events. Inspect idempotency scope, canonical request binding, uniqueness/atomic updates and external-effect uncertainty.
- Approvals must cover actual action, target, parameters and authority; caller-supplied approval flags are insufficient. Preserve legitimate retries/recovery.
- Cite concrete sequences/interleavings, trusted state, consequences and corrected/legitimate counterparts. Obtain Database/Architecture evidence for storage/distributed guarantees.

Two requests can both grant an unused credit before either marks it used. Reserve/consume atomically under the verified store contract and reconcile permitted retries. Security owns abuse; Code contributes local correctness and Database/Architecture atomicity. Lost payment notification alone does not prove duplicate payment; use Architecture's fault-window method for that claim.

### SEC-22 — Security events, errors and failed controls

Security actions/failures must remain attributable without leaking protected data or granting unauthorized capability when a control fails.

- Establish events/recipients, actor/tenant/correlation fields, redaction, access/retention, failure behavior and actual response for authentication/access decisions, privileged changes, suspicious input, security exceptions, logs/telemetry and errors.
- Trace events into supplied sinks/consumers. Inspect untrusted-field encoding, trusted identity/time, sensitive values, log injection, access/tamper exposure and excessive logging cost.
- Follow denied/unavailable policy, key, identity and logging services through exception handling. Distinguish unauthorized effects from reduced observability; a logging outage need not halt every operation.
- Cite event/error paths and fields, protected output, failure behavior and actual monitoring evidence. Emitting messages does not prove alerting works.

Converting authorization-service exceptions to `allowed = true` while logging bearer tokens compounds access and disclosure failures. Follow the supported secure failure path, retain redacted attributable events and return nonsensitive errors. Security owns event meaning; DevOps supplies delivery/alert response and Compliance audit obligations. Do not reproduce secrets or infer nonrepudiation from ordinary logs.

### SEC-23 — AI, retrieval and tool authority

Untrusted text/model output must not gain permission to access another actor's data, invoke privileged tools or spend beyond the authorized task.

- Establish actor/task authority, tools/resources/actions, retrieval/memory tenancy, model/provider version, recipients, budget/loop limits and approval scope for prompts, vector stores, agent memory, tools/MCP, generated code/output and autonomous loops.
- Trace direct/indirect instructions from documents, tool results and retrieval into actions/outputs. Check authorization outside model text, exact targets/arguments, rendering/query/command sinks, retrieval filters/post-retrieval access, shared memory/poisoning and sensitive context/telemetry.
- Bound recursive delegation, loops and token/cost use. Required approval must cover the actual actor/action and resist replay after parameter changes.
- Cite tool-authority boundaries, data partitions and execution controls with malicious-content/legitimate-data cases and explicit model uncertainty. Delimiters/filters do not prove isolation.

A retrieved document must not make a tool send another tenant's records to an external URL. Retrieval/execution must independently enforce actor, tenant and recipient boundaries, with bounded repeated work. Security owns hostile-instruction/authority abuse; Code/Architecture supply execution details, DevOps deployment and Compliance data use. One refusal does not prove prompt-injection resistance. No new host or exploitation authority follows.

### SEC-24 — Native memory and unsafe runtime boundaries

Native/unsafe code reached by untrusted input must preserve memory, type and resource safety across calculations, ownership and foreign-function boundaries.

- Cover C/C++, unsafe Rust, FFI, native extensions, binary parsers and manually managed memory. Establish language/compiler/ABI and dependency versions, lengths/ranges, allocation/ownership, sandbox/hardening and actual attack entry.
- Trace attacker-controlled lengths, indices and conversions before allocation/copy. Check bounds, overflow, use-after-free, double-free, uninitialized data, format strings, ownership across threads/FFI, cleanup and mitigations.
- Read actual language/library contracts before asserting undefined behavior or exploitation. For integer arithmetic, establish the actual promotion rules, widths and signedness before claiming evaluation overflow; distinguish a demonstrated narrowing conversion from overflow that depends on an unspecified target ABI. Sanitizer/fuzz results cover only captured scope. Cite the reachable operation, size/lifetime relationship, API semantics and distinguishing boundary case; corruption alone does not prove arbitrary execution.

An image wrapper can allocate using overflowed width-times-height, then copy full decoded pixels into the smaller buffer. Checked arithmetic/bounds must establish allocation-versus-copy sizes with correct ownership and failure cleanup. Security owns hostile impact; Code contributes language correctness and Testing evidence. A managed language does not make native extensions safe; sanitizer success does not cover all inputs.

## Verification

Each control states the investigation and evidence needed to assess it. Return supported findings with relevant requirements, control references, inspected locations and limitations. Explain attacker control, preconditions, protective checks, reachable consequence, focused correction and a verification that distinguishes faulty from corrected behavior. Inspect a plausible safe counterexample before finalizing a finding. A tool's warning must be checked against its actual version/configuration and the captured flow.

Use available source, configuration and supplied execution evidence within the assignment. Review does not authorize exploitation, fuzzing, load generation, dependency installation, live credential use, access to other accounts or production queries. Propose a bounded later check when execution is needed and unavailable. Retain failed and unperformed checks distinctly. A missing security requirement cannot be filled with an invented organizational approval or numeric threshold.

### Stack-specific reasoning examples

These fragments illustrate one control distinction; they are not complete application code or executed tests. Their omitted authorization, error and resource checks still apply. Verify the actual target's version before using them as an analogy.

| Context | Defective pattern | Compatible safer pattern and remaining checks |
| --- | --- | --- |
| Python 3.14 `sqlite3` | `db.execute(f"SELECT id FROM accounts WHERE name = '{name}'")` constructs SQL syntax from a value. | `db.execute("SELECT id FROM accounts WHERE name = ?", (name,))` binds that value. Select structural identifiers from trusted mappings and separately enforce account/tenant authorization. |
| JavaScript with a MongoDB-style driver | `{name: request.body.name}` accepts an object where a scalar was intended; driver query objects alone do not prevent operator injection. | Require the intended string/type and field rules before constructing `{name}`. Do not accept arbitrary client query operators; the specific driver contract still needs verification. |
| Browser DOM | `element.innerHTML = comment` interprets a comment as markup. | For an ordinary text element, `element.textContent = comment` inserts text. Rich content and script/style elements require different handling. |
| Python 3.14 `pickle` | `pickle.loads(uploaded_bytes)` grants an untrusted producer object-execution capability. | Use a bounded data-only representation and validate its schema; format conversion alone does not impose resource or authorization limits. |
| OS process API | Passing a user value as a separate argument prevents shell parsing only if the API truly bypasses the shell; it can still become an option or dangerous operand. | Fix the executable, validate argument meaning, use documented option termination where applicable, and enforce destination/file permissions. No universal `shell=False` claim is made for every platform/API. |

## Responsibilities and exceptions

Security owns vulnerability, trust-boundary, adversarial-access and abuse judgments. Architecture owns structural failure propagation; Code local implementation; Database store/transaction semantics; DevOps deployment, delivery and operational evidence; Performance measurement/capacity; Testing verification quality; Compliance established legal/license obligations; Design user interaction. These contributors do not authorize this leaf to delegate. The lead assigns actually available roles, consolidates shared findings and retains unperformed handoffs as coverage limits.

Use the Security Policy (POL) and the assignment’s Review scope and criteria section for supplements, replacements and waivers, including whole-domain replacement. Apply the effective captured rule rather than secretly judging against a displaced default. A waiver does not change facts or erase a contradiction. No exception can grant this reviewer live exploitation, secret access, target edits or permission to falsify evidence. The team-owned developer handoff and re-review contract remains unchanged.

## Ownership, review, and related policy

The package maintainer owns this catalogue and revisits affected controls when source guidance, supported mechanisms, observed review failures or agreed domain boundaries change. Capture the version and relevant guidance with each review. Living sources require a fresh check when an actual conclusion depends on their current advice. Never claim universal security coverage from this catalogue's length or a clean returned report.

## Research reference

[Sources and control mappings](../research/security.md) support maintenance and source verification. Load them only when needed; apply the controls and version qualifications in this standard during routine review.
