# Step 4 -- Duplicate and Sibling Check

## JQL Search

Search for sibling Vulnerability issues with the same CVE label, excluding the current issue:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

## Search Results

One sibling issue found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Stream Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- **TC-7999** stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`

Both issues have the **same** stream suffix `[rhtpa-2.2]`, mapping to the same product version stream `2.2.x`.

## Classification: DUPLICATE

Per Step 4.1 of the triage procedure, TC-7999 is a **same-stream sibling** of TC-8003. Both track CVE-2026-31812 for the same stream (2.2.x / [rhtpa-2.2]).

When a same-stream sibling exists and is open or in progress, the recommendation is to close the current issue (TC-8003) as a Duplicate of the existing issue (TC-7999).

### Sibling Details

- **TC-7999** is currently **In Progress**, meaning it is already being actively worked on.
- **TC-7999** has Affects Versions: **RHTPA 2.2.0, RHTPA 2.2.1** -- this is a superset of TC-8003's Affects Versions (RHTPA 2.2.0 only), so TC-7999 already covers the full version scope.

## Outcome

Same-stream sibling detected. TC-8003 should be closed as a Duplicate of TC-7999. This short-circuits the triage flow -- no further steps (version lifecycle check, already-fixed check, remediation task creation) are needed.
