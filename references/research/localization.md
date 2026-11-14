# Localization research and coverage

Primary sources checked on 13 November 2026. Source versions below identify the researched material, not mandatory product dependencies. Runtime guidance lives in the [Localization Technical Standard (STD)](../standards/localization.md); this record supports verification and maintenance and is not loaded on every assignment.

## Scope and interpretation

The uploaded minimum scope requires string extraction, dynamic formatting, layout adaptation, targeted RTL and pluralization. The agreed roster adds Unicode/encoding, preferences, interpolation, fallback, sorting, time zones, locale-data behavior, pseudolocalization, communications and compatible resource delivery. LOC-01–LOC-16 preserve that complete scope. The [procedure](../domains/localization.md) owns investigation; the [Policy (POL)](../policies/localization.md) owns obligations; shared team documents own discovery, authority, report formats and developer exchange.

Several checklist absolutes need conditional application. Extraction concerns applicable localizable messages, not protocol tokens or every deliberately fixed literal. Locale-aware formatting preserves the value's currency and temporal meaning; it does not authorize conversion. Expansion varies with message length, script and font, so 30% is not a universal threshold. Full RTL interface support follows actual commitments, while accepted mixed-direction data may need handling independently. Plural categories follow the supported locale and permitted value domain, not a universal six-branch requirement.

External guidance supplies technical reasoning, not new markets, legal duties, project approvals or universal folder/library conventions. Framework examples are conditional. Context/cache/recipient/release checks are engineering deductions from the cited behavior and agreed scope; expected precedence, enqueue-time versus send-time settings and fallback must come from actual project criteria.

## Policy and responsibility support

| Obligation | Supporting basis and boundary |
| --- | --- |
| LOC-POL-01: effective requirements | Shared review policy and intent procedure own authority; S01/S02 distinguish engineering readiness and actual preferences. Optional project documents remain optional. |
| LOC-POL-02: text/value integrity | S05–S08, S11–S13 and S19 support text units, identity, amounts and temporal distinctions; selected product contracts define permitted values. |
| LOC-POL-03: proportionality | S01/S15/S19/S24 support conditional language/runtime/layout checks. A small product need not adopt a translation service or every locale feature. |
| LOC-POL-04: context/delivery | S03/S09/S10/S14/S18/S22 support resources, message formats and context. Cross-request/job and release checks are derived, with project-specific expectations. |
| LOC-POL-05: usable output | S05/S15–S17/S20/S21 support script, expansion and direction checks; Design retains general presentation/accessibility ownership. |
| LOC-POL-06: evidence limits | S01/S22/S24 distinguish technical checks from translation quality. Shared evidence/report rules govern provenance and uncertainty. |

The lead routes relevant sections of requirements, interface/design/decision documents, adopted locale matrices, terminology, resource contracts and supplied verification through the team-owned map. Localization consumes that assignment; it does not maintain a duplicate document-discovery process or treat Technical Writer templates as product requirements.

## Requested coverage map

| Requested item | Controls | Key qualification |
| --- | --- | --- |
| String extraction | LOC-02, LOC-14 | Required for applicable translation/readiness scope; not every literal. |
| Dates and times | LOC-07 | Distinguish display, parsing and temporal meaning. |
| Currency and numbers | LOC-06 | Currency identity is separate from locale; parsing is separate from formatting. |
| Layout adaptation and expansion | LOC-11, LOC-14 | No fixed expansion percentage or universal German ratio. |
| Targeted RTL | LOC-12 | Full RTL UI is target-dependent; accepted bidi data may matter independently. |
| Pluralization | LOC-09 | Locale categories, cardinal/ordinal distinction and domain values. |
| Unicode and encoding | LOC-03, LOC-04 | Applies to accepted text even without translation. |
| Locale and time zones | LOC-01, LOC-05, LOC-07 | Locale, currency and zone are distinct settings. |
| Interpolation | LOC-08, LOC-09 | Complete messages, compatible placeholders and actual dialect. |
| Fallbacks | LOC-10, LOC-14 | Product message fallback differs from formatter-data inheritance. |
| Sorting | LOC-13 | Human-facing collation differs from internal deterministic order. |
| CLDR/ICU | LOC-06–LOC-10, LOC-13–LOC-14 | Technical baseline; inspect the installed runtime/version. |
| Pseudolocalization | LOC-11, LOC-14 | Diagnostic aid; no linguistic approval. |
| User/tenant locale preferences | LOC-05, LOC-15 | Established precedence and isolation; no universal precedence. |
| Localized communications | LOC-15 | Applies when those channels are localized. |
| Translation-release compatibility | LOC-08, LOC-10, LOC-14 | Follow the actual catalog/build/deployment model. |
| Linguistic limits | LOC-16 | State what was checked and by whom. |

