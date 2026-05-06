---
name: performance-analyze-module
description: |
  Inspect source code to detect performance anti-patterns by examining bundle composition, API call patterns, component structure, and resource loading.
argument-hint: "[target-repository-path]"
---

# performance-analyze-module skill

You are an AI performance analysis assistant. You **inspect source code** to detect performance anti-patterns in a user-selected workflow. You examine bundle composition, API call patterns, component render logic, and resource loading to identify common performance issues including over-fetching, N+1 queries, unused table joins, waterfall loading, render-blocking resources, unused code, and expensive re-renders.

**Key Distinction:** This skill performs source code analysis to identify performance issues. The `performance-plan-optimization` skill reads this analysis report and creates Jira tasks — it does not inspect code.

## Guardrails

- This skill creates files in designated performance directories (`.claude/performance/analysis/`)
- This skill does NOT modify source code files — only creates performance analysis artifacts
- This skill requires Performance Analysis Configuration with a selected workflow and an existing baseline report

**Apply:** [Execution Guardrails](../performance/execution-guardrails.template.md)

### Blocking Steps (this skill)
- Step 1 – Target repository path (if not provided as argument)

### Completeness Requirements (this skill)
- All anti-patterns checked (Steps 6.1–6.9), even if zero instances found for each
- All discovered endpoints analyzed in Step 7 (none silently omitted)
- All bundle sizes measured where stats are available
- Complete analysis report written to file before Step 9 output summary

### Error Handling (this skill)
- Missing config → halt at Step 2 with remediation: run `performance-setup`
- Missing selected workflow → halt at Step 2.1 with remediation: run `performance-baseline`
- Missing baseline report → halt at Step 3 with remediation: run `performance-baseline`
- Step 6.10 Serena probe failure → do NOT halt; record exact error, set
  `serena_mode = down`, continue with Grep paths (Steps 7.x-B)

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

**Validate repository type based on analysis scope:**

1. **Check if performance-config.md exists:**
   - If exists: Read `metadata.analysis_scope` field
   - If not exists: Skip validation (setup hasn't run yet, proceed to Step 2)

2. **Conditional validation based on scope:**

   **If `analysis_scope = "backend-only"`:**
   - Verify backend repository indicators exist:
     - Rust: `Cargo.toml`, `src/main.rs` or `src/lib.rs`
     - Java: `pom.xml` or `build.gradle`, `src/main/java/`
     - Python: `requirements.txt` or `pyproject.toml`, Python files
     - Node: `package.json` with server dependencies (express, fastify, etc.)
     - Ruby: `Gemfile`, `.rb` files
     - C#: `.csproj`, `.cs` files
   - **Skip frontend indicator validation**

   **If `analysis_scope = "frontend-only"`:**
   - Verify frontend application indicators exist:
     - `package.json` with frontend dependencies
     - `src/` or `app/` directory
     - Frontend framework indicators (React, Vue, Angular, Svelte, Next.js configuration files)
   - **Skip backend indicator validation**

   **If `analysis_scope = "full-stack"` or `"full-stack-monorepo"`:**
   - **Verify BOTH frontend AND backend indicators exist**
   - Frontend indicators (same as frontend-only above)
   - Backend indicators (same as backend-only above)
   - Both must be present for full-stack analysis

   **If config doesn't exist:**
   - Skip validation entirely (setup phase hasn't completed)
   - Proceed to Step 2

## Step 2 – Verify Performance Configuration and Selected Workflow

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Verify config exists, stop if missing
- Read configuration for workflow and backend settings

### Step 2.0 – Read Analysis Assumptions

Read the `## Analysis Assumptions` section from `performance-config.md` and extract the
constants used in impact calculations:

| Config field | Variable | Default (if section missing) |
|---|---|---|
| Average Bandwidth | `analysis_bandwidth_mbps` | 5 |
| API Latency (average) | `analysis_api_latency_ms` | 100 |
| Layout Reflow Cost | `analysis_reflow_cost_ms` | 5 |
| Cache Hit Rate | `analysis_cache_hit_rate` | 0.8 |
| Chain Analysis Depth | `analysis_chain_depth` | 3 |
| DB Query Base Latency | `analysis_db_latency_ms` | 10 |

**Validation:**
- `analysis_bandwidth_mbps` must be > 0
- `analysis_api_latency_ms` must be > 0
- `analysis_reflow_cost_ms` must be > 0
- `analysis_cache_hit_rate` must be between 0.0 and 1.0 inclusive
- `analysis_chain_depth` must be an integer between 1 and 5 inclusive
- `analysis_db_latency_ms` must be > 0

If any value fails validation, use the default and log a warning:
> ⚠️ Invalid value for `{field}` in Analysis Assumptions — using default ({default})

If the `## Analysis Assumptions` section is absent (e.g., pre-existing config), use all defaults
and log:
> ℹ️ Analysis Assumptions section not found in config — using built-in defaults.
> Run `/sdlc-workflow:performance-setup` to add configurable assumptions to your config.

Store all values for use throughout Steps 6 and 7.

### Step 2.1 – Check for Selected Workflow

**Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-6-workflow-validation)

**Specific actions for this skill:**
- Extract workflow name, entry point, key screens for scope analysis
- Store for module discovery and anti-pattern detection

### Step 2.2 – Read Backend Availability from Metadata (Updated)

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction)

**Specific field to extract:**
- `metadata.backend_available` → backend_available (cached status, no re-validation)

**If `backend_available = true`:**

Extract backend configuration from `### Backend Repository` section (under `## Repository Configuration`):
- Backend repo name
- Backend path
- Backend framework
- Serena instance name
- API base path

**If frontend is included (`analysis_scope` in ["full-stack", "full-stack-monorepo", "frontend-only"]):**

Extract frontend configuration from `### Frontend Repository` section (under `## Repository Configuration`):
- Frontend repo name
- Frontend path
- Frontend framework
- Bundler

Store for use in module analysis and bundler-specific optimization detection.

**Serena instance name from config:**

Store `serena_instance_name` for use in Step 6.10 probe and Step 7 Serena calls.
All Step 7 Serena tool calls use `mcp__{serena_instance_name}__<tool>` directly.

### Step 2.2.1 – Note on Serena Availability

Serena availability is determined at runtime by a live probe in **Step 6.10**, immediately before
backend analysis begins. The probe call (`get_symbols_overview`) sets `serena_mode` to one of:

- `live` — Serena responded; backend analysis uses Serena-only paths (Steps 7.x-A)
- `down` — Serena errored; backend analysis uses Grep paths (Steps 7.x-B)
- `not-configured` — no `serena_instance` in config; Grep paths used

**If `serena_instance` is not configured, display to user now (early warning):**

> ℹ️ **Serena MCP not configured — backend analysis will use Grep**
>
> Backend analysis will use Grep-based pattern matching (medium confidence).
>
> **For higher accuracy:** Serena MCP provides semantic code intelligence with high-confidence
> detection of N+1 query patterns, over-fetching via full schema extraction, and unused JOINs.
>
> **To enable:** Add Serena instance to CLAUDE.md Repository Registry and re-run this skill.
>
> Analysis will continue with Grep (some patterns may be missed).

**If `serena_instance` is configured but probe fails at Step 6.10, display at that point:**

> ⚠️ **Serena MCP configured but unavailable** — falling back to Grep.
>
> Check MCP server is running and verify Serena instance name in CLAUDE.md.

**If unavailable:** `serena_instance` is stored for later use. Backend analysis will use Grep paths when the live probe runs at Step 6.10. Continue to Step 3.

**If `backend_available = false`:**

Display informative message to user:

> ℹ️ **Frontend-only analysis mode**
>
> Backend repository is not configured. Analysis will focus on:
> ✓ Frontend bundle composition and code-splitting
> ✓ Frontend API call patterns (limited to request inspection)
> ✓ Frontend render optimization opportunities
> ✓ Resource loading patterns
>
> ⚠️ **The following analysis will be SKIPPED:**
> ✗ Backend response schema extraction
> ✗ Cross-repository over-fetching detection
> ✗ Database N+1 query pattern detection
> ✗ Backend caching opportunities
>
> **To enable full-stack analysis**, re-run:
> ```
> /sdlc-workflow:performance-setup
> ```
> and configure backend repository when prompted.

Store backend configuration and `backend_available` flag for use in Step 7.

**Note:** Backend availability is cached in config metadata and validated during setup. This avoids redundant path checks and provides clear feedback about analysis limitations.

## Step 3 – Verify Baseline Report Exists

Read `metadata.metric_type` from `performance-config.md` to determine which baseline file(s) to check.

Determine the baseline directory from the **Target Directories** section (e.g., `.claude/performance/baselines/`).

**If metric_type = "frontend" or "hybrid":**

Check for frontend baseline: `{baseline-directory}/baseline-report.md`

- **If baseline does not exist:** Inform the user:
  > "Frontend baseline report not found. Please run `/sdlc-workflow:performance-baseline` first to capture browser metrics, then re-run this skill."
  
  Stop execution.

**If metric_type = "backend":**

Check for backend baseline: `{baseline-directory}/benchmark-results.json`

- **If baseline does not exist:** Inform the user:
  > "Backend baseline not found. Please run `/sdlc-workflow:performance-baseline` first to capture API metrics, then re-run this skill."
  
  Stop execution.

**If metric_type = "hybrid":**

Check for BOTH `baseline-report.md` AND `benchmark-results.json`. Both must exist.

- **If either is missing:** Inform the user which baseline(s) are missing and instruct to run `/sdlc-workflow:performance-baseline`.
  
  Stop execution.

**If baseline(s) exist:** Proceed to Step 4.

**Note:** 
- Frontend baselines use cold-start mode (Playwright browser automation)
- Backend baselines use api-benchmark mode (HTTP load testing)
- Hybrid mode captures both

## Step 4 – Read Baseline Data

Read `metadata.metric_type` from configuration to determine which baseline data to parse.

**If metric_type = "frontend" or "hybrid":**

