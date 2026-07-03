# Unsupported Ecosystem Notification: TC-8040

## Triage Halted -- Unsupported Ecosystem

**Issue**: TC-8040
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Detected ecosystem**: Go modules

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Explanation

The triage-security skill determines the ecosystem from the vulnerable library name and component context. The supported ecosystems are defined in each version stream's `security-matrix.md` Ecosystem Mappings table. For this project, the configured ecosystems are:

| Stream | Configured Ecosystems |
|--------|-----------------------|
| 2.1.x (rhtpa-release.0.3.z) | Cargo, RPM |
| 2.2.x (rhtpa-release.0.4.z) | Cargo, RPM |

The detected ecosystem "Go modules" does not appear in any stream's Ecosystem Mappings table. Without a configured mapping, the skill cannot determine:

- Which **repository** contains the Go module dependency
- Which **lock file** to inspect (e.g., `go.sum`, `go.mod`)
- Which **check command** to use for version extraction
- Which **upstream branch** to check for fix status

### What Was Completed

- Step 0: Project configuration validated (Security Configuration present and complete)
- Step 0.3: Matrix staleness check (Last-Updated: 2026-06-28, 5 days ago -- within 14-day threshold)
- Step 1: CVE data extraction completed (see data-extraction.md)
- Step 1 Ecosystem Detection: Resolved to "Go modules" -- not in Ecosystem Mappings

### What Cannot Proceed

- Step 2: Version impact analysis -- cannot inspect lock files without ecosystem mapping
- Steps 3-8: All subsequent triage steps depend on version impact data from Step 2

### Recommended Actions

1. **Add Go modules to the Ecosystem Mappings** in `security-matrix.md` for each affected stream. The mapping should include:
   - Ecosystem: `Go modules`
   - Repository: the source repository containing Go dependencies
   - Lock File: `go.sum` (or the appropriate Go lock file)
   - Check Command: `git show <tag>:go.sum | grep <library>` (or equivalent)
   - Upstream Branch: the branch feeding each stream

2. **Re-run triage** after updating the ecosystem mappings:
   ```
   /sdlc-workflow:triage-security TC-8040
   ```

3. **Manual assessment alternative**: if adding ecosystem support is not feasible, perform manual version impact analysis by inspecting Go dependency files at the pinned source commits listed in the supportability matrix and compare against the fix threshold (quinn-proto >= 0.11.14).
