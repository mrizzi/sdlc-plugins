# Unsupported Ecosystem Notification

## Triage Halted: Unsupported Ecosystem Detected

**Issue**: TC-8040
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected Ecosystem**: Go modules

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

## Details

During Step 1 (Data Extraction) ecosystem detection, the vulnerable library `quinn-proto` was resolved to the **Go modules** ecosystem. However, the Ecosystem Mappings tables in the security matrices for the configured version streams do not include Go modules:

**Stream 2.1.x** (`rhtpa-release.0.3.z`) supported ecosystems:
- Cargo
- RPM

**Stream 2.2.x** (`rhtpa-release.0.4.z`) supported ecosystems:
- Cargo
- RPM

Since Go modules is not listed in any stream's Ecosystem Mappings table, the skill cannot determine:
- Which lock file to inspect (e.g., `go.sum`, `go.mod`)
- Which check command to use for dependency version extraction
- Which repository contains the Go module dependencies
- Which upstream branch to check for fix status

## Recommended Actions

1. **Manual assessment**: An engineer should manually verify whether `quinn-proto` (or a Go equivalent) is present in the project's dependency tree and at what version.

2. **Add Go modules ecosystem support**: If the project uses Go modules, update the `security-matrix.md` files for each stream to include a Go modules row in the Ecosystem Mappings table. For example:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum` | `release/0.4.z` |

3. **Re-run triage**: After adding Go modules to the ecosystem mappings, re-invoke `/sdlc-workflow:triage-security TC-8040` to complete automated triage.

## Triage Status

- Step 0 (Validate Configuration): PASSED
- Step 0.3 (Matrix Staleness Check): PASSED (Last-Updated: 2026-06-28, 4 days ago -- within 14-day threshold)
- Step 1 (Data Extraction): COMPLETED (see outputs/data-extraction.md)
- Step 1 (Ecosystem Detection): HALTED -- unsupported ecosystem
- Steps 2-8: NOT EXECUTED
