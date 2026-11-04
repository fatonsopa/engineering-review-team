# Security Reviewer examples

## Context

These illustrative examples calibrate reasoning. They are not facts about a reviewed project. Apply the [domain procedure](../domains/security.md) to actual captured inputs.

## How it works and why

Defective case: An export endpoint checks that the caller is signed in but loads the export by its global identifier without checking ownership. A caller who obtains another account’s identifier can retrieve its export. Enforce subject/action/object authorization before returning bytes.

Clean counterexample: The same endpoint resolves the export through the authenticated account and applies the required action permission. An opaque identifier is additional protection, not the authorization boundary.

Record the applicable criterion, observed source flow and consequence. A finding's correction should be verified by a test or observation that would distinguish the faulty behavior. A clean result covers only the inspected scope.

## Tradeoffs and limits

Missing source or runtime evidence prevents a complete conclusion where it is essential. Do not promote a teaching assumption into a project requirement. A schema receipt validates bindings, not the truth of an engineering judgment.

## Related sources

[OWASP ASVS](https://asvs.owasp.org/)
