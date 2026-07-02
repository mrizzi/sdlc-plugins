# Unsupported Ecosystem Notification

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

---

Automated triage has stopped at Step 1 (Data Extraction / Ecosystem Detection). The detected ecosystem "Go modules" does not appear in the Ecosystem Mappings table for any configured version stream. Without a matching ecosystem entry, the skill cannot determine the lock file path or check command needed for version impact analysis.

No version impact analysis, Affects Versions correction, or remediation task creation was performed.

Please assess the vulnerability manually:
- Determine which lock file or dependency manifest tracks Go module dependencies
- Inspect pinned source commits for the vulnerable library version
- Evaluate version impact across supported product versions
- Create remediation tasks if affected versions are identified
