# Design review research references

Consult this record for source verification and maintenance. The [Design Technical Standard (STD)](../standards/design.md) owns controls; the [Design Policy (POL)](../policies/design.md) owns domain obligations. Do not preload this bibliography for routine reviews. Sources inform package defaults and do not establish project adoption, legal duties or actual product test results.

## Context

The supplied Design checklist and agreed roster require design-system consistency, accessibility, responsive behavior, interaction states and supported-browser layout, with applicable SaaS journeys. This record explains their qualification and source mapping; no particular product, browser matrix or legal obligation is assumed.

## How it works and why

### Requested coverage


| Requested responsibility | Proposed controls and correction |
| --- | --- |
| Uploaded Design System Compliance: padding, typography, colors, shadows, corporate library and hardcoded values | DES-01 checks actual adopted tokens/components and exceptions. No universal corporate library or hardcoded-value prohibition. DES-06 checks actual contrast consequences independently. |
| Uploaded Digital Accessibility: semantics, keyboard, image alternatives, ARIA/screen readers | DES-02–DES-09 and DES-15/16 cover actual semantics, interaction, perception, navigation and evidence. No ARIA-presence checklist; correct native semantics need no redundant ARIA. DES-02 distinguishes media branches and images of text; DES-06 retains sensory-instruction limits. |
| Uploaded Responsive Fidelity: viewport size, aspect ratio, content scaling and device types | DES-07/11 cover reflow, resize, spacing, dimensions, orientation and actual support. DES-14 covers dense content. |
| Uploaded State & Interaction UX: hover, focus, active, loading, disabled and error | DES-03/04/10 cover behavior, semantics, visual feedback, empty/recovery paths and conditional state applicability. |
| Uploaded Cross-Browser Layout: Chromium, WebKit, Gecko and uniformity | DES-11/15 check supported combinations, broken functionality/layout and evidence. No universal engine requirement or pixel-identical rendering. |
| Plan: user flows, design consistency, accessibility/recovery from first release | DES-01–DES-10/12/13; product phase does not waive relevant checks, and recommendations remain separate from established obligations. |
| Plan: distinguish inspected code from observed UI | DES-15 and the bounded screenshot proposal; source, screenshot, interaction, device and AT evidence remain distinct. |
| Plan: support commitments and browser/viewport matrices | DES-01/11/15; absent commitments remain uncertain, not invented requirements. |
| Plan: SaaS onboarding, tenant switching, roles | DES-05/12; Security/Code retain authorization and state enforcement. |
| Plan: destructive actions, subscriptions and entitlements | DES-09/10/13; Code retains transaction correctness and Compliance established legal obligations. |
| Plan: growth, reusable components and dense/large-data interactions | DES-01/14; no premature design-system or virtualization mandate. |
| Plan: concrete applicability, thresholds, safe/defective examples, source/version and verification | Each proposed control supplies checks, applicability and examples; source register below and DES-15 state evidence limits. These proposals need exact-document review and actual later validation. |
| Common-UI coverage supplement: bypass, page titles, link purpose, descriptive headings/labels, consistent navigation/identification, focus/input context | DES-16 owns these checks, with structural semantics retained in DES-02/04/05. DES-12 uses DES-16 for onboarding/tenant navigation rather than maintaining another On Input rule. |

### Design decisions

- Preserve all five uploaded Design families and the agreed SaaS responsibilities. Apply corporate tokens only where adopted, use appropriate native semantics instead of demanding ARIA everywhere, and judge supported browser usability rather than universal pixel identity.
- Use conditional WCAG 2.2 A/AA-derived checks as the packaged web baseline. Distinguish AAA recommendations and formal conformance scope. A scoped review cannot certify every page/process or legal compliance.
- Keep one coherent standard with a control index. Read applicable controls fully; source/version records are conditional maintenance material. No token-savings or comparative-effectiveness claim has been measured.
- The lead owns document discovery and shared routing. Design receives relevant project sections and captured evidence; it does not maintain another project-document catalogue.
- Source, DOM/accessibility representations, screenshot viewing, interaction, emulated devices, real devices and assistive-technology observations support different claims. No product evaluation occurred during this research.
- Text descriptions do not establish image inspection. Use actual read-only viewing of relevant screenshots and retain their context and limits; a role definition alone does not establish viewing or native activation.

## Tradeoffs and limits

Conditional controls preserve small-project usefulness without dropping relevant failures. One standard reduces navigation but still needs selective full-control loading; no context-size benefit has been measured. More complex evidence needs stronger observations: screenshots add visual inspection, while interaction and assistive-technology claims still require their own records. Registration, image capture and actual host behavior need separate validation.

