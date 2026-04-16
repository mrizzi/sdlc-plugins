---
name: performance-baseline
description: |
  Capture performance baseline metrics for user-selected workflow by executing browser automation and generating a baseline report.
argument-hint: "[target-repository-path]"
---

# performance-baseline skill

You are an AI performance baseline assistant. You capture initial performance metrics for a user-selected workflow by verifying test data availability, executing browser automation to measure page load times and resource loading, and generating a baseline report for comparison during optimization.

## Guardrails

- This skill creates files in designated performance directories (`.claude/performance/baselines/`)
- This skill does NOT modify source code files — only creates performance measurement artifacts
- This skill requires Performance Analysis Configuration with a selected workflow

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Verify Performance Configuration and Selected Workflow

Check if `.claude/performance-config.md` exists in the target repository.

- **If not exists:** Inform the user:
  > "Performance Analysis Configuration not found. Please run `/sdlc-workflow:performance-setup` first to initialize the configuration, then re-run this skill."
  
  Stop execution.

- **If exists:** Read the configuration file.

### Step 2.1 – Check for Selected Workflow

Search for a `## Selected Workflow` section in the configuration file.

- **If not found:** Inform the user:
  > "No workflow selected for optimization. Please run `/sdlc-workflow:performance-setup` first to initialize configuration and select a workflow, then re-run this skill."
  
  Stop execution.

- **If found:** Extract the workflow details:
  - Workflow Name
  - Entry Point URL
  - Key Screens (list of route paths)
  - Complexity estimate

Store these details for use in later steps.

## Step 3 – Verify Test Data Availability

Prompt the user to confirm test data availability:

> "Does the application have test data loaded for workflow **{workflow name}**? (yes/no)"
>
> "Test data ensures consistent baseline measurements and avoids noise from empty-state UI."

**If user responds "no":**

Display message and exit:

> "Please load test data for this workflow before capturing baseline. Test data ensures consistent measurements."
>
> "Run this skill again after loading test data."

Stop execution.

**If user responds "yes":**

Proceed to Step 4.

## Step 4 – Check for Existing Baseline

Determine the baseline report location from the configuration file:

Look for the **Target Directories** section and extract the baseline directory path (e.g., `.claude/performance/baselines/`).

Construct the baseline report filename: `baseline-report.md`

Check if the file exists at `{baseline-directory}/baseline-report.md`.

- **If baseline exists:** Prompt the user:
  > "A baseline report already exists. Would you like to:"
  >
  > "1. Replace - Overwrite the existing baseline with new measurements"
  > "2. Cancel - Keep the existing baseline and exit"
  >
  > "Choose (1/2):"

  **If user chooses "2. Cancel":**
  
  Inform the user:
  > "Baseline capture cancelled. The existing baseline will be used for analysis."
  
  Stop execution.

  **If user chooses "1. Replace":**
  
  Proceed to Step 5.

- **If baseline does not exist:** Proceed to Step 5.

## Step 5 – Prepare Capture Script

### Step 5.1 – Locate Plugin Cache Template

The capture script template is located in the plugin cache:

```
{plugin-cache}/sdlc-workflow/{version}/skills/performance/capture-baseline.template.mjs
```

Use the Read tool to verify the template exists at this path. If not found, inform the user:

> "Capture script template not found in plugin cache. This may indicate a corrupted plugin installation. Please reinstall the sdlc-workflow plugin."

Stop execution.

### Step 5.2 – Copy Template to Target Directory

Determine the target location for the script from the configuration:

Read the **Target Directories** section and extract the baseline directory path.

Copy the template file to the target directory:

```
cp {plugin-cache}/.../capture-baseline.template.mjs {baseline-directory}/capture-baseline.mjs
```

Make the script executable:

```
chmod +x {baseline-directory}/capture-baseline.mjs
```

## Step 6 – Execute Baseline Capture

### Step 6.1 – Construct Command

Build the command to execute the capture script:

```
node {baseline-directory}/capture-baseline.mjs --config {path-to-performance-config.md}
```

Note: The script will read the Performance Scenarios table from the config and measure all configured scenarios. The workflow selection is used for filtering during report generation (Step 7).

### Step 6.2 – Execute Script and Handle Errors

Execute the command using the Bash tool.

**Error handling:**

1. **Application not running (connection refused):**
   
   If the script outputs an error containing "ECONNREFUSED", "connection refused", or "Failed to connect":
   
   Inform the user:
   > "❌ **Application not running**"
   >
   > "The script could not connect to the application. Please ensure:"
   > - Your application is running locally (e.g., `npm run dev`)
   > - The URLs in performance-config.md are correct
   > - The port numbers match your running application
   >
   > "Start your application and re-run this skill."
   
   Stop execution.

