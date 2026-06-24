# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

Fix threshold (enriched, high confidence): **0.4.8**

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Summary by Stream

| Stream | Affected Versions | Not Affected Versions | Stream Status |
|--------|-------------------|-----------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NO versions affected** |

This is a **mixed impact** scenario: the 2.1.x stream ships a vulnerable version of h2 (0.4.5), while the 2.2.x stream ships the patched version (0.4.8+) in all releases.

### Dependency Chain Context

Dependency chain for h2 (Cargo):
- backend (workspace) uses h2 as a dependency (direct or transitive via hyper/reqwest HTTP stack)
- Profile: production (h2 is a runtime HTTP/2 protocol dependency)

In the 2.1.x stream, backend tags `v0.3.8` and `v0.3.12` both pin h2 at 0.4.5, which is below the fix threshold of 0.4.8.

In the 2.2.x stream, starting from the earliest version (2.2.0, tag `v0.4.5`), h2 is already at 0.4.8, which is at or above the fix threshold. The vulnerability was resolved before any 2.2.x release shipped.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD (simulated) | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | unknown (needs verification) | TBD |
| 2.2.x | Cargo | `release/0.4.z` | >= 0.4.8 (per shipped versions) | YES |

The 2.2.x stream's upstream branch already ships a fixed version. The 2.1.x stream requires verification of whether `release/0.3.z` has been updated with the h2 bump.
