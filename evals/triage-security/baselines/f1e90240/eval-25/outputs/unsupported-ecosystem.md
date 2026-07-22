# Unsupported Ecosystem Notification

## TC-8040 — CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

Ecosystem detection for the vulnerable library **quinn-proto** resolved to **Go modules**. However, the Ecosystem Mappings tables in the configured `security-matrix.md` files for all version streams only list the following supported ecosystems:

- **Cargo** — Rust crates (lock file: `Cargo.lock`)
- **RPM** — System packages (lock file: `rpms.lock.yaml`)

**Go modules** does not appear in any stream's Ecosystem Mappings table.

### Affected Streams

| Stream | Supported Ecosystems | Go modules listed? |
|--------|---------------------|--------------------|
| 2.1.x (rhtpa-release.0.3.z) | Cargo, RPM | No |
| 2.2.x (rhtpa-release.0.4.z) | Cargo, RPM | No |

### What this means

Automated version impact analysis (Step 2) cannot proceed because:

1. There is no lock file path configured for Go modules (e.g., `go.sum` or `go.mod`).
2. There is no check command configured for Go modules (e.g., `git show <tag>:go.sum`).
3. There is no upstream branch mapping for Go modules.

Without these mappings, the skill cannot determine which product versions ship the vulnerable dependency, cannot build the version impact table, and cannot generate remediation tasks.

### Recommended Actions

1. **Manual triage** — An engineer should manually inspect the relevant source repositories to determine if `quinn-proto` (or a Go module equivalent) is present in any supported product version.
2. **Add Go modules support** — If Go modules are a valid ecosystem for this product, update the `security-matrix.md` files for each version stream to add a Go modules row to the Ecosystem Mappings table with the appropriate repository, lock file path, check command, and upstream branch.
3. **Re-run triage** — After adding Go modules to the Ecosystem Mappings, re-run `/sdlc-workflow:triage-security TC-8040` to complete automated triage.

### Triage Status

Triage for TC-8040 has been **halted** at Step 1 (Ecosystem Detection) due to the unsupported ecosystem. No Jira mutations have been made. The issue remains in its current state.
