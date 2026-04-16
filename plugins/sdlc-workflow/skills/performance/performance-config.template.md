---
metadata:
  version: 1.0
  created: {{timestamp}}
  last_updated: {{timestamp}}
  config_schema_version: 2
  workflow_selected: false
  baseline_captured: false
  baseline_mode: null
  baseline_timestamp: null
  baseline_commit_sha: null
  backend_available: false
  analysis_scope: "frontend-only"
  backend_endpoint_discovery_method: null
  dev_command_approved: false
  dev_command_hash: null
---

# Performance Analysis Configuration

This configuration defines performance scenarios, baseline capture settings, and optimization targets for the sdlc-workflow performance optimization workflow.

## Performance Scenarios

List the key user workflows and pages to measure. Each scenario should represent a distinct user journey.

**Note:** Scenarios will be auto-populated by `performance-baseline` after workflow selection.

| Scenario Name | URL Path | Description |
|---|---|---|
| (Will be populated after workflow selection) | - | - |

## Baseline Capture Settings

| Setting | Value | Description |
|---|---|---|
| Iterations | 20 | Number of times to run each scenario |
| Warmup Runs | 2 | Iterations to discard before collecting metrics |
| Metrics to Collect | LCP, FCP, DOM Interactive, Total Load Time, Resource Timing | Core Web Vitals and resource-level metrics |
| Browser | Chromium (headless) | Playwright browser for automation |

## Baseline Capture Mode

Determines how performance metrics are captured.

**Status:** Not yet configured (will be set during first baseline capture)

| Mode | Description | Use Case |
|---|---|---|
| **cold-start** | Direct URL navigation with cold cache | Worst-case performance (first visit, direct links, bookmarks) |

**Configured Mode:** cold-start (only supported mode)

**Important:** All baseline captures use cold-start mode for consistent cold-cache measurements.

## Target Directories

| Directory | Purpose |
|---|---|
| `.claude/performance/baselines/` | Baseline performance reports |
| `.claude/performance/analysis/` | Module and application analysis reports |
| `.claude/performance/plans/` | Optimization plan documents |
| `.claude/performance/optimization-results/` | Per-task optimization results (audit trail) |
| `.claude/performance/verification/` | Verification reports for optimization PRs |

## Optimization Targets

Core Web Vitals thresholds to achieve after optimization.

**Status:** Baseline values not yet captured

| Metric | Baseline (p95) | Latest Verified (p95) | Target | Unit | Last Updated |
|---|---|---|---|---|---|
| LCP (Largest Contentful Paint) | TBD | TBD | 2.5 | seconds | - |
| FCP (First Contentful Paint) | TBD | TBD | 1.8 | seconds | - |
| DOM Interactive | TBD | TBD | 3.5 | seconds | - |
| Total Load Time | TBD | TBD | 4.0 | seconds | - |

**Columns explained:**
- **Baseline (p95):** Initial value from first baseline capture (never changes)
- **Latest Verified (p95):** Most recent measured value on main branch (updated by re-running `/performance-baseline` after merging optimizations)
- **Target:** Goal to achieve (can be adjusted based on requirements)
- **Last Updated:** Timestamp of last metric update

**Note:** Baseline values will be auto-filled after first `/sdlc-workflow:performance-baseline` run. Latest Verified values track the current state on main branch - re-run baseline after merging each optimization PR to measure cumulative progress. Target values follow Google's Core Web Vitals "Good" thresholds.

## Module Registry

Frontend modules/pages to analyze individually. Each entry represents a distinct bundle or route that can be optimized separately.

**Note:** Modules will be auto-populated by `performance-baseline` after workflow selection.

| Module Name | Entry Point | Description |
|---|---|---|
| (Will be populated after workflow selection) | - | - |

## Repository Configuration

This section tracks the repositories involved in performance analysis based on the configured analysis scope.

### Frontend Repository

| Setting | Value | Description |
|---|---|---|
| Repository Name | {{frontend-repo-name}} | Frontend repository name |
| Repository Path | {{/absolute/path/to/frontend}} | Absolute path to frontend repository |
| Framework | {{frontend-framework}} | e.g., React, Vue, Angular, Svelte |
| Bundler | {{bundler}} | e.g., Rsbuild, Vite, Webpack, Rollup |

