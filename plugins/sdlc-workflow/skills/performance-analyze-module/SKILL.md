---
name: performance-analyze-module
description: |
  Inspect source code to detect performance anti-patterns by examining bundle composition, API call patterns, component structure, and resource loading.
argument-hint: "[target-repository-path]"
---

# performance-analyze-module skill

You are an AI performance analysis assistant. You **inspect source code** to detect performance anti-patterns in a user-selected workflow. You examine bundle composition, API call patterns, component render logic, and resource loading to identify common performance issues including over-fetching, N+1 queries, waterfall loading, render-blocking resources, unused code, and expensive re-renders.

**Key Distinction:** This skill performs source code analysis to identify performance issues. The `performance-plan-optimization` skill reads this analysis report and creates Jira tasks — it does not inspect code.

## Guardrails

- This skill creates files in designated performance directories (`.claude/performance/analysis/`)
- This skill does NOT modify source code files — only creates performance analysis artifacts
- This skill requires Performance Analysis Configuration with a selected workflow and an existing baseline report

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Verify Performance Configuration and Selected Workflow

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Verify config exists, stop if missing
- Read configuration for workflow and backend settings

### Step 2.1 – Check for Selected Workflow

**Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-7-workflow-validation)

**Specific actions for this skill:**
- Extract workflow name, entry point, key screens for scope analysis
- Store for module discovery and anti-pattern detection

### Step 2.2 – Read Backend Availability from Metadata (Updated)

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction)

**Specific field to extract:**
- `metadata.backend_available` → backend_available (cached status, no re-validation)

**If `backend_available = true`:**

Extract backend configuration from `## Backend Repository Configuration` section:
- Backend repo name
- Backend path
- Backend framework
- Serena instance name
- API base path

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
> **To enable full-stack analysis**, run:
> ```
> /sdlc-workflow:performance-setup --refresh-backend
> ```

Store backend configuration and `backend_available` flag for use in Step 6.10.

**Note:** Backend availability is cached in config metadata and validated during setup. This avoids redundant path checks and provides clear feedback about analysis limitations.

## Step 3 – Verify Baseline Report Exists

Determine the baseline report location from the configuration file:

Look for the **Target Directories** section and extract the baseline directory path (e.g., `.claude/performance/baselines/`).

Construct the baseline report filename: `baseline-report.md`

Check if the file exists at `{baseline-directory}/baseline-report.md`.

- **If baseline does not exist:** Inform the user:
  > "Baseline report not found. Please run `/sdlc-workflow:performance-baseline` first to capture baseline metrics, then re-run this skill."
  
  Stop execution.

- **If baseline exists:** Proceed to Step 4.
  
  **Note:** Baseline can be captured in cold-start, e2e, or both modes. Analysis uses metrics from whichever mode was selected.

## Step 4 – Read Baseline Data

