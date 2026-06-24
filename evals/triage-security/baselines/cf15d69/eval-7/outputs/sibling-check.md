# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8006

## 4.0 -- JQL Search for Siblings

Search query (simulated):
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Results: 1 sibling found

| Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **Different-stream sibling** (companion tracker)

TC-8001 is NOT a same-stream duplicate. It tracks the same CVE but for a different version stream. PSIRT creates one issue per stream intentionally.

No same-stream duplicates found. No duplicate closure recommended.

## 4.2 -- Cross-stream Coordination

TC-8001 is a **different-stream sibling** (companion tracker for stream 2.2.x).

### Link Check (Idempotent)

Per Step 4.2 procedure: before creating a link, check the current issue's `issuelinks` array (already fetched in Step 1) for an existing link that satisfies ALL of:
1. `type.name` is "Related"
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

**Existing links on TC-8006:**
- Related: TC-8001 (outward, Link ID: 1990401)

**Check result:** A matching link exists:
- Type: "Related" -- matches criterion 1
- outwardIssue.key: TC-8001 -- matches criterion 2

**Decision: Related link to TC-8001 already exists -- skipping link creation.**

No `jira.create_link()` call is needed. The pre-existing Related link satisfies the cross-stream coordination requirement.

### Affects Versions Overlap Check

- TC-8006 (stream 2.1.x) Affects Versions: RHTPA 2.1.0
- TC-8001 (stream 2.2.x) Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1

No overlap detected. Each issue carries versions only from its own stream. This is correct -- no version overlap flag needed.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

Note: TC-8006's Affects Versions (RHTPA 2.1.0) may need correction in Step 3 -- the version impact table shows both 2.1.0 and 2.1.1 are affected, but the PSIRT-assigned Affects Versions only includes 2.1.0. The Affects Versions correction should add RHTPA 2.1.1 (pending Jira version discovery and engineer confirmation).

## 4.3 -- Cross-CVE Overlap Detection

The Security Configuration does not include an Upstream Affected Component custom field, PS Component custom field, or Stream custom field. Per the skill procedure, Step 4.3 is **skipped entirely** when these fields are not configured.

## 4.4 -- Preemptive Task Reconciliation

Search query (simulated):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 in stream 2.1.x. Proceeding to Step 5.
