# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8006

## Step 4 JQL Search

Search for sibling Vulnerability issues with the same CVE label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

**Result**: 1 sibling found.

| Key | Summary | Status | Stream Suffix | Affects Versions |
|-----|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

TC-8001 is a **different-stream sibling** (companion tracker), not a same-stream duplicate. No duplicate closure applies.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a cross-stream companion for the same CVE (CVE-2026-31812), tracking the 2.2.x stream while TC-8006 tracks the 2.1.x stream.

### Link Check (Idempotent)

Before creating a Related link to TC-8001, check the current issue's `issuelinks` array (fetched in Step 1).

Existing issuelinks on TC-8006:
- Link ID 1990401: type.name = "Related", direction = outward, outwardIssue.key = "TC-8001"

**Check result**: A link satisfying all conditions exists:
1. `type.name` is "Related" -- YES
2. `outwardIssue.key` matches sibling key TC-8001 -- YES

> Related link to TC-8001 already exists -- skipping

No `jira.create_link` call is made. The pre-existing Related link (ID 1990401) already establishes the cross-stream companion relationship.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue carries versions from its own stream only.

### Sibling Landscape Table

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The sibling landscape is presented to the engineer for awareness. TC-8001 is already being actively triaged (status: In Progress) for the 2.2.x stream. Triage of TC-8006 proceeds independently for the 2.1.x stream.
