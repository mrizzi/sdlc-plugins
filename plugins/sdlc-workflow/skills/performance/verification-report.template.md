---
generated_by: {{skill-name}}
timestamp: {{iso-8601-timestamp}}
repository: {{repository-name}}
task: {{task-jira-key}}
pr: {{pr-url}}
---

# Performance Verification Report

## Verification Summary

**Task:** {{task-jira-key}} - {{task-title}}

**PR:** {{pr-url}}

**Verification Date:** {{verification-date}}

**Result:** {{result}} (PASS / PARTIAL SUCCESS / FAIL)

**Decision:** {{decision}} (APPROVE / REQUEST CHANGES / NEEDS INVESTIGATION)

## Before/After Comparison

### Target Scenario: {{target-scenario-name}}

| Metric | Before (Baseline) | After (Current) | Target | Status |
|---|---|---|---|---|
| **LCP** | {{before-lcp}}ms | {{after-lcp}}ms | ≤ {{target-lcp}}ms | {{lcp-status}} |
| **FCP** | {{before-fcp}}ms | {{after-fcp}}ms | ≤ {{target-fcp}}ms | {{fcp-status}} |
| **TTI** | {{before-tti}}ms | {{after-tti}}ms | ≤ {{target-tti}}ms | {{tti-status}} |
| **Total Load Time** | {{before-total}}ms | {{after-total}}ms | ≤ {{target-total}}ms | {{total-status}} |
| **Bundle Size** | {{before-bundle}}KB | {{after-bundle}}KB | ≤ {{target-bundle}}KB | {{bundle-status}} |

**Improvement Summary:**
- LCP: {{lcp-improvement}}% improvement
- FCP: {{fcp-improvement}}% improvement
- TTI: {{tti-improvement}}% improvement
- Total Load Time: {{total-improvement}}% improvement
- Bundle Size: {{bundle-improvement}}% reduction

**Status Legend:**
- ✅ PASS: Target achieved
- ⚠️ PARTIAL: Significant improvement (> 20%) but target not fully met
- ❌ FAIL: Target not met and improvement < 20%

## Regression Check

Performance validation for non-target scenarios to ensure no regressions introduced:

| Scenario | Metric | Before | After | Change | Status |
|---|---|---|---|---|---|
| {{scenario-1-name}} | LCP | {{scenario-1-before-lcp}}ms | {{scenario-1-after-lcp}}ms | {{scenario-1-lcp-change}}% | {{scenario-1-lcp-status}} |
| {{scenario-1-name}} | FCP | {{scenario-1-before-fcp}}ms | {{scenario-1-after-fcp}}ms | {{scenario-1-fcp-change}}% | {{scenario-1-fcp-status}} |
| {{scenario-2-name}} | LCP | {{scenario-2-before-lcp}}ms | {{scenario-2-after-lcp}}ms | {{scenario-2-lcp-change}}% | {{scenario-2-lcp-status}} |
| {{scenario-2-name}} | FCP | {{scenario-2-before-fcp}}ms | {{scenario-2-after-fcp}}ms | {{scenario-2-fcp-change}}% | {{scenario-2-fcp-status}} |

**Regression Threshold:** > 5% degradation in any metric

**Regressions Detected:** {{regressions-detected-count}}

{{regressions-detail}}

## Target Achievement

### Overall Assessment

**Acceptance Criteria Met:** {{acceptance-criteria-met}} / {{acceptance-criteria-total}}

**Specific Criteria:**
- [ ] {{criterion-1}} — {{criterion-1-status}}
- [ ] {{criterion-2}} — {{criterion-2-status}}
- [ ] {{criterion-3}} — {{criterion-3-status}}
- [ ] Target metrics achieved (LCP ≤ {{target-lcp}}ms, FCP ≤ {{target-fcp}}ms) — {{target-metrics-status}}
- [ ] No performance regressions in non-target scenarios (< 5% degradation) — {{regression-check-status}}

### Functional Testing

**Functional Tests:** {{functional-tests-status}} (PASS / FAIL)

**Test Results:**
- {{test-1-name}}: {{test-1-status}}
- {{test-2-name}}: {{test-2-status}}
- {{test-3-name}}: {{test-3-status}}

## Review Feedback

### PR Review Comments

{{pr-review-comments}}

### Code Review Issues

{{code-review-issues}}

## Recommendations

### For This PR

**Recommendation:** {{pr-recommendation}}

**Justification:** {{pr-justification}}

### Next Steps

{{next-steps}}

### Follow-Up Tasks

{{follow-up-tasks}}

## Verification Details

**Verification Method:** {{verification-method}}

**Baseline Used:** {{baseline-file-path}}

**Verification Run:** {{verification-run-timestamp}}

**Environment:**
- Node.js: {{nodejs-version}}
- Playwright: {{playwright-version}}
- Application Port: {{application-port}}

## Appendix

### Raw Metrics

<details>
<summary>Full baseline metrics JSON</summary>

```json
{{baseline-metrics-json}}
```
</details>

<details>
<summary>Full current metrics JSON</summary>

```json
{{current-metrics-json}}
```
</details>
