# Step 1 -- Data Extraction: TC-8002

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-28940 | Labels: `CVE-2026-28940`; Summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | serde_json | Description text |
| Affected version range | versions before 1.0.135 (i.e., < 1.0.135) | Description text |
| Fixed version | 1.0.135 | Description text |
| CVSS | 5.3 (Medium) | Description text |
| Upstream fix PR | Not present | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 | Remote links |
| Due date | 2026-07-30 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Issue status | New | Issue status field |
| Assignee | Unassigned | Issue assignee field |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 3-4 apply to this stream only)

## Ecosystem Detection

- Library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Vulnerability Summary

serde_json versions before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit that defaults to 128 levels of nesting.

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
