# Design review technical standard

## Purpose and scope

Assess user-facing task completion, accessible operation, presentation, recovery and supported environments. Apply this catalogue to the changed interface and relevant consumers. It governs review of captured sources and supplied observations; it grants no permission to operate the target.

The [Design Policy (POL)](../policies/design.md) governs judgment. Shared [Review scope and criteria](../intent_context.md#review-scope-and-criteria) determines effective requirements, replacements and waivers; the shared [Review Technical Standard (STD)](../review_standard.md) owns findings and coverage. Keep source editions and mappings in the [research record](../research/design.md), rather than loading its bibliography for every assignment.

## Definitions

- A **user journey** is the sequence needed to reach a required outcome, including recovery.
- A **state** changes what users perceive or can do: for example, loading, focused, failed or complete.
- A **CSS pixel** is a browser layout unit, not necessarily one physical display pixel.
- An **accessible name** is the name exposed through accessibility APIs; it can differ from visible text.
- A **support commitment** identifies adopted environments or input methods. A **captured observation** records a particular revision, state, environment and method.

## Principles

Judge requirements and user consequences rather than visual taste. Preserve native behavior where it meets the need. Applicable project rules specialize the review; inferred conventions do not become obligations. Use shared authority handling for replacements and waivers.

The web-accessibility fallback uses the applicable WCAG 2.2 Level A/AA-derived checks below. It is a technical review baseline, not a legal obligation or a whole-product conformance claim. Retain each criterion's scope and exceptions. Additional AAA checks are recommendations unless adopted. Native UI needs its actual platform semantics and evidence; HTML rules do not apply unchanged.

Source inspection can establish some defects; observed appearance, interaction and assistive technology (AT) behavior need their respective evidence. Verification methods below identify evidence to inspect or request through the lead, not actions this read-only leaf may execute. Request only what the conclusion needs, and mark missing observations honestly.

## Applicability and phases

| Context | Review depth |
| --- | --- |
| No user interface | Exclude Design with the reason; retain any separately assigned user-facing artifact. |
| Small or early interface | Check relevant tasks, semantics, readability, keyboard operation, states and recovery. No corporate library, all-browser matrix or enterprise onboarding programme is presumed. |
| Production interface | Include adopted support/accessibility commitments, representative content and important user journeys. Small traffic does not waive a consequential failure. |
| Growth or critical work | Extend affected shared components, dense data, roles/tenants and high-consequence flows as the actual interface requires. Do not invent scale, a design-system migration or a performance budget. |

## Control index

Read selected controls in full, including exceptions and examples. Examples illustrate one mechanism; they do not certify a component. This is a targeted catalogue, not an exhaustive WCAG audit. Route additional applicable project or content-specific criteria through the lead.

- [DES-01 — Design commitments and reusable components](#des-01-design-commitments-and-reusable-components)
- [DES-02 — Structure and non-text information](#des-02-structure-and-non-text-information)
- [DES-03 — Keyboard operation and focus](#des-03-keyboard-operation-and-focus)
- [DES-04 — Accessible names, roles, values and state](#des-04-accessible-names-roles-values-and-state)
- [DES-05 — Input labels, errors and authentication](#des-05-input-labels-errors-and-authentication)
- [DES-06 — Contrast and noncolor cues](#des-06-contrast-and-noncolor-cues)
- [DES-07 — Text resizing, spacing and reflow](#des-07-text-resizing-spacing-and-reflow)
- [DES-08 — Pointer, touch, drag and targets](#des-08-pointer-touch-drag-and-targets)
- [DES-09 — Motion, automatic updates and time limits](#des-09-motion-automatic-updates-and-time-limits)
- [DES-10 — State feedback and recovery](#des-10-state-feedback-and-recovery)
- [DES-11 — Responsive and supported-browser behavior](#des-11-responsive-and-supported-browser-behavior)
- [DES-12 — Onboarding, tenant context and roles](#des-12-onboarding-tenant-context-and-roles)
- [DES-13 — Consequential actions, subscriptions and entitlements](#des-13-consequential-actions-subscriptions-and-entitlements)
- [DES-14 — Dense data and growth in shared interfaces](#des-14-dense-data-and-growth-in-shared-interfaces)
- [DES-15 — Evidence and scope of conclusions](#des-15-evidence-and-scope-of-conclusions)
- [DES-16 — Navigation and predictable context](#des-16-navigation-and-predictable-context)

## Rules

### DES-01: Design commitments and reusable components

- Identify the adopted library, tokens, themes and design version. Compare required padding, typography, colors, shadows, layout and states within that scope.
- Trace adopted semantic tokens through theme overrides and generated styles. Check variants and approved exceptions before reporting hardcoded values; a copied color matching one theme can still break another.
- Without an adopted system, assess consistency, legibility and concrete maintenance consequences. Recommend reuse for demonstrated divergence; do not require token extraction, DTCG files, a naming scheme or a large framework for a small page.
- Check shared-component changes in affected consumers and themes. Design-system reuse does not prove the component configuration is accessible.

Inspect adopted designs, dependency versions, token resolution and supplied rendered states. Screenshot comparisons need matching versions, states, fonts and viewports.

An approved illustration may use literal colors while controls use semantic tokens. A shared error label overriding its token with an unreadable pale brand color on the supported dark theme is defective. DTCG 2025.10 defines interchange and aliases, not a mandatory library or accessible palette.

### DES-02: Structure and non-text information

- Match native elements to content and actions: headings, lists, links, buttons, form groups and data tables. Preserve meaningful reading order and visual relationships; do not require a particular tag for stylistic preference.
- Match text alternatives to purpose: informative images convey equivalent information; functional images name actions; decorative or redundant images may have empty alternatives. Charts may need explanations or data beyond a filename or “chart”.
- Where technology supports the intended presentation, use text rather than images of text. Exceptions allow user-customizable images and essential presentation, including logotypes. Text in pictures containing significant other visual information is outside this definition. Alternative text alone does not satisfy this separate criterion.
- Preserve nonvisual access to essential CSS-generated, canvas and SVG information. Custom controls must supply the semantics and operation that suitable native elements provide.
- Check programmatic page and passage language. Passage exceptions include proper names, technical terms, indeterminate language and adopted vernacular. Localization owns language selection/content correctness; AT speech alone cannot establish a markup failure.
- Prerecorded audio-only media needs an equivalent time-based-media alternative; prerecorded video-only media needs that alternative or an equivalent audio track, except when the media itself is a clearly labeled alternative to text.
- Prerecorded synchronized media needs audio captions and, at Level A, video audio description or a time-based-media alternative, retaining the clearly labeled text-alternative exceptions. At Level AA, text alone does not replace audio description; additional description is unnecessary if audio conveys all important visual information.
- Live audio in synchronized media needs captions at Level AA. Distinguish broadcasts from individual two-way calls and identify content-provider/host responsibility; do not presume platform captioning of every call regardless of user needs.

Compare source, supplied accessibility structure and alternatives with the actual information/task. Media assessment may need playback evidence and a qualified contributor; alternative-text presence alone proves neither meaning nor media coverage.

A labeled download button may contain a decorative icon; an audio announcement may use an equivalent transcript. An action named only “arrow.svg”, an uncustomizable raster heading despite equivalent text support, or a broadcast missing applicable captions is defective.

### DES-03: Keyboard operation and focus

- Check keyboard operation without precise keystroke timing, except functions inherently dependent on a movement path. Dragging alone is not that exception. A discoverable equivalent path can suffice; every pointer target need not enter the tab order.
- Check entry, traversal, activation and exit for dialogs, menus, tabs and nested widgets. Focus order must preserve meaning and operation, not every visual position. Provide keyboard exits and explain unusual exit commands.
- Require visible keyboard focus. WCAG 2.2 AA permits partial obscuration but not a component entirely hidden by author-created content. Complete visibility and AAA focus-appearance metrics are not AA requirements; assess contrast separately.
- Modal interactions move focus inside, prevent background interaction, allow keyboard dismissal and restore focus to the invoker or a logical next location when it is gone. Initial focus may belong on a heading or safer action rather than the first button.
- Character-only shortcuts must be disableable, remappable with a non-printable key, or active only while the component has focus. Check custom shortcuts against typing and assistive input.

Inspect handlers, DOM order and recorded keyboard sequences through open, update, error and close states at affected viewports. Assess user-movable panels in their initial positions. User-opened content may obscure focus if users can reveal it without advancing focus.

Closing a deleted-row dialog may focus the next surviving row. Leaving focus behind an inert overlay or entirely beneath an author-created sticky footer is defective.

### DES-04: Accessible names, roles, values and state

- Inspect computed names/roles, user-settable states/properties/values and change notifications. Correct native controls need no redundant ARIA.
- Check custom widgets' allowed roles/properties and promised behavior. `role="button"` supplies no keyboard behavior; native-semantic overrides need a supported reason.
- Include visible label text in accessible names. Check icon-only and repeated-row names in context; unrelated `aria-label` text must not replace an accurate visible label.
- Match expanded, selected, pressed, checked, invalid and disabled states to behavior. `aria-disabled` does not prevent activation; verify the handler and explanation. Keep focused/operable content exposed to accessibility APIs.

Compare source with supplied computed accessibility representations and relevant AT interaction records, observing DES-15's evidence distinctions.

A disclosure button can expose its expanded state and control a named panel. A visible “Save” named “Submit purchase”, or a checkbox changing visually without exposing its value, is defective.

### DES-05: Input labels, errors and authentication

- Label or instruct every input, including optional fields, and associate relevant text programmatically. Convey necessary formats and required fields beyond placeholders/color alone.
- For user-information fields, expose applicable WCAG-listed purposes when technology supports them, such as HTML `autocomplete` tokens. Input type may be too broad. This does not cover every input or guarantee autofill. Retain technology limitations for fields accepting multiple purposes.
- Identify automatically detected input errors in text. Suggest known corrections unless security or the content's purpose would be jeopardized. Inline errors and summaries are alternatives; every form need not provide both.
- Preserve valid input through recovery without unnecessary re-entry. Information required again in the same process must be populated or selectable unless repetition is essential, required for security, or the information is no longer valid. Cross-session storage is not required.
- Check every existing-user authentication step, including recovery and multi-factor steps. Cognitive tests need an allowed alternative/assistance mechanism or the object-recognition/personal-content exception. Password managers and paste can assist; audio transcription puzzles are not automatically accessible alternatives.

Inspect recorded valid/invalid/missing input, server rejection, correction, password-manager/paste and keyboard paths. Coordinate account-enumeration concerns with Security; a detailed UI explanation does not establish a security-safe error message.

Checkout may reuse an earlier invoice address. A failed submission clearing valid non-sensitive entries is defective, as is a required OTP that must be manually transcribed because paste is blocked without an alternative accessible authentication route. Check the actual alternatives.

### DES-06: Contrast and noncolor cues

- Check AA text contrast of at least 4.5:1, or 3:1 for large text: at least 18 points, 14 points bold, or equivalent script size. Do not round failing ratios upward. Include overlays, gradients and supported themes.
- Retain text exceptions: inactive controls, pure decoration, invisible text, incidental text in a picture with other significant content, and logos/brand names. Ordinary branded body text is not exempt.
- Require 3:1 against adjacent colors for cues needed to identify controls/states and meaningful graphic parts. Exceptions: inactive controls, unmodified user-agent appearance and essential graphic presentation. Decorative borders need not pass as identifying cues when other sufficient cues exist.
- Convey information, actions, errors and states beyond color alone, using text, shape, pattern or another perceptible cue. Contrast concerns adjacent colors; hover color need not contrast 3:1 with the previous nonadjacent resting color.
- Instructions must not depend solely on shape, color, size, location, orientation or sound. Name the control or supply other usable information; sensory cues may supplement it.

Inspect supplied computed/resolved color measurements against actual backgrounds and rendered layering/meaning. Anti-aliased screenshot samples do not reliably represent underlying text colors.

Required fields can use a label and explained marker. A red border as the sole error cue, or placeholder text below its applicable contrast ratio, is defective. “Choose Continue” remains useful when “the green button on the right” cannot be perceived.

### DES-07: Text resizing, spacing and reflow

- Check text resizing to 200% without content/functionality loss, including relevant intermediate sizes. Captions and images of text are excluded from this criterion; an effective supported resizing mechanism can suffice.
- Check reflow without information/functionality loss or two-dimensional scrolling at 320 CSS pixels wide for vertical content, or 256 CSS pixels high for horizontal content. A 1280-pixel-wide viewport at 400% zoom is one vertical-content setup, not a required device width.
- Permit necessary two-dimensional layout for content such as tables/maps. Scope the exception to that content; table cells and surrounding controls still need applicable adaptation.
- Where markup supports them, assess simultaneous overrides of line height to 1.5 times font size, paragraph spacing to 2 times, letter spacing to 0.12 times and word spacing to 0.16 times. Preserve content/functionality. These are test overrides, not required defaults; apply only properties used by the language/script.

Inspect supplied zoom/text-size and spacing observations for clipping, overlap, unreachable controls and content loss. Small-viewport evidence alone does not establish zoom behavior.

A wide table may scroll within a region while its heading, filters and page reflow. A fixed-height dialog clipping its confirm action at 200% text size is defective.

### DES-08: Pointer, touch, drag and targets

- Multipoint/path gestures need a single-pointer alternative without path gestures unless essential. Dragging needs a non-dragging single-pointer alternative unless essential or supplied by the unmodified user agent. Keyboard access alone does not meet the pointer requirement.
- Check a permitted cancellation design: no down-event action; up-event completion with abort/undo; up-event reversal; or essential down-event action. Prefer suitable native activation and assess accidental activation paths.
- AA targets need at least 24 by 24 CSS pixels or an exception. For spacing, a 24-CSS-pixel-diameter circle centered on each undersized target's bounding box must intersect neither another target nor another undersized target's circle. Other exceptions: a conforming equivalent control on the same page; inline targets constrained by surrounding text; unmodified user-agent size; essential or legally required presentation. The 44-by-44 enhanced criterion is AAA.
- Motion-operated functionality needs UI operation and disableable motion activation, except accessibility-supported interfaces or essential motion. Touch access must not depend on hover for necessary information/actions.

Inspect hit regions/overlap and separately recorded pointer/touch and keyboard paths. Icon dimensions may differ from target dimensions.

A sortable list can offer drag, keyboard moves and touch-operable “Move to position”. Arrow keys without a non-dragging pointer method do not satisfy 2.5.7.

### DES-09: Motion, automatic updates and time limits

- Content-set time limits need disabling before encounter, adjustment beforehand to at least ten times the default, or a warning allowing at least 20 seconds for a simple extension and at least ten extensions. Retain real-time, essential and longer-than-20-hours exceptions. Coordinate real security constraints without inventing a blanket session-timeout exemption.
- Automatic moving/blinking/scrolling information lasting more than five seconds alongside other content needs pause/stop/hide unless essential. Automatic updating alongside other content needs pause/stop/hide or frequency control unless essential; this branch has no five-second condition.
- Check flashing against the no-more-than-three-flashes-per-second route or general/red-flash thresholds. Require suitable analysis; casual observation of dangerous content cannot certify them.
- Recommend disable controls or reduced-motion support for nonessential interaction-triggered motion. WCAG 2.3.3 is AAA, an adopted commitment or a recommendation, not an AA requirement. Autoplay audio exceeding three seconds needs pause/stop or independent volume control.

Inspect timers, preference handling and recorded animation/media, expiry/warning and extension behavior from controlled checks.

A decorative transition may become instantaneous under reduced motion while progress stays clear. Uncontrolled automatic updates or an expiring sole error message that prevents recovery are defective.

### DES-10: State feedback and recovery

- Assess actual states: hover, focus, pressed/active, selected, disabled, loading, empty, success, partial failure, error and recovery. Noninteractive images need no hover state; styling alone does not establish semantics/operation.
- Distinguish initial emptiness, no search matches, missing permission and loading failure. Explain the situation and any available next action; a failed request is not “No records”.
- Report progress/completion accurately. Preserve recovery context and explain cancellation, retry and uncertain outcomes. A lost destructive/payment response needs a safe status check before duplicate submission is offered as the only recovery.
- Make success, waiting, progress and error status messages available programmatically without focus when they appear without context changes. Choose urgency and frequency to avoid unnecessary interruption; not every update is a live alert, and search results differ from their status count.
- Hover/focus content must be dismissible without moving pointer hover or keyboard focus, hoverable when hover-triggered, and persistent until dismissal, trigger removal or invalidation. Retain dismissibility exceptions for input errors/nonobscuring content and the unmodified user-agent presentation exception.
- Repeated human-contact, self-help and automated-contact mechanisms need consistent relative order across a page set unless users initiate relevant layout changes. Compare the same page variation; this requires neither help on every page, identical pixels nor continuous human support.

Inspect recorded loading, zero-data, network/permission failure and retry transitions and announcements. Static stories showing labels do not establish end-to-end recovery.

A failed report load can retain filters and offer “Try again”, separately from successful zero results. A spinner that never resolves after a rejected request, or “Saved” persisting after the server rejects the operation, is defective. Code owns retry/idempotency correctness.

### DES-11: Responsive and supported-browser behavior

- Identify adopted browsers/versions, engines, operating systems, devices and embedded contexts. Unknown support remains a gap; assume neither all browsers nor only the reviewer's browser.
- Assess representative widths/heights, aspect ratios and breakpoint transitions, including variable/optional content, font loading and software-keyboard obstruction. Mobile/tablet/desktop labels alone do not supply sufficient test dimensions.
- Check both orientations unless one is essential, respecting users' device-level orientation locks.
- Compare functionality, layout integrity and access across supported engines. Native controls, fonts and antialiasing may differ; require exact pixels only for an adopted bounded visual requirement.
- Check feature detection/fallbacks or adopted minimum versions for unsupported features. Baseline badges summarize availability, not accessibility, older-device/webview support or AT interoperability.

Inspect actual browser-build/platform records. Playwright profiles emulate viewport, user agent and touch; they do not establish physical-device testing. Name unverified supported environments, risks and needed follow-up.

Safari's native select may look different while remaining usable. A required action obscured by a software keyboard in a supported flow is defective.

### DES-12: Onboarding, tenant context and roles

- Where onboarding exists, check required/optional steps, progress, next actions, failed/expired invitations, interrupted setup and supported return paths. Do not add enterprise provisioning to products without it.
- When users access multiple tenants/workspaces, make active context understandable at decision points and identify consequential-action targets. Assess switching with pending edits, loading/failure, similar names and stale previous-tenant content.
- Explain role/permission limits and supported recovery/request-access paths. Assess role changes/revocation; distinguish unavailable capabilities from empty data and transient failure.
- Apply DES-16 to tenant selectors and onboarding focus/input behavior.

Compare product requirements with recorded representative role/membership paths in controlled fixtures. UI clarity does not prove isolation; route stale-data/cross-tenant actions to Security/Code through the lead.

A switch may show pending status, then destination and role actions, with recoverable failure. Showing tenant B's header while tenant A's records remain actionable, or a blank dashboard after an invite error, is defective. These checks require no Azure integration.

### DES-13: Consequential actions, subscriptions and entitlements

- For legal/financial submissions, changes/deletions of user-controllable stored data and test-response submissions, check reversibility, input checking with correction, or review/confirm/correct before submission. Confirmation dialogs are not required for every save.
- Explain destructive scope: resource, tenant/workspace, affected count and relevant effects on users/data. Promise undo only when available; focus and confirmation must support deliberate choice.
- Where subscriptions/entitlements exist, compare price/period/quantity, renewal/cancellation timing, plan/access changes and recovery with approved behavior. Do not invent laws, grace periods or provider state models.
- Match pending, action-required, success and failure displays to provider/application state. Redirects do not prove payment; subscription “active”, invoice payment and entitlement may differ. Check actual provider version and product contract.

Inspect safe-fixture records for final review, cancellation, failure, delayed confirmation and provider return. Code owns charging/idempotency/state correctness, Security permission enforcement and Compliance established disclosures/legal obligations.

Cancellation may accurately state that access continues until the agreed end date and expose the resulting state. A checkout saying “Payment complete” solely because its return URL loaded while the transaction remains pending is defective. Stripe is an illustrative provider, not a required integration.

### DES-14: Dense data and growth in shared interfaces

- For tables, virtualized lists, grids and bulk operations, check headers, sort/filter/selection state, total-versus-visible scope and full-content access. Do not introduce virtualization or a custom grid merely because a list might grow.
- Preserve focus and item identity across mounting, deletion, sorting and refresh. Assess loaded-window keyboard boundaries and applicable accessible row/count metadata.
- Prefer native tables when their interaction model fits. Custom ARIA grids need implemented keyboard navigation/focus management; the role supplies neither.
- Distinguish selected visible rows from all matching records; preserve recovery and report partial results. Route correctness to Code/Database and measured rendering/interaction latency to Performance.

Inspect recorded empty, single-item, long-label and representative large-data states, sorting/filtering and focused-item deletion. Sample sizes/timings need project workloads; no universal row count or performance budget applies.

“12 selected on this page” can accurately describe a 12-row bulk action. Reusing focused rows for different records or silently changing “Select all” to the full tenant dataset is defective.

### DES-15: Evidence and scope of conclusions

- Bind observations to revision/build, route/component, state/data, browser/platform/version, viewport/zoom and method. Record inspected, executed and unknown work; compare claims with captured artifacts/logs.
- Separate source/DOM, screenshots, automated/manual interaction, physical-device and AT evidence. Screenshots show appearance, not tab order, focus restoration, event behavior, announcements or full accessibility. Browser accessibility-tree output is not a screen-reader test. An animation-free screenshot proves little about timing or motion behaviors.
- Preserve automated-tool rule versions, warnings and exclusions. Automated checks miss accessibility issues; zero violations do not prove conformance or usability.
- AT evidence needs actual product/version, browser/platform and performed task. Static expectations and authored “screen reader” labels are not observations. APG examples need target browser/AT validation and do not guarantee mobile support.
- Complete supported analysis while naming gaps. A code-evident missing handler can support a defect without running every environment. Unrun manual checks cannot pass; request specific evidence or qualified contributors through the lead.

State reviewed criteria and samples. Whole-product conformance requires the complete evaluation scope; this catalogue cannot establish it.

“The captured screenshot at 320 CSS pixels shows the confirm button clipped; keyboard behavior was not exercised.” accurately scopes an observation. “Accessible on mobile” from desktop emulation and an automated scan does not.

### DES-16: Navigation and predictable context

- Verify effective keyboard/assistive-technology bypass of blocks repeated across pages. A particular skip-link implementation is not universally required; isolated repeated words or links are not blocks.
- Page titles and present headings/labels must describe topic or purpose. Check route/error-page titles for stale or misleading text; DES-02/04/05 own semantics and associations.
- Link purpose must follow from text alone or text plus programmatic context, except where ambiguous to users generally. Generic text can suffice with appropriate context; visual proximity alone does not establish it.
- Keep repeated navigation in the same relative order within a page set unless users initiate changes. Identify the same functionality consistently. Relevant additions/context-specific text are permitted; different functions need not have identical names or layouts.
- Focus must not initiate context changes. Input-setting changes must not automatically change context without advance notice. Clearly labeled link/button activation is distinct. This control owns On Input; DES-12 applies it to SaaS flows.

Compare representative pages' titles, link context and structure with recorded bypass, focus, input and route transitions. Limit conclusions to observed routes/states under DES-15.

A header can offer keyboard bypass, invoice pages descriptive titles, and a workspace selector advance navigation notice. Submitting on billing-field focus, identifying different actions as “Help” unpredictably, or retaining loading titles after invoice completion is defective.

## Verification

Apply DES-15 to supplied source and observations. Methods named in the controls specify evidence to inspect or request; the lead arranges separately authorized checks. They do not authorize this read-only leaf to execute tests, render interfaces or force states. A missing observation does not prove testing never happened.

For a correction, retain the original failure and verify the actual proposed change against it plus relevant successful behavior. An added role without keyboard handling, a changed screenshot from another revision, a disabled assertion or altered expected result does not prove correction. Developers own changes. Use the shared developer-response and re-review contracts.

## Responsibilities and exceptions

Design owns the assigned UI assessment. The lead owns capture, criteria, routing, authority, acceptance and synthesis. Route mechanism/authorization/storage/performance/language/legal questions to their responsible specialists without treating a handoff as a pass. Keep all criterion assessments, material exclusions and uncertainty in the shared report.

Honor valid mapped replacements; retain unrelated obligations. A waiver records the contradiction and consequence. Expired or out-of-scope decisions do not apply. Neither a project preference nor this catalogue silently overrides an independently established obligation; use the shared resolution procedure.

## Ownership, review, and related policy

The package maintainer updates affected controls when platform behavior, supported standards or observed reviewer failures change. Keep the [Design Policy (POL)](../policies/design.md), [procedure](../domains/design.md), shared contracts and [research mappings](../research/design.md) consistent. Mechanical document checks do not establish product usability, accessibility conformance or reviewer effectiveness.
