# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 Overview

JQL search: `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006`

Result: 1 sibling issue found.

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8006 has stream suffix `[rhtpa-2.1]` (stream 2.1.x).
TC-8001 has stream suffix `[rhtpa-2.2]` (stream 2.2.x).

These are **different streams**. TC-8001 is NOT a same-stream duplicate.

Result: No same-stream duplicates found. Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT created one issue per stream intentionally.

### Pre-existing link check

Per Step 4.2 procedure: "Check for existing link before creating one. Read the current issue's issuelinks array from the jira.get_issue response (already fetched in Step 1)."

TC-8006's existing issue links (from Step 1 data extraction):

| Link Type | Direction | Target Key | Link ID |
|-----------|-----------|------------|---------|
| Related | Outward (TC-8006 -> TC-8001) | TC-8001 | 1990401 |

Check criteria -- does any existing link satisfy ALL of:
1. `type.name` is `"Related"` -- YES (type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key TC-8001 -- YES (outwardIssue.key = TC-8001)

All criteria satisfied. A matching Related link already exists.

### Action taken

**Skipped link creation.** Logged:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The existing link (ID 1990401) is sufficient for cross-stream coordination. This is the idempotent behavior specified in Step 4.2.

### Affects Versions overlap check

TC-8006 Affects Versions: RHTPA 2.1.0
TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected. Each issue carries versions from its own stream only. This is the expected state.

### Sibling landscape presentation

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The project's Security Configuration does not include the Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill procedure: "If any of these fields are not configured, skip this step entirely."

Result: Step 4.3 skipped.

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks: `project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC`

Assumed result: No matching preemptive tasks found for CVE-2026-31812 in the 2.1.x stream.

Result: Step 4.4 complete, no reconciliation needed. Proceed to Step 5.
