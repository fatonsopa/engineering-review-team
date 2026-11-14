# Localization review standard

Package default governed by the [Localization Policy (POL)](../policies/localization.md) and shared authority procedure. Select applicable controls; this is not a requirement to support every language or feature.

## Purpose and scope

Assess text preservation, messages, locale-sensitive behavior and delivery in changed software. Follow established project support and value contracts. For small or single-language work, check relevant text/data behavior without requiring unused localization infrastructure. Expand coverage for actual multilingual journeys and consequential values, regardless of traffic volume.

## Definitions

- A **language tag** identifies language and optional script/region subtags. A **locale** supplies conventions; currency and time zone remain separate facts.
- An **instant** identifies a point on the timeline. A **civil date** has no time zone; a **wall time** needs contextual rules to identify an instant. An offset is not a complete time-zone rule set.
- A **grapheme cluster** approximates a user-perceived character. Bytes, code units and code points are different units.
- **Message fallback** is the product's lookup behavior. **Locale-data inheritance** supplies formatter data and does not define that product behavior.
- **Pseudolocalization** transforms text to expose engineering assumptions; it is not a natural-language translation or linguistic approval.

## Principles

Preserve meaning and established identity rules. Follow the actual stack, message dialect and locale-data version where behavior depends on them. Distinguish product decisions from technical defaults, safe alternatives from defects, and observed results from source-supported analysis. Keep source/version support in the [research record](../research/localization.md).

## Control index

