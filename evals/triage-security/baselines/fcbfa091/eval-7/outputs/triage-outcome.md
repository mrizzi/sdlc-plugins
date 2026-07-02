# Triage Outcome -- Step 4.2 Pre-Existing Link Handling: TC-8006

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a pre-existing Related link to sibling issue TC-8001 (stream [rhtpa-2.2]). Step 4.2 handled this correctly through the idempotent link check protocol.

## How Step 4.2 Handled the Pre-Existing Link

Step 4.2 requires cross-stream coordination for different-stream siblings. When a sibling like TC-8001 is found via JQL, the procedure is:

1. **Check for existing link before creating one.** Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
   - `type.name` is `"Related"`
   - `inwardIssue.key` or `outwardIssue.key` matches the sibling key

2. **Evaluation for TC-8006**: The issuelinks array contains Link ID 1990401 with `type.name = "Related"` and `outwardIssue.key = "TC-8001"`. Both conditions are satisfied.

3. **Result**: The link creation is skipped. The log message is:

   > Related link to TC-8001 already exists -- skipping

   No `jira.create_link` API call is made. This is the idempotent behavior specified in Step 4.2 of `jira-triage-operations.md`.

## Why This Matters

The idempotent link check prevents two failure modes:

- **Duplicate link errors**: Jira may reject a create_link call if the link already exists, causing an unnecessary API error.
- **Duplicate links**: Some Jira configurations allow multiple links of the same type between the same pair of issues, which would create clutter and confusion.

By checking existing issuelinks first, Step 4.2 is safe to run repeatedly on the same issue (re-triage scenario) without creating redundant links.

## What Still Happens Despite Link Skip

Even though link creation is skipped, Step 4.2 still completes the remaining substeps:

1. **Affects Versions overlap check**: Verified no overlap -- TC-8006 carries RHTPA 2.1.0 (2.1.x stream) and TC-8001 carries RHTPA 2.2.0, RHTPA 2.2.1 (2.2.x stream). Each issue owns versions from its own stream only.

2. **Sibling landscape table**: Presented to the engineer for cross-stream awareness:

   | Issue | Stream | Status | Affects Versions |
   |-------|--------|--------|------------------|
   | TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
   | TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

   The landscape table is always presented regardless of whether a new link was created or an existing link was found. It gives the engineer visibility into the full cross-stream picture for CVE-2026-31812.

## Classification

- TC-8001 is a **different-stream companion** (not a duplicate) -- PSIRT intentionally creates one Vulnerability issue per stream.
- No duplicate closure recommended.
- Triage proceeds to Steps 4.3/4.4 and beyond for TC-8006's own stream (2.1.x).