## Related sources

### Primary-source register

Sources were opened on **2026-11-05**. “Living” means the opened page supplied no immutable release binding used here. A source edition is not a claim about the reviewed application's installed version. Every WCAG Understanding page below is informative guidance for the named criterion in WCAG 2.2; the Recommendation supplies normative authority. APG pages are informative patterns, not ready-made compatibility certificates. Source text has been paraphrased; the proposed catalogue combines these sources with the project's scope requirements.

| ID | Source and version observed | Mapping and limit |
| --- | --- | --- |
| S01 | [WCAG 2.2](https://www.w3.org/TR/2024/REC-WCAG22-20241212/), W3C Recommendation 12 December 2024; latest URL resolved to this edition | Normative criterion identities/levels and conformance framework. No legal adoption inferred. |
| S02 | [Understanding conformance](https://www.w3.org/WAI/WCAG22/Understanding/conformance.html), living WCAG 2.2 guidance | DES-15; full-page/process and accessibility-support limits; scoped review is not certification. |
| S03 | [Selecting Web Accessibility Evaluation Tools](https://www.w3.org/WAI/test-evaluate/tools/selecting/), living WAI guidance | DES-15; automated checks require human judgment and have coverage/false-result limits. |
| S04 | [APG Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/), living guide referencing ARIA 1.2 | DES-04/15; roles do not add behavior; browser/AT and mobile limits. |
| S05 | [ARIA in HTML](https://www.w3.org/TR/2026/REC-html-aria-20260811/), W3C Recommendation 11 August 2026 | DES-04; allowed and redundant semantics. Match actual HTML/ARIA support. |
| S06 | [HTML button element](https://html.spec.whatwg.org/multipage/form-elements.html#the-button-element), Living Standard updated 4 November 2026 | DES-02/04; native form/button semantics. New HTML capabilities still need target support evidence. |
| S07 | [Design Tokens Format Module 2025.10](https://www.designtokens.org/tr/2025.10/format/), Final Community Group Report 28 October 2025 | DES-01; token interchange, aliases and type resolution. Explicitly not a W3C Standard or universal adoption mandate. |
| S08 | [Info and Relationships, 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html) | DES-02; presentation relationships must survive alternate access. |
| S09 | [Non-text Content, 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) | DES-02; purpose-specific alternatives and decorative exceptions. |
| S10 | [Captions (Prerecorded), 1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html) | DES-02; synchronized media and clearly labeled text-alternative exception. |
| S11 | [Audio Description (Prerecorded), 1.2.5](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html) | DES-02; Level AA visual information, including when audio already conveys it. |
| S12 | [HTML form elements](https://html.spec.whatwg.org/multipage/form-elements.html), same Living Standard as S06 | DES-02; native form structures; same source, not independent corroboration. |
| S13 | [Keyboard, 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html) | DES-03; functionality, timing and inherent-path exception; equivalents are allowed. |
| S14 | [No Keyboard Trap, 2.1.2](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html) | DES-03; keyboard exit and nonstandard-exit instructions. |
| S15 | [Focus Order, 2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html) | DES-03; meaningful operability, not compulsory visual-order identity. |
| S16 | [Focus Visible, 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) | DES-03; visible keyboard indication. |
| S17 | [Focus Not Obscured (Minimum), 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html) | DES-03; entirely hidden threshold and user-movable/opened-content qualifications. |
| S18 | [APG modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), living | DES-03; initial/return focus, inert background, exit and logical exceptions. |
| S19 | [Character Key Shortcuts, 2.1.4](https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html) | DES-03; disabling, remapping or focus-scoped shortcuts. |
| S20 | [Name, Role, Value, 4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html) | DES-04; accessible semantics and changed values. |
| S21 | [Label in Name, 2.5.3](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html) | DES-04; visible label text in computed name. |
| S22 | [Labels or Instructions, 3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html) | DES-05; input labels, optional fields and distinction from programmatic association. |
| S23 | [Error Identification, 3.3.1](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html) | DES-05; textual description of automatically detected input error. |
| S24 | [Error Suggestion, 3.3.3](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html) | DES-05; known correction and security/purpose exception. |
| S25 | [Redundant Entry, 3.3.7](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html) | DES-05/12; same-process reuse and exceptions, no cross-session storage mandate. |
| S26 | [Accessible Authentication (Minimum), 3.3.8](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html) | DES-05; existing-user authentication, cognitive-test alternatives/assistance and exceptions. |
| S27 | Supplied attachment section 6 and Engineering Review Team Implementation Plan (IP), read locally on 2026-11-05 | Requested UX/recovery/SaaS scope; package synthesis, not external technical authority. |
| S28 | [Contrast (Minimum), 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | DES-06; text thresholds, exceptions and no rounding. |
| S29 | [Non-text Contrast, 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | DES-06; required cues, adjacency and exceptions. |
| S30 | [Use of Color, 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | DES-06; color cannot be the sole information channel. |
| S31 | [Resize Text, 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) | DES-07; 200%, exceptions and supported resizing mechanisms. |
| S32 | [Reflow, 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | DES-07; 320/256 CSS pixels, zoom relationship and bounded two-dimensional exceptions. |
| S33 | [Text Spacing, 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) | DES-07; simultaneous overrides and language/script exception, not default design tokens. |
| S34 | [Pointer Gestures, 2.5.1](https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html) | DES-08; single-pointer alternatives to path/multipoint gestures. |
| S35 | [Dragging Movements, 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html) | DES-08; non-dragging pointer alternative is separate from keyboard access. |
| S36 | [Pointer Cancellation, 2.5.2](https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation.html) | DES-08; permitted down/up/abort/undo behaviors. |
| S37 | [Target Size (Minimum), 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | DES-08; 24 CSS pixels, exact circle-spacing test and five exceptions. |
| S38 | [Motion Actuation, 2.5.4](https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html) | DES-08; alternate operation, disable control and exceptions. |
| S39 | [Timing Adjustable, 2.2.1](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html) | DES-09; tenfold/20-second/ten-extension paths and time-limit exceptions. |
| S40 | [Pause, Stop, Hide, 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) | DES-09; five-second moving-content condition differs from auto-updating content. |
| S41 | [Three Flashes or Below Threshold, 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html) | DES-09; rate or general/red threshold route, not casual visual certification. |
| S42 | [Animation from Interactions, 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) | DES-09; explicitly Level AAA; reduced-motion technique and essential-motion exception. |
| S43 | [Audio Control, 1.4.2](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html) | DES-09; autoplay over three seconds and independent controls. |
| S44 | [Status Messages, 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) | DES-10; defined status messages without context change, not every update. |
| S45 | [Content on Hover or Focus, 1.4.13](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html) | DES-10; dismissible, hoverable, persistent conditions and exceptions. |
| S46 | [Carbon empty states](https://www.carbondesignsystem.com/building-blocks/core/patterns/empty-states), updated 11 August 2026 | DES-10; distinguish reasons for absent data and useful recovery. Carbon patterns inform UX; they are not adopted project policy. |
| S47 | [Orientation, 1.3.4](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html) | DES-11; author orientation restrictions and essential exception. |
| S48 | [MDN Baseline compatibility](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility), living | DES-11/15; availability summary excludes broad testing guarantees. |
| S49 | [Playwright emulation](https://playwright.dev/docs/emulation), living; no installed version assumed | DES-11/15; emulated device parameters are distinct from real devices. |
| S50 | [Azure multitenant identity considerations](https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/identity), living | DES-12; tenant-scoped identity and conditional switching. Architectural choices and Azure are not mandated. |
| S51 | [On Input, 3.2.2](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html) | DES-16; advance notice for context changes triggered by input settings; DES-12 applies this owner. |
| S52 | [Error Prevention (Legal, Financial, Data), 3.3.4](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html) | DES-13; alternatives to confirmation and significant consequence scope. |
| S53 | [Stripe subscription lifecycle](https://docs.stripe.com/billing/subscriptions/overview), living | DES-13; provider states, delayed payment and invoice/access distinctions. No Stripe API version or actual integration assumed. |
| S54 | [APG grid pattern](https://www.w3.org/WAI/ARIA/apg/patterns/grid/), living | DES-14; grid interaction obligations, not a universal table replacement. |
| S55 | [Consistent Help, 3.2.6](https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html) | DES-10; repeated mechanisms, relative order and user-initiated layout exception; no help-service mandate. |
| S56 | [Identify Input Purpose, 1.3.5](https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html) | DES-05; user information, enumerated purposes, technology support and multi-purpose limitations. |
| S57 | [Language of Page, 3.1.1](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html) | DES-02; programmatically available default language; Localization owns language choice. |
| S58 | [Language of Parts, 3.1.2](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html) | DES-02; passage metadata, exceptions and limitations of judging markup from AT speech. |
| S59 | [Bypass Blocks, 2.4.1](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html) | DES-16; repeated blocks and effective bypass, not a single mandatory technique. |
| S60 | [Page Titled, 2.4.2](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html) | DES-16; titles describe topic or purpose. |
| S61 | [Link Purpose (In Context), 2.4.4](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html) | DES-16; text plus programmatic context and general-ambiguity exception. |
| S62 | [Headings and Labels, 2.4.6](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html) | DES-16; descriptive topic/purpose, separate from structural markup. |
| S63 | [Consistent Navigation, 3.2.3](https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html) | DES-16; repeated relative order within a page set and user-initiated-change exception. |
| S64 | [Consistent Identification, 3.2.4](https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html) | DES-16; consistent identification of the same functionality. |
| S65 | [On Focus, 3.2.1](https://www.w3.org/WAI/WCAG22/Understanding/on-focus.html) | DES-16; focus alone must not initiate context changes. |
| S66 | [Sensory Characteristics, 1.3.3](https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html) | DES-06; instructions need information beyond sensory characteristics alone. |
| S67 | [Images of Text, 1.4.5](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html) | DES-02; supported text presentation, customizable/essential exceptions and definition limits. |
| S68 | [Audio-only and Video-only (Prerecorded), 1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html) | DES-02; equivalent time-based alternative/audio-track branches and clearly labeled text-alternative exception. |
| S69 | [Captions (Live), 1.2.4](https://www.w3.org/WAI/WCAG22/Understanding/captions-live.html) | DES-02; live synchronized audio and broadcast versus individual-call responsibility. |
| S70 | [Audio Description or Media Alternative (Prerecorded), 1.2.3](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-or-media-alternative-prerecorded.html) | DES-02; Level A alternatives and the distinction from Level AA 1.2.5. |

### Agent and skill guidance

The following pages were opened, not merely found. Recommendations below are this package's design judgments; the sources do not prescribe its exact roster or file layout.

| Source, opened 2026-11-05 | Supported decision |
| --- | --- |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | Metadata selects a skill before full instructions are loaded. Make the description concrete about scope and keep the root focused on workflow; route conditional detail explicitly. |
| [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Custom Codex agents use `name`, `description` and `developer_instructions`; skills and permissions inherit from the parent. Supported feature disables can reduce capabilities. Agent-file `sandbox_mode` and `approval_policy` do not override the parent. Inspect the actual tool surface before claiming enforcement. |
| [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Assess outcomes and observable process, with focused deterministic checks and retained execution traces. An acceptable final paragraph alone cannot prove correct loading, evidence handling or scope discipline. |
| [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Write concise domain instructions, use conditional references, and evaluate representative tasks. Its 500-line recommendation concerns `SKILL.md`; it does not require splitting a coherent supporting standard into one file per control. |
| [Anthropic: Create custom subagents](https://code.claude.com/docs/en/sub-agents) | Claude Code supports Markdown/YAML role definitions and explicit `Read, Glob, Grep` tools. Omitting `tools` inherits available tools. `skills` preloads full listed skill content; inspect effective instructions and avoid accidental lead-role preloading. |

Use concise native assets to establish identity, allowed work, required reads and return contract. Load the control index and applicable controls in full; do not confuse an index-only read with completed assessment. Keep research citations and authoring history out of routine role instructions unless source verification is necessary. Claim reduced context use or improved behavior only after measuring actual loaded resources and outcomes.

The official host documentation supports conditional read-only image capabilities: [Claude Code Read](https://code.claude.com/docs/en/tools-reference#read-tool-behavior), [OpenAI image inputs](https://learn.chatgpt.com/docs/image-inputs), and [Codex view_image guidance](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide#view_image). Actual tools, permissions, resizing and viewing must be observed on each supported execution host. A configuration file or general API capability does not prove that the registered reviewer received an image.

### Screenshot decoder sources

The optional adapter specifies Pillow 13.0.0, whose [release notes](https://pillow.readthedocs.io/en/stable/releasenotes/13.0.0.html) and [Python support table](https://pillow.readthedocs.io/en/stable/installation/python-support.html) were checked on 2026-11-05. [Image API guidance](https://pillow.readthedocs.io/en/stable/reference/Image.html) distinguishes lazy identification, verification and complete load. [Format guidance](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html) supports the PNG/JPEG, APNG/MPO and truncation qualifications; [security guidance](https://pillow.readthedocs.io/en/stable/handbook/security.html) supports bounded untrusted-image handling and dependency updates. The eight-image batch, 20 MiB, 32-million-pixel and 10-second limits are package choices, not vendor recommendations or product design limits. Dependency installation, adapter execution and actual viewing need distinct validation records.
