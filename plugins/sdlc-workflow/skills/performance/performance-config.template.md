# Performance Analysis Configuration

---
metadata:
  version: 1.0
  created: {{timestamp}}
  last_updated: {{timestamp}}
  config_schema_version: 2
  workflow_selected: true
  baseline_captured: false
  baseline_mode: null
  baseline_timestamp: null
  baseline_commit_sha: null
  backend_available: false
  e2e_test_path: null
  e2e_coverage: false
---

This configuration defines performance scenarios, baseline capture settings, and optimization targets for the sdlc-workflow performance optimization workflow.

## Performance Scenarios

List the key user workflows and pages to measure. Each scenario should represent a distinct user journey.

**Note:** Scenarios are auto-populated from the selected workflow's key screens.

| Scenario Name | URL Path | Description |
|---|---|---|
| {{scenario-1-name}} | {{/path}} | {{Brief description of user journey}} |
| {{scenario-2-name}} | {{/path}} | {{Brief description of user journey}} |

**Example scenarios to consider:**
- Home/landing page load (cold cache)
- List views with pagination/filtering
- Detail/item views with related data
- Search/query interfaces
- Form-heavy workflows
- Dashboard/summary pages

## Baseline Capture Settings

| Setting | Value | Description |
|---|---|---|
| Iterations | 5 | Number of times to run each scenario |
| Warmup Runs | 2 | Iterations to discard before collecting metrics |
| Metrics to Collect | LCP, FCP, TTI, Total Load Time, Resource Timing | Core Web Vitals and resource-level metrics |
| Browser | Chromium (headless) | Playwright browser for automation |

## Baseline Capture Mode

Determines how performance metrics are captured.

**Status:** Not yet configured (will be set during first baseline capture)

| Mode | Description | Use Case |
|---|---|---|
| **cold-start** | Direct URL navigation with cold cache | Worst-case performance (first visit, direct links, bookmarks) |
| **e2e** | Use e2e test automation scripts | Realistic user workflow with warm cache (click navigation) |
| **both** | Run e2e first, then cold-start | Comprehensive measurement (both realistic and worst-case) |

**Configured Mode:** Not yet selected (will be set during `/sdlc-workflow:performance-baseline` execution and stored in config metadata)

**E2E Configuration** (if mode = e2e or both):
- Repository Path: (Path to e2e test repository)
- Command: (Command to run e2e tests, e.g., `npm run e2e`)
- Environment Variables: (Optional env vars)

**Important:** Once baseline is captured with a mode, all subsequent baseline captures (during implement, verify) MUST use the same mode for valid comparisons. The selected mode is stored in config metadata and enforced by downstream skills.

## Target Directories

| Directory | Purpose |
|---|---|
| `.claude/performance/baselines/` | Baseline performance reports |
| `.claude/performance/analysis/` | Module and application analysis reports |
| `.claude/performance/plans/` | Optimization plan documents |
| `.claude/performance/verification/` | Verification reports for optimization PRs |

## Optimization Targets

Core Web Vitals thresholds to achieve after optimization.

**Status:** Baseline values not yet captured

| Metric | Baseline (p95) | Current (p95) | Target | Unit | Last Updated |
|---|---|---|---|---|---|
| LCP (Largest Contentful Paint) | TBD | TBD | 2.5 | seconds | - |
| FCP (First Contentful Paint) | TBD | 1.8 | seconds | - |
| TTI (Time to Interactive) | TBD | TBD | 3.5 | seconds | - |
| Total Load Time | TBD | TBD | 4.0 | seconds | - |

**Columns explained:**
- **Baseline (p95):** Initial value from first baseline capture (never changes)
- **Current (p95):** Latest measured value (updated after each optimization)
- **Target:** Goal to achieve (can be adjusted based on requirements)
- **Last Updated:** Timestamp of last metric update

**Note:** Baseline values will be auto-filled after first `/sdlc-workflow:performance-baseline` run. Current values will be updated by `/sdlc-workflow:performance-implement-optimization` after each optimization. Target values follow Google's Core Web Vitals "Good" thresholds.

## Module Registry

Frontend modules/pages to analyze individually. Each entry represents a distinct bundle or route that can be optimized separately.

**Discovery guidance:** Identify lazy-loaded routes, code-split chunks, or major feature modules from build configuration (Webpack/Vite) or dynamic imports in route definitions.

| Module Name | Entry Point | Description |
|---|---|---|
| {{module-1}} | {{src/path/to/entry.tsx}} | {{Module purpose}} |
| {{module-2}} | {{src/path/to/entry.tsx}} | {{Module purpose}} |

**Example modules to consider:**
- Route-level code splits (each lazy-loaded page)
- Feature modules with distinct bundles
- Heavy UI libraries (e.g., chart/visualization components)
- Third-party integrations with separate chunks

## Backend Repository Configuration

**Status:** Not configured

If your application has a separate backend repository, configure it here to enable backend source code analysis and over-fetching detection.

| Setting | Value | Description |
|---|---|---|
| Backend Repository | {{backend-repo-name}} | Name from Repository Registry |
| Backend Path | {{/absolute/path/to/backend}} | Absolute path to backend repository |
| Backend Framework | {{framework}} | e.g., actix-web, axum, spring-boot, express, fastapi |
| Serena Instance | {{serena-instance}} | Instance name from Code Intelligence section (or "none") |
| API Base Path | {{/api/v2}} | Base path for API routes |
| Backend Available | false | Cached validation status (auto-updated) |
| Last Validated | - | Timestamp of last validation check |

**Analysis Mode:**
- `backend_available = false` → Frontend-only analysis (API field usage analysis limited)
- `backend_available = true` → Full-stack analysis (cross-reference backend schemas with frontend usage)

**Note:** Backend configuration can be updated by re-running `/sdlc-workflow:performance-setup --refresh-backend` or edited manually. If no backend repository is configured, analysis will focus on frontend-only optimizations.

## Selected Workflow

The following workflow has been selected for performance optimization:

| Property | Value |
|---|---|
| Workflow Name | {{workflow-name}} |
| Entry Point | {{entry-point-url}} |
| Key Screens | {{key-screens-comma-separated}} |
| Complexity | {{complexity-estimate}} |
| Selected On | {{current-date}} |

**Next Steps:**
1. Ensure your application is running locally with test data loaded for this workflow
2. Run `/sdlc-workflow:performance-baseline` to capture baseline metrics
3. Run `/sdlc-workflow:performance-analyze-module` to analyze performance bottlenecks