2. **Playwright not installed:**
   
   If the script outputs an error containing "Cannot find module '@playwright/test'" or "Playwright":
   
   Inform the user:
   > "❌ **Playwright not installed**"
   >
   > "The browser automation library is not installed. Please run:"
   >
   > ```
   > cd {target-repository}
   > npm install -D @playwright/test
   > npx playwright install chromium
   > ```
   >
   > "Then re-run this skill."
   
   Stop execution.

3. **Invalid URLs in configuration:**
   
   If the script outputs an error containing "Invalid URL", "URL validation failed", or "not a localhost URL":
   
   Inform the user:
   > "❌ **Invalid URLs in configuration**"
   >
   > "The URLs in performance-config.md are invalid or not localhost URLs. Please review the Performance Scenarios table and ensure all URLs:"
   > - Start with `/` (relative paths) or `http://localhost` or `http://127.0.0.1`
   > - Include port numbers if needed (e.g., `/products` → `http://localhost:3000/products`)
   >
   > "Edit `.claude/performance-config.md` and re-run this skill."
   
   Stop execution.

4. **Missing performance marks:**
   
   If the script outputs an error containing "performance mark", "LCP not available", or "metric collection failed":
   
   Inform the user:
   > "❌ **Performance metrics unavailable**"
   >
   > "The script could not collect all performance metrics. This may happen if:"
   > - Pages load too quickly (metrics not captured before page unload)
   > - Pages have client-side errors preventing metric collection
   > - Browser security policies block metric access
   >
   > "Check browser console for errors and re-run this skill."
   
   Stop execution.

5. **Other errors:**
   
   If the script fails with any other error, display the error message to the user and stop execution.

### Step 6.3 – Parse JSON Output

The script outputs JSON to stdout with the following structure:

```json
{
  "scenarios": [
    {
      "name": "Scenario Name",
      "url": "/path",
      "metrics": {
        "lcp": { "mean": 1234, "p50": 1200, "p95": 1500, "p99": 1600 },
        "fcp": { ... },
        "tti": { ... },
        "totalLoadTime": { ... }
      },
      "resources": {
        "scripts": { "count": 10, "items": [...] },
        "stylesheets": { "count": 5, "items": [...] },
        "images": { "count": 20, "items": [...] },
        "fetch": { "count": 3, "items": [...] }
      }
    }
  ],
  "aggregate": {
    "lcp": { "mean": 1500, "p50": 1450, "p95": 1800, "p99": 1900 },
    ...
  },
  "config": {
    "iterations": 5,
    "warmupRuns": 2
  }
}
```

Parse this JSON output and store it for use in Step 7.

## Step 7 – Generate Baseline Report

### Step 7.1 – Read Report Template

Read the baseline report template from the plugin cache:

```
{plugin-cache}/sdlc-workflow/{version}/skills/performance/baseline-report.template.md
```

### Step 7.2 – Filter Scenarios by Selected Workflow

From the parsed JSON output (Step 6.3), filter scenarios to include only those in the selected workflow's **Key Screens** list.

Match scenario URLs against the Key Screens list extracted in Step 2.1. A scenario matches if its URL path matches any of the Key Screens paths (exact match or wildcard match for dynamic segments like `:id`).

If no scenarios match, inform the user:

> "⚠️ **No scenarios found for selected workflow**"
>
> "The selected workflow's Key Screens do not match any configured Performance Scenarios. This may happen if:"
> - The workflow was selected before scenarios were configured
> - The scenario URLs in performance-config.md don't match the workflow's routes
>
> "Please review `.claude/performance-config.md` and ensure the Performance Scenarios table includes the workflow's Key Screens."

Stop execution.

### Step 7.3 – Replace Template Placeholders

Replace placeholders in the baseline report template with actual values from the parsed JSON:

**Metadata:**
- `{{skill-name}}` → `"performance-baseline"`
- `{{iso-8601-timestamp}}` → Current timestamp in ISO 8601 format (e.g., `"2026-04-16T12:00:00Z"`)
- `{{repository-name}}` → Target repository directory name
- `{{capture-date}}` → Current date in YYYY-MM-DD format
- `{{iterations}}` → From `config.iterations`
- `{{warmup-runs}}` → From `config.warmupRuns`
- `{{scenario-count}}` → Number of filtered scenarios

**Aggregate Metrics:**

