# Performance Skills Reference

Quick reference for all performance optimization skills.

---

## Overview

| # | Skill | Purpose | Key Action |
|---|---|---|---|
| 1 | performance-setup | Initialize infrastructure (dirs, settings, backend) | Creates minimal `.claude/performance-config.md` (no workflow) |
| 2 | performance-baseline | **Discover workflows**, select workflow, capture metrics | Workflow selection + Playwright automation → `baseline-report.md` + config update |
| 3 | performance-analyze-module | Detect anti-patterns | **Inspects source code** → `workflow-analysis-report.md` |
| 4 | performance-plan-optimization | Create Jira tasks | **Reads analysis report** → Jira Epic/Tasks |
| 5 | performance-implement-optimization | Execute optimization | Implements + validates → PR |
| 6 | performance-verify-optimization | Verify PR | Review feedback + validation → report |

---

## performance-setup

**Invocation:** `/sdlc-workflow:performance-setup [path]`

**One-time infrastructure setup. Does NOT select workflow (that happens in baseline).**

| Input | Output |
|---|---|
| Target repository path (optional) | Minimal `.claude/performance-config.md` (no workflow selected) |
| User responses (backend config, baseline settings, targets) | Target directories created |

**What it does:**
1. Determines target frontend repository
2. **Discovers and configures backend repository** (upfront)
3. Detects existing configuration (offers update or skip)
4. Creates directories: `baselines/`, `analysis/`, `plans/`, `verification/`
5. Collects baseline capture settings (iterations, warmup runs)
6. Collects optimization targets
7. Generates minimal config with:
   - Backend configured
   - Settings configured
   - Empty Performance Scenarios (populated by baseline)
   - Empty Module Registry (populated by baseline)
   - Empty Selected Workflow (populated by baseline)
   - `workflow_selected: false`

**Default targets:** LCP 2500ms, FCP 1800ms, TTI 3500ms, Total Load 4000ms

**Next step:** Run `/sdlc-workflow:performance-baseline` to discover workflows and capture metrics

---

## performance-baseline

**Invocation:** `/sdlc-workflow:performance-baseline [path]`

**Discover workflows, select target workflow, and capture performance metrics.**

| Input | Output |
|---|---|
| Target repository path (optional) | `baseline-report.md` + config updated with selected workflow |
| User responses: workflow selection, mode selection, test data confirmation | Metrics: LCP, FCP, TTI, Total Load Time |

**Prerequisites:**
- Application running locally
- Playwright installed: `npm install -D @playwright/test && npx playwright install`

**What it does:**

**IF workflow not yet selected (first run):**
1. **Discovers routes from router configuration**
2. **Infers workflows by grouping related routes**
3. **Prompts user to select ONE workflow**
4. **Auto-populates scenarios from workflow's key screens**
5. **Discovers modules (lazy-loaded components)**
6. **Updates config** with selected workflow, scenarios, modules
7. Sets `workflow_selected: true`

**Always (whether workflow just selected or already selected):**
8. Verifies test data availability
9. Checks for existing baseline (prompts to replace or cancel)
10. Executes baseline capture using **cold-start mode** (Playwright automation with direct URL navigation, cold cache)
11. Generates baseline report with p95 metrics
12. Updates config with baseline metadata

**Key metrics captured:**
- LCP (Largest Contentful Paint)
- FCP (First Contentful Paint)
- TTI (Time to Interactive)
- Total Load Time
- Resource breakdown (scripts, CSS, images, API calls)

---

## performance-analyze-module

**Invocation:** `/sdlc-workflow:performance-analyze-module [path]`

**Inspect source code to detect performance anti-patterns.**

| Input | Output |
|---|---|
| Target repository path (optional) | `workflow-analysis-report.md` |
| Baseline data | Anti-pattern findings with severity, impact, locations |

**Key distinction:** This skill **inspects source code**. The next skill (plan-optimization) **reads this report**.

**What it does:**
1. Reads baseline data
2. **Analyzes source code** (components, API calls, resources)
3. Detects 9 anti-patterns (see table below)
4. Classifies severity (High/Medium/Low)
5. Estimates impact (time or KB savings)
6. Locates code instances (file paths, line numbers)
7. Generates recommendations

**Anti-patterns detected:**

