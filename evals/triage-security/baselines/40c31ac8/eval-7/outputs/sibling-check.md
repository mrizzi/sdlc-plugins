# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## Step 4 -- JQL Search for Siblings

**Query executed:**
```
jira.search_jql(
  "project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006"
)
```

**Result:** 1 sibling issue found.

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Sibling Classification

- **TC-8001**: stream suffix `[rhtpa-2.2]` vs. current issue TC-8006 stream suffix `[rhtpa-2.1]`
- Classification: **Different-stream sibling** (companion tracker, NOT a duplicate)
- Rationale: PSIRT creates one Vulnerability issue per stream intentionally. TC-8001 tracks the 2.2.x stream; TC-8006 tracks the 2.1.x stream. These are companion issues for the same CVE across different product version streams.

## Step 4.1 -- Same-Stream Duplicate Check

No same-stream siblings found. TC-8001 has a different stream suffix (`[rhtpa-2.2]` vs `[rhtpa-2.1]`), so it is not a same-stream duplicate.

Result: **No duplicates detected.** Proceed with triage.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream companion. Per Step 4.2 procedure:

### 1. Check for existing link before creating one

Read TC-8006's `issuelinks` array from the `jira.get_issue` response (already fetched in Step 1). Check if any existing link satisfies all of:
- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches `TC-8001`

**Existing links on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward | TC-8001 |

**Match found:** Link ID 1990401 has `type.name = "Related"` and `outwardIssue.key = "TC-8001"`. All conditions are satisfied.

**Decision: Related link to TC-8001 already exists -- skipping link creation.**

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The pre-existing link is sufficient for cross-stream coordination.

### 2. Verify no Affects Versions overlap

- TC-8006 (stream 2.1.x): Affects Versions = [RHTPA 2.1.0]
- TC-8001 (stream 2.2.x): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

**No overlap detected.** Each issue carries only versions from its own stream. The version sets are disjoint (2.1.x vs 2.2.x). No action required.

### 3. Present the sibling landscape

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<-`) marks the current issue being triaged.

## Summary of Step 4.2 Actions

| Action | Result |
|--------|--------|
| Check existing issuelinks for Related link to TC-8001 | Found: Link ID 1990401 (Related, outward, TC-8006 -> TC-8001) |
| Create Related link to TC-8001 | **SKIPPED** -- link already exists |
| Check Affects Versions overlap | No overlap (2.1.x vs 2.2.x versions are disjoint) |
| Present sibling landscape table | Presented above |

## Step 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the Security Configuration for this project. Per the skill definition, Step 4.3 is skipped entirely when these fields are not configured.

## Step 4.4 -- Preemptive Task Reconciliation

A JQL search for preemptive tasks matching CVE-2026-31812 and stream rhtpa-2.1 would be performed:

```
jira.search_jql(
  "project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC",
  fields: ["summary", "status", "labels", "issuelinks"]
)
```

Per the eval instructions, no preemptive task data is provided, so this step proceeds silently to Step 5.
