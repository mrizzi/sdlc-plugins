# Unsupported Ecosystem Notification

## CVE: CVE-2026-31812
## Issue: TC-8040
## Library: quinn-proto
## Detected Ecosystem: Go modules

---

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

The triage-security skill determines the ecosystem from the vulnerable library name and component context. The supported ecosystems are defined in each stream's `security-matrix.md` Ecosystem Mappings table. For this product, the configured ecosystems are:

| Stream | Configured Ecosystems |
|--------|-----------------------|
| 2.1.x  | Cargo, RPM            |
| 2.2.x  | Cargo, RPM            |

The detected ecosystem **Go modules** does not appear in the Ecosystem Mappings table for any configured version stream. Without an ecosystem mapping, the skill cannot determine:

- Which **lock file** to inspect (e.g., `go.sum`, `go.mod`)
- Which **check command** to run for dependency version extraction
- Which **upstream branch** to check for fix status
- Which **repository** contains the relevant dependency metadata

### Recommended Actions

1. **Manual assessment**: Manually inspect the relevant repositories to determine whether `quinn-proto` (or an equivalent Go module dependency) is present in supported product versions and whether it falls within the affected range (versions before 0.11.14).

2. **Add Go modules to the Ecosystem Mappings**: If Go module dependencies are used in this product, update the `security-matrix.md` files to include a Go modules row in the Ecosystem Mappings table with the appropriate lock file path (`go.sum`), check command, and upstream branch. Example:

   | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
   |-----------|------------|-----------|---------------|-----------------|
   | Go modules | backend | `go.sum` | `git show <tag>:go.sum \| grep <library>` | `release/x.y.z` |

3. **Re-run triage**: After adding the ecosystem mapping, re-run `/triage-security TC-8040` to perform automated version impact analysis.

### Triage Status

Automated triage is **halted** at Step 1 (Ecosystem Detection). Steps 2 through 8 cannot proceed without a configured ecosystem mapping for Go modules.
