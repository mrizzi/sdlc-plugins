<!-- SYNTHETIC TEST DATA — Vulnerability issue for a transitive dependency (h2) for triage-security eval testing -->

# Mock Jira Vulnerability Issue

**Key**: TC-8060
**Summary**: CVE-2026-99010 h2 - Memory exhaustion via CONTINUATION frames [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Labels**: CVE-2026-99010, pscomponent:org/rhtpa-server
**Affects Versions**: RHTPA 2.2.0
**Due Date**: 2026-08-15
**Assignee**: Unassigned
**Reporter**: psirt-analyst (account ID: 557058:psirt-analyst-mock-id)

## Remote Links

- [CVE-2026-99010](https://www.cve.org/CVERecord?id=CVE-2026-99010) — CVE Record
- [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) — Upstream fix PR

## Comments

_(no comments)_

---

## Description

A vulnerability was found in h2. The h2 crate before version 0.4.5 allows a remote attacker to cause memory exhaustion by sending a large number of CONTINUATION frames. This vulnerability is classified as a denial of service (DoS).

**Affected package**: h2
**Affected versions**: versions before 0.4.5
**Fixed version**: 0.4.5
**CVSS**: 7.5 (High)

The vulnerability exists because h2 does not properly limit the number of CONTINUATION frames that can be received for a single HEADERS frame, allowing an attacker to send an unbounded sequence that consumes server memory.

### References

- https://www.cve.org/CVERecord?id=CVE-2026-99010

---

## Mock Dependency Chain Data

The following data simulates what Step 2.3.5 would discover when inspecting
the Cargo.toml manifest files and Cargo.lock. In a real triage, the skill
reads manifests via `git show`; in this eval, use this data as the simulated
output.

### h2 dependency chain for backend

```
Dependency chain for h2:
  backend (workspace) → reqwest → hyper → h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup — reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency — it comes through reqwest → hyper → h2
```

**Lock file evidence (affected versions):**
```
# Cargo.lock (versions 2.2.0 through 2.2.2)
[[package]]
name = "h2"
version = "0.4.4"

[[package]]
name = "hyper"
version = "1.4.1"
dependencies = ["h2"]

[[package]]
name = "reqwest"
version = "0.12.5"
dependencies = ["hyper"]
```

**Lock file evidence (fixed versions):**
```
# Cargo.lock (versions 2.2.3+)
[[package]]
name = "h2"
version = "0.4.5"
```
