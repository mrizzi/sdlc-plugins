# Triage Outcome — TC-8003

## Decision: Close as Duplicate

**Recommendation:** Close TC-8003 as a duplicate of **TC-7999**.

### Proposed Jira Actions

1. **Transition** TC-8003 to **Closed** with resolution **Duplicate**
2. **Link** TC-8003 to TC-7999 with link type "duplicates" (TC-8003 duplicates TC-7999)
3. **Add comment** to TC-8003 (see below)

### Proposed Comment for TC-8003

> Closing as duplicate of TC-7999.
>
> Both TC-8003 and TC-7999 track the same vulnerability — CVE-2026-31812 (quinn-proto panic on large stream counts) — for the same product stream [rhtpa-2.2] (2.2.x). TC-7999 is already **In Progress**, so remediation is already underway.
>
> TC-7999 also covers a broader set of affected versions (RHTPA 2.2.0 and RHTPA 2.2.1) compared to this issue (RHTPA 2.2.0 only), making it the more complete tracking issue.
>
> No further triage or remediation action is required on this issue.

### Rationale

- **Same CVE:** Both issues carry the label CVE-2026-31812 and reference the same vulnerability in the quinn-proto crate (versions before 0.11.14).
- **Same stream:** Both issues have the stream suffix [rhtpa-2.2], mapping to the 2.2.x version stream. There is no need for two separate tracking issues for the same CVE in the same stream.
- **Work already in progress:** TC-7999 is in **In Progress** status, indicating that remediation has already been started. Duplicating the effort would be wasteful.
- **Broader coverage on original:** TC-7999 already lists RHTPA 2.2.0 and RHTPA 2.2.1 in its Affects Versions, while TC-8003 only lists RHTPA 2.2.0.

### What is NOT done (short-circuited by duplicate detection)

The following triage steps are intentionally skipped because the duplicate check short-circuits the triage flow:

- Version exposure analysis (checking which builds ship the vulnerable quinn-proto version)
- Fix verification (checking whether the fix is present in latest builds)
- Remediation task creation
- Upstream fix tracking

All of these activities are expected to be handled under TC-7999.
