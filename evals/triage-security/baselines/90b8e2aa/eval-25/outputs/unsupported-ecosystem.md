# Unsupported Ecosystem Notification

## TC-8040 -- CVE-2026-31812 (quinn-proto)

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

### Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Supported ecosystems in 2.2.x stream**: Cargo, RPM
- **Supported ecosystems in 2.1.x stream**: Cargo, RPM

### Why triage stopped

The triage-security skill reads supported ecosystems from each stream's `security-matrix.md` Ecosystem Mappings table. The detected ecosystem (Go modules) does not appear in the Ecosystem Mappings table for any configured version stream. Without a matching ecosystem mapping, the skill cannot determine:

1. Which lock file to inspect (no `Lock File` configured for Go modules)
2. Which command to run for version extraction (no `Check Command` configured)
3. Which upstream branch to check for fixes (no `Upstream Branch` configured)

Automated version impact analysis (Step 2), dependency version extraction (Step 2.3), and remediation task creation (Step 8) all depend on the ecosystem mapping configuration.

### Required action

To enable automated triage for Go modules vulnerabilities, add an ecosystem mapping row to each stream's `security-matrix.md`:

```markdown
| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Go modules | backend | `go.sum` | `git show <tag>:go.sum` | `release/0.4.z` |
```

After updating the Ecosystem Mappings table, re-run `/sdlc-workflow:triage-security TC-8040` to resume automated triage.

Alternatively, proceed with manual assessment of the vulnerability impact across supported product versions.