**Apply:** [Common Pattern: Baseline Report Reading](../performance/common-patterns.md#pattern-5-baseline-report-reading)

**Specific data to extract from baseline-report.md:**
- **Per-scenario metrics**: LCP, FCP, DOM Interactive, Total Load Time (p50, p95, p99)
- **Resource timing breakdown**: URLs, load duration, transfer size per resource
- **Aggregate metrics**: Overall performance across all scenarios
- **Capture mode**: cold-start

Store frontend baseline data for anti-pattern detection in Steps 5 and 6.

**If metric_type = "backend" or "hybrid":**

Parse `benchmark-results.json` for backend baseline data.

**Specific data to extract:**
- **Per-endpoint metrics**: Response time (p50, p95, p99), throughput (req/sec), error rate (%)
- **Cache effectiveness**: Cold vs warm latency comparison
- **Endpoints profiled**: List of API routes tested

Store backend baseline data for anti-pattern detection in Step 7.

**If metric_type = "hybrid":**

Parse BOTH baseline-report.md AND benchmark-results.json. Store both frontend and backend baseline data for comprehensive analysis.

## Step 5 – Analyze Bundle Composition

Analyze the JavaScript bundle composition for the selected workflow.

### Step 5.1 – Locate Bundle Stats (Optional)

Check if the target repository has webpack or vite bundle stats:

Common locations:
- `dist/stats.json` (webpack)
- `build/stats.json` (webpack)
- `.vite/stats.json` (vite)
- `stats.json` in the repository root

If bundle stats exist, parse them to extract:
- Module names and sizes
- Third-party library dependencies
- Code-split chunk boundaries
- Source map for module-to-file mapping

### Step 5.2 – Identify Third-Party Libraries

Extract the list of JavaScript files loaded in the baseline scenarios (from resource timing breakdown).

For each JavaScript file, classify it as:
- **Third-party library** — matches pattern `/node_modules/`, `/vendor/`, or known CDN domains
- **Application code** — all other JavaScript files

Calculate:
- Total size of third-party libraries (sum of transfer sizes)
- Total size of application code
- Ratio of third-party to application code

List the top 10 third-party libraries by size.

### Step 5.3 – Calculate Module-Specific vs Shared Code Ratio

If bundle stats are available, calculate the ratio of:
- **Module-specific code** — code only used by the selected workflow
- **Shared code** — code shared across multiple workflows/routes

If bundle stats are not available, estimate by examining import patterns in the workflow's route components (see Step 6.5 for unused code detection approach).

## Step 6 – Detect Performance Anti-Patterns (Frontend)

**Scope Check:** Read `metadata.metric_type` from configuration.

**If metric_type = "backend":**

Log: "Skipping frontend analysis (backend-only mode configured)."

Skip to Step 7 (Backend Source Code Analysis).

**If metric_type = "frontend" or "hybrid":**

Proceed with frontend anti-pattern detection below.

> **Note on impact estimates:** Quantified impact figures in this section are
> rough order-of-magnitude estimates based on heuristic constants, not measurements.
> They should be used to prioritize optimization effort (larger numbers warrant
> more attention) but not cited as actual performance projections. Replace with
> Lighthouse or WebPageTest measurements after implementation.

> **Note on detection methodology:** Several detection approaches in this step use Grep-based
> pattern matching to identify anti-patterns in source code. This methodology has known limitations:
>
> - **Over-Fetching Detection (Step 6.1):** Grep cannot reliably determine if a field is "unused" —
>   it may be used indirectly via destructuring, spread operators, passed to libraries, or used
>   conditionally. False positives are likely. Manual code review is required to validate findings.
>
> - **N+1 Query Detection (Step 6.2):** Grep cannot distinguish between frontend N+1 patterns
>   (sequential API calls in loops) and backend N+1 patterns (database queries inside loops).
>   This step focuses on frontend patterns only. Backend N+1 detection requires backend source
>   analysis (Step 7.3).
>
> - **Layout Thrashing Detection (Step 6.7):** Grep-based read-write pattern detection has high
>   false-positive rates. A `offsetWidth` read followed by a `style.height` write may not cause
>   forced reflow if they occur in separate execution contexts or with browser optimizations.
>   Manual profiling with Chrome DevTools Performance tab is required to confirm actual reflows.
>
> **Recommendation:** Treat Grep-based findings as candidates for investigation, not confirmed issues.
> Always verify with browser profiling tools before investing optimization effort.

For each anti-pattern, search the codebase for indicators and report findings with severity classification and quantified impact.

### Step 6.1 – Over-Fetching Detection

> ⚠️ **Detection Limitation:** This grep-based analysis cannot detect destructuring patterns (`const { field } = data`), dynamic property access (`data[key]`), or fields used in child components after prop drilling. Treat results as leads for manual review, not definitive over-fetching evidence.

**Definition:** API responses include fields that are never used in the UI.

**Detection approach:**

1. **Identify API calls in workflow components:**
   - Use Grep to search for `fetch(`, `axios.get(`, `useQuery(` in workflow route components
   - Extract API endpoint URLs from the search results
   - For each endpoint, identify the response schema (check TypeScript interfaces, OpenAPI specs, or backend handler types from Step 7.2)

2. **Analyze field usage in components:**
   - For each API endpoint response schema, identify the fields returned
   - Use Grep to search for usage of each field in the component that consumes the response
   - Flag fields that appear in the response schema but are never referenced in the consuming code

**Severity classification:**
- **High:** > 50% of response fields unused, or response size > 100KB with > 30% unused
- **Medium:** 25-50% of response fields unused, or response size > 50KB with 25-30% unused
- **Low:** < 25% of response fields unused

**Quantified impact:**
- Estimated size savings: `(unused_fields / total_fields) * response_size`
- Estimated time savings: `estimated_size_savings / (analysis_bandwidth_mbps * 125000)` (using configured bandwidth: `analysis_bandwidth_mbps` Mbps)

**Confidence Level:** Low — Grep cannot track destructuring, prop drilling, or dynamic access.
Report each finding with confidence = **Low** unless backend schema analysis (Step 8) confirms the
field is absent from frontend usage.

**Verification Checklist (include in analysis report for each finding):**
- [ ] Confirm the field is not accessed via destructuring (`const { field } = data`)
- [ ] Confirm the field is not passed as a prop to child components
- [ ] Confirm the field is not used in a dynamically-keyed access (`data[key]`)
- [ ] Validate actual payload size with DevTools Network tab before estimating savings
- [ ] Apply impact threshold: only flag if `unused_fields × avg_record_size > 50 KB`

### Step 6.2 – N+1 Query Detection

> ⚠️ **Detection Limitation:** Proximity-based grep cannot track control flow. Patterns in service layers, Redux thunks, or `useEffect` chains more than 10 lines apart will not be detected. This step surfaces candidates only — verify each finding manually.

**Definition:** Sequential API calls in loops, leading to many round-trips.

**Detection approach:**

1. **Search for loops with API calls:**
   - Use Grep to search for patterns:
     - `.forEach(` or `.map(` or `for (` followed by `fetch(` or `axios.` within 10 lines
     - `await` inside loops (indicator of sequential execution)
   - Extract code snippets showing the loop and API call pattern

2. **Verify sequential execution:**
   - Check if the loop uses `await` (sequential) vs `Promise.all` (parallel)
   - Flag sequential loops with > 5 iterations as high severity

**Severity classification:**
- **High:** Loop with > 10 iterations calling API sequentially
- **Medium:** Loop with 5-10 iterations calling API sequentially
- **Low:** Loop with < 5 iterations calling API sequentially

**Quantified impact:**
- Estimated time savings: `(n_iterations - 1) * analysis_api_latency_ms` (using configured latency: `analysis_api_latency_ms` ms)

**Confidence Level:** Medium — Grep proximity (10-line window) detects obvious patterns but misses
service-layer indirection and Redux/saga chains.

**Verification Checklist (include in analysis report for each finding):**
- [ ] Confirm the loop iterates at runtime (not just defined but never called on this workflow)
- [ ] Confirm the call is `await`-ed inside the loop body (sequential), not batched with `Promise.all`
- [ ] Verify the loop iteration count with actual test data, not a static estimate
- [ ] Check whether a batch endpoint already exists but is unused

### Step 6.3 – Waterfall Loading Detection

**Definition:** Resources loaded sequentially due to dependency chains, delaying page interactivity.

**Detection approach:**

1. **Analyze resource timing from baseline:**
   - Extract resource timing data from baseline report
   - For each resource, identify dependencies (resources that must load before this one)
   - Build a dependency graph of resource loading

2. **Detect sequential chains:**
   - Identify chains of > 3 resources loading sequentially (each starting after the previous completes)
   - Calculate the waterfall depth (longest sequential chain)
   - Flag chains where total load time exceeds 500ms

**Severity classification:**
- **High:** Waterfall depth > 5, or total chain time > 1000ms
- **Medium:** Waterfall depth 4-5, or total chain time 500-1000ms
- **Low:** Waterfall depth 3, or total chain time < 500ms

**Quantified impact:**
- Estimated time savings: `total_chain_time - (slowest_resource_time * 1.2)` (assume 20% overhead for parallel loading)

### Step 6.4 – Render-Blocking Resources Detection

**Definition:** Synchronous scripts or non-async CSS in the critical rendering path, delaying FCP/LCP.

**Detection approach:**

1. **Search for synchronous script tags:**
   - Use Grep to search for `<script src=` without `async` or `defer` attributes in HTML entry points
   - Check `index.html`, `public/index.html`, or framework-generated entry HTML

2. **Search for blocking CSS:**
   - Use Grep to search for `<link rel="stylesheet"` without `media="print"` or other non-blocking attributes
   - Identify CSS files loaded before first paint

3. **Cross-reference with baseline FCP/LCP:**
   - For each blocking resource, estimate impact by comparing resource load time to FCP/LCP metrics
   - If resource load time > 50% of FCP, flag as high severity

**Severity classification:**
- **High:** Blocking resource load time > 50% of FCP, or blocking JS > 200KB
- **Medium:** Blocking resource load time 25-50% of FCP, or blocking JS 100-200KB
- **Low:** Blocking resource load time < 25% of FCP, or blocking JS < 100KB

**Quantified impact:**
- Estimated FCP improvement: `blocking_resource_load_time * 0.8` (assume 80% can be deferred)

### Step 6.5 – Unused Code Detection

**Definition:** Imported modules, functions, or components that are never called or rendered.

**Detection approach:**

1. **Identify imports in workflow components:**
   - Use Grep to extract all `import` statements from workflow route components
   - Parse imported symbols (e.g., `import { Foo, Bar } from './utils'`)

2. **Search for usage of each imported symbol:**
   - For each imported symbol, use Grep to search for its usage in the importing file
   - Flag symbols that appear in import statements but are never referenced in the file body

3. **Estimate unused bundle size:**
   - If bundle stats are available, look up the size of each unused import
   - Otherwise, estimate based on typical module sizes (e.g., 5KB for utility functions, 20KB for components)

**Severity classification:**
- **High:** > 100KB of unused code imported, or > 10 unused imports
- **Medium:** 50-100KB of unused code imported, or 5-10 unused imports
- **Low:** < 50KB of unused code imported, or < 5 unused imports

**Quantified impact:**
- Estimated size savings: `sum_of_unused_module_sizes`
- Estimated load time improvement: `size_savings / (analysis_bandwidth_mbps * 125000)` (using configured bandwidth)

### Step 6.6 – Expensive Re-Render Detection

**Definition:** React/Vue components that re-render unnecessarily due to missing memoization.

**Detection approach:**

1. **Identify component hierarchy in workflow:**
   - Use Grep to find all components in workflow route paths
   - Extract component names and file paths

2. **Search for memoization patterns:**
   - **React:** Search for `React.memo`, `useMemo`, `useCallback` in component files
   - **Vue:** Search for `computed`, `watch` with proper dependency tracking
   - Flag components that:
     - Receive complex props (objects, arrays) without memoization
     - Define inline functions passed as props (React anti-pattern)
     - Lack `key` props in list rendering

3. **Cross-reference with DOM Interactive metric:**
   - If DOM Interactive is high (> 3500ms), expensive re-renders are more likely to be impactful
   - Prioritize components in the critical render path (those rendered before LCP element)

**Severity classification:**
- **High:** Components in critical path without memoization, and DOM Interactive > 3500ms
- **Medium:** Components in critical path without memoization, and DOM Interactive 2500-3500ms
- **Low:** Non-critical components without memoization, or DOM Interactive < 2500ms

**Quantified impact:**
- Estimated DOM Interactive improvement: Hard to quantify without runtime profiling, report as "Potential improvement: 10-30% reduction in DOM Interactive"

### Step 6.7 – Long Task Detection

**Definition:** JavaScript execution blocks that run for > 50ms, blocking the main thread.

**Detection approach:**

1. **Check baseline for performance traces:**
   - If baseline includes browser performance traces (long task API data), extract long task entries
   - For each long task, identify the script URL and duration

2. **Fallback (if traces unavailable):**
   - Use Grep to search for computationally expensive patterns:
     - Synchronous loops over large datasets (e.g., `.forEach` on arrays with > 1000 items)
     - JSON parsing of large payloads (e.g., `JSON.parse` of > 100KB strings)
     - DOM manipulation in loops (e.g., `document.createElement` inside loops)

**Severity classification:**
- **High:** Long task > 200ms, or multiple tasks > 100ms
- **Medium:** Long task 100-200ms
- **Low:** Long task 50-100ms

**Quantified impact:**
- Estimated DOM Interactive improvement: `sum_of_long_task_durations - 50ms` (assume tasks can be chunked to 50ms each)

### Step 6.8 – Layout Thrashing Detection

> ⚠️ **Detection Limitation:** Static analysis cannot determine execution ordering. A component that reads one layout property and then writes one style property is valid batching but will match this grep. Only flag patterns where the read and write appear inside a loop or are definitively sequential. True layout thrashing detection requires Chrome DevTools Performance profiler.

**Definition:** Interleaved read-write DOM operations causing multiple reflows.

**Detection approach:**

1. **Search for DOM read-write patterns:**
   - Use Grep to search for patterns indicating layout thrashing:
     - Reading layout properties (`offsetWidth`, `offsetHeight`, `getBoundingClientRect`) followed by writes (`style.width =`, `classList.add`)
     - Loops that alternate between reads and writes

2. **Example anti-pattern:**
   ```javascript
   for (let i = 0; i < elements.length; i++) {
     const width = elements[i].offsetWidth; // Read (causes reflow)
     elements[i].style.width = width + 10 + 'px'; // Write (invalidates layout)
   }
   ```

**Severity classification:**
- **High:** Read-write pattern in loops with > 10 iterations
- **Medium:** Read-write pattern in loops with 5-10 iterations
- **Low:** Read-write pattern in loops with < 5 iterations, or isolated read-write pairs

**Quantified impact:**
- Estimated rendering time improvement: `(n_iterations - 1) * analysis_reflow_cost_ms` (using configured reflow cost: `analysis_reflow_cost_ms` ms per reflow)

**Confidence Level:** Low — static analysis cannot determine execution ordering. Read-then-write
on separate lines may not cause forced reflow if they occur in different event loop ticks.

**Verification Checklist (include in analysis report for each finding):**
- [ ] Confirm the read and write occur in the same synchronous execution block (same function, no `await` between them)
- [ ] Confirm the loop iterates at runtime on this workflow, not only in edge cases
- [ ] Validate with Chrome DevTools Performance → "Layout" events before investing fix effort
- [ ] Check whether the pattern is inside a `requestAnimationFrame` callback (already batched)

### Step 6.9 – Missing Lazy Loading Detection

**Definition:** Large components or routes loaded eagerly instead of on-demand.

**Detection approach:**

1. **Identify route-level code splitting:**
   - Use Grep to search for dynamic imports in route configuration:
     - **React Router:** `React.lazy(() => import('./Component'))`
     - **Vue Router:** `component: () => import('./Component.vue')`
     - **Next.js:** `dynamic(() => import('./Component'), { ssr: false })`

2. **Identify routes without lazy loading:**
   - For each route in the selected workflow, check if it uses lazy loading
   - Flag routes that use static imports (e.g., `import Component from './Component'`) for large components

3. **Estimate component size:**
   - If bundle stats are available, look up the size of each statically imported component
   - Otherwise, estimate based on file size (use `wc -l` or file size inspection)

**Severity classification:**
- **High:** Route component > 100KB loaded eagerly, or > 5 routes without lazy loading
- **Medium:** Route component 50-100KB loaded eagerly, or 3-5 routes without lazy loading
- **Low:** Route component < 50KB loaded eagerly, or < 3 routes without lazy loading

**Quantified impact:**
- Estimated initial bundle size reduction: `sum_of_eagerly_loaded_component_sizes`
- Estimated FCP improvement: `size_reduction / (analysis_bandwidth_mbps * 125000)` (using configured bandwidth)

## Step 6.10 – Serena Availability Probe (Backend Analysis Gate)

**If `backend_available = false`:** Skip Steps 6.10 and 7 entirely (frontend-only mode).

**If `backend_available = true`:** Run the probe:

```bash
serena_instance=$(grep "Serena Instance" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
```

**If `serena_instance` is non-empty and not "—":**

Call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`.

- **Response received (any result):** `serena_mode = live`. Store overview. Proceed to Step 7 using **-A** sub-steps.
- **Error response:** `serena_mode = down`. Record exact error. Proceed to Step 7 using **-B** sub-steps.

**If `serena_instance` is "—" or empty:** `serena_mode = not-configured`. Proceed to Step 7 using **-B** sub-steps.

> `serena_mode` is set once here and applies to all of Steps 7.1 through 7.6.

---

## Step 7 – Backend Source Code Analysis

**CRITICAL:** This step is MANDATORY for comprehensive over-fetching detection when backend is configured.

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 6.10. Follow -A sub-steps when `serena_mode = live`, -B sub-steps otherwise.)

For EACH API endpoint identified in Step 6.1 (Over-Fetching Detection):

### Step 7.1-A – Locate Backend Handler via Serena (`serena_mode = live`)

> Grep is not available in this path.

Call:

```
mcp__{serena_instance}__find_symbol(
    name_path_pattern="<endpoint_path_fragment>",
    relative_path=".",
    substring_matching=true,
    include_body=true,
    include_kinds=[12]
)
```

Extract handler function name and file location. Set `confidence = "high"`.

If not found: try a broader `name_path_pattern`. If still not found after two attempts:
document "Handler for endpoint {endpoint_path} not found via Serena" in report limitations.
Skip Step 7.2-A for this endpoint and continue with the next.

---

### Step 7.1-B – Locate Backend Handler via Grep (`serena_mode = down | not-configured`)

Search for handler by endpoint path fragment using Grep across `backend_path`.
Extract handler function name and file location. Set `confidence = "medium"`.

If handler not found: document limitation in report. Skip Step 7.2-B for this endpoint.

---

### Step 7.2-A – Extract Backend Response Schema via Serena (`serena_mode = live`)

Call `mcp__{serena_instance}__find_symbol` with `include_body=true` on the handler function.

Identify return type from function signature:
- **Rust:** `async fn handler() -> Json<ProductResponse>`
- **Java:** `public ResponseEntity<ProductResponse> handler()`
- **Python:** `def handler() -> ProductResponse:`
- **Node:** Response object or TypeScript return type

Call `mcp__{serena_instance}__find_symbol` again to read the response struct/class definition.
Extract ALL fields recursively (including nested objects, arrays).

---

### Step 7.2-B – Extract Backend Response Schema via Read (`serena_mode = down | not-configured`)

Use the Read tool to read the handler file. Parse return type manually from function signature.
Search for the response struct/class definition. Extract fields (best-effort parsing).

**CRITICAL:** Do not skip backend schema extraction. Find the struct definition and extract all fields before concluding. If extraction fails after exhaustive search, document the search attempts and specific errors encountered, not generic "cannot confirm" statements.

---

**Document complete response schema (both paths):**
```
Endpoint: GET /api/v2/products/:id
Response Type: ProductResponse
Fields:
  - id: string
  - name: string
  - description: string
  - price: number
  - inventory: object
    - quantity: number
    - warehouse_location: string
  - created_at: timestamp
  - updated_at: timestamp
  - internal_notes: string (UNUSED by frontend)
```

### Step 7.3 – Detect Backend Database N+1 Queries

**Definition:** Handler executes queries in a loop instead of batch fetching.

**Detection approach:**

1. **Read handler implementation** (use `mcp__{serena_instance}__find_symbol` with `include_body=true` if `serena_mode = live`, otherwise use Read tool)

2. **Search for query patterns inside loops:**
   - **Rust (sqlx):** 
     ```rust
     for item in items {
         query!("SELECT * FROM table WHERE id = ?", item.id)
             .fetch_one(&pool).await
     }
     ```
   - **Rust (SeaORM):**
     ```rust
     for item in items {
         Entity::find_by_id(item.id)
             .one(&db).await?
     }
     ```
   - **Rust (Diesel):**
     ```rust
     for item in items {
         table.find(item.id)
             .first::<Model>(&conn)?
     }
     ```
   - **Java (JPA/Hibernate):**
     ```java
     for (Item item : items) {
         repository.findById(item.getId())
     }
     ```
   - **Python (SQLAlchemy/Django ORM):**
     ```python
     for item in items:
         session.query(Model).filter(Model.id == item.id).first()
     ```
   - **Node (TypeORM/Prisma):**
     ```javascript
     for (const item of items) {
         await db.model.findUnique({ where: { id: item.id } })
     }
     ```

3. **Count loop iterations:**
   - Use static analysis of the handler code to identify the source of the iterated collection
   - Check if the collection size is determinable from the query (e.g., fixed LIMIT clause, array length constant)
   - If indeterminate, note it as "estimated N items" in the finding

4. **Verify sequential execution:**
   - Check if queries are awaited inside loop (synchronous execution)
   - vs. parallelized (Promise.all, async batch queries)

**Severity classification:**
- **High:** > 10 queries in loop, sequential execution
- **Medium:** 5-10 queries in loop, sequential execution
- **Low:** < 5 queries in loop, or parallelized execution

**Quantified impact:**
- Estimated latency impact: `(n_queries - 1) * analysis_db_latency_ms`
  (using configured DB Query Base Latency; default 10ms)
- Example: 10 queries → `(10-1) * analysis_db_latency_ms = 90ms` added latency (at default)

### Step 7.4 – Detect Missing Pagination

**Definition:** Endpoint returns unbounded result sets without pagination.

**Detection approach:**

1. **Identify collection endpoints:**
   - Response type is a collection: `Vec<T>`, `List<T>`, `Array<T>`
   - Example: `GET /api/v2/products` returns `Vec<Product>`

2. **Check handler parameters for pagination:**
   - Look for params: `page`, `limit`, `offset`, `per_page`, `page_size`
   - **Rust:** `Query<PaginationParams>`, `page: web::Query<i32>`
   - **Java:** `@RequestParam("page") int page`
   - **Python:** `page: int = Query(default=1)`
   - **Node:** `req.query.page`, `@Query('page') page: number`

3. **Check query for pagination methods:**
   - **Rust (sqlx):** `.limit()`, `.offset()`
   - **Rust (SeaORM):** `.limit()`, `.offset()`, `.paginate(db, page_size)`
   - **Rust (Diesel):** `.limit()`, `.offset()`
   - **Java (JPA):** `setMaxResults()`, `setFirstResult()`
   - **Python (SQLAlchemy):** `.limit()`, `.offset()`
   - **Node:** `.take()`, `.skip()`

**Severity classification:**
- **High:** No pagination, returns > 100 items (from baseline data or database count)
- **Medium:** No pagination, returns 50-100 items
- **Low:** No pagination, returns < 50 items

**Quantified impact:**
- Estimated payload reduction: `(total_items - items_per_page) * avg_item_size`
- Assume `items_per_page = 20` and estimate `avg_item_size` from baseline
- Example: 100 items, 5KB each → `(100-20) * 5KB = 400KB` saved

### Step 7.5 – Detect Missing Caching

**Definition:** Handler executes expensive operations on every request without caching.

**Detection approach:**

1. **Identify expensive operations:**
   - Database queries for static/slow-changing data (e.g., product categories, user roles)
   - External API calls (HTTP requests to third-party services)
   - Complex computations (aggregations, analytics)

2. **Check for cache usage:**
   - **Rust:** `Cache`, `moka`, `redis-rs`, `cached` crate, `lazy_static!` with `HashMap`
   - **Rust (SeaORM integration):** `sea_orm::QueryResult` with manual cache layer
   - **Java:** `@Cacheable`, `Redis`, `Caffeine`
   - **Python:** `@lru_cache`, `Redis`, `@cache`
   - **Node:** `node-cache`, `Redis`, `memory-cache`
   - Search for cache get/set patterns in handler code

3. **Determine data change frequency:**
   - Static data (never changes): HIGH priority for caching
   - Slow-changing (updates hourly/daily): MEDIUM priority
   - Fast-changing (real-time): LOW priority (caching may not help)

**Severity classification:**
- **High:** Expensive operation (> 100ms) on high-traffic endpoint, no cache, static/slow-changing data
- **Medium:** Operation 20-100ms on medium-traffic endpoint, no cache
- **Low:** Operation < 20ms, or low-traffic endpoint, or fast-changing data

**Quantified impact:**
- Estimated latency reduction: `operation_time * analysis_cache_hit_rate` (using configured cache hit rate: `analysis_cache_hit_rate`)
- Example: 200ms query with 0.8 hit rate → `200ms × 0.8 = 160ms` saved per cached request

### Step 7.6 – Detect Inefficient Queries

**Definition:** Queries that fetch unnecessary data (SELECT *, missing indexes).

**Detection approach:**

1. **Extract SQL queries from handler:**
   - Look for query builders or raw SQL strings
   - **Rust (sqlx):** `query!("SELECT ...")`, `query_as!(...)`
   - **Rust (SeaORM):** `Entity::find()`, `.column()`, `.select_only()`
   - **Rust (Diesel):** `table::dsl::*`, `.select()`, `.filter()`
   - **Java (JPA):** `@Query("SELECT ...")`, `createQuery(...)`
   - **Python (SQLAlchemy):** `session.query(Model).filter(...)`
   - **Node (TypeORM):** `createQueryBuilder().select(...)`

2. **Check for SELECT *:**
   - Flag queries using `SELECT *` or ORM equivalents that fetch all columns
   - Example: `query!("SELECT * FROM products WHERE id = ?")`

3. **Identify which fields are actually used:**
   - Cross-reference queried fields with response schema (from Step 7.2)
   - If query returns 20 columns but response only uses 5, flag as inefficient

4. **Check for missing indexes (if schema available):**
   - Look for WHERE clauses on non-indexed columns
   - Look for JOINs without foreign key indexes
   - This requires access to database schema (migrations, SQL files)

**Severity classification:**
- **High:** `SELECT *` on table with > 10 columns, > 1000 rows (from baseline or DB stats)
- **Medium:** Unnecessary JOINs, or fetching > 50% unused columns
- **Low:** Minor inefficiencies, or < 25% unused columns

**Quantified impact:**
- "Potential 30-50% query time reduction" (qualitative estimate)
- Payload reduction: `unused_columns * avg_column_size`

### Step 7.6.1 – Detect Unused Table Joins

**Definition:** Database queries that JOIN tables but never access fields from the joined tables, wasting database resources.

**Why this matters:** Each JOIN operation requires database engine to:
- Read indexes for join keys
- Potentially perform table scans if indexes missing
- Allocate memory for join buffers
- Sort/hash join keys if necessary

Even if joined columns aren't returned (no SELECT from joined table), the JOIN itself has overhead.

**Detection approach:**

#### 1. Extract Queries with JOINs

Search handler code for queries containing JOIN operations:

**Framework-specific patterns:**

| Framework | JOIN Pattern | Example |
|---|---|---|
| Rust (sqlx) | `JOIN`, `INNER JOIN`, `LEFT JOIN` in query strings | `query!("SELECT ... FROM products p JOIN categories c ON p.category_id = c.id")` |
| Rust (Diesel) | `.inner_join()`, `.left_join()` method calls | `products::table.inner_join(categories::table)` |
| Rust (SeaORM) | `.join()`, `.find_with_related()`, `.find_also_related()` | `Product::find().join(JoinType::LeftJoin, product::Relation::Category.def())` |
| Java (JPA/JPQL) | `JOIN`, `LEFT JOIN`, `@OneToMany`, `@ManyToOne` with fetch | `@Query("SELECT p FROM Product p JOIN p.category c")` |
| Java (Hibernate) | `.join()`, `.leftJoin()` in Criteria API | `criteriaBuilder.join(product, "category")` |
| Python (SQLAlchemy) | `.join()`, `.outerjoin()` method calls | `session.query(Product).join(Category)` |
| Python (Django ORM) | `.select_related()`, `.prefetch_related()` | `Product.objects.select_related('category')` |
| Node (TypeORM) | `.leftJoin()`, `.innerJoin()` in QueryBuilder | `.leftJoinAndSelect("product.category", "category")` |
| Node (Sequelize) | `include:` with model references | `include: [{ model: Category }]` |
| Raw SQL | `JOIN`, `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN` | Any raw SQL strings |

**If Serena/MCP available:**
- Use `find_symbol` to locate query functions
- Use `find_symbol` with `include_body=true` to read query strings

**If Serena unavailable:**
- Use Grep with framework-specific JOIN patterns:
  ```bash
  # Raw SQL JOINs
  grep -i "JOIN\s\+\w\+" handler_file
  
  # ORM JOINs (Diesel, SeaORM, SQLAlchemy, Django, TypeORM, etc.)
  grep -E "\.join\(|\.inner_join\(|\.left_join\(|\.select_related\(|\.leftJoin\(|\.find_with_related\(|\.find_also_related\(" handler_file
  ```

#### 2. Identify Joined Tables

For each query with JOINs, extract:
- **Base table** (the primary FROM table)
- **Joined tables** (all tables referenced in JOIN clauses)
- **Join type** (INNER, LEFT, RIGHT, OUTER)
- **Join condition** (ON clause or foreign key reference)

#### 3. Check Field Usage from Joined Tables

For each joined table, determine if ANY fields from that table are actually used:

**A. Check SELECT clause:**
- Raw SQL: Parse SELECT clause for table aliases or table names
  - `SELECT p.*, c.name` → Uses `categories.name` ✓
  - `SELECT p.*` → Does NOT use any `categories` fields ✗

- ORM: Check if joined table fields appear in query projection
  - `.select_related('category')` + no `.category.field` access → UNUSED ✗
  - `.leftJoinAndSelect("product.category", "category")` → USED (explicit select) ✓

**B. Check WHERE/HAVING clauses:**
- If joined table fields used in WHERE: `WHERE c.active = true` → USED ✓
- If only join condition uses joined table: `ON p.category_id = c.id` → Check further

**C. Check handler code after query:**

Search handler code (after the query) for field accesses:

```bash
# For joined table "categories" with alias "c"
grep -E "result\.category|row\.category|\.category\.|c\.name|c\.id" handler_file

# For ORM results
grep -E "product\.category\.|item\.manufacturer\." handler_file
```

**D. Check response schema (from Step 7.2):**
- If response includes fields from joined table → USED ✓
- If response only includes base table fields → Check if joined table used for filtering only

#### 4. Classify Unused Joins

Mark JOIN as **UNUSED** if ALL of the following are true:
1. No fields from joined table in SELECT clause
2. No fields from joined table in WHERE/HAVING clauses
3. No fields from joined table accessed in handler code
4. No fields from joined table in response schema

Mark JOIN as **FILTER-ONLY** if:
1. Joined table fields used in WHERE but not returned in response
2. This is sometimes legitimate (filtering by related entity) but can often be optimized

**Examples of UNUSED joins:**

```sql
-- UNUSED: categories table joined but never used
SELECT p.* FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.price > 100

-- Should be: SELECT * FROM products WHERE price > 100
```

```python
# UNUSED: manufacturer eagerly loaded but never accessed
products = Product.objects.select_related('manufacturer').all()
return [{"name": p.name, "price": p.price} for p in products]

# Should be: Product.objects.all()
```

```rust
// UNUSED: SeaORM - Category relation loaded but never accessed
let products = Product::find()
    .find_with_related(Category)
    .all(&db)
    .await?;

// Response only uses product fields, never accesses category
products.iter().map(|(product, _categories)| {
    ProductResponse {
        id: product.id,
        name: product.name.clone(),
        price: product.price,
    }
}).collect()

// Should be: Product::find().all(&db).await?
```

```rust
// UNUSED: SeaORM - Explicit JOIN but related fields never used
let products = Product::find()
    .join(JoinType::LeftJoin, product::Relation::Category.def())
    .all(&db)
    .await?;

// Category fields never accessed in handler
// Should be: Product::find().all(&db).await?
```

```rust
// UNUSED: SeaORM - find_also_related with unused Option<Model>
let products = Product::find()
    .find_also_related(Category)
    .all(&db)
    .await?;

// Response ignores the Option<category::Model> entirely
products.iter().map(|(product, _category)| {
    json!({ "name": product.name, "price": product.price })
}).collect()

// Should be: Product::find().all(&db).await?
```

```sql
-- FILTER-ONLY: Could be optimized with subquery or EXISTS
SELECT p.* FROM products p
INNER JOIN categories c ON p.category_id = c.id
WHERE c.active = true

-- Better: SELECT * FROM products WHERE category_id IN (SELECT id FROM categories WHERE active = true)
-- Or: SELECT * FROM products p WHERE EXISTS (SELECT 1 FROM categories c WHERE c.id = p.category_id AND c.active = true)
```

#### 5. Calculate Impact

For each unused or filter-only JOIN:

**Query complexity impact:**
- **INNER JOIN on indexed column:** +10-30ms typical overhead
- **LEFT JOIN on indexed column:** +15-40ms typical overhead  
- **JOIN without index:** +50-500ms (depends on table size)
- **Multiple unnecessary JOINs:** Multiplicative impact

**Memory impact:**
- Join buffers: Estimated based on table sizes (if available from migrations/schema)
- Temporary tables: For complex joins without proper indexes

**Severity classification:**
- **Critical:** 
  - INNER JOIN that excludes most results + filter could use subquery instead
  - Multiple (3+) unused JOINs
  - JOIN on non-indexed foreign key with table > 10,000 rows
  
- **High:**
  - Single unused JOIN on large table (> 10,000 rows)
  - Filter-only JOIN that could use subquery/EXISTS
  - LEFT JOIN returning many null results (> 50% nulls)
  
- **Medium:**
  - Single unused JOIN on medium table (1,000-10,000 rows)
  - Eagerly loaded relationship never accessed in ORM
  
- **Low:**
  - Unused JOIN on small table (< 1,000 rows) with indexes

**Quantified impact estimation:**

```
Impact per request = (num_unused_joins * avg_join_overhead)

Example:
- 2 unused LEFT JOINs on indexed columns: 2 × 25ms = 50ms saved
- 1 unused INNER JOIN on non-indexed column: 1 × 200ms = 200ms saved

If endpoint called N times (from N+1 detection):
Total impact = impact_per_request × N
```

#### 6. Recommended Fixes

For each unused JOIN, suggest the appropriate fix:

**For completely unused JOINs:** Remove JOIN entirely
**For filter-only JOINs:** Replace with subquery or EXISTS clause
**For ORM eager loading:** Remove `.select_related()`, `.find_with_related()`, or `.join()` calls

#### 7. Report in Analysis Document

Add findings to the analysis report template under "Backend Database Anti-Patterns" section with: endpoint, handler location, query, unused join details, estimated impact, and recommended fix.

**Detection confidence levels:**
- **High confidence:** Raw SQL with clear unused table, or ORM with no field accesses found
- **Medium confidence:** Complex ORM query where field usage is ambiguous
- **Low confidence:** Dynamic queries where JOIN usage determined at runtime

**Note:** For low confidence detections, flag for manual review rather than auto-suggesting removal.

### Step 7.6.2 – Deep Service Chain Analysis

**Purpose:** Trace function calls from each handler into service methods, model builders, and utility functions to detect anti-patterns hidden below the handler layer. This step closes the gap between handler-level analysis (Steps 7.3-7.6.1) and the actual query execution depth.

**Apply:** [Common Pattern: Call Chain Analysis Strategy — Pattern 12](../performance/common-patterns.md#pattern-12-call-chain-analysis-strategy)

**Configurable depth:** `analysis_chain_depth` (default: 3). Read from `## Analysis Assumptions` section in `performance-config.md` if present; otherwise use default.

**For EACH handler analyzed in Steps 7.1-7.6:**

Initialize:
- `call_graph = []`
- `visited = {(handler_file, handler_name)}`
- `query_ledger = []` (carries forward any queries already found in Steps 7.3-7.6 for this handler)
- `depth = 0`

---

#### Step 7.6.2-A – Recursive Chain Tracing via Serena (`serena_mode = live`)

> Grep is not available in this path.

**A1. Extract call sites from handler body** (already retrieved in Step 7.1-A):

Parse body text to identify method/function calls. For each call expression, classify and resolve it:

| Call Pattern | Resolution Strategy |
|---|---|
| `self.method_name(...)` | `mcp__{serena_instance}__find_declaration(relative_path=handler_file, regex="self\\.(method_name)\\(", include_body=true)` |
| `service.method_name(...)` | Determine service type from handler params (e.g., `fetcher: web::Data<SbomService>`), then `mcp__{serena_instance}__find_symbol(name_path_pattern="SbomService/method_name", relative_path="modules/", include_body=true, max_matches=1)` |
| `Type::associated_fn(...)` | `mcp__{serena_instance}__find_symbol(name_path_pattern="Type/associated_fn", include_body=true, max_matches=1)` |
| Trait method call | `mcp__{serena_instance}__find_implementations(name_path="TraitName/method", relative_path=file, include_info=true)`, then `find_symbol` on concrete implementation with `include_body=true` |

If `find_symbol` returns no results, retry once with `substring_matching=true`. If still empty, record "Unresolved call: {expression}" and skip this branch.

**A2. For each resolved callee:**

1. **Check cycle:** if `(callee_file, callee_name) in visited` → record edge with "⟳ Circular" annotation, skip
2. **Check depth:** if `depth >= analysis_chain_depth` → record edge with "⋯ Depth limit" annotation, skip
3. Add `(callee_file, callee_name)` to `visited`
4. Record edge in `call_graph`: `{caller: handler_name, callee: callee_name, file: callee_file, depth: depth+1}`
5. Read callee body (already retrieved via `find_symbol` with `include_body=true`)
6. **Apply anti-pattern checks** at this depth:
   - N+1 patterns (same detection logic as Step 7.3)
   - Unused JOINs (same logic as Step 7.6.1)
   - SELECT * patterns (same logic as Step 7.6)
   - Missing caching (same logic as Step 7.5)
7. **Detect conditional query parameters (Memo/Option pattern):**
   - Scan the callee's function signature for parameters of type `Memo<T>`, `Option<T>`, or
     equivalent lazy-load wrappers
   - If found, scan the callee's body for branching patterns where one branch triggers a query
     and the other uses the pre-provided value
   - Check what the CALLER passes for this parameter:
     - If `Memo::NotProvided` / `None` / lazy variant → the conditional query WILL fire
     - If `Memo::Provided(value)` / `Some(value)` → the conditional query is SKIPPED
   - When a conditional query is detected and the caller triggers it:
     - Add to `query_ledger` with `conditional: true` and `trigger` annotation
     - **Extend depth by 1 for this branch:** If the conditional query is at
       `depth == analysis_chain_depth`, extend by 1 level to trace the query itself.
       This ensures that conditional queries at the depth boundary are not silently truncated.
       (Maximum extension: 1 level beyond configured depth.)
8. For each query found, add to `query_ledger`:
   ```
   {description, depth: depth+1, loop_multiplier, source_file, source_symbol, query_type, conditional: false, trigger: null}
   ```
9. Extract call sites from this callee's body → recurse back to A1 with `depth + 1`

**A3. Model builder heuristic:**

When a call matches `Type::from_entity(...)`, `Type::from_row(...)`, `Type::from_model(...)`, or `Type::new(...)`:
- These commonly contain hidden queries in Rust/Java/Python ORMs
- Always trace into them regardless of call priority
- Flag any query found inside a `from_entity` method with annotation: "Model construction query — fires once per entity instantiation"

**A4. Trait dispatch resolution:**

When a callee is a trait method (detected by `impl TraitName for Type` in surrounding context):
- Use `mcp__{serena_instance}__find_implementations(name_path="TraitName/method_name", relative_path=file)` to find all concrete implementations
- Trace into the concrete implementation matching the handler's type parameter or the most likely runtime type

---

#### Step 7.6.2-B – Recursive Chain Tracing via Grep (`serena_mode = down | not-configured`)

**B1. Extract call sites from handler body** (already retrieved via Read in Step 7.1-B):

Same text parsing as A1, but resolution uses Grep and Read:

| Call Pattern | Resolution Strategy |
|---|---|
| `self.method_name(...)` | Grep for `fn method_name` in the handler's module directory |
| `service.method_name(...)` | Determine service type from params; `grep -rn "impl ServiceType" modules/`; find method in matching file |
| `Type::associated_fn(...)` | `grep -rn "impl Type" modules/`; find `fn associated_fn` in matching file |
| Trait method call | `grep -rn "impl TraitName for" modules/`; find concrete implementation |

**B2. For each located callee:**

1. Read file with Read tool (use line offset/limit from grep result)
2. Apply same cycle detection, depth check, anti-pattern detection, and recursion as A2
3. Set `confidence = "medium"` for depth-0 findings, `"low"` for depth > 0

**B2a. Conditional query detection (Memo/Option) in Grep path:**

Conditional query detection (sub-step 7 from A2) is **Serena-only** for full caller argument
analysis. In the Grep path, determining what each caller passes for a `Memo<T>`/`Option<T>`
parameter requires `find_referencing_symbols` — this cannot be reliably done with Grep across files.

**If a function with `Memo<T>` / `Option<T>` parameters is encountered in the Grep path:**
- Log: "Conditional query parameter detected in `{function_name}` — Serena MCP required for
  caller argument analysis. Flagging as potential conditional query (confidence: low)."
- Add to query_ledger with `conditional: true, trigger: "Unknown — Grep cannot resolve caller arguments"`
- Set confidence to **low** for this finding

**B3. Grep limitations at depth:**

Document in report: "Grep-based chain tracing may miss calls through trait objects, closures, or dynamic dispatch. Serena MCP provides more accurate cross-file tracing. Conditional query detection (Memo/Option pattern) requires Serena for caller argument analysis."

---

#### Step 7.6.2-C – Build Call Graph Summary

After recursion completes for each handler, produce two outputs:

**Call Graph (text format, for report):**
```
GET /v3/sbom/{id}/advisory
  └─ SbomService::fetch_sbom_details          [service/sbom.rs:88]
       ├─ SbomService::fetch_sbom              [service/sbom.rs:71]    ← 1 query
       └─ SbomDetails::from_entity             [model/details.rs:76]
            ├─ SbomSummary::from_entity         [model/mod.rs:93]
            │    ├─ describes_packages           [service/sbom.rs:493]  ← 1 query (N+1 if in loop)
            │    └─ SbomHead::from_entity       [model/mod.rs:55]      ← 1 query (COUNT)
            └─ [advisory join query]            [model/details.rs:88]  ← 1 query (multi-JOIN)
```

**Query Ledger (table format, for report):**

| # | Query | Source | Depth | Loop Mult. | Cond? | Effective Count |
|---|---|---|---|---|---|---|
| 1 | {description} | {file:line} | {depth} | {multiplier} | | {effective} |
| **Total** | | | | | | **{total_queries}** |

**†** Conditional query — fires only when caller passes `Memo::NotProvided` / `None`.
See Conditional Query Patterns section for caller analysis. Mark with `†` in the `Cond?` column.

**Multiplier propagation:** For each query in the ledger, walk the `call_graph` from handler root to the query's source symbol. If any edge on the path is inside a loop, multiply the query count by the loop's iteration count. The effective count for a query is:
```
effective_count = product(loop_multipliers on path from root to query)
```

**Estimated total DB latency:** `total_queries * analysis_db_latency_ms` (using configured DB Query Base Latency)

---

### Step 7.6.3 – Wasted Computation Detection

**Purpose:** Detect when a handler calls a service method that computes/fetches substantial data but the handler only uses a subset of the result. This catches cases like `fetch_sbom_details()` returning full SBOM data while the handler only serializes `.advisories`.

**Detection approach:**

**For each handler analyzed in Step 7.1:**

1. **Identify the service call return value and its usage:**
   - From the handler body, extract the variable receiving the service result (e.g., `let result = service.fetch_sbom_details(...)`)
   - Identify which fields of the result the handler actually accesses (e.g., `result.advisories`, `v.advisories`)
   - Look for patterns: `result.field_name`, `v.field`, direct field access after `match` or `if let`

2. **Determine the service method's full return type:**
   - From the call chain analysis (Step 7.6.2), the callee's return type is visible in its signature
   - Use `find_symbol` on the return type struct to enumerate all its fields (with `include_body=true`)

3. **Compare handler field access vs. full struct fields:**
   - Count total fields in the return type struct
   - Count fields accessed by the handler
   - Calculate usage ratio: `used_fields / total_fields`

4. **Cross-reference with query_ledger for wasted query cost:**
   - For each unused field in the return type, check if populating that field requires queries (visible in the call graph from Step 7.6.2)
   - Sum the query costs attributable to unused fields

5. **Flag wasted computation:**

**Severity classification:**
- **High:** Handler uses < 50% of returned fields AND unused portion involves queries from the call graph (quantified as `wasted_query_count * analysis_db_latency_ms`)
- **Medium:** Handler uses < 50% of returned fields but unused portion is CPU-only (serialization, transformation)
- **Low:** Handler uses 50-75% of returned fields, or unused portion is trivial

**Report format per finding:**
```
Handler: {handler_name} ({file}:{line})
Calls: {service_method} → returns {ReturnType} ({total_fields} fields)
Uses: Only {used_field_list} ({used_count} fields)
Wasted: {unused_field_list} ({unused_count} fields, {usage_pct}% used)
Wasted Queries: {count} queries ({wasted_latency}ms estimated)
Recommendation: Create {optimized_method_name}() that returns only needed data
```

---

### Step 7.6.4 – Missing Index Detection

**Purpose:** Cross-reference query WHERE/JOIN columns (found at any depth in the call chain from Step 7.6.2) against migration files to detect missing database indexes.

**Detection approach:**

**For each query in `query_ledger` (from Step 7.6.2):**

#### 1. Extract filterable columns

From the query text or ORM call, extract columns used in:
- **WHERE clauses:** equality (`=`), range (`<`, `>`), IN, LIKE, BETWEEN filters
- **JOIN ON clauses:** columns in join conditions
- **ORDER BY:** columns used for sorting on large result sets
- **ORM filter methods:** `.filter(Column::Name.eq(...))`, `.filter(Column::Name.is_in(...))`, etc.

#### 2. Build index registry from migration files

Search the `migration/` directory (or framework-specific migration path) for index definitions:

```bash
# Rust (SeaORM) migrations
grep -rn "create_index\|CreateIndex\|add_index" migration/src/ --include="*.rs"

# Raw SQL indexes
grep -rn "CREATE INDEX\|CREATE UNIQUE INDEX" migration/src/ --include="*.rs" --include="*.sql"

# Also check for primary keys and unique constraints
grep -rn "primary_key\|unique_index\|UniqueIndex" migration/src/ --include="*.rs"
```

Parse index definitions to build an index registry:
```
{table_name: [indexed_column_set_1, indexed_column_set_2, ...]}
```

Include primary keys and unique constraints as "indexed."

#### 3. Check index coverage

For each WHERE/JOIN column extracted in sub-step 1:
- Look up the column's table in the index registry
- If no index covers the column (either as a single-column index or as the leading prefix of a composite index), flag it

#### 4. Report missing indexes

For each missing index:
```
Missing Index: {table_name}.{column_name}
Used In: {query_description} ({source_file}:{line})
Query Type: WHERE filter / JOIN condition / ORDER BY
Loop Multiplier: {from query_ledger — how many times this query fires per request}
Estimated Impact: Sequential scan on {estimated_rows} rows vs. index lookup
Recommended Fix: CREATE INDEX idx_{table}_{column} ON {table}({column});
```

**Severity classification:**
- **High:** Missing index on JOIN column or WHERE equality filter, query is in a loop (multiplier > 1 from query_ledger)
- **Medium:** Missing index on WHERE range filter or single-execution query on large table
- **Low:** Missing index on ORDER BY, or small table (< 1,000 estimated rows)

**Note:** If migration files are not found at the expected location, document: "Migration files not found at {searched_path}. Index analysis skipped." and continue with remaining steps.

### Step 7.6.5 – Inter-Query Duplication Detection

**Purpose:** Detect when multiple queries within the same handler's call chain contain overlapping
SQL logic (shared CTEs, repeated subqueries, or identical JOIN structures), causing the database
to compute the same intermediate results multiple times per request.

**Detection approach:**

**For each handler's `query_ledger` (from Step 7.6.2):**

#### 1. Collect raw SQL text for all queries

For each entry in the query_ledger:
- If the query is a raw SQL string (e.g., from `Statement::from_sql_and_values` or `Expr::cust`),
  extract the full SQL text
- If the query is an ORM query builder chain, extract the generated SQL (from body analysis) or
  reconstruct the logical query from the builder calls (table names, JOIN clauses, WHERE filters)
- If the query includes inline SQL fragments (e.g., `Expr::cust_with_values(SOME_CONSTANT, ...)`),
  resolve the constant to its SQL text

#### 2. Extract CTE and subquery names

Parse each SQL string for:
- **WITH clauses:** Extract CTE names (e.g., `WITH related_nodes AS (...)`)
- **Subquery aliases:** Extract aliased subqueries in FROM clauses
- **Inline subqueries:** Extract subqueries in WHERE/JOIN conditions (e.g., `IN (SELECT ...)`)
- **SQL constant references:** Resolve Rust/Java/Python constants that hold SQL fragments
  (e.g., `CONTEXT_CPE_FILTER_SQL`) to their string values

Build a map: `{cte_or_subquery_name: [query_ledger_entry_indices]}`

#### 3. Detect overlapping logic

For each CTE or subquery name that appears in 2+ queries within the same handler chain:
- Compare the SQL body of the CTE/subquery across the occurrences
- If the SQL bodies are identical or semantically equivalent (same tables, same JOINs,
  same filters with same parameters):
  - Flag as **duplicated computation**
  - Estimate the overhead: `(occurrence_count - 1) × analysis_db_latency_ms`
    (Use `analysis_db_latency_ms` from Analysis Assumptions as the per-execution estimate
    when CTE cost cannot be directly measured.)

For queries without named CTEs, compare:
- JOIN structures (same tables joined in same order with same conditions)
- WHERE clause patterns (same filter columns and operators)
- Flag as **partially overlapping** if > 50% of JOIN/WHERE logic is shared

#### 4. Report duplicated computations

For each duplicated CTE/subquery:

```
Duplicated SQL Logic: {cte_name} (appears in {count} queries within same handler)
Queries:
  - Query #{ledger_idx_1}: {description_1} ({source_file_1}:{line_1})
  - Query #{ledger_idx_2}: {description_2} ({source_file_2}:{line_2})
SQL Body (shared):
  {sql_fragment}
Estimated Overhead: {(count-1)} redundant executions per request
Recommendation: Extract shared CTE into a materialized subquery or temporary table,
  or refactor to execute the shared logic once and pass results to both consumers
```

**Severity classification:**
- **High:** Same CTE executed 3+ times per request, or duplicated logic involves table scans
  on large tables (> 10,000 rows estimated from migration files or schema)
- **Medium:** Same CTE executed 2 times per request, or table size cannot be estimated
  statically (default to Medium when row count is unknown)
- **Low:** Partially overlapping logic (> 50% shared) across 2 queries

**Confidence Level:** High for exact CTE name matches; Medium for semantic equivalence
detection.

**Note:** This step analyzes queries within a single handler's call chain. Cross-handler
duplication (e.g., two different endpoints sharing CTEs) is out of scope — it would be caught
if both handlers are analyzed for the same workflow.

## Step 7.7 – Backend Dynamic Performance Testing

**Purpose:** Validate static analysis findings with actual HTTP benchmarking when the backend is running.

**Execution:** This step runs **automatically** when prerequisites are met. If any prerequisite is missing, it skips gracefully and continues with static analysis only.

**Prerequisites:**
- Backend service running on configured port
- Test data manifest exists (generated by performance-baseline)
- `curl` available (used for curl-loop percentile measurement)

This step complements static analysis (Steps 7.1-7.6) with real runtime measurements.

**Apply:** [Pattern 10: API Profiling](../performance/common-patterns.md#pattern-10-api-profiling)

**Specific actions for this skill:**

Wrap Pattern 10 in a shell function for this module's endpoints only:

```bash
function run_module_profiling() {
  export CALLER_SKILL="performance-analyze-module"
  
  # Pattern 10 Step A - Check Prerequisites and Install benchmark tool
  # (Full code from common-patterns.md)
  
  # Pattern 10 Step B - Execute Benchmark with Cache Measurement
  # (Full code from common-patterns.md)
  
  # Results are now available in dynamic_results associative array
}

run_module_profiling

# If profiling was skipped, continue with static-only analysis
if [ "$skip_dynamic" = "true" ]; then
  echo "ℹ️ Module analysis will include static findings only."
fi
```

**Using the results in report generation:**

After Pattern 10 completes, the `dynamic_results` associative array contains benchmarking data for each endpoint.

**Regression Detection (if metric_type = "backend" or "hybrid"):**

Compare current metrics against baseline from `benchmark-results.json` (if it exists).

Extract metrics and compare against baseline:

```bash
# Load baseline metrics if available
baseline_file=".claude/performance/baselines/benchmark-results.json"
if [ -f "$baseline_file" ]; then
  has_baseline=true
else
  has_baseline=false
fi

# Example: Include dynamic metrics with regression detection in module analysis report
for scenario in "${!dynamic_results[@]}"; do
  result_json="${dynamic_results[$scenario]}"
  
  # Current metrics
  p50=$(echo "$result_json" | jq -r '.p50_ms')
  p95=$(echo "$result_json" | jq -r '.p95_ms')
  p99=$(echo "$result_json" | jq -r '.p99_ms')
  mean=$(echo "$result_json" | jq -r '.mean_ms')
  cache_status=$(echo "$result_json" | jq -r '.cache_status')
  cache_pct=$(echo "$result_json" | jq -r '.cache_improvement_pct')
  
  # Baseline comparison (if available)
  if [ "$has_baseline" = "true" ]; then
    baseline_p95=$(jq -r ".\"$scenario\".p95_ms // null" "$baseline_file")
    baseline_p99=$(jq -r ".\"$scenario\".p99_ms // null" "$baseline_file")
    baseline_throughput=$(jq -r ".\"$scenario\".throughput_rps // null" "$baseline_file")
    baseline_error_rate=$(jq -r ".\"$scenario\".error_rate_pct // null" "$baseline_file")
    
    if [ "$baseline_p95" != "null" ]; then
      # Calculate regression
      p95_delta=$(echo "$p95 - $baseline_p95" | bc)
      p95_delta_pct=$(echo "scale=1; ($p95_delta / $baseline_p95) * 100" | bc)
      
      # Regression thresholds for backend:
      # - p95 response time: > 50ms AND > 10% = regression
      # - Throughput: < -20% = regression
      # - Error rate: > +1% (absolute) = regression
      
      if (( $(echo "$p95_delta > 50" | bc -l) )) && (( $(echo "$p95_delta_pct > 10" | bc -l) )); then
        echo "⚠️  PERFORMANCE REGRESSION DETECTED: $scenario"
        echo "  p95 response time increased by ${p95_delta}ms (${p95_delta_pct}%)"
        echo "  Baseline: ${baseline_p95}ms → Current: ${p95}ms"
      fi
    fi
  fi
  
  # Add to report:
  # - Dynamic Performance Testing section with current metrics
  # - Regression detection results (if baseline exists)
  # - Cache Effectiveness analysis
  # - Comparison with static estimates
  
  echo "Endpoint: $scenario"
  echo "  p50: ${p50}ms, p95: ${p95}ms, p99: ${p99}ms"
  echo "  Cache: $cache_status (${cache_pct}% improvement)"
  
  if [ "$has_baseline" = "true" ] && [ "$baseline_p95" != "null" ]; then
    echo "  Baseline p95: ${baseline_p95}ms (delta: ${p95_delta}ms, ${p95_delta_pct}%)"
  fi
done
```

### Step 7.7.3 – Document Results for Report Generation

Dynamic results are already stored in the associative array and saved to `dynamic-results.sh`.

Report generation (Step 9.2) will source this file and create the Dynamic Performance Testing section.

**Note:** Static analysis Step 7 produces unstructured markdown narrative (e.g., "Estimated Overhead: 100ms per query"). Automated parsing is not reliable. The report will include a comparison table populated from the dynamic_results array, with manual instructions for comparing against static estimates.

## Step 8 – Cross-Reference Over-Fetching (ENHANCED with Backend Schema)

**CRITICAL:** Perform for ALL endpoints identified in Step 6.1, especially those with N+1 patterns.

**This step is ENHANCED when backend is available.** If backend_available = false, use original Step 6.1 detection (frontend-only field usage analysis).

For each endpoint:

**Step A – Extract Backend Response Fields** (if backend_available)
- Use response schema from Step 7.2 (which MUST have been extracted - do not skip)
- List ALL fields including nested objects
- Document field types and estimated sizes
- If Step 7.2 schema extraction was incomplete, STOP and go back to complete it before proceeding

**Step B – Analyze Frontend Field Usage**
- Use Grep to search for property accesses across ALL frontend code:
  ```bash
  grep -r "response\.field_name" {{frontend-path}}/src/
  grep -r "data\.field_name" {{frontend-path}}/src/
  grep -r "\.field_name" {{frontend-path}}/src/  # Broad search
  ```
- Check code locations:
  - Component render functions
  - useEffect hooks
  - useMemo/useCallback
  - Event handlers
  - State updates
- Mark each field as USED or UNUSED

**Step C – Calculate Over-Fetching Waste**
1. **Field-level waste:**
   - Total backend fields vs. used frontend fields
   - Waste %: `(unused_fields / total_fields) * 100`

2. **If N+1 pattern detected (from Step 6.1 or 7.3):**
   - Multiply waste by call count
   - Example: If endpoint called 10 times with 80% over-fetching → 10x the impact

3. **Payload-level waste:**
   - Get uncompressed response size from baseline data
   - Calculate waste bytes: `(unused_fields / total_fields) * total_response_size`
   - If N+1: multiply by call count

**Step D – Updated Severity Classification**
- **Critical:** N+1 pattern (10+ calls) with > 50% over-fetching
- **High:** Single call with > 50% unused fields, OR N+1 (5-10 calls) with > 30% unused
- **Medium:** 25-50% unused fields
- **Low:** < 25% unused fields

**Step E – Quantified Impact**
- Payload reduction: `(unused_fields / total_fields) * response_size * call_count`
- Latency improvement: `payload_reduction / (analysis_bandwidth_mbps * 125000)` (using configured bandwidth)

**Example Output:**
```
Endpoint: GET /api/v2/products/:id
Backend Response: 12 fields (ProductResponse)
Frontend Usage: 4 fields used (id, name, price, image_url)
Unused Fields: 8 (description, inventory.*, created_at, updated_at, internal_notes, ...)
Over-Fetching: 67% (8/12 fields unused)
Call Pattern: Single call (no N+1)
Payload Waste: 3.5 KB unused per call
Recommendation: Create ProductSummaryResponse with only used fields, or use GraphQL
```

**Step F – Cross-Layer Computation Waste Detection**

**Purpose:** Detect when the backend computes expensive fields (requiring DB queries) that the
frontend never uses. This extends Step 7.6.3 (handler-level waste) to the full frontend→backend
layer boundary.

**Prerequisites:** Step 7.6.2 query_ledger AND Step 8B frontend field usage results.

**Guard conditions — skip Step 8.F if ANY of the following are true:**
- `backend_available = false` (no backend to analyze)
- `analysis_scope` is `"backend-only"` or `"frontend-only"` (cross-layer analysis requires both)
- The endpoint has no `query_ledger` from Step 7.6.2 (chain analysis was skipped or failed)

**If skipped:** Log "Step 8.F skipped — requires full-stack analysis scope with completed
chain analysis." and continue to Step 9.

**Detection approach:**

For each endpoint analyzed:

1. **Map response fields to their computation cost:**
   - From the call graph (Step 7.6.2), identify which queries populate which response fields
   - For each field in the response type, determine:
     - Whether populating it requires database queries (and which ones from the query_ledger)
     - The estimated cost: sum of `effective_count × analysis_db_latency_ms` for queries
       attributable to this field

   **Heuristic for field→query mapping:**
   - If a field is populated by a `from_entity` / `from_model` call that contains queries,
     those queries are attributable to that field
   - If a response struct field is populated by a service method call that returns a sub-struct,
     all queries in that service method's sub-tree are attributable to that field
   - Example: `SbomSummary.described_by` is populated by `describes_packages()` which runs 1 query
     → that query is attributable to the `described_by` field

2. **Cross-reference with frontend field usage (from Step 8B):**
   - For each response field marked as UNUSED by the frontend:
     - Look up its computation cost from sub-step 1
     - If computation cost > 0 (field requires queries), flag as **cross-layer waste**

3. **Calculate total cross-layer waste:**
   - Sum the query costs for all frontend-unused fields that require backend queries
   - Multiply by call count if N+1 pattern exists for this endpoint
   - Compare against total endpoint query cost to get waste percentage

**Severity classification:**
- **Critical:** Frontend-unused fields account for > 50% of the endpoint's total query cost
  AND endpoint is called in N+1 pattern (waste multiplied by N)
- **High:** Frontend-unused fields account for > 50% of total query cost (single call)
- **Medium:** Frontend-unused fields account for 25-50% of total query cost
- **Low:** Frontend-unused fields account for < 25% of total query cost

**Report format per finding:**
```
Endpoint: {method} {path}
Total Backend Query Cost: {total_queries} queries ({total_latency}ms)
Frontend-Used Fields: {used_field_list} — Cost: {used_queries} queries ({used_latency}ms)
Frontend-Unused Fields: {unused_field_list} — Cost: {wasted_queries} queries ({wasted_latency}ms)
Cross-Layer Waste: {waste_pct}% of backend computation serves no frontend purpose
Call Pattern: {single / N+1 with count}
Total Wasted Queries: {wasted_queries × call_count}
Recommendation: {Create targeted endpoint / Add field projection / Use GraphQL}
```

**Example:**
```
Endpoint: GET /v3/advisory
Total Backend Query Cost: 53 queries (530ms) for 10 advisories
Frontend-Used Fields: head.uuid, head.document_id, head.ingested, total — Cost: 3 queries (30ms)
Frontend-Unused Fields: vulnerabilities[] (with scores, descriptions) — Cost: 50 queries (500ms)
Cross-Layer Waste: 94% of backend computation serves no frontend purpose
Call Pattern: Single call
Total Wasted Queries: 50
Recommendation: Create lightweight /v3/advisory/summary endpoint returning only
  {uuid, document_id, ingested} with count, skipping vulnerability loading entirely
```

## Step 9 – Generate Workflow Analysis Report

Create a comprehensive analysis report at `{analysis-directory}/workflow-analysis-report.md`.

### Step 9.1 – Determine Analysis Report Location

Read the **Target Directories** section from performance-config.md and extract the analysis directory path (e.g., `.claude/performance/analysis/`).

Construct the report filename: `workflow-analysis-report.md`

### Step 9.2 – Report Structure

The report must include sections appropriate to the metric_type:

Read the analysis report template from `plugins/sdlc-workflow/skills/performance/performance-analysis-report.template.md` in the plugin cache and populate it with the collected data from Steps 2-8.

**If metric_type = "frontend" or "hybrid":**

Include sections:
- Frontend Performance Summary (LCP, FCP, DOM Interactive, Total Load Time from baseline)
- Frontend anti-patterns (blocking resources, long tasks, layout thrashing, etc.)
- Bundle analysis and third-party libraries

**If metric_type = "backend" or "hybrid":**

Include sections:
- Backend Performance Summary (Response Time p50/p95/p99, Throughput, Error Rate from benchmark-results.json)
- Backend anti-patterns (N+1 queries, missing pagination, missing caching, over-fetching, unused JOINs)
- Service chain analysis with call graphs and query ledgers (from Step 7.6.2)
- Wasted computation findings (from Step 7.6.3)
- Conditional query pattern findings (from Step 7.6.2 extended — Memo/Option detection)
- Inter-query SQL duplication findings (from Step 7.6.5)
- Missing database index findings (from Step 7.6.4)
- Cross-layer computation waste findings (from Step 8.F, only when analysis_scope is full-stack)
- Dynamic performance testing results (if Step 7.7 executed)
- Regression detection results (if baseline exists)

**If metric_type = "hybrid":**

Include BOTH frontend and backend sections above.

### Step 9.3 – Calculate Overall Performance Rating

Based on the workflow metrics and metric_type, assign an overall rating:

**If metric_type = "frontend" or "hybrid":**

Compare frontend metrics against targets from Optimization Targets table:
- **Excellent:** All metrics within targets (LCP < target, FCP < target, DOM Interactive < target, Total < target)
- **Good:** 1-2 metrics slightly above targets (within 20% over)
- **Needs Improvement:** 2-3 metrics above targets (> 20% over)
- **Poor:** All metrics above targets or any metric > 50% over target

**If metric_type = "backend" or "hybrid":**

Compare backend metrics against targets from Optimization Targets table:
- **Excellent:** All metrics within targets (Response Time p95 < target, Throughput > target, Error Rate < target)
- **Good:** 1-2 metrics slightly outside targets (within 20%)
- **Needs Improvement:** 2-3 metrics outside targets (> 20%)
- **Poor:** All metrics outside targets or any metric > 50% deviation from target

**If metric_type = "hybrid":**

Calculate separate ratings for frontend and backend, then combine:
- Overall = worst of (frontend_rating, backend_rating)

### Step 9.4 – Prioritize Optimizations

Sort all detected anti-patterns by estimated impact (time or size savings) descending.

**Impact estimation using query ledger data:** When the deep service chain analysis (Step 7.6.2) has produced a query ledger, use the total estimated queries per endpoint as the primary impact metric for backend optimizations. An endpoint with 73 total queries (accounting for loop multipliers) should rank higher than one with 3 surface-level N+1 instances.

Assign effort estimates based on:
- **Low effort:** Configuration changes, adding `async`/`defer` attributes, removing unused imports, adding indexes
- **Medium effort:** Refactoring API calls, adding memoization, implementing lazy loading, batching N+1 queries
- **High effort:** Bundle splitting, architecture changes, replacing third-party libraries, creating new service methods

Generate the prioritized optimization table with the top 10 recommendations.

### Step 9.5 – Write Report to File

Write the generated report to `{analysis-directory}/workflow-analysis-report.md`.

## Step 10 – Output Summary

Report to the user:

> ✅ **Performance analysis complete!**
>
> **Workflow:** {workflow name}  
> **Overall Rating:** {rating}  
> **Report location:** `.claude/performance/analysis/workflow-analysis-report.md`
>
> **Key Findings:**
> - {finding-1}
> - {finding-2}
> - {finding-3}
>
> **Top Optimization:** {top-optimization} — Estimated impact: {impact}
>
> {dynamic-testing-summary-if-executed}
>
> {warnings-if-any}
>
> **Next Steps:**
>
> 1. Review the full analysis report
> 2. Prioritize optimizations with your team
> 3. Run `/sdlc-workflow:performance-plan-optimization` to create Jira Epic and tasks from this report
> 4. After implementing optimizations, re-baseline to measure improvements

Where `{dynamic-testing-summary-if-executed}` includes (if Step 7.7 was executed):

> **Dynamic Testing Results:**
> - Endpoints tested: {count}
> - Effective caching: {count} endpoints
> - Slow endpoints (>500ms): {count} endpoints

Where `{warnings-if-any}` includes warnings for critical issues:

- If overall rating is "Poor": "⚠️ Performance is significantly below targets. Recommend prioritizing optimization work."
- If any anti-pattern has > 10 instances: "⚠️ {anti-pattern-name}: {count} instances detected. Consider systemic refactoring."

## Important Rules

- Never modify source code files — only create performance analysis artifacts
- Always verify selected workflow and baseline exist before proceeding
- All anti-pattern detection must be based on actual code search results — do not fabricate findings
- Quantified impact estimates should be conservative — use documented performance metrics and reasonable assumptions
- If bundle stats are unavailable, clearly note estimations in the report
- Scope all analysis to the selected workflow only — do not analyze code outside the workflow's route components
- If an anti-pattern detection step finds zero instances, include it in the report with "No instances detected" rather than omitting it
- Use Serena instance from Code Intelligence configuration (with Grep/Glob fallback if not available)
- Generate report even if some anti-pattern detection steps fail — document failed steps in the report
- Save report to directory specified in performance-config.md, never to the repository root
- **Backend schema extraction is mandatory when backend_available = true:** Always search for struct/class definitions and extract all fields. Do not write "Cannot confirm without schema" without documenting exhaustive search attempts and specific failures
- **Unused table join detection (Step 7.6.1) is required for backend analysis:** When analyzing backend queries, always check for JOIN operations and verify that fields from joined tables are actually used in SELECT clauses, WHERE conditions, handler logic, or response schemas. Flag joins where no fields are accessed as optimization opportunities
- **Backend-only mode analysis:** When `analysis_scope = "backend-only"`, skip all frontend anti-pattern detection steps (Steps 5-6) and focus exclusively on backend analysis (Step 7). No browser metrics will be available in backend-only mode
