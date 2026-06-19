# Step 2 -- Version Impact Analysis

## Supportability Matrix

Loaded from two streams configured in Security Configuration:

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction

Extracted h2 versions from `Cargo.lock` at each pinned tag via
`git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`:

| Tag | h2 version |
|-----|------------|
| `v0.3.8` | 0.4.5 |
| `v0.3.12` | 0.4.5 |
| `v0.4.5` | 0.4.8 |
| `v0.4.8` | 0.4.8 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.4.9 |
| `v0.4.12` | 0.4.9 |

## Version Impact Table

CVE-2026-33501 affects h2 versions **before 0.4.8**. Fixed in 0.4.8.

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 |

**Summary**: Mixed impact across streams.
- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

## Dependency Chain Context

Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime dependency used for HTTP/2 support)

The h2 crate is a transitive dependency pulled in via hyper, the HTTP library
used by the backend service. It is present in all production builds that include
HTTP/2 support.

Present in: 2.1.x stream (h2 0.4.5 -- vulnerable)
Not vulnerable in: 2.2.x stream (h2 >= 0.4.8 -- fixed)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | Not checked (proposed) | Unknown |
| 2.2.x | Cargo | release/0.4.z | >= 0.4.8 | YES |

The 2.2.x stream already ships the fixed version. Remediation is only needed
for the 2.1.x stream. The upstream branch `release/0.3.z` should be checked
to determine if a fix has already been applied at HEAD.
