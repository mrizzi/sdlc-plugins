# Step 1 -- Data Extraction

## Issue: TC-8001

**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Ecosystem | Cargo | Identified from library name (quinn-proto is a Rust crate) and confirmed by Ecosystem Mappings table in security-matrix.md |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Due date | 2026-07-15 | Jira `duedate` field |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Parsed stream: **2.2.x**
- Matched to Version Streams table: **2.2.x** at `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 2-7 apply only to this stream)

## Ecosystem Detection

- Library: **quinn-proto** -- this is a Rust crate (published on crates.io)
- Ecosystem Mappings in the 2.2.x stream's security-matrix.md confirms **Cargo** ecosystem
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: `backend`
- Upstream branch: `release/0.4.z`

Since this is a **Cargo** (source dependency) ecosystem, remediation will require **two tasks**: an upstream backport task and a downstream propagation subtask with a Blocks dependency.
