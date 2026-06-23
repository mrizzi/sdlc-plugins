# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8003

## 4.0 -- JQL Search for Sibling Issues

JQL query executed (simulated):

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results: 1 sibling found.**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-Stream Duplicate Analysis

### Stream comparison

| Issue | Stream Suffix | Mapped Stream |
|-------|---------------|---------------|
| TC-8003 (current) | [rhtpa-2.2] | 2.2.x |
| TC-7999 (sibling) | [rhtpa-2.2] | 2.2.x |

**Classification: Same-stream sibling** -- both TC-8003 and TC-7999 carry the stream suffix `[rhtpa-2.2]`, mapping to the same version stream (2.2.x).

### Duplicate determination

TC-7999 is a same-stream sibling that is currently **In Progress**. Per Step 4.1 of the triage-security methodology:

> "If a same-stream sibling exists and is open or in progress: Recommendation -- Close the current issue as Duplicate."

TC-7999 already has a broader set of Affects Versions (RHTPA 2.2.0 and RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only), and is actively being worked on (status: In Progress). The current issue TC-8003 is a duplicate that adds no new tracking value.

### Conclusion

**TC-8003 is a duplicate of TC-7999.**

- Both issues track CVE-2026-31812 for the same component (pscomponent:org/rhtpa-server) in the same stream (2.2.x).
- TC-7999 is already In Progress with a superset of Affects Versions.
- The duplicate detection short-circuits the triage flow -- no remediation tasks should be created, and Steps 5-7 are not reached.

## 4.2 -- Cross-Stream Coordination

Not applicable -- no different-stream siblings were found. The only sibling (TC-7999) is a same-stream duplicate.

## 4.3 -- Cross-CVE Overlap Detection

Skipped -- the Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in Security Configuration. Step 4.3 requires all three fields to be configured.
