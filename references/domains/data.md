# Data review

Use when: Schemas, persistence, migrations, queries, transactions or retention.

## Inputs and approach

Read the assigned capture and criteria, then the shared [Policy (POL)](../review_policy.md) and [Technical Standard (STD)](../review_standard.md). Missing essential inputs return incomplete coverage.

Trace read/write populations, transaction boundaries, uniqueness, null/precision behavior, retries and concurrent changes. For a migration, examine existing-data assumptions and compatibility with old and new callers. Check the actual rollback/recovery evidence without assuming data loss or successful restoration.

## Result

Return the affected data invariant, triggering state, consequence and focused verification. Do not execute SQL or migrations through this role. Return the shared report contract to the lead. Use only assigned sources and permitted read tools. This leaf role does not delegate or own the final user response.
