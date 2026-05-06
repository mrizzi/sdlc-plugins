# Performance Optimization Plan

**Workflow:** {workflow-name}  
**Generated:** {iso-8601-timestamp}  
**Overall Rating:** {current-rating} → Target: Excellent

---

## Executive Summary

**Current State:**
- LCP (p95): {current-lcp} ms (Target: 2500 ms)
- FCP (p95): {current-fcp} ms (Target: 1800 ms)
- DOM Interactive (p95): {current-domInteractive} ms (Target: 3500 ms)
- Total Load Time (p95): {current-total} ms (Target: 4000 ms)

**Expected Impact:**
- Estimated LCP improvement: {lcp-improvement} ms ({lcp-percentage}% reduction)
- Estimated FCP improvement: {fcp-improvement} ms ({fcp-percentage}% reduction)
- Estimated DOM Interactive improvement: {domInteractive-improvement} ms ({domInteractive-percentage}% reduction)
- Estimated bundle size reduction: {bundle-size-reduction} KB

**Total Effort Estimate:** {total-effort-days} days

---

## Impact Analysis Summary

**Total Optimizations Evaluated:** {total-count}  
**Recommended:** {recommend-count} optimizations → {task-count} tasks  
**Recommended with Caution:** {caution-count} optimizations (extra safeguards required)  
**Conditional:** {conditional-count} optimizations (prerequisites not met)  
**Deferred:** {defer-count} optimizations (documented for future review)  
**Rejected:** {reject-count} optimizations (risk > benefit)

### Decision Distribution

| Decision | Count | Reason |
|---|---|---|
| RECOMMEND | {recommend-count} | Safe, high-benefit optimizations |
| RECOMMEND WITH CAUTION | {caution-count} | High benefit but medium-high risk, extra safeguards required |
| CONDITIONAL | {conditional-count} | Prerequisites not met (infrastructure, feature flags, etc.) |
| DEFER | {defer-count} | Risk currently outweighs benefit |
| REJECT | {reject-count} | Not worth pursuing |

---

## Task Sequence

| # | Task | Category | Impact | Effort | Dependencies |
|---|---|---|---|---|---|
| 1 | {task-1-summary} | {category-1} | {impact-1} | {effort-1} | None |
| 2 | {task-2-summary} | {category-2} | {impact-2} | {effort-2} | Task 1 |
| ... | ... | ... | ... | ... | ... |

---

## Task Details

### Task 1: {task-1-summary}

**Category:** {category}  
**Impact:** {quantified-impact}  
**Effort:** {effort-estimate}  
**Risk:** {High / Medium / Low}

**Description:**
{what-this-task-achieves}

**Files to Modify:**
- `{file-path-1}` — {reason}
- `{file-path-2}` — {reason}

**Baseline Metrics:**
- LCP: {current-lcp} ms
- Bundle size: {current-bundle-size} KB

**Target Metrics:**
- LCP: < {target-lcp} ms
- Bundle size: < {target-bundle-size} KB

**Acceptance Criteria:**
- [ ] {criterion-1}
- [ ] {criterion-2}

**Performance Test Requirements:**
- [ ] Re-run baseline capture after implementation
- [ ] Verify LCP improvement of at least {improvement} ms
- [ ] Ensure no regressions in other metrics

**Dependencies:** {prerequisite-tasks}

**Rollback Strategy:** {how-to-undo-if-needed}

---

{... repeat for each task ...}

---

## Deferred and Rejected Optimizations

### Deferred for Future Review

{For each DEFER or CONDITIONAL decision:}

#### {optimization-name}

**Performance Benefit:** {quantified-impact} ({percentage}% improvement)  
**Decision:** {DEFERRED | CONDITIONAL}  
**Reason:** {why deferred or what prerequisites are missing}

**Impact Analysis:**
- **Impact Scope:** {scope}
- **Impact Severity:** {severity}
- **Affected Workflows:** {list}
- **Risk Factors:** {list}

**Conditions for Reconsideration:**
- {condition-1}
- {condition-2}

{If CONDITIONAL, list prerequisites:}
**Prerequisites:**
- {prerequisite-1}
- {prerequisite-2}
- **Estimated time to satisfy:** {estimate}

---

### Rejected Optimizations

{For each REJECT decision:}

#### {optimization-name}

**Performance Benefit:** {quantified-impact} ({percentage}% improvement)  
**Decision:** REJECTED  
**Reason:** {why rejected - explain risk/benefit analysis}

**Impact Analysis:**
- **Impact Scope:** {scope}
- **Impact Severity:** {severity}
- **Risk Factors:** {list}

**Rationale:** {detailed explanation of why risk far outweighs benefit}

**Alternative Approaches:** (if any)
- {alternative-1}
- {alternative-2}

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| {risk-1} | {likelihood} | {impact} | {mitigation-strategy} |
| {risk-2} | {likelihood} | {impact} | {mitigation-strategy} |
| ... | ... | ... | ... |

**Common Risks:**
- **Breaking changes:** Optimizations may introduce regressions. Mitigation: Comprehensive testing before merging.
- **Performance measurement noise:** Baseline variability may obscure small improvements. Mitigation: Run multiple baseline iterations.
- **Third-party library constraints:** Some optimizations may be blocked by library limitations. Mitigation: Evaluate alternative libraries.

---

## Rollback Strategy

If an optimization causes issues:

1. **Immediate rollback:** Revert the commit and redeploy previous version
2. **Root cause analysis:** Investigate what caused the issue
3. **Revised approach:** Update the optimization plan and re-attempt with fixes
4. **Re-baseline:** Capture new baseline to measure impact of rollback

---

## Next Steps

1. **Review this plan** with the team and adjust task sequencing if needed
2. **Create Jira Epic and Tasks** — This skill will create these automatically
3. **Implement tasks** in sequence using `/sdlc-workflow:implement-task {task-id}`
4. **Re-baseline after each task** using `/sdlc-workflow:performance-baseline` to measure improvements
5. **Final verification** using `/sdlc-workflow:performance-verify-optimization` to validate all targets met
