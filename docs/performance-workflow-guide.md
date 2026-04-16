# Performance Optimization Workflow Guide

Quick reference for using the performance optimization workflow in sdlc-workflow plugin.

---

## Overview

**Purpose:** Measure, analyze, and improve frontend application performance using automated metrics collection, anti-pattern detection, and Jira-integrated planning.

**When to use:**
- ✅ Feature is functionally complete but has performance issues
- ✅ Establishing performance baseline before changes
- ✅ Identifying bottlenecks in a user journey
- ✅ Preparing for release (validate targets)

**When NOT to use:**
- ❌ Building new features from scratch → use `plan-feature`
- ❌ Fixing non-performance bugs → use `implement-task`

---

## Prerequisites

| Requirement | Details |
|---|---|
| Playwright installed | `npm install -D @playwright/test && npx playwright install` |
| Application running | Localhost (e.g., `http://localhost:3000`) |
| Test data loaded | Representative data for accurate measurements |
| Stable environment | Close unnecessary apps, disable browser extensions |

---

## Workflow Steps

```
setup (with workflow selection) → baseline → analyze → plan → implement → verify
```

| Step | Skill | Purpose | Output |
|---|---|---|---|
| 1 | `performance-setup` | Initialize configuration & select workflow | `.claude/performance-config.md` with selected workflow |
| 2 | `performance-baseline` | **Select mode** (cold/e2e/both) & capture metrics | `baseline-report.md` with Core Web Vitals |
| 3 | `performance-analyze-module` | **Inspect source code** to detect anti-patterns | `workflow-analysis-report.md` with findings |
| 4 | `performance-plan-optimization` | **Read analysis report** and create Jira tasks | Jira Epic + Tasks, `optimization-plan.md` |
| 5 | `performance-implement-optimization` | Execute optimization with validation | PR with before/after metrics |
| 6 | `performance-verify-optimization` | Verify PR and detect regressions | Verification report (PASS/WARN/FAIL) |

**Key distinction:** Step 4 analyzes code, Step 5 reads the report.

---

## Workflow Diagram

```mermaid
graph TD
    A[performance-setup<br/>Select workflow] --> B[performance-baseline]
    B --> C[performance-analyze-module<br/>Source code inspection]
    C --> D[performance-plan-optimization<br/>Read report, create tasks]
    D --> E[performance-implement-optimization]
    E --> F{Targets<br/>met?}
    F -->|Regression| G[Stop - investigate]
    F -->|Improvement| H[Create PR]
    H --> I[performance-verify-optimization]
    I --> J{Overall?}
    J -->|PASS| K[Merge]
    J -->|WARN/FAIL| E
    K --> L{More<br/>tasks?}
    L -->|Yes| E
    L -->|No| M[Done]
```

---

## Baseline Capture Modes

The baseline skill supports three measurement modes:

**cold-start (Recommended for initial baseline):**
- Direct navigation to each URL
- Measures worst-case performance (first visit, cold cache)
- Use case: Establish performance floor, measure direct-link scenarios

**e2e (Realistic workflow measurement):**
- Uses your existing e2e test automation scripts
- Measures realistic navigation flow (list → click → detail)
- Captures warm cache benefits and API call timing
- **No special instrumentation required:** Metrics captured from browser DevTools during e2e execution

**both (Comprehensive):**
- Runs e2e workflow first, then cold-start direct navigation
- Provides both realistic and worst-case metrics
- Best for comparing optimization impact across both scenarios

---

## Quick Example

```bash
# 1. Setup and select workflow (one-time)
/sdlc-workflow:performance-setup
# User selects workflow: "Product Catalog Browse"

# 2. Capture baseline
npm start  # Start app first
/sdlc-workflow:performance-baseline
# Output: LCP 3200ms (target 2500ms) ⚠️

# 3. Analyze source code
/sdlc-workflow:performance-analyze-module
# Output: 3 anti-patterns detected, 900ms improvement estimated

# 4. Create Jira tasks
/sdlc-workflow:performance-plan-optimization
# Output: Epic TC-5001, Tasks TC-5002, TC-5003, TC-5004

# 5. Implement optimization
/sdlc-workflow:performance-implement-optimization TC-5002
# Output: PR created, LCP improved 3200ms → 2900ms

# 6. Verify PR
/sdlc-workflow:performance-verify-optimization TC-5002
# Output: PASS (Partial Success - continue with remaining tasks)

# 7. Repeat steps 5-6 for TC-5003, TC-5004 until targets met
```

---

## Anti-Patterns Detected (Step 4)

| Anti-Pattern | Detection |
|---|---|
| Over-fetching | API responses with unused fields |
| N+1 queries | Sequential API calls in loops |
| Waterfall loading | Sequential resource dependencies |
| Render-blocking | Synchronous scripts/styles in `<head>` |
| Unused code | Dead code, unreachable branches |
| Expensive re-renders | Missing React.memo, useMemo |
| Long tasks | Main thread blocking > 50ms |
| Layout thrashing | Forced reflows in loops |
| Missing lazy loading | Large components loaded eagerly |

---

## Common Issues

| Issue | Solution |
|---|---|
| "ECONNREFUSED" during baseline | Start application: `npm start` |
| "Cannot find module @playwright/test" | Install: `npm install -D @playwright/test && npx playwright install` |
| Metrics vary >10% between runs | Close background apps, clear cache, use consistent test data |
| "Performance regression detected" | Review implementation, check for unintended side effects |
| "Atlassian MCP failed" | Choose "Use REST API" when prompted, or skip Jira operations |

---

## Best Practices

**Re-baseline when:**
- Before starting optimization (establish baseline)
- After major features (validate no regressions)
- After library upgrades (detect version-related slowdowns)
- Before releases (ensure targets met)

**Prioritization:**
- Quick wins first (low effort, high impact)
- Dependencies (tasks that unblock others)
- Low-risk before high-risk

**Target setting:**
- Use industry benchmarks (see [Performance Metrics Guide](performance-metrics-guide.md))
- Set intermediate targets if baseline is far from benchmark
- Adjust for application complexity and user expectations

**Iteration pattern:**
- **Incremental:** One task → verify → merge → repeat (lower risk)
- **Batched:** Multiple tasks → verify → merge (fewer PRs)

**Regression threshold:** 5% degradation in non-target scenarios triggers investigation

---

## See Also

- [Performance Skills Reference](performance-skills-reference.md) - Detailed skill documentation
- [Performance Metrics Guide](performance-metrics-guide.md) - Metric definitions and thresholds
- [Workflow Documentation](workflow.md) - Full workflow catalog
