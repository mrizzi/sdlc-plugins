# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

The triage-security skill detected the ecosystem for the vulnerable library **quinn-proto** as **Go modules**. However, the Ecosystem Mappings table in the security-matrix.md for the issue's scoped stream (2.2.x) does not include "Go modules" as a supported ecosystem.

**Supported ecosystems for stream 2.2.x:**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Detected ecosystem**: Go modules

Since "Go modules" is not present in the Ecosystem Mappings table, the skill cannot determine:
- Which lock file to inspect (e.g., `go.sum`, `go.mod`)
- Which check command to use for dependency version extraction
- Which repository contains the Go module dependencies
- Which upstream branch to check for fixes

### Impact

Automated version impact analysis (Step 2) cannot proceed for this ecosystem. The following triage steps are blocked:

- Step 2 (Version Impact Analysis) -- cannot inspect lock files without ecosystem mapping
- Step 2.3 (Dependency version extraction) -- no check command configured
- Step 2.3.5 (Dependency chain tracing) -- no lock file path known
- Step 2.5 (Upstream fix check) -- no upstream branch configured
- Step 8 (Remediation task creation) -- cannot generate tasks without version impact data

### Recommended Actions

1. **Manual assessment**: An engineer should manually inspect the relevant repositories to determine if quinn-proto (Go modules ecosystem) is present and at what version in each supported product version.

2. **Update security-matrix.md**: If Go modules dependencies are part of this product, add an ecosystem mapping row to the security-matrix.md files for each relevant stream:

   ```
   | Go modules | <repository> | go.sum | git show <tag>:go.sum | <upstream-branch> |
   ```

3. **Re-run triage**: After adding the ecosystem mapping, re-run `/sdlc-workflow:triage-security TC-8040` for automated triage.

### Triage Status

Automated triage has been **stopped** at Step 1 (Ecosystem Detection) due to the unsupported ecosystem. No Jira mutations have been performed. The issue remains in its current state (Status: New, Affects Versions: RHTPA 2.0.0).
