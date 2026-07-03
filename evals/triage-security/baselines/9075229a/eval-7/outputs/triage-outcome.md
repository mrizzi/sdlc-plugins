# Triage Outcome -- How Step 4.2 Handled the Pre-Existing Link for TC-8006

## Context

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) had a **pre-existing Related link** to sibling TC-8001 (stream [rhtpa-2.2]) when triage began. This link (ID 1990401, direction: outward from TC-8006 to TC-8001) was already present in the issue's `issuelinks` array at the time of the Step 1 data extraction.

## Step 4.2 Procedure Applied

Step 4.2 (Cross-stream coordination) requires that before creating a Related link to a different-stream sibling, the skill must **check for an existing link** to avoid creating duplicates. The procedure from `jira-triage-operations.md` specifies:

> "Check for existing link before creating one. Read the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
> - `type.name` is `"Related"`
> - `inwardIssue.key` or `outwardIssue.key` matches the sibling key"

## How the Check Was Evaluated

1. **Read existing links**: TC-8006's `issuelinks` array contained one entry:
   - Link ID: 1990401
   - Type: Related
   - Direction: outward (TC-8006 -> TC-8001)

2. **Evaluated conditions**:
   - `type.name` is `"Related"` -- **matched** (the link type is Related)
   - `outwardIssue.key` matches the sibling key TC-8001 -- **matched**

3. **Both conditions satisfied**: The existing link fully matches the link that Step 4.2 would have created.

## Outcome

**Link creation was skipped.** The skill logged:

> "Related link to TC-8001 already exists -- skipping"

No Jira mutation occurred for this step. This is the **idempotent behavior** specified by Step 4.2 -- the skill detects pre-existing links and avoids creating duplicate Related links between companion CVE issues.

## Why This Matters

The idempotency check in Step 4.2 ensures that:

1. **Re-triaging is safe**: If an issue is triaged a second time (or if a link was manually created before triage), the skill does not create duplicate links or fail with a conflict error.
2. **PSIRT-created links are preserved**: If PSIRT or another analyst already linked companion issues before triage, Step 4.2 respects those existing links rather than overwriting or duplicating them.
3. **No unnecessary Jira mutations**: Consistent with the guardrail that every Jira mutation requires confirmation -- when no mutation is needed, none is proposed.

## Remaining Step 4 Actions

After the link check, Step 4.2 proceeded with the other sub-steps:

- **Affects Versions overlap verification**: No overlap found. TC-8006 carries RHTPA 2.1.0 (stream 2.1.x); TC-8001 carries RHTPA 2.2.0 and RHTPA 2.2.1 (stream 2.2.x). Each issue owns only its own stream's versions.
- **Sibling landscape presentation**: Both companion issues were presented in a summary table showing their respective streams, statuses, and Affects Versions.
- **Step 4.3 (Cross-CVE overlap)**: Skipped because Upstream Affected Component, PS Component, and Stream custom fields are not configured in Security Configuration.
- **Step 4.4 (Preemptive task reconciliation)**: No preemptive tasks found for CVE-2026-31812 in the 2.1.x stream.
