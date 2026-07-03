# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check for TC-8006

## Step 4 -- JQL Sibling Search

JQL query executed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

### Sibling Classification

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker, not a duplicate)

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 is a different-stream companion (2.2.x vs 2.1.x).

Result: **No duplicates detected.** Proceed to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion tracker. PSIRT creates one issue per stream intentionally.

### Link Idempotency Check

Before creating a Related link to TC-8001, checked the current issue's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1).

Existing links on TC-8006:

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward | TC-8001 |

Check criteria for existing link:
1. `type.name` is `"Related"` -- **YES** (type is Related)
2. `outwardIssue.key` matches the sibling key TC-8001 -- **YES**

**All conditions satisfied.** A matching Related link already exists.

Action: **Skipped link creation.**

> "Related link to TC-8001 already exists -- skipping"

### Affects Versions Overlap Verification

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

No overlapping versions detected. Each issue carries versions only from its own stream.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions          |
|------------|--------|-------------|---------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 <- | 2.1.x  | New         | RHTPA 2.1.0              |
```

The arrow `<-` indicates the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration in CLAUDE.md does not include Upstream Affected Component custom field, PS Component custom field, or Stream custom field.

Result: **Step 4.3 skipped entirely** (prerequisite fields not configured).

## Step 4.4 -- Preemptive Task Reconciliation

JQL query for preemptive tasks:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: No matching preemptive tasks found for CVE-2026-31812 in stream 2.1.x.

Result: **No preemptive tasks to reconcile.** Proceed to Step 5.