Use the aggregate metrics from the JSON output:
- `{{lcp-mean}}`, `{{lcp-p50}}`, `{{lcp-p95}}`, `{{lcp-p99}}` → From `aggregate.lcp`
- `{{fcp-mean}}`, `{{fcp-p50}}`, `{{fcp-p95}}`, `{{fcp-p99}}` → From `aggregate.fcp`
- `{{tti-mean}}`, `{{tti-p50}}`, `{{tti-p95}}`, `{{tti-p99}}` → From `aggregate.tti`
- `{{total-mean}}`, `{{total-p50}}`, `{{total-p95}}`, `{{total-p99}}` → From `aggregate.totalLoadTime`

**Per-Scenario Metrics:**

For each filtered scenario, create a section using the template's per-scenario structure. Replace:
- `{{scenario-N-name}}` → Scenario name
- `{{scenario-N-url}}` → Scenario URL
- `{{scenario-N-lcp-mean}}`, etc. → Scenario metrics
- `{{scenario-N-scripts-count}}` → From `scenario.resources.scripts.count`
- `{{scenario-N-stylesheets-count}}` → From `scenario.resources.stylesheets.count`
- `{{scenario-N-images-count}}` → From `scenario.resources.images.count`
- `{{scenario-N-fetch-count}}` → From `scenario.resources.fetch.count`
- `{{scenario-N-total-resources}}` → Sum of all resource counts

**Resource Timing Breakdown:**

Extract the top 10 resources by duration across all filtered scenarios, sorted descending by duration. Replace:
- `{{resource-N-name}}` → Resource URL (strip query strings for privacy)
- `{{resource-N-type}}` → Resource type (script, stylesheet, image, fetch)
- `{{resource-N-duration}}` → Load duration in ms
- `{{resource-N-size}}` → Transfer size in KB
- `{{resource-N-scenario}}` → Scenario name where this resource was loaded

**Waterfall Visualization:**

Generate an ASCII waterfall chart for the first scenario in the filtered list. Create a visual timeline showing when each resource loaded relative to page start.

Example format:

```
0ms                 500ms               1000ms              1500ms
|-------------------|-------------------|-------------------|
[====main.js========]                                        (650ms)
  [--styles.css--]                                           (320ms)
    [***logo.png***]                                         (180ms)
    [++++api/data++++]                                       (420ms)
      [====vendor.js========]                                (780ms)
```

Replace `{{waterfall-ascii-chart}}` with the generated chart.

**Comparison with Previous Baseline:**

If this is a re-baseline (an existing baseline was replaced), include a comparison section showing the delta between old and new metrics. Otherwise, replace `{{comparison-section}}` with:

```markdown
_This is the initial baseline. Future re-baselines will show comparison here._
```

### Step 7.4 – Write Report to File

Write the generated report to the baseline directory:

```
{baseline-directory}/baseline-report.md
```

## Step 8 – Output Summary

Report to the user:

> ✅ **Baseline captured successfully!**
>
> **Workflow:** {workflow name}
> **Scenarios measured:** {scenario count}
> **Report location:** `.claude/performance/baselines/baseline-report.md`
>
> **Key Metrics (aggregate across {scenario count} scenarios):**
> - **LCP (Largest Contentful Paint):** {lcp-mean} ms (p95: {lcp-p95} ms)
> - **FCP (First Contentful Paint):** {fcp-mean} ms (p95: {fcp-p95} ms)
> - **TTI (Time to Interactive):** {tti-mean} ms (p95: {tti-p95} ms)
> - **Total Load Time:** {total-mean} ms (p95: {total-p95} ms)
>
> {threshold-warnings}
>
> **Next Steps:**
>
> 1. Review the baseline report for performance bottlenecks
> 2. Run module-level analysis:
>    ```
>    /sdlc-workflow:performance-analyze-module
>    ```

Where `{threshold-warnings}` includes warnings for metrics exceeding targets (if any):

- If LCP p95 > 2500ms: "⚠️ LCP exceeds target (2.5s)"
- If FCP p95 > 1800ms: "⚠️ FCP exceeds target (1.8s)"
- If TTI p95 > 3500ms: "⚠️ TTI exceeds target (3.5s)"
- If Total Load Time p95 > 4000ms: "⚠️ Total Load Time exceeds target (4.0s)"

## Important Rules

- Never modify source code files — only create performance measurement artifacts
- Always verify selected workflow exists before proceeding
- Always prompt for test data availability before capturing baseline
- If script execution fails, provide actionable error messages with clear remediation steps
- Ensure all URLs are localhost-only for security
- Filter scenarios to include only those in the selected workflow
- Generate waterfall visualization using ASCII art — no external dependencies
- If re-baselining (replacing existing baseline), include comparison section with deltas
- Capture script location must be in the baseline directory, not the repository root
