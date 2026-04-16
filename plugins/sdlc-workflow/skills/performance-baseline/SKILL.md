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

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Verify config exists, stop if missing
- Read configuration file for workflow and baseline settings

### Step 2.1 – Check for Selected Workflow

**Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-7-workflow-validation)

**Specific actions for this skill:**
- Extract workflow name, entry point, key screens, complexity
- Store for scenario generation and baseline capture

### Step 2.2 – Read Baseline Mode and E2E Coverage from Metadata (Updated)

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction)

**Specific fields to extract:**
- `metadata.baseline_mode` → stored_mode (for mode consistency enforcement)
- `metadata.baseline_captured` → baseline_already_captured (check if re-run)
- `metadata.e2e_test_path` → e2e_test_path (for e2e mode automation)
- `metadata.e2e_coverage` → e2e_coverage (for mode recommendation)

**Store for mode selection in Step 3:**
- `stored_mode`: null | "cold-start" | "e2e" | "both"
- `baseline_already_captured`: true | false
- `e2e_test_path`: path | null
- `e2e_coverage`: true | false

## Step 3 – Select Baseline Capture Mode

### Step 3.0 – Check for Existing Baseline Mode (New)

**Apply:** [Common Pattern: Mode Consistency Enforcement](../performance/common-patterns.md#pattern-3-mode-consistency-enforcement)

**Specific actions for this skill:**
- Read `stored_mode` from Step 2.2 metadata extraction
- If `stored_mode` is not null (baseline previously captured):
  - Inform user of stored mode and consistency requirement
  - Offer: use stored mode | reset baseline | cancel
  - If user chooses stored mode, skip Step 3.1-3.3 (mode selection)
  - If user chooses reset, continue to Step 3.1 (new mode selection)
  - If user chooses cancel, stop execution
- If `stored_mode` is null (first baseline), proceed to Step 3.1

### Step 3.1 – Mode Selection Prompt (Updated with E2E Auto-Recommendation)

Prompt the user to select the baseline capture mode with auto-recommendation based on e2e coverage.

**If `e2e_coverage = true` (from Step 2.2):**

Display mode selection with e2e recommendation:

> "Which baseline capture mode would you like to use?"
>
> ℹ️ **E2E test detected for this workflow:** {e2e_test_path}
>
> **Recommended mode:** e2e or both
> - This workflow has e2e test coverage, enabling realistic user flow measurement
>
> **Options:**
> 1. **e2e** (Recommended) — Use existing e2e test. Measures realistic user workflow with warm cache.
> 2. **cold-start** — Direct URL navigation. Measures worst-case/first-visit performance with cold cache.
> 3. **both** — Run e2e test first, then cold-start baseline. Provides comprehensive measurement.

**If `e2e_coverage = false` (from Step 2.2):**

Display mode selection with cold-start recommendation:

> "Which baseline capture mode would you like to use?"
>
> ℹ️ **No e2e test detected for this workflow**
>
> **Recommended mode:** cold-start
> - This workflow has no e2e test coverage, using direct URL navigation
>
> **Options:**
> 1. **cold-start** (Recommended) — Direct navigation to each URL. Measures worst-case/first-visit performance with cold cache.
> 2. **e2e** — Use end-to-end test automation scripts (you will need to provide e2e test path).
> 3. **both** — Run e2e tests first, then cold-start baseline.

### Step 3.2 – cold-start Mode

If user selects "cold-start":

- Store mode: `cold-start`
- Proceed to Step 4 (Verify Test Data Availability)
- Use the standard capture script (direct navigation)

### Step 3.3 – e2e Mode

If user selects "e2e":

**Check if e2e test path is already configured (from Step 2.2):**

```bash
if e2e_test_path is not null:
  # E2E test was configured during setup
  use_stored_e2e = true
  e2e_test_file = e2e_test_path
else:
  # No e2e test configured, prompt user
  use_stored_e2e = false
```

**If `use_stored_e2e = true`:**

Inform user:

> ℹ️ **Using e2e test from setup:** {e2e_test_path}

Extract e2e command from the test file or infer from package.json:
- Look for `package.json` in e2e repo directory
- Find script that runs the test file (e.g., `"e2e": "playwright test"`)
- Prompt user to confirm or override:
  > "Detected e2e command: `{inferred-command}`"
  > 
  > Use this command? (yes/no)
  > - If no: Prompt for custom command

**If `use_stored_e2e = false`:**

**Prompt for e2e repository:**

> "Please provide the absolute path to your e2e test automation repository:"

Validate that the path exists and contains test files (e.g., `package.json`, `playwright.config.ts`, `cypress.json`, or similar).

**Prompt for e2e command:**

> "What command should I run to execute e2e tests for the selected workflow?"
>
> "Examples:"
> - `npm run e2e`
> - `npx playwright test --project=sbom-workflow`
> - `npm run test:e2e -- --spec=sbom-management`

**Prompt for optional environment variables:**

> "Any environment variables or setup needed? (optional, press Enter to skip)"
>
> "Example: `HEADLESS=false BASE_URL=http://localhost:3000`"

**Inform user about e2e performance measurement approach:**

> "ℹ️ **E2E Performance Measurement**"
>
> "The skill will measure performance during your e2e test execution by:"
> - Capturing browser DevTools Network timing for each page navigation
> - Measuring API call duration from browser performance timeline
> - Tracking page navigation transitions (e.g., list → click → detail)
> - Recording overall workflow completion time
>
> "**E2E Flow Metrics:**"
> - Total workflow time: Target <30s for complete user journey
> - Per-page navigation time: Time from click → page interactive
> - API call duration: Individual API request timing from browser
> - Cache effectiveness: Warm vs cold resource loading
>
> "No special instrumentation required in your e2e tests - metrics are captured from browser APIs during test execution."

**Security Note:**

The e2e command executes with full access to your environment variables. Only run trusted e2e test commands. Do not use `--e2e-command` with:
- Inline secrets (e.g., `API_KEY=secret npm run e2e`)
- Untrusted third-party scripts
- Commands from untrusted configuration files

**Execute e2e tests with performance capture:**

1. Store mode: `e2e`
2. Store e2e config: `{ repo_path, command, env_vars }`
3. Instrument e2e execution:
   - If e2e framework is Playwright: Use built-in `page.on('requestfinished')` and Performance API
   - If e2e framework is Cypress: Inject `cy.task()` to collect `performance.timing` after each navigation
   - If unknown framework: Execute e2e command and prompt user to manually capture browser DevTools Network export (HAR file)
4. Capture metrics:
   - **Page navigation timing:** Measure each `page.goto()` or click navigation duration
   - **API calls:** Extract from browser Network tab (via CDP or HAR export)
   - **Resource loading:** Warm cache hits vs cold cache misses
   - **Total workflow time:** Start of first page → completion of last page
5. Store e2e metrics separately from cold-start metrics
6. Proceed to Step 8 (Generate Baseline Report) with e2e metrics

### Step 3.4 – both Mode

If user selects "both":

1. Follow Step 3.2 (e2e Mode) first
2. After e2e execution completes, proceed with cold-start flow (Step 4-7)
3. Step 8 (Generate Baseline Report) will include **both** e2e and cold-start metrics in separate sections

**Note:** Store the selected mode (`cold-start`, `e2e`, or `both`) for use in report generation.

## Step 4 – Verify Test Data Availability

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

Proceed to Step 5.

## Step 5 – Check for Existing Baseline

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
  
  Proceed to Step 6.

- **If baseline does not exist:** Proceed to Step 6.

## Step 6 – Prepare Capture Script

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

## Step 7 – Execute Baseline Capture

### Step 7.1 – Construct Command

Build the command to execute the capture script based on the selected mode from Step 3:

**If mode = `cold-start`:**
```
node {baseline-directory}/capture-baseline.mjs --config {path-to-performance-config.md} --port {port} --mode cold-start
```

**If mode = `e2e`:**
```
node {baseline-directory}/capture-baseline.mjs --config {path-to-performance-config.md} --mode e2e --e2e-command "{e2e-command}"
```

**If mode = `both`:**
```
node {baseline-directory}/capture-baseline.mjs --config {path-to-performance-config.md} --port {port} --mode both --e2e-command "{e2e-command}"
```

Note: The script will read the Performance Scenarios table from the config and measure all configured scenarios. The workflow selection is used for filtering during report generation (Step 8).

### Step 7.2 – Execute Script and Handle Errors

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

### Step 7.3 – Parse JSON Output

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

Parse this JSON output and store it for use in Step 8.

## Step 8 – Generate Baseline Report

### Step 8.1 – Determine Report Structure Based on Mode

- **If mode = `cold-start`:** Generate standard baseline report with cold-start metrics
- **If mode = `e2e`:** Generate baseline report with e2e metrics only, add note that cold-start was skipped
- **If mode = `both`:** Generate combined report with two sections:
  - Section 1: E2E Workflow Metrics (realistic user flow with warm cache)
  - Section 2: Cold-Start Metrics (worst-case direct navigation)

### Step 8.2 – Read Report Template

Read the baseline report template from the plugin cache:

```
{plugin-cache}/sdlc-workflow/{version}/skills/performance/baseline-report.template.md
```

### Step 8.3 – Filter Scenarios by Selected Workflow

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

### Step 8.4 – Replace Template Placeholders

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

### Step 8.5 – Write Report to File

Write the generated report to the baseline directory:

```
{baseline-directory}/baseline-report.md
```

### Step 8.6 – Update Configuration with Baseline Data (New)

After generating the baseline report, update the performance-config.md with baseline metadata and metrics:

**Step 8.6.1 – Read Current Configuration**

Read `.claude/performance-config.md` from the target repository.

**Step 8.6.2 – Update Metadata Section**

Update the metadata frontmatter with:

```yaml
metadata:
  # ... existing fields ...
  last_updated: {current-timestamp}
  baseline_captured: true
  baseline_mode: {selected-mode from Step 3}
  baseline_timestamp: {current-timestamp}
  baseline_commit_sha: {git rev-parse HEAD}
```

**Step 8.6.3 – Update Optimization Targets (If First Baseline)**

Check if the Optimization Targets table has "TBD" in the Baseline (p95) column:

**If Baseline column = "TBD" (first baseline):**

Update the Optimization Targets section:

| Metric | Baseline (p95) | Current (p95) | Target | Unit | Last Updated |
|---|---|---|---|---|---|
| LCP | **{lcp-p95 from aggregate}** | **{lcp-p95}** | {target} | seconds | **{timestamp}** |
| FCP | **{fcp-p95}** | **{fcp-p95}** | {target} | seconds | **{timestamp}** |
| TTI | **{tti-p95}** | **{tti-p95}** | {target} | seconds | **{timestamp}** |
| Total Load Time | **{total-p95}** | **{total-p95}** | {target} | seconds | **{timestamp}** |

- Populate **Baseline (p95)** column with p95 metrics from aggregate JSON output
- Set **Current (p95)** column = Baseline (p95) (initial values match)
- Keep **Target** column unchanged (from setup)
- Set **Last Updated** = current timestamp

**If Baseline column already has values (re-baseline):**

- Leave Baseline column unchanged (baseline is immutable)
- Update Current (p95) column with new p95 metrics (this is a re-baseline after changes)
- Update Last Updated column with current timestamp

**Step 8.6.4 – Write Updated Configuration**

Write the updated configuration back to `.claude/performance-config.md`.

**Step 8.6.5 – Log Configuration Update**

Log to user:

```
✓ Configuration auto-updated:
  - Baseline mode: {selected-mode}
  - Baseline metrics captured (p95)
  - Commit SHA: {baseline_commit_sha}
  - Last updated: {timestamp}
```

**Note:** This step ensures the configuration is kept in sync with the baseline report, enabling downstream skills to read baseline mode and validate freshness.

## Step 9 – Output Summary

Report to the user:

> ✅ **Baseline captured successfully!**
>
> **Mode:** {cold-start | e2e | both}
> **Workflow:** {workflow name}
> **Scenarios measured:** {scenario count}
>
> (Continue with existing output format below)

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
