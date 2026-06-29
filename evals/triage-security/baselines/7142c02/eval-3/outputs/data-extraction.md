# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Existing comments | None | Issue comments |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped to a single stream)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

**Ecosystem**: Cargo (Rust crate)
**Lock file**: `Cargo.lock`
**Source repository**: rhtpa-backend

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812
- RUSTSEC Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
