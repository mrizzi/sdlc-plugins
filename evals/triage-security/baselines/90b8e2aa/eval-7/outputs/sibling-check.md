# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 JQL Search

Query executed (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, which maps to stream **2.2.x**.
TC-8006 has stream suffix `[rhtpa-2.1]`, which maps to stream **2.1.x**.

These are **different streams**. TC-8001 is NOT a same-stream duplicate.

Result: **No same-stream duplicates found.** Proceeding to Step 4.2.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT intentionally creates one Vulnerability issue per stream.

### Link Existence Check

Before creating a "Related" link to TC-8001, the skill checks the current issue's `issuelinks` array (already fetched in Step 1).

Existing links on TC-8006:
- Link ID 1990401: type.name = "Related", outwardIssue.key = "TC-8001"

Check criteria -- does any existing link satisfy ALL of:
1. `type.name` is `"Related"` -- **YES** (type is "Related")
2. `inwardIssue.key` or `outwardIssue.key` matches "TC-8001" -- **YES** (outwardIssue.key = "TC-8001")

**All criteria satisfied.** A matching Related link to TC-8001 already exists.

**Action: Skip link creation.**

Log: "Related link to TC-8001 already exists -- skipping"

No `jira.create_link()` call is made. The existing link (ID 1990401) is preserved as-is.

### Affects Versions Overlap Check

- TC-8006 (stream 2.1.x) Affects Versions: RHTPA 2.1.0
- TC-8001 (stream 2.2.x) Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected. Each issue carries only versions from its own stream. This is the expected configuration.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-8001    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <--| 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow indicates TC-8006 is the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration does not include the Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill specification, Step 4.3 is **skipped entirely** when any of these fields are not configured.

Result: **Skipped** (required custom fields not configured).

## Step 4.4 -- Preemptive Task Reconciliation

Search for preemptive tasks (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: **No matching preemptive tasks found** for CVE-2026-31812 in stream rhtpa-2.1.

Result: **No preemptive tasks to reconcile.** Proceeding to Step 5.
