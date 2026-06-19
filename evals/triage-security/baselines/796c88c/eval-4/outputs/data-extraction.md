# Data Extraction — TC-8004

## Step 1: Parse Issue Fields

| Field | Value |
|-------|-------|
| **Key** | TC-8004 |
| **Summary** | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Labels** | CVE-2026-33501, pscomponent:org/rhtpa-server |
| **Affects Versions** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **CVSS** | 7.5 (High) |

## CVE Details

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-33501 |
| **Affected package** | h2 (Rust crate) |
| **Ecosystem** | Cargo |
| **Affected versions** | < 0.4.8 |
| **Fixed version** | 0.4.8 |
| **Vulnerability** | Memory exhaustion via excessive CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block. |
| **Fix** | Adds a configurable maximum header list size (defaults to 16 KiB) |

## Scope Determination

The issue summary has **NO stream suffix** — this is an **UNSCOPED** issue covering all streams. The version impact analysis must check ALL versions across ALL streams.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Component

- `pscomponent:org/rhtpa-server` — maps to `rhtpa-backend` repository (Cargo ecosystem)

## Lock File Location

- Repository: `rhtpa-backend`
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
