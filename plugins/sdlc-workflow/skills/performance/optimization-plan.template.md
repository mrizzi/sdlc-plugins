---
generated_by: {{skill-name}}
timestamp: {{iso-8601-timestamp}}
repository: {{repository-name}}
module: {{module-name}}
---

# Performance Optimization Plan: {{module-name}}

## Executive Summary

**Optimization Goal:** {{optimization-goal}}

**Expected Impact:**
- LCP improvement: {{expected-lcp-improvement}}% ({{baseline-lcp}}ms → {{target-lcp}}ms)
- FCP improvement: {{expected-fcp-improvement}}% ({{baseline-fcp}}ms → {{target-fcp}}ms)
- Bundle size reduction: {{expected-bundle-reduction}}% ({{baseline-bundle}}KB → {{target-bundle}}KB)

**Total Effort Estimate:** {{total-effort-estimate}} engineering days

**Risk Level:** {{risk-level}} (LOW/MEDIUM/HIGH)

## Task Sequence

Optimizations listed in recommended implementation order:

| # | Task | Impact | Effort | Dependencies |
|---|---|---|---|---|
| 1 | {{task-1-title}} | {{task-1-impact}} | {{task-1-effort}} | None |
| 2 | {{task-2-title}} | {{task-2-impact}} | {{task-2-effort}} | Task 1 |
| 3 | {{task-3-title}} | {{task-3-impact}} | {{task-3-effort}} | Task 1 |
| 4 | {{task-4-title}} | {{task-4-impact}} | {{task-4-effort}} | Task 2, Task 3 |

**Sequencing Rationale:** {{sequencing-rationale}}

## Per-Task Details

### Task 1: {{task-1-title}}

**Jira Issue:** {{task-1-jira-key}}

**Baseline Metrics:**
- LCP: {{task-1-baseline-lcp}}ms
- Bundle Size: {{task-1-baseline-bundle}}KB

**Target Metrics:**
- LCP: {{task-1-target-lcp}}ms ({{task-1-improvement}}% improvement)
- Bundle Size: {{task-1-target-bundle}}KB

**Optimization Strategy:** {{task-1-strategy}}

**Files to Modify:**
- `{{task-1-file-1}}`
- `{{task-1-file-2}}`

**Risk Assessment:** {{task-1-risk}}

**Rollback Plan:** {{task-1-rollback}}

### Task 2: {{task-2-title}}

**Jira Issue:** {{task-2-jira-key}}

**Baseline Metrics:**
- API Latency (p95): {{task-2-baseline-latency}}ms
- Over-fetching: {{task-2-baseline-overfetch}}% unused fields

**Target Metrics:**
- API Latency (p95): {{task-2-target-latency}}ms ({{task-2-improvement}}% improvement)
- Over-fetching: {{task-2-target-overfetch}}%

**Optimization Strategy:** {{task-2-strategy}}

**Files to Modify:**
- `{{task-2-file-1}}`
- `{{task-2-file-2}}`

**Risk Assessment:** {{task-2-risk}}

**Rollback Plan:** {{task-2-rollback}}

### Task 3: {{task-3-title}}

**Jira Issue:** {{task-3-jira-key}}

**Baseline Metrics:**
- Render-blocking resources: {{task-3-baseline-blocking}} resources
- Critical path duration: {{task-3-baseline-critical-path}}ms

**Target Metrics:**
- Render-blocking resources: {{task-3-target-blocking}} resources
- Critical path duration: {{task-3-target-critical-path}}ms ({{task-3-improvement}}% improvement)

**Optimization Strategy:** {{task-3-strategy}}

**Files to Modify:**
- `{{task-3-file-1}}`
- `{{task-3-file-2}}`

**Risk Assessment:** {{task-3-risk}}

**Rollback Plan:** {{task-3-rollback}}

## Risk Assessment

### Overall Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| {{risk-1-name}} | {{risk-1-likelihood}} | {{risk-1-impact}} | {{risk-1-mitigation}} |
| {{risk-2-name}} | {{risk-2-likelihood}} | {{risk-2-impact}} | {{risk-2-mitigation}} |
| {{risk-3-name}} | {{risk-3-likelihood}} | {{risk-3-impact}} | {{risk-3-mitigation}} |

**Risk Levels:**
- **LOW:** Well-understood optimization, minimal code changes, easy rollback
- **MEDIUM:** Moderate code changes, requires thorough testing, rollback plan required
- **HIGH:** Architectural changes, affects multiple modules, requires staged rollout

## Rollback Strategy

### Per-Task Rollback

Each task includes a specific rollback plan in the task details above.

### Global Rollback Strategy

If multiple optimizations are deployed and regressions are detected:

1. **Immediate rollback:** Revert the most recent deployment
2. **Identify culprit:** Use baseline comparison to identify which optimization caused regression
3. **Selective revert:** Revert only the problematic optimization, keep successful ones
4. **Root cause analysis:** Investigate why regression occurred (missed test scenario, incorrect metric interpretation, etc.)
5. **Re-test and re-deploy:** Fix issue, re-run baseline, re-deploy

### Rollback Trigger Criteria

Automatic rollback if:
- Any Core Web Vital degrades > 10% from baseline in production
- Error rate increases > 2% from baseline
- User-reported performance complaints increase significantly

## Jira Epic and Tasks

**Epic:** {{epic-jira-key}} - {{epic-title}}

**Tasks:**
- {{task-1-jira-key}}: {{task-1-title}}
- {{task-2-jira-key}}: {{task-2-title}}
- {{task-3-jira-key}}: {{task-3-title}}
- {{task-4-jira-key}}: {{task-4-title}}

All tasks linked to Epic via "Incorporates" relationship.

## Next Steps

1. Review this plan with team
2. Confirm task priorities and sequencing
3. Begin implementation with Task 1: {{task-1-jira-key}}
4. Run `/sdlc-workflow:performance-implement-optimization {{task-1-jira-key}}` to start
