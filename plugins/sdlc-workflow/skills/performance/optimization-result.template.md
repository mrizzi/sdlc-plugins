---
metadata:
  jira_key: {{jira-key}}
  workflow: {{workflow-name}}
  timestamp: {{iso-timestamp}}
  branch: {{git-branch}}
  commit_sha: {{commit-sha}}
  baseline_commit_sha: {{baseline-commit-sha}}
  capture_mode: {{capture-mode}}
  status: pending_verification
---

# Optimization Result: {{jira-key}}

**Task:** {{task-summary}}  
**Workflow:** {{workflow-name}}  
**Executed:** {{formatted-timestamp}}  
**Branch:** {{git-branch}}

## Performance Impact

| Metric | Baseline (p95) | After Optimization (p95) | Delta | Target | Status |
|---|---|---|---|---|---|
| LCP | {{baseline-lcp}}ms | {{current-lcp}}ms | {{delta-lcp}} | {{target-lcp}}ms | {{status-lcp}} |
| FCP | {{baseline-fcp}}ms | {{current-fcp}}ms | {{delta-fcp}} | {{target-fcp}}ms | {{status-fcp}} |
| DOM Interactive | {{baseline-dom}}ms | {{current-dom}}ms | {{delta-dom}} | {{target-dom}}ms | {{status-dom}} |
| Total Load Time | {{baseline-total}}ms | {{current-total}}ms | {{delta-total}} | {{target-total}}ms | {{status-total}} |

**Performance Summary:**
- {{summary-line}}

## Test Scenarios Measured

{{scenarios-list}}

## Code Changes

- Commit: {{commit-sha}}
- PR: {{pr-url}}
- Files modified: {{files-changed}}

## Validation

{{validation-checks}}

## Next Steps

- Verify PR passes acceptance criteria with `/sdlc-workflow:performance-verify-optimization {{jira-key}}`
- After PR merge to main, re-run `/sdlc-workflow:performance-baseline` to update configuration with fresh metrics
- Continue with remaining optimization tasks if targets not fully met