### Backend Repository

| Setting | Value | Description |
|---|---|---|
| Repository Name | {{backend-repo-name}} | Backend repository name |
| Repository Path | {{/absolute/path/to/backend}} | Absolute path to backend repository |
| Framework | {{backend-framework}} | e.g., actix-web, axum, spring-boot, express, fastapi |
| Serena Instance | {{serena-instance}} | Instance name from Code Intelligence section (or "none") |
| API Base Path | {{/api/v2}} | Base path for API routes (e.g., /api/v1, /api/v2) |
| Backend Available | false | Cached validation status (auto-updated) |
| Last Validated | - | Timestamp of last validation check |

**Analysis Capabilities by Scope:**
- **full-stack:** Both frontend and backend repositories configured → Full cross-layer analysis (bundle, browser metrics, API handlers, database queries, over-fetching detection)
- **frontend-only:** Frontend repository only → Frontend analysis (bundle, browser metrics, component rendering, API usage patterns)
- **backend-only:** Backend repository only → Backend analysis (API endpoints, database queries, caching, pagination, response schemas)

**Note:** Repository configuration can be updated by re-running `/sdlc-workflow:performance-setup --refresh-backend` or edited manually.

## Analysis Scope

**Current Mode:** {{analysis-scope}}

The analysis scope determines which repositories are analyzed and what performance metrics are collected:

- **full-stack-monorepo:** Frontend and backend in same repository → Full cross-layer analysis (bundle, browser metrics, API handlers, database queries, over-fetching detection)
- **full-stack:** Frontend and backend in separate repositories → Full cross-layer analysis (bundle, browser metrics, API handlers, database queries, over-fetching detection)
- **frontend-only:** Frontend repository only → Frontend analysis (bundle, browser metrics, component rendering, API usage patterns)
- **backend-only:** Backend repository only → Backend analysis (API endpoints, database queries, caching, pagination, response schemas)

This is configured during setup and determines which sections of the Repository Configuration are populated.

**To change analysis scope:** Re-run `/sdlc-workflow:performance-setup` and select a different option.

## Development Environment

Commands and configuration for starting the application during performance testing.

| Setting | Value | Description |
|---|---|---|
| Dev Command | TBD | Command to start application (e.g., `npm run dev`) |
| Documentation Source | TBD | Where command was discovered (package.json, README.md, etc.) |
| Port | TBD | Port where dev server runs |
| Command Approved | false | User has approved this command for execution |
| Command Hash | - | SHA-256 hash for change detection |
| Last Validated | - | Timestamp of last successful execution |

**Note:** The dev command will be auto-discovered during the first baseline capture run. You can modify it before approval if needed (e.g., add environment variables like `AUTH_DISABLED=true npm run dev`).

## Analysis Assumptions

Constants used by `performance-analyze-module` when estimating impact of detected anti-patterns.
Adjust these to match your environment for more accurate estimates.

| Assumption | Value | Unit | Description |
|---|---|---|---|
| Average Bandwidth | 5 | Mbps | Network bandwidth for bundle size impact calculation |
| API Latency (average) | 100 | ms | Baseline API round-trip time for N+1 impact calculation |
| Layout Reflow Cost | 5 | ms | CPU time per forced reflow operation |
| Cache Hit Rate | 0.8 | ratio (0.0–1.0) | Proportion of API requests expected to be served from cache |

**Note:** Impact estimates derived from these constants are order-of-magnitude approximations.
Always verify with browser profiling tools before committing to an optimization.

## Selected Workflow

No workflow selected yet. Run `/sdlc-workflow:performance-baseline` to discover and select a workflow.

The baseline skill will:
1. Discover workflows from your application's routes
2. Prompt you to select a target workflow
3. Auto-populate Performance Scenarios and Module Registry sections
4. Capture initial performance metrics

**Next Steps:**
1. Ensure your application is running locally
2. Run `/sdlc-workflow:performance-baseline` to discover workflows and capture baseline