**Apply:** [Common Pattern: Baseline Report Reading](../performance/common-patterns.md#pattern-6-baseline-report-reading)

**Specific data to extract:**
- **Per-scenario metrics**: LCP, FCP, TTI, Total Load Time (p50, p95, p99)
- **Resource timing breakdown**: URLs, load duration, transfer size per resource
- **Aggregate metrics**: Overall performance across all scenarios
- **Capture mode**: For understanding measurement context

Store this data for anti-pattern detection in Steps 5 and 6.

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

## Step 6 – Detect Performance Anti-Patterns

For each anti-pattern, search the codebase for indicators and report findings with severity classification and quantified impact.

### Step 6.1 – Over-Fetching Detection

**Definition:** API responses include fields that are never used in the UI.

**Detection approach:**

1. **Identify API calls in workflow components:**
   - Use Grep to search for `fetch(`, `axios.get(`, `useQuery(` in workflow route components
   - Extract API endpoint URLs from the search results
   - For each endpoint, identify the response schema (check TypeScript interfaces, OpenAPI specs, or sample responses in baseline data)

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
- Estimated time savings: `estimated_size_savings / average_bandwidth` (assume 5 Mbps average)

### Step 6.2 – N+1 Query Detection

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
- Estimated time savings: `(n_iterations - 1) * average_api_latency` (assume 100ms average latency)

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
- Estimated load time improvement: `size_savings / average_bandwidth`

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

3. **Cross-reference with TTI metric:**
   - If TTI is high (> 3500ms), expensive re-renders are more likely to be impactful
   - Prioritize components in the critical render path (those rendered before LCP element)

**Severity classification:**
- **High:** Components in critical path without memoization, and TTI > 3500ms
- **Medium:** Components in critical path without memoization, and TTI 2500-3500ms
- **Low:** Non-critical components without memoization, or TTI < 2500ms

**Quantified impact:**
- Estimated TTI improvement: Hard to quantify without runtime profiling, report as "Potential improvement: 10-30% reduction in TTI"

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
- Estimated TTI improvement: `sum_of_long_task_durations - 50ms` (assume tasks can be chunked to 50ms each)

### Step 6.8 – Layout Thrashing Detection

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
- Estimated rendering time improvement: `(n_iterations - 1) * 5ms` (assume 5ms per forced reflow)

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
- Estimated FCP improvement: `size_reduction / average_bandwidth`

### Step 6.10 – Backend Source Code Analysis (if backend_available)

**CRITICAL:** This step is MANDATORY for comprehensive over-fetching detection when backend is configured.

**Check cached backend availability from Step 2.2:**

- **If `backend_available = false`:** Skip this entire step (frontend-only mode, as indicated in Step 2.2 message)
- **If `backend_available = true`:** Proceed with backend analysis using configuration from Step 2.2

For EACH API endpoint identified in Step 6.1 (Over-Fetching Detection):

#### Step 6.10.1 – Locate Backend Handler

Find the backend handler function that serves this endpoint.

**If Serena available for backend:**
- Use `mcp__{{backend-serena}}__find_symbol` to search for route patterns
- Search patterns by framework:
  - **Rust (actix-web/axum):** `#[get("/api/v2/products")]`, `#[post("/api/v2/orders")]`
  - **Java (Spring Boot):** `@GetMapping("/api/v2/products")`, `@PostMapping("/api/v2/orders")`
  - **Python (FastAPI/Django):** `@app.get("/api/v2/products")`, `@router.post("/api/v2/orders")`
  - **Node (Express):** `app.get('/api/v2/products')`, `router.post('/api/v2/orders')`
- Extract handler function name and file location

**If Serena NOT available:**
- Fallback to Grep search across backend source:
  ```bash
  grep -r "GET.*\"/api/v2/products\"" {{backend-path}}/src/
  grep -r "@GetMapping.*products" {{backend-path}}/src/
  ```
- Parse results to identify handler file and approximate location

**If handler not found:**
- Document limitation: "Handler for endpoint {{url}} not found. Backend analysis skipped for this endpoint."
- Continue with next endpoint

#### Step 6.10.2 – Extract Backend Response Schema

Read the handler implementation to extract the complete response schema.

**If Serena available:**
- Use `mcp__{{backend-serena}}__find_symbol` with `include_body=true` to read handler function
- Identify response type from function signature:
  - **Rust:** `async fn handler() -> Json<ProductResponse>`
  - **Java:** `public ResponseEntity<ProductResponse> handler()`
  - **Python:** `def handler() -> ProductResponse:`
  - **Node:** Response object or TypeScript return type
- Use `mcp__{{backend-serena}}__find_symbol` to read the response struct/class definition
- Extract ALL fields recursively (including nested objects, arrays)

**If Serena NOT available:**
- Use Read tool to read handler file
- Parse response type manually from function signature
- Search for response type definition in backend codebase
- Extract fields (best-effort parsing)

**Document complete response schema:**
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

#### Step 6.10.3 – Detect Backend Database N+1 Queries

**Definition:** Handler executes queries in a loop instead of batch fetching.

**Detection approach:**

1. **Read handler implementation** (using Serena or Read tool)
   
2. **Search for query patterns inside loops:**
   - **Rust (sqlx):** 
     ```rust
     for item in items {
         query!("SELECT * FROM table WHERE id = ?", item.id)
             .fetch_one(&pool).await
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
   - Estimate from baseline data (e.g., if endpoint returns list of 10 items, loop runs 10 times)
   - Or use static analysis to count array length if determinable

4. **Verify sequential execution:**
   - Check if queries are awaited inside loop (synchronous execution)
   - vs. parallelized (Promise.all, async batch queries)

**Severity classification:**
- **High:** > 10 queries in loop, sequential execution
- **Medium:** 5-10 queries in loop, sequential execution
- **Low:** < 5 queries in loop, or parallelized execution

**Quantified impact:**
- Estimated latency impact: `(n_queries - 1) * avg_db_query_latency`
- Assume `avg_db_query_latency = 10ms` for calculation
- Example: 10 queries → `(10-1) * 10ms = 90ms` added latency

#### Step 6.10.4 – Detect Missing Pagination

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

#### Step 6.10.5 – Detect Missing Caching

**Definition:** Handler executes expensive operations on every request without caching.

**Detection approach:**

1. **Identify expensive operations:**
   - Database queries for static/slow-changing data (e.g., product categories, user roles)
   - External API calls (HTTP requests to third-party services)
   - Complex computations (aggregations, analytics)

2. **Check for cache usage:**
   - **Rust:** `Cache`, `moka`, `redis-rs`
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
- Estimated latency reduction: `operation_time * cache_hit_rate`
- Assume `cache_hit_rate = 0.8` (80% of requests served from cache)
- Example: 200ms query → `200ms * 0.8 = 160ms` saved per cached request

#### Step 6.10.6 – Detect Inefficient Queries

**Definition:** Queries that fetch unnecessary data (SELECT *, missing indexes).

**Detection approach:**

1. **Extract SQL queries from handler:**
   - Look for query builders or raw SQL strings
   - **Rust (sqlx):** `query!("SELECT ...")`, `query_as!(...)`
   - **Java (JPA):** `@Query("SELECT ...")`, `createQuery(...)`
   - **Python (SQLAlchemy):** `session.query(Model).filter(...)`
   - **Node (TypeORM):** `createQueryBuilder().select(...)`

2. **Check for SELECT *:**
   - Flag queries using `SELECT *` or ORM equivalents that fetch all columns
   - Example: `query!("SELECT * FROM products WHERE id = ?")`

3. **Identify which fields are actually used:**
   - Cross-reference queried fields with response schema (from Step 6.10.2)
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

### Step 6.11 – Cross-Reference Over-Fetching (ENHANCED with Backend Schema)

**CRITICAL:** Perform for ALL endpoints identified in Step 6.1, especially those with N+1 patterns.

**This step is ENHANCED when backend is available.** If backend_available = false, use original Step 6.1 detection (frontend-only field usage analysis).

For each endpoint:

**Step A – Extract Backend Response Fields** (if backend_available)
- Use response schema from Step 6.10.2
- List ALL fields including nested objects
- Document field types and estimated sizes

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

2. **If N+1 pattern detected (from Step 6.1 or 6.10.3):**
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
- Latency improvement: `payload_reduction / average_bandwidth`
- Assume `average_bandwidth = 1 MB/s` for 4G mobile

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

## Step 7 – Generate Workflow Analysis Report

Create a comprehensive analysis report at `{analysis-directory}/workflow-analysis-report.md`.

### Step 7.1 – Determine Analysis Report Location

Read the **Target Directories** section from performance-config.md and extract the analysis directory path (e.g., `.claude/performance/analysis/`).

Construct the report filename: `workflow-analysis-report.md`

### Step 7.2 – Report Structure

The report must include the following sections:

```markdown
# Performance Analysis Report

**Generated:** {iso-8601-timestamp}  
**Workflow:** {workflow-name}  
**Baseline Date:** {baseline-capture-date}

---

## Executive Summary

**Overall Performance Rating:** {rating} (Excellent / Good / Needs Improvement / Poor)

**Key Findings:**
- {summary-bullet-1}
- {summary-bullet-2}
- {summary-bullet-3}

**Top 3 Optimization Opportunities:**
1. {opportunity-1} — Estimated impact: {impact-1}
2. {opportunity-2} — Estimated impact: {impact-2}
3. {opportunity-3} — Estimated impact: {impact-3}

---

## Workflow Metrics

| Metric | Current (p95) | Target | Status |
|---|---|---|---|
| LCP (Largest Contentful Paint) | {lcp-p95} ms | 2500 ms | {status} |
| FCP (First Contentful Paint) | {fcp-p95} ms | 1800 ms | {status} |
| TTI (Time to Interactive) | {tti-p95} ms | 3500 ms | {status} |
| Total Load Time | {total-p95} ms | 4000 ms | {status} |

---

## Bundle Composition

**Total JavaScript Size:** {total-js-size} KB  
**Third-Party Libraries:** {third-party-size} KB ({third-party-percentage}%)  
**Application Code:** {application-code-size} KB ({application-code-percentage}%)

**Top Third-Party Libraries by Size:**

| Library | Size | Used In |
|---|---|---|
| {library-1} | {size-1} KB | {scenarios-1} |
| {library-2} | {size-2} KB | {scenarios-2} |
| ... | ... | ... |

---

## Anti-Pattern Analysis

### {Anti-Pattern-Name}

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** {quantified-impact}

**Description:**
{brief-explanation-of-anti-pattern}

**Detected Instances:**

1. **{file-path}:{line-number}**
   ```{language}
   {code-snippet}
   ```
   **Issue:** {specific-issue-description}
   **Recommended Fix:** {actionable-recommendation}

{... repeat for each anti-pattern ...}

---

## Backend Source Code Analysis

**Note:** This section is included only if backend repository is configured (`backend_available = true`). Otherwise, omit this section entirely.

**Backend Repository:** {backend-repo-name} ({backend-framework})  
**Analysis Coverage:** {endpoints-analyzed} endpoints analyzed  
**Serena Status:** {serena-instance-name or "Grep fallback"}

### Backend Anti-Patterns Detected

#### Database N+1 Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Impact:** {(n_queries - 1) * 10ms}

**Detected Instances:**

1. **{handler-file-path}:{line-number}**
   ```{language}
   {code-snippet-showing-loop-with-queries}
   ```
   **Issue:** {count} queries executed sequentially in loop  
   **Recommended Fix:** Use batch query (e.g., `SELECT * FROM table WHERE id IN (...)`) or ORM eager loading

{... repeat for each N+1 instance ...}

#### Missing Pagination

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Payload Waste:** {(total_items - 20) * avg_item_size}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** Returns {item-count} items without pagination  
   **Recommended Fix:** Add `page` and `limit` query parameters, implement `.limit()` and `.offset()` in query

{... repeat for each pagination issue ...}

#### Missing Caching

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Latency Reduction:** {operation_time * 0.8}

**Detected Instances:**

1. **Endpoint:** GET {endpoint-path}
   **Handler:** {handler-file-path}  
   **Issue:** {expensive-operation-description} on every request (no cache detected)  
   **Data Change Frequency:** {static / slow-changing / fast-changing}  
   **Recommended Fix:** Implement cache layer (Redis, in-memory) with appropriate TTL

{... repeat for each caching issue ...}

#### Inefficient Queries

**Severity:** {High / Medium / Low}  
**Instances Found:** {count}  
**Estimated Impact:** 30-50% query time reduction

**Detected Instances:**

1. **Query:** {query-snippet}
   **Handler:** {handler-file-path}:{line-number}  
   **Issue:** SELECT * fetches {column-count} columns but only {used-count} used in response  
   **Recommended Fix:** Specify exact columns: `SELECT id, name, price FROM products WHERE ...`

{... repeat for each inefficient query ...}

### Cross-Repository Over-Fetching Analysis

**Note:** This analysis cross-references backend response schemas with frontend field usage.

#### Per-Endpoint Analysis

##### Endpoint: GET {endpoint-path}

**Backend Handler:** {handler-file-path}  
**Response Type:** {ResponseStructName}  
**Total Fields:** {total-field-count}  
**Used by Frontend:** {used-field-count}  
**Unused Fields:** {unused-field-list}  
**Over-Fetching Percentage:** {waste-percentage}%  
**Call Pattern:** {Single call / N+1 (count calls)}  
**Payload Waste:** {waste-bytes} KB per request × {call-count if N+1} calls = {total-waste} KB  
**Recommendation:** {Create specialized DTO / Use GraphQL / Field projection}

{... repeat for each endpoint ...}

---

## Recommended Optimizations

**Note:** Optimizations are categorized by layer (Frontend / Backend / Integration) when backend analysis is available.

Optimizations are prioritized by estimated impact (time or size savings).

| Priority | Optimization | Estimated Impact | Effort |
|---|---|---|---|
| 1 | {optimization-1} | {impact-1} | {effort-1} |
| 2 | {optimization-2} | {impact-2} | {effort-2} |
| 3 | {optimization-3} | {impact-3} | {effort-3} |
| ... | ... | ... | ... |

**Effort Legend:**
- **Low:** < 1 day of work
- **Medium:** 1-3 days of work
- **High:** > 3 days of work

---

## Next Steps

1. Review this report with the team and prioritize optimizations
2. Create Jira tasks for high-priority optimizations using `/sdlc-workflow:define-feature` or `/sdlc-workflow:plan-feature`
3. After implementing optimizations, re-run `/sdlc-workflow:performance-baseline` to capture new baseline and measure improvements
```

### Step 7.3 – Calculate Overall Performance Rating

Based on the workflow metrics, assign an overall rating:

- **Excellent:** All metrics within targets (LCP < 2500ms, FCP < 1800ms, TTI < 3500ms, Total < 4000ms)
- **Good:** 1-2 metrics slightly above targets (within 20% over)
- **Needs Improvement:** 2-3 metrics above targets (> 20% over)
- **Poor:** All metrics above targets or any metric > 50% over target

### Step 7.4 – Prioritize Optimizations

Sort all detected anti-patterns by estimated impact (time or size savings) descending.

Assign effort estimates based on:
- **Low effort:** Configuration changes, adding `async`/`defer` attributes, removing unused imports
- **Medium effort:** Refactoring API calls, adding memoization, implementing lazy loading
- **High effort:** Bundle splitting, architecture changes, replacing third-party libraries

Generate the prioritized optimization table with the top 10 recommendations.

### Step 7.5 – Write Report to File

Write the generated report to `{analysis-directory}/workflow-analysis-report.md`.

## Step 8 – Output Summary

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
> {warnings-if-any}
>
> **Next Steps:**
>
> 1. Review the full analysis report
> 2. Prioritize optimizations with your team
> 3. Create Jira tasks for high-priority items
> 4. After implementing optimizations, re-baseline to measure improvements

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
- Use Grep/Glob for all code analysis (Serena not configured for this repository)
- Generate report even if some anti-pattern detection steps fail — document failed steps in the report
- Save report to directory specified in performance-config.md, never to the repository root