| Anti-Pattern | What It Detects |
|---|---|
| Over-fetching | API responses with unused fields |
| N+1 queries | Sequential API calls in loops |
| Waterfall loading | Sequential resource dependencies |
| Render-blocking resources | Synchronous scripts/styles in critical path |
| Unused code | Dead code, unreachable branches |
| Expensive re-renders | Missing React.memo, useMemo, useCallback |
| Long tasks | Main thread blocking > 50ms |
| Layout thrashing | Forced reflows in loops |
| Missing lazy loading | Large components loaded eagerly |

---

## performance-plan-optimization

**Invocation:** `/sdlc-workflow:performance-plan-optimization [path]`

**Read analysis report and create Jira Epic + Tasks.**

| Input | Output |
|---|---|
| Target repository path (optional) | Jira Epic + Tasks |
| Analysis report | `optimization-plan.md` |

**Key distinction:** This skill **reads the analysis report**. It does NOT inspect source code.

**What it does:**
1. **Reads** `workflow-analysis-report.md`
2. Groups optimizations by category (bundle size, API, render, resource, long task)
3. Calculates effort estimates
4. Creates Jira Epic: "Performance Optimization: {workflow}"
5. Creates Jira Tasks (one per category)
6. Links tasks with dependencies
7. Generates `optimization-plan.md`

**Task categories:**

| Category | Optimizations Included |
|---|---|
| Bundle Size Reduction | Code splitting, tree shaking, lazy loading, dead code removal |
| API Optimization | Reduce over-fetching, eliminate N+1 queries, parallel fetching |
| Render Optimization | Memoization, virtual scrolling, layout thrashing fixes |
| Resource Optimization | Async/defer scripts, parallel loading, compression |
| Long Task Mitigation | Code splitting, web workers, async patterns |

---

## performance-implement-optimization

**Invocation:** `/sdlc-workflow:performance-implement-optimization TC-XXXX`

**Execute optimization task with performance validation.**

| Input | Output |
|---|---|
| Jira task ID | Code changes committed to branch |
| Task description (from plan-optimization) | PR with before/after metrics |

**Extends:** `implement-task` workflow with performance steps

**What it does:**
1. Reads Jira task (standard + performance sections)
2. Inspects code and implements optimization
3. Runs functional tests
4. **Re-runs baseline** for affected scenarios
5. Compares results: current vs baseline vs targets
6. Stops if any metric regressed
7. Commits with `perf` type + performance impact in body
8. Creates PR with before/after table
9. Updates Jira and transitions to In Review

**Performance validation (Step 4):**
- Re-captures metrics after implementation
- Compares: baseline → current → target
- Stops execution if regression detected
- Continues if improvement (even if target not fully met)

---

## performance-verify-optimization

**Invocation:** `/sdlc-workflow:performance-verify-optimization TC-XXXX`

**Verify PR with optional baseline re-run.**

| Input | Output |
|---|---|
| Jira task ID | Verification report (PASS/WARN/FAIL) |
| PR reviews/comments | Sub-tasks for review feedback |

**Extends:** `verify-pr` workflow with performance validation

**What it does:**
1. Reads Jira task and PR
2. Checks out PR branch
3. Reads PR review feedback → creates sub-tasks for change requests
4. **Prompts:** "Re-run baseline? (yes/no)"
   - If yes: re-runs baseline, flags >10% drift
   - If no: uses implementation results from PR
5. Validates target achievement (Full/Partial Success, Regression)
6. Runs standard PR checks (scope, CI, acceptance criteria)
7. Generates verification report
8. Posts to PR and Jira

**Target achievement classification:**

| Result | Criteria |
|---|---|
| Full Success | All target metrics met |
| Partial Success | Improvement > 20% but targets not fully met |
| Insufficient Improvement | Improvement < 20% |
| Regression | Any metric worse than baseline |

**Overall result:**
- **PASS:** All checks pass or N/A
- **WARN:** At least one WARN, no FAIL
- **FAIL:** At least one FAIL

---

## Skill Dependencies

```
setup (infrastructure) → baseline (workflow discovery) → analyze-module → plan-optimization → implement-optimization → verify-optimization
         ↓                           ↓                          ↓                  ↓                       ↓                        ↓
  minimal config          config updated with workflow     analysis        Jira Epic/Tasks            PR with           Verification
  (no workflow)           + baseline report                 report                                    metrics            report
```

---

## See Also

- [Performance Workflow Guide](performance-workflow-guide.md) - End-to-end workflow
- [Performance Metrics Guide](performance-metrics-guide.md) - Metric definitions
- [Workflow Documentation](workflow.md) - Full skill catalog
