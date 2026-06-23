# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8006

## Step 4 -- JQL Search for Sibling Issues

**Query:**
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Results:** 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- Current issue TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Sibling TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

**Result:** TC-8001 is a **different-stream companion**, NOT a same-stream duplicate. The streams differ (2.1.x vs 2.2.x). PSIRT created one issue per stream intentionally. No duplicate closure needed.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling (companion tracker for the 2.2.x stream).

### Link Check (Idempotent)

Per Step 4.2 of `jira-triage-operations.md`, before creating a Related link, we must check the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches the sibling key `TC-8001`

**Checking existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward | TC-8001 |

**Match found:** Link ID 1990401 is a Related link connecting TC-8006 to TC-8001 (outward direction).

> Related link to TC-8001 already exists -- skipping

No `jira.create_link` call is needed. The pre-existing link already establishes the cross-stream relationship.

### Affects Versions Overlap Check

- TC-8006 (stream 2.1.x) Affects Versions: RHTPA 2.1.0
- TC-8001 (stream 2.2.x) Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

**Result:** No version overlap detected. Each issue carries versions exclusively from its own stream. This is the expected pattern for PSIRT-created per-stream companion issues.

### Sibling Landscape Table

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |

**Note:** TC-8001 is already In Progress in the 2.2.x stream, indicating active remediation work is underway for that stream. The 2.1.x stream (this issue) still requires triage and remediation.

## Step 4.3 -- Cross-CVE Overlap Detection

**Prerequisite check:** The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are NOT configured in the Security Configuration section of CLAUDE.md. These optional fields are required for Step 4.3.

**Result:** Step 4.3 skipped entirely -- required custom fields not configured.