- [LOC-01 — Applicable locale behavior](#loc-01-applicable-locale-behavior)
- [LOC-02 — Localizable messages](#loc-02-localizable-messages)
- [LOC-03 — Unicode preservation](#loc-03-unicode-preservation)
- [LOC-04 — Text identity](#loc-04-text-identity)
- [LOC-05 — Preferences and context](#loc-05-preferences-and-context)
- [LOC-06 — Numbers and money](#loc-06-numbers-and-money)
- [LOC-07 — Dates and times](#loc-07-dates-and-times)
- [LOC-08 — Message structure and interpolation](#loc-08-message-structure-and-interpolation)
- [LOC-09 — Plurals and ordinals](#loc-09-plurals-and-ordinals)
- [LOC-10 — Fallback behavior](#loc-10-fallback-behavior)
- [LOC-11 — Text fit and scripts](#loc-11-text-fit-and-scripts)
- [LOC-12 — Direction](#loc-12-direction)
- [LOC-13 — Sorting and search](#loc-13-sorting-and-search)
- [LOC-14 — Resource delivery and verification](#loc-14-resource-delivery-and-verification)
- [LOC-15 — Localized communications](#loc-15-localized-communications)
- [LOC-16 — Linguistic coverage](#loc-16-linguistic-coverage)

## Rules

### LOC-01: Applicable locale behavior

- Establish supported/planned languages, scripts, regions and channels, source/default language, runtime/resource versions and relevant product rules. Keep unknowns visible.
- Trace affected user-facing and machine-facing surfaces; inspect the actual support contract rather than inferring it from catalog filenames.
- Separate language, currency, time zone, calendar and numbering-system choices. Do not infer residence or financial currency from a language preference.

A deliberately single-language tool may have no translation catalog. Corrupting accepted Unicode user data is a separate concern.

### LOC-02: Localizable messages

- Where translation or readiness is required, trace changed visible messages and attributes through extraction, resources and delivered output. Include errors, loading/empty states, accessible names and generated communications when present.
- Inspect dynamic keys, generated text and dependencies that static extraction may miss. Preserve meaning/context where identical wording serves different purposes.
- Keep translatable messages complete enough to reorder arguments and grammar. Resource keys alone do not fix concatenated English-order fragments.
- Respect intentional fixed text, brands, protocol tokens and diagnostic identifiers under their contracts; do not require every literal to be translated.

Compare an affected message in a supported locale with its source and declared resource coverage. A catalog's existence does not prove completeness.

### LOC-03: Unicode preservation

- Trace accepted text through decoding, processing, transport, persistence, export and redisplay. Verify declared encodings match bytes and malformed input follows the contract.
- Check relevant non-Latin text, combining marks, supplementary-plane characters and joined emoji. Preserve supported content rather than silently replacing or dropping it.
- Distinguish byte, code-unit, code-point and grapheme limits. Display truncation, cursor movement or promised character counts need appropriate boundaries; protocol byte limits may remain byte limits with valid boundary handling.
- Inspect relevant shaping/font evidence separately. Unicode-capable storage does not prove glyph display.

An opaque byte limit can be valid. Cutting a UTF-16 surrogate pair while promising a complete display character is not equivalent behavior.

### LOC-04: Text identity

- Establish required equivalence before reviewing normalization, case conversion, search, matching or deduplication. Compare canonical variants and relevant locale-sensitive cases.
- Trace transforms and uniqueness checks across application/storage boundaries; retain original text where required.
- Do not normalize every string or apply compatibility normalization indiscriminately: it can erase meaningful distinctions.
- Preserve specified identity for opaque identifiers, signatures, passwords, hashes and protocol values. Display conventions cannot redefine those contracts.

Human-name search and byte-exact token validation may correctly use different comparison rules.

### LOC-05: Preferences and context

- Trace the project's actual precedence among explicit choice, tenant settings, request/browser preference and default. Verify negotiation, persistence and supported-locale handling.
- Check relevant conflicting choices, invalid/unsupported tags, anonymous/authenticated transitions and locale changes.
- Inspect concurrent requests, cache keys and asynchronous context where applicable; one user's locale must not silently become another's.
- Headers may initialize a preference but cannot establish currency, residence or time zone. Do not prescribe universal user-versus-tenant precedence.

Compare two affected recipients/requests with different preferences and the declared default or unavailable behavior.

### LOC-06: Numbers and money

- Trace raw value, currency/unit, locale and required precision into a suitable locale-aware formatter or justified equivalent. Formatting does not convert currency.
- Check relevant separators, grouping, signs, percentages, digits and currency fraction rules using supported locales, zero, negative and representative amounts.
- Keep stored values and transaction currency independent of display language; changing USD to EUR is not translating an amount.
- Where localized entry is accepted, inspect separators/digits, ambiguity and invalid input separately. A formatting API is not necessarily a parser.
- Preserve invariant machine-interchange syntax where required.

A French-language USD receipt can be correct; replacing only an English decimal point without handling grouping or ambiguity can change the value.

### LOC-07: Dates and times

- Identify each value as an instant, civil date, wall time, recurrence or duration before assessing conversions. Trace locale, calendar, time zone and hour cycle separately.
- Compare near-midnight instants in relevant zones. Preserve date-only meaning across zones rather than accidentally changing the day.
- Where scheduling changes, check daylight-saving gaps/overlaps and the established recurrence/disambiguation rule. A fixed offset is not a substitute for zone rules.
- Assess supported date input and ambiguity separately from formatting. Preserve machine serialization and duration semantics.

A birthday need not become a midnight instant. A scheduled local appointment may need an explicit rule for a repeated clock time.

### LOC-08: Message structure and interpolation

- Inspect complete messages, placeholder names/types, translator context, nested branches and the actual syntax/dialect. Permit grammatical reordering.
- Check changed resource parsing/compilation and representative apostrophes, braces, empty/long arguments and branch values through supplied evidence or separately authorized verification.
- Preserve safe treatment of values and translated markup in their rendering context; route injection analysis to Security rather than disabling escaping.
- Do not mandate ICU syntax for another suitable system or assume different MessageFormat generations/framework dialects are interchangeable.

Two valid fragments can form an invalid translated sentence. A correctly typed full-message argument permits another word order.

### LOC-09: Plurals and ordinals

- Use the supported locale's actual rules for cardinal and ordinal cases where used. Inspect applicable categories, explicit-number cases, defaults and offsets.
- Select distinguishing samples from runtime rules, not only 0/1/2. Include fractional or visible-decimal cases when the value domain permits them.
- Inspect the complete rendered message and formatted number; category `one` does not universally mean equality to 1.
- Do not require all categories for every language, fractions for integer-only counts, or ordinals where none are used.

An English suffix rule is not a general plural implementation. Branch coverage alone does not certify natural wording.

### LOC-10: Fallback behavior

- Trace message lookup, supported-locale negotiation and formatter-data inheritance separately. The product defines intended fallback, explicit unavailability or controlled failure.
- Inspect missing keys/files, meaningful empty values, regional/script variants and lazy resources where relevant. Do not assume shortening a tag always gives the correct parent.
- Compare output language/direction metadata with the actual fallback content.
- Check an affected missing translation or unsupported request against the adopted policy. An intentional fallback is not automatically defective; promised coverage and consequence determine the concern.

CLDR parent data does not by itself establish how the application finds a missing message.

### LOC-11: Text fit and scripts

- Inspect supplied rendered states for representative translations and expanded text at relevant widths, text settings and UI states.
- Check clipping, overlap, hidden actions, unwanted ellipses, long-word wrapping, vertical growth, fonts and shaping. Coordinate shared accessibility/layout findings with Design.
- Do not use one expansion ratio for every language or message. Short labels may expand substantially; other translations shrink or need different glyph metrics.
- Tie findings to unreadable information, unavailable actions or an adopted rule; different line breaks alone are not a defect.

A 30% German expansion sample is illustrative. It cannot establish that every supported translation fits.

### LOC-12: Direction

- For supported RTL interfaces, inspect base direction, logical start/end layout, directional controls and mixed content. Separately assess accepted bidi user data in LTR interfaces.
- Use opposite-direction values, numerals and punctuation to inspect spillover; include editing/copy behavior where affected and evidenced.
- In HTML, distinguish language metadata from direction. Appropriate `dir`, `bdi` or isolation handles text; logical CSS handles layout. Plain-text channels may need isolation controls.
- Do not reverse stored strings or mirror all icons, media and numbers. Legitimate RTL text is not itself malicious; route hostile control/spoofing concerns to Security.

An Arabic name in an English receipt can need isolation without requiring a fully Arabic interface.

### LOC-13: Sorting and search

- Establish locale and intended case/accent/numeric comparison for human-facing sorting/search. Use distinguishing supported names or labels.
- Check consistency across client/server, pagination and persisted sort keys when affected. Coordinate index/uniqueness consequences with Database.
- Preserve deterministic internal ordering and opaque identity contracts where binary/code-point/code-unit rules are intended.

Locale collation need not govern an internal signed list. A human-facing order changing between pages can violate its actual contract.

### LOC-14: Resource delivery and verification

- Inspect the shipped build for required catalogs, locale data and fonts; record versions when behavior depends on them.
- Check changed keys/arguments, stale translations, old/new clients, cached or asynchronous catalogs and rollback combinations permitted by the actual delivery design.
- Use pseudolocalization when useful to expose extraction, fragmentation, expansion or direction assumptions. Retain real representative locale cases.
- Check the chosen missing-translation policy. A successful build may still warn about missing resources; neither compilation nor pseudolocalization proves linguistic accuracy.

A stale catalog accepting the old key but not its new argument needs a compatibility check, not an automatic translation-platform mandate.

### LOC-15: Localized communications

- Where email, push, SMS, exports or generated documents are localized, trace recipient/user/tenant context through enqueue, retry and rendering.
- Determine whether settings are captured at enqueue time or read at send time; test the actual rule and another recipient's preferences.
- Apply relevant message, value, fallback, encoding and direction checks to subject, body and attachments. Inspect context restoration between jobs.

A fixed-language operational feed may remain fixed under its contract. A background worker leaking the previous recipient's language is a different failure.

### LOC-16: Linguistic coverage

- State the locales, scripts, journeys, messages, method and language competence actually assessed.
- Separate structural/runtime/visual checks from meaning, terminology, idiom, tone and cultural suitability.
- Report concrete mistranslation evidence when supported; otherwise retain the comparison as unassessed or request appropriate language evidence through the lead.
- Do not infer missing work merely from unavailable evidence or treat fluent model output as qualified human approval.

A placeholder check can establish argument compatibility without establishing whether a warning conveys the intended meaning.

## Verification

For each selected control, retain its criterion, exact input/locale/value, source identity, expected contract, supported observation or analysis, consequence and limits. Use the control's distinguishing checks and legitimate counterexamples. Runtime, rendered, interaction and linguistic claims need their respective evidence; written proposals and absent observations do not count as execution.

Record material exclusions and unresolved comparisons. The leaf recommends verification; it does not execute targets or rewrite translations. The lead can obtain separately authorized results and route related Code, Database, Security, Design or Testing questions without losing criterion coverage.

## Responsibilities and exceptions

The lead establishes scope, authority and evidence; Localization assesses assigned locale consequences; developers implement and verify corrections. Use the shared customization procedure for actual supplements, replacements and waivers. Preserve unaffected obligations, expired history, evidence honesty and review boundaries; a waived unmet requirement is not satisfied.

## Ownership, review, and related policy

The package maintainer owns defaults and validation. Revisit affected controls for changed runtimes, resource formats, locale data, shared rules or demonstrated missed defects/false positives. Follow the [Localization Policy (POL)](../policies/localization.md), [procedure](../domains/localization.md) and shared [Review Technical Standard (STD)](../review_standard.md).