## Primary sources

Versions below describe retrieved sources, not versions a reviewed product is required to adopt. Living documentation has no verified release binding unless stated. Prefer its project's actual supported version when applying a control. Draft/advisory sources supply technical reasoning rather than automatic conformance obligations.

| ID | Source, exact URL and version/status | Relevant support and limit |
| --- | --- | --- |
| S01 | [W3C: Localization vs. Internationalization](https://www.w3.org/International/questions/qa-i18n.en.html), living explanatory article | Separates adaptation from enabling it; includes Unicode, preferences and separation of localizable content. Does not mandate every translation feature for every product. |
| S02 | [W3C: Accept-Language used for locale setting](https://www.w3.org/International/questions/qa-accept-lang-locales.en.html), living advisory article | Language negotiation is insufficient to infer all regional settings; initial inference and user override are distinct. Does not define tenant precedence. |
| S03 | [Microsoft: Software internationalization](https://learn.microsoft.com/en-us/globalization/methodology/software-internationalization), living official guidance | Resource separation, translator context, avoiding concatenation and adapting layout; differentiates end-user strings from debugging/logging. |
| S04 | [Angular: Work with translation files](https://angular.dev/guide/i18n/translation-files), living official guide | Extraction covers marked messages and attributes; plurals/alternate expressions require translation. Conditional framework example, not universal tooling. |
| S05 | [W3C: Choosing and applying a character encoding](https://www.w3.org/International/questions/qa-choosing-encodings.en.html), living advisory article | Declared encoding must match actual bytes and system boundaries; Unicode encoding does not ensure shaping/display. UTF-8 guidance is for web content, not a ban on valid internal UTF-16. |
| S06 | [Unicode UAX #29](https://www.unicode.org/reports/tr29/tr29-49.html), revision 49, Unicode 18.0.0, 2026-09-01 | Grapheme, word and sentence boundaries; defaults may need language/script tailoring. It is not the line-breaking specification and does not redefine protocol byte limits. |
| S07 | [Unicode UAX #15](https://www.unicode.org/reports/tr15/tr15-58.html), revision 58, Unicode 18.0.0, 2026-08-12 | Canonical versus compatibility equivalence; compatibility normalization may remove distinctions. Supports conditional identity decisions, not blanket normalization. |
| S08 | [W3C: Internationalization Best Practices for Spec Developers](https://www.w3.org/TR/2026/NOTE-international-specs-20260807/), Group Note, 2026-08-07; sections 6.2–6.8 | Distinguishes internal deterministic ordering from human-facing sorting; covers identity, case, normalization and text units. Advisory specification guidance, not a universal product mandate or W3C Recommendation. |
| S09 | [Unicode UTS #35, Part 1: Core](https://www.unicode.org/reports/tr35/tr35-79/tr35.html), revision 79, CLDR 49, 2026-10-21 | Locale identifiers, inheritance and explicit parent overrides, including component-dependent inheritance. Application catalog fallback remains a separate contract. |
| S10 | [Django: Translation](https://docs.djangoproject.com/en/5.2/topics/i18n/translation/), documentation version 5.2; sections on language discovery and translations outside views/templates | Concrete resource and language-context example; temporary activation must restore previous context. Supports checking background recipient contexts by inference; does not prescribe a cross-framework precedence rule. |
| S11 | [Unicode UTS #35, Part 3: Numbers](https://www.unicode.org/reports/tr35/tr35-79/tr35-numbers.html), revision 79, CLDR 49, 2026-10-21 | Number/currency patterns, currency precision, cardinal/ordinal rules, explicit values and visible-decimal operands. Apply the product runtime's rules and supported domains. |
| S12 | [Unicode UTS #35, Part 4: Dates](https://www.unicode.org/reports/tr35/tr35-79/tr35-dates.html), revision 79, CLDR 49, 2026-10-21 | Calendar symbols, date/time styles, hour cycles and time-zone display. Does not alone determine domain storage or scheduling semantics. |
| S13 | [W3C: Working with Time and Timezones](https://www.w3.org/TR/2025/DNOTE-timezone-20250726/), Group Draft Note, 2025-07-26 | Instant, wall/floating time, offsets, zones, recurrence and daylight-saving cases. Explicitly a work in progress, not an endorsed W3C standard. |
| S14 | [ICU: Formatting Messages](https://unicode-org.github.io/icu/userguide/format_parse/messages/), living ICU User Guide; classic MessageFormat and documented ICU 4.8 apostrophe behavior change | Complete translatable units, select/plural structure, typed arguments and syntax quoting. Pin actual implementation/dialect; this page is not a claim of compatibility with MessageFormat 2. |
| S15 | [W3C: Text size in translation](https://www.w3.org/International/articles/article-text-size.en.html), living explanatory article | Expansion differs by source length, language, words and glyph width; flexibility and reflow matter. Its historical examples are illustrations, not universal acceptance thresholds. |
| S16 | [W3C: Structural markup and right-to-left text in HTML](https://www.w3.org/International/questions/qa-html-dir.en.html), living advisory article | HTML base direction, runtime text direction and logical CSS properties. Applies to HTML rather than prescribing native-platform APIs. |
| S17 | [W3C: Inline markup and bidirectional text in HTML](https://www.w3.org/International/articles/inline-bidi-markup/), living advisory article | Direction/isolation for mixed and runtime-inserted text, including `dir=auto` and `bdi`. Review actual supported-browser behavior. |
| S18 | [Angular: Merge translations into the app](https://angular.dev/guide/i18n/merge), living official guide | Locale-specific builds and configurable missing-translation behavior. A successful build can still include a missing-translation warning; framework defaults are not product acceptance criteria. |
| S19 | [ECMA-402, 13th edition](https://402.ecma-international.org/13.0/), June 2026 | Separate locale/currency/time-zone concepts; `Intl` formatter, plural, collation and segmentation APIs; implementation-dependent locale data/output. Conditional JavaScript example. Formatting availability does not establish localized parsing or translation. |
| S20 | [W3C: Unicode controls for bidi text](https://www.w3.org/International/questions/qa-bidi-unicode-controls.en.html), living advisory article | Isolation controls for plain text and markup-restricted contexts; isolates prevent surrounding text interactions. Controls do not replace document/block direction metadata. |
| S21 | [Unicode UAX #9](https://www.unicode.org/reports/tr9/tr9-52.html), revision 52, Unicode 18.0.0, 2026-09-01 | Bidirectional algorithm, isolates, higher-level protocols, shaping and mirroring. Algorithm conformance alone does not certify complete RTL interface design. |
| S22 | [GNU gettext utilities](https://www.gnu.org/software/gettext/manual/gettext.html), retrieved living manual; sections 7.1, 9.7.6 and 11.1.10 | `msgmerge` can produce fuzzy translations needing human revision; `msgfmt --check-format` checks supported format-string compatibility. These checks neither cover every custom formatter nor approve meaning. No installed gettext version was inspected. |
| S23 | [Unicode UTS #35, Part 5: Collation](https://www.unicode.org/reports/tr35/tr35-79/tr35-collation.html), revision 79, CLDR 49, 2026-10-21 | Locale tailoring, sorting/searching/grouping and collation fallback. Does not override machine identifiers or database identity contracts. |
| S24 | [Android: Test your app with pseudolocales](https://developer.android.com/guide/topics/resources/pseudolocales), living official guide | Artificial expansion/accents/brackets and RTL simulation expose resource/layout issues. Android tooling is conditional; simulated text is not an actual translation. |


## Host and instruction design

The role remains a bounded leaf under the existing lead, with separate Codex TOML and Claude Code Markdown assets. Shared rules stay team-owned; one coherent standard has a control index and selectively loaded full controls. Sources stay in this research file. This applies the following official guidance without adding another orchestration system:

- [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): narrow roles with explicit instructions; standalone TOML; parent permissions remain in force. A written read-only instruction is not a separate sandbox.
- [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills): keep the entry point focused and load supporting instructions when relevant.
- [Anthropic: Custom subagents](https://code.claude.com/docs/en/sub-agents): separate agent instructions and tool declarations; explicit preloads and actual context behavior need verification.
- [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): concise guidance, context-dependent freedom, realistic evaluation and a contents index for long references. These recommendations do not require splitting a single standard into many files.

The package's actual host definitions, loaded guidance and returns need runtime validation. Reference syntax and correct file names establish neither native activation nor host-enforced restrictions. Bounded reads and recovery of truncation carry forward the observed Design loading repair.
