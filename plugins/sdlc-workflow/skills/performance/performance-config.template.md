# Performance Analysis Configuration

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

## Target Directories

| Directory | Purpose |
|---|---|
| `.claude/performance/baselines/` | Baseline performance reports |
| `.claude/performance/analysis/` | Module and application analysis reports |
| `.claude/performance/plans/` | Optimization plan documents |
| `.claude/performance/verification/` | Verification reports for optimization PRs |

## Optimization Targets

Core Web Vitals thresholds to achieve after optimization.

| Metric | Current (Baseline) | Target | Unit |
|---|---|---|---|
| LCP (Largest Contentful Paint) | TBD | 2.5 | seconds |
| FCP (First Contentful Paint) | TBD | 1.8 | seconds |
| TTI (Time to Interactive) | TBD | 3.5 | seconds |
| Total Load Time | TBD | 4.0 | seconds |

**Note:** Current (Baseline) values will be filled in after running `performance-baseline` skill. Target values follow Google's Core Web Vitals "Good" thresholds but can be adjusted based on application requirements.

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

## Backend Repository Configuration (Optional)

If your application has a separate backend repository, configure it here to enable backend source code analysis and over-fetching detection.

| Setting | Value | Description |
|---|---|---|
| Backend Repository | {{backend-repo-name}} | Name from Repository Registry |
| Backend Path | {{/absolute/path/to/backend}} | Absolute path to backend repository |
| Backend Framework | {{framework}} | e.g., actix-web, axum, spring-boot, express, fastapi |
| Serena Instance | {{serena-instance}} | Instance name from Code Intelligence section (or "none") |
| API Base Path | {{/api/v2}} | Base path for API routes |

**Note:** If no backend repository is configured, analysis will focus on frontend-only optimizations.

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
