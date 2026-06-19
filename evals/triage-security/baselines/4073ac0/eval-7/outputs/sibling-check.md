# Step 4 -- Duplicate and Sibling Check: TC-8006

## JQL Search

Query executed:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

- Current issue TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- Sibling TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
- Classification: **DIFFERENT-STREAM companion** (not a same-stream duplicate)

No same-stream duplicates found. TC-8001 is a cross-stream companion tracker, not a duplicate. Triage continues.

## Step 4.2 -- Cross-Stream Coordination

### Idempotent Link Check for TC-8001

Before creating a 'Related' link to sibling TC-8001, checking existing issuelinks on TC-8006.

Existing issuelinks on TC-8006 (from Step 1 data extraction):

| Link ID | Type | Direction | Target Key |
|---------|------|-----------|------------|
| 1990401 | Related | outward | TC-8001 |

Check criteria for TC-8001:
- type.name == "Related"? **YES**
- outwardIssue.key == "TC-8001"? **YES**

**Result: A matching 'Related' link already exists.**

> Related link to TC-8001 already exists -- skipping

Link creation (`jira.create_link`) is NOT called. The pre-existing link (ID 1990401) already satisfies the cross-stream coordination requirement.

### Affects Versions Overlap Check

- TC-8006 (stream 2.1.x): Affects Versions = [RHTPA 2.1.0]
- TC-8001 (stream 2.2.x): Affects Versions = [RHTPA 2.2.0, RHTPA 2.2.1]

No version overlap detected. Each issue carries only versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The sibling landscape is presented despite the link already existing -- the idempotent check only affects link creation, not the sibling summary.

## Outcome

- TC-8001 is a **different-stream companion** (stream 2.2.x vs current 2.1.x)
- Pre-existing 'Related' link detected and skipped (idempotent)
- No version overlap between the two issues
- No same-stream duplicates found
- Triage continues to Step 5 (Version Lifecycle Check)
