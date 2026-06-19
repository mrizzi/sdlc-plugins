# Triage Outcome: TC-8006

## Step 4.2 Idempotent Link Handling

### How the Pre-Existing Link Was Handled

Step 4.2 of the triage-security skill requires cross-stream coordination for different-stream siblings. When TC-8001 was identified as a cross-stream companion (stream [rhtpa-2.2] vs current [rhtpa-2.1]), the skill performed the following idempotent check before attempting link creation:

1. **Read existing issuelinks** from the TC-8006 issue data (already fetched in Step 1). The issue has one existing link:
   - Link ID: 1990401
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)

2. **Checked matching criteria** per Step 4.2 specification:
   - `type.name` is `"Related"`? YES
   - `outwardIssue.key` matches `"TC-8001"`? YES

3. **Both criteria satisfied** -- a matching link already exists.

4. **Logged skip message:**
   > Related link to TC-8001 already exists -- skipping

5. **Did NOT call `jira.create_link`** -- creating a duplicate link would be redundant and potentially cause errors. The existing link (ID 1990401) already fulfills the cross-stream coordination requirement.

### What Was NOT Skipped

The idempotent link check only affects link creation. The following Step 4.2 operations were still performed:

- **Affects Versions overlap check**: Verified that TC-8006 (RHTPA 2.1.0) and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1) have no overlapping versions. No overlap detected.
- **Sibling landscape table**: Presented the full companion issue table showing both TC-8001 (2.2.x, In Progress) and TC-8006 (2.1.x, New) with their respective Affects Versions.

### Why This Matters

The idempotent check prevents the following failure modes:
- **Duplicate links** in Jira that clutter the issue
- **API errors** from attempting to create a link that already exists
- **Unnecessary Jira mutations** that would trigger confirmation prompts for no purpose

The pre-existing link indicates that either a previous triage run or manual action already established the cross-stream relationship. Step 4.2 respects this and moves on.

## Continuation After Step 4

Since TC-8001 is a different-stream companion (not a same-stream duplicate), triage is NOT short-circuited. The workflow continues through:

- **Step 5** -- Version Lifecycle Check: Verify that RHTPA 2.1.0 is still within its support lifecycle
- **Step 6** -- Already Fixed Check: Cross-reference resolved siblings (TC-8001 is In Progress, not resolved, so no already-fixed scenario applies)
- **Step 7** -- Remediation: Based on version impact analysis, determine whether to create remediation tasks or close the issue

## Version Impact Context (from Security Matrix)

For the 2.1.x stream (TC-8006's scope):

| Version | Build Tag | quinn-proto version | Vulnerable? |
|---------|-----------|---------------------|-------------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is within the affected range (versions before 0.11.14). The issue's current Affects Versions (RHTPA 2.1.0) is incomplete -- Step 3 would propose adding RHTPA 2.1.1.

For reference, the sibling TC-8001's 2.2.x stream:

| Version | Build Tag | quinn-proto version | Vulnerable? |
|---------|-----------|---------------------|-------------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| RHTPA 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed version) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed version) |
