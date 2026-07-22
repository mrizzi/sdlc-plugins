# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8006

## Step 4 JQL Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling issue found:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]` (stream 2.2.x).
TC-8006 has stream suffix `[rhtpa-2.1]` (stream 2.1.x).

These are **different** streams. TC-8001 is NOT a same-stream duplicate.

Result: No same-stream duplicates found. Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT created one issue per stream intentionally.

### Link Idempotency Check

Before creating a Related link to TC-8001, the skill checks the current issue's existing `issuelinks` array (fetched in Step 1).

**Existing links on TC-8006:**

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | 1990401 |

**Check criteria (all must be satisfied):**
1. `type.name` is `"Related"` -- YES (the existing link type is Related)
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key TC-8001 -- YES (outwardIssue.key = TC-8001)

**All criteria satisfied.** A matching Related link already exists.

**Action: SKIP link creation.**

Log message:
> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link()` call is made. The pre-existing link (ID 1990401) already establishes the cross-stream relationship between TC-8006 and TC-8001. Creating a duplicate link would be redundant and could cause Jira API errors.

### Affects Versions Overlap Check

Checking for version overlap between the two sibling issues:

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlap detected. Each issue carries only versions from its own stream. This is correct.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field is NOT configured in the project's Security Configuration (claude-md-security-config.md does not include it). Per the skill instructions, Step 4.3 is skipped entirely when this field is not configured.

Result: Skipped.

## Step 4.4 -- Preemptive Task Reconciliation

Simulated JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks found for CVE-2026-31812 in stream 2.1.x.

Result: No reconciliation needed. Proceed to Step 5.
