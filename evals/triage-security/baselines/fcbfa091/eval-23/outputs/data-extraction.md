# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2]) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Ecosystem | Cargo |

## Deployment Context Lookup

Source repository identified from component label `pscomponent:org/rhtpa-server` -> **rhtpa-backend**.

Looked up in Source Repositories table from Security Configuration (Step 0):

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. The `customer-shipped` context requires coordination with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

From security-matrix.md Ecosystem Mappings (2.2.x stream):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Version Impact Analysis

### 2.2.x stream (issue scope)

| Version | Build | Backend Tag | quinn-proto Version | Affected? |
|---------|-------|-------------|---------------------|-----------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 (same as 2.2.1, retag) | YES (< 0.11.14) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO (>= 0.11.14, fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO (>= 0.11.14, fixed) |

### 2.1.x stream (cross-stream check)

| Version | Build | Backend Tag | quinn-proto Version | Affected? |
|---------|-------|-------------|---------------------|-----------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

### Summary

- **2.2.x stream** (scoped): Versions 2.2.0, 2.2.1, 2.2.2 are affected. Fix already present in 2.2.3+ (quinn-proto bumped to 0.11.14 in build 0.4.11).
- **2.1.x stream** (cross-stream): All versions (2.1.0, 2.1.1) are affected. No fix present in this stream.

### Affects Versions Correction

Current Affects Versions `RHTPA 2.0.0` is incorrect -- there is no 2.0.x version stream in the configuration. Based on lock file evidence, the correct Affects Versions for the 2.2.x-scoped issue are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.
