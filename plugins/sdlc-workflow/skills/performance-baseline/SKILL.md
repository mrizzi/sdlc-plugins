---
name: performance-baseline
description: |
  Discover workflows from the codebase, prompt user to select a target workflow, auto-populate configuration, then capture performance baseline metrics via browser automation and generate a baseline report.
argument-hint: "[target-repository-path]"
---

# performance-baseline skill

You are an AI performance baseline assistant. When no workflow has been selected yet, you discover user workflows from the codebase (by reading router configuration and inferring user journeys), prompt the user to select a target workflow, and auto-populate the Performance Scenarios and Module Registry in `performance-config.md`. Once a workflow is selected, you verify test data availability, execute browser automation to measure page load times and resource loading, and generate a baseline report for comparison during optimization.

## Guardrails

### File Scope
- This skill creates files in designated performance directories (`.claude/performance/baselines/`)
- This skill does NOT modify source code files — only creates performance measurement artifacts
- This skill requires Performance Analysis Configuration with a selected workflow

### Execution Order — MANDATORY
**Every step in this skill MUST be executed in the exact sequence defined in this document. No step may be reordered, merged with another step, or silently omitted.**

- Steps are numbered to enforce a strict linear order: Step 1 → Step 2 → Step 2.0 → Step 2.0.5 → Step 2.1 → Step 2.2 → … → Step 11.
- Sub-steps (e.g., Step 8.4.B4.1, Step 8.4.B4.2) must be completed in their defined sub-order before the parent step is considered done.
- Conditional paths (e.g., "if backend-only, skip to Step 3") are the **only permitted deviations** from sequential order, and they are explicitly stated in the step text. Any step not applicable to the current execution path must still be **acknowledged** with a brief output note before moving on (see Output Rules below).

### Step-Skip Policy
- A step may be **conditionally skipped** only when the step itself contains an explicit conditional instruction (e.g., "This step runs ONLY if …", "skip if metadata.workflow_selected = true").
- When a step is skipped due to a condition, output **must** include: `⏭ Step X skipped — <reason>` before proceeding to the next step.
- A step may **never** be skipped to save time, reduce verbosity, or because the result seems obvious.

**Never proceed silently.** If a step produces no data (e.g., no routes found), output must explicitly state that fact rather than moving on without comment.

### Blocking Steps — CANNOT BE BYPASSED
Steps that require user confirmation or user input (e.g., Step 4.4 – workflow selection, Step 8.3 – script review, Step 8.4.B4.3 – test data confirmation) are **hard blocking**. The skill must pause and wait for explicit user response before executing the next step. These steps may not be auto-answered, assumed, or skipped.

### Completeness Enforcement
- All outputs defined for a step (tables, summaries, file writes, console messages) must be produced **in full** before the step is marked complete.
- Partial output (e.g., showing only a subset of discovered endpoints, truncating a table) is not permitted.
- If a step's output would exceed reasonable length, summarise with counts and highlight key items — but the full artifact (file) must still be written completely.

### Error Handling
- If any mandatory step fails (e.g., config missing, script error, no functional endpoints), the skill must halt at that step, output a clear error message with the step number, and provide actionable remediation instructions. It must not silently skip to a later step.

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Verify Performance Configuration

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Verify config exists, stop if missing
- Read configuration file for baseline settings

## Step 2.0 – Check if Workflow Selection Required

Read config metadata.workflow_selected:

- **If false:** Workflow not yet selected, proceed to Step 3 (workflow discovery)
- **If true:** Workflow already selected, skip workflow discovery and proceed to Step 2.1 (read selected workflow)

**Note:** Setup skill creates minimal config with workflow_selected = false. Baseline skill discovers workflows and sets workflow_selected = true after user selection.

### Step 2.0.5 – Check Analysis Scope

Read config metadata.analysis_scope to determine workflow discovery method:

- **If "frontend-only" or "full-stack" or "full-stack-monorepo":** Proceed to Step 4.1 (frontend route discovery)
- **If "backend-only":** Skip to Step 3 (backend API endpoint discovery)

**Note:** Analysis scope is set during performance-setup and determines what kind of workflows are discovered.

## Step 2.1 – Read Selected Workflow (If Already Selected)

**Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-6-workflow-validation)

**Specific actions for this skill:**
- Extract workflow name, entry point, key screens, complexity from Selected Workflow section
- Store for scenario filtering and baseline capture
- Skip to Step 2.2 (Read Baseline Mode)

### Step 2.2 – Read Baseline Mode from Metadata

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction)

**Specific fields to extract:**
- `metadata.baseline_mode` → stored_mode (for mode consistency enforcement)
- `metadata.baseline_captured` → baseline_already_captured (check if re-run)

**Store for mode selection in Step 4:**
- `stored_mode`: null | "cold-start"
- `baseline_already_captured`: true | false

---

## Step 3 – Backend API Endpoint Discovery (Backend-Only Mode)

**This entire Step 3 runs ONLY if `metadata.analysis_scope = "backend-only"` AND `metadata.workflow_selected = false`.**

**Purpose:** Discover API endpoints from backend code, group them into workflows by resource/controller, and generate scenarios for static analysis.

### Step 3.0 – Serena Availability Probe

```bash
backend_path=$(grep "Backend Path" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
backend_framework=$(grep "Backend Framework" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
serena_instance=$(grep "Serena Instance" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
```

**If `serena_instance` is non-empty and not "—":**

Call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`.

- **Response received (any result):** `serena_mode = live`. Store the overview. Proceed to **Step 3.1-A**.
- **Error response:** `serena_mode = down`. Record exact error string. Proceed to **Step 3.1-B**.

**If `serena_instance` is "—" or empty:** `serena_mode = not-configured`. Proceed to **Step 3.1-B**.

> `serena_mode` is set once here and applies to all of Steps 3.1, 3.1.1, and 3.5.

---

### Step 3.1 – Locate API Route Definitions

Search backend codebase for API endpoint definitions using framework-specific patterns.

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 3.0 and applies here.)

---

### Step 3.1-A – Locate API Route Definitions via Serena (`serena_mode = live`)

> Grep and shell-based symbol discovery are not available in this path.

For each endpoint module file identified under `backend_path`, call:

```
mcp__{serena_instance}__find_symbol(
    name_path_pattern="/",
    relative_path="<endpoint_module_file>",
    include_body=true,
    include_kinds=[12],
    max_matches=100
)
```

This single call per file returns all HTTP handler functions including their route decorators.
From the response, extract for each handler:
- HTTP method (from `#[get]`, `#[post]`, `@GetMapping`, `@app.get`, etc. in function body)
- Path pattern (from decorator argument)
- Handler function name
- File location (absolute path)

If a `find_symbol` call errors on a specific file: mark that file `discovery_status: error`,
continue with remaining files. Do not switch to grep.

Set `discovery_method = "Serena MCP"` on all results. Proceed to **Step 3.1.1-A**.

---

### Step 3.1-B – Locate API Route Definitions via Grep (`serena_mode = down | not-configured`)

**Run ONE grep per framework using `-A 3` context lines** so the decorator line and the
`fn` / `async fn` handler name appear together in the same result block. This eliminates any
need to run a second lookup or write a parsing script.

**Framework-specific grep commands (use the one matching the detected framework):**

| Framework | Grep command |
|---|---|
| actix-web (Rust) | `grep -rn --include="*.rs" -A 3 '#\[get\|#\[post\|#\[put\|#\[delete\|#\[patch' <backend_root>` |
| axum (Rust) | `grep -rn --include="*.rs" -A 3 '\.route("' <backend_root>` |
| poem (Rust) | `grep -rn --include="*.rs" -A 3 '\.at("' <backend_root>` |
| Spring Boot (Java) | `grep -rn --include="*.java" -A 3 '@GetMapping\|@PostMapping\|@PutMapping\|@DeleteMapping' <backend_root>` |
| FastAPI (Python) | `grep -rn --include="*.py" -A 3 '@app\.get\|@router\.\(get\|post\|put\|delete\)' <backend_root>` |
| Express (Node) | `grep -rn --include="*.js" --include="*.ts" -A 3 'router\.\(get\|post\|put\|delete\)\|app\.\(get\|post\)' <backend_root>` |

**Parse the grep output in-context — do NOT write a script to /tmp or any file.**
Each result block gives you the decorator line (method + path) and the next 1–3 lines give
you the handler function name. Read the blocks directly and fill the endpoint table row by row.

If a result block does not contain a `fn` / `async fn` / `def` / `function` name within the
3 context lines, use the filename + line number as the handler identifier (e.g., `line_42`).

Set `discovery_method = "Grep"` on all results. Proceed to **Step 3.1.1-B**.

---

> **◆ File Coverage Self-Check — Step 3.1 (mandatory, applies to both -A and -B paths)**
>
> Before building the endpoint table, answer each question explicitly in your response:
>
> **Q1 — Files scanned:** List every source file you examined for endpoint definitions.
>
> **Q2 — Files skipped:** Did any file produce an error or get no results?
> If yes, list each file and the reason (error, empty, test-only, etc.).
>
> **Q3 — Coverage gap check:** Use Glob to list all source files under `backend_root`
> matching the framework extension (e.g., `**/*.rs`, `**/*.java`, `**/*.py`).
> Compare that list against the files you already scanned.
> Are there any files in the Glob result that are **absent from your scanned list**?
>
> **Q4 — Remediation:** If Q3 reveals unscanned files → scan them now using the same
> Step 3.1-A or Step 3.1-B method before continuing. Do not skip them.
>
> Only proceed to the endpoint table once every source file is accounted for.

---

**Output all discovered endpoints as an in-context markdown table in your response — this table is
the live endpoint registry for all subsequent steps. Do NOT write results to /tmp or shell
variables. Counting, grouping, and validation in Steps 3.1.2–3.2.1 reference this table.**

| # | HTTP Method | Path Pattern | Handler | File | Impact | Discovery Method |
|---|---|---|---|---|---|---|
| 1 | GET | /api/v2/... | handler_fn | src/... | low | Serena MCP / Grep |

### Step 3.1.1 – Validate Endpoint Safety (Impact Analysis)

For each discovered endpoint, determine how many places reference the handler to classify impact.

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 3.0 and applies here.)

---

### Step 3.1.1-A – Validate Endpoint Safety via Serena (`serena_mode = live`)

For each discovered endpoint handler, call:

```
mcp__{serena_instance}__find_referencing_symbols(
    name_path="<handler_function_name>",
    relative_path="<handler_file>"
)
```

Count references returned. If a call errors on a specific handler: record
`impact_method: "error"` for that handler and continue with remaining endpoints.

---

### Step 3.1.1-B – Validate Endpoint Safety via Grep (`serena_mode = down | not-configured`)

For each discovered endpoint handler:

```bash
grep -r "$handler_function_name" "$backend_path" | wc -l
```

Count occurrences as reference count.

---

**Impact Classification (both paths):**
- **Low impact:** < 5 references
- **Medium impact:** 5–10 references
- **High impact:** > 10 references

**Store impact classification with each endpoint:**
```
endpoint {
  path: "/api/v2/products/{id}"
  method: "GET"
  handler: "get_product_by_id"
  references: 12
  impact: "high"
  impact_method: "Serena MCP" | "Grep" | "error"
}
```

**Warning to user:** High-impact endpoints will be flagged during workflow selection (Step 3.3).

### Step 3.1.2 – Record Discovered Endpoint Count

After Steps 3.1.1-A or 3.1.1-B complete, **count the rows in your in-context endpoint table**
(the table you built in Step 3.1) and record the total. No shell command needed — count the
table rows in your response.

State this count explicitly:

> `▶ Endpoint discovery complete — N endpoints found across all modules.`

This count is the **source of truth** for the grouping integrity check in Step 3.2.1.
Any grouping that does not account for all N endpoints is incomplete.

### Step 3.2 – Group Endpoints into Workflows

Group discovered endpoints into logical workflows using resource-based grouping.

**IMPORTANT:** Wait for the complete endpoint discovery from Step 3.1 to finish before grouping. Once all endpoints are discovered, group them into workflows and present **ALL workflows** to the user in Step 3.3. Do not filter, limit, or omit any workflows. Every endpoint from the backend source code must be assigned to at least one workflow, and all workflows must be displayed regardless of size or complexity.

**Grouping strategies:**

**1. Resource-based grouping (Primary):**
Extract resource from path and group endpoints operating on same resource:

Example:
```
/api/v2/products          (GET)    → "Product Management" workflow
/api/v2/products/{id}     (GET)    → "Product Management" workflow
/api/v2/products          (POST)   → "Product Management" workflow
/api/v2/products/{id}     (PUT)    → "Product Management" workflow
```

**Resource extraction algorithm:**
```python
def extract_resource(path):
    # Remove API version prefix
    path_parts = path.split('/')
    
    # Filter out: empty strings, 'api', version numbers, parameter placeholders
    resource_parts = [
        part for part in path_parts 
        if part and part not in ['api', 'v1', 'v2', 'v3'] and not part.startswith('{')
    ]
    
    # Return first meaningful part
    return resource_parts[0] if resource_parts else None
```

**2. Controller/Module-based grouping (Secondary):**
If endpoints are in the same file, group by filename:

Example:
```
src/controllers/product_controller.rs → "Product Management" workflow
src/controllers/order_controller.rs   → "Order Management" workflow
```

**3. OpenAPI tags (Tertiary):**
If `openapi.yaml` or `swagger.json` exists in backend_path:
1. Read OpenAPI spec
2. Extract paths and their tags
3. Group endpoints by tags
4. Cross-reference with discovered endpoints

**Estimate workflow complexity:**
For each workflow, calculate complexity based on endpoint count:
- **Simple:** 1-2 endpoints
- **Moderate:** 3-4 endpoints
- **Complex:** 5+ endpoints

**Extract for each workflow:**
- Workflow name (e.g., "Product Management")
- Entry endpoint (first endpoint in group)
- Key endpoints (list of all endpoint paths)
- Complexity (Simple/Moderate/Complex)
- Total reference count (sum of all endpoint references from Step 3.1.1)

### Step 3.2.1 – Validate Grouping Completeness

Before presenting workflows to the user, perform an **in-context count** (count table rows —
no shell):

1. Count the total endpoints in your in-context endpoint table from Step 3.1.2 → `N`
2. Count how many endpoints appear across all workflow groups you built in Step 3.2 → `M`

**If N == M:** Output confirmation and proceed to Step 3.3:

> `✓ Grouping integrity check passed — N endpoints discovered, N endpoints grouped across W workflows.`

**If N ≠ M:** Output a mismatch warning and redo Step 3.2 from scratch:

> `⚠ Grouping mismatch — N endpoints discovered but M endpoints grouped. Re-running grouping.`

Scan your endpoint table row-by-row and identify which rows have no workflow assignment.
Re-run the Step 3.2 grouping logic in-context, placing every unassigned endpoint into an
existing workflow or a new "Miscellaneous" workflow. Repeat Step 3.2.1 until N == M.

**Do not proceed to Step 3.3 until the counts match exactly. No shell scripts for this check.**

### Step 3.3 – Present Workflows and Prompt Selection

**Display ALL discovered backend workflows** from Step 3.2 in a numbered table. 

**CRITICAL: Do not filter, limit, or omit any workflows. Every workflow must be presented to the user.**

```
## Discovered Backend Workflows

| # | Workflow Name | Entry Endpoint | Key Endpoints | Complexity | Impact |
|---|---|---|---|---|---|
| 1 | Product Management | GET /api/v2/products | GET /products, GET /products/{id}, POST /products | Moderate | Medium (23 refs) |
| 2 | Order Management | GET /api/v2/orders | GET /orders, POST /orders, PUT /orders/{id} | Complex | High (45 refs) |
| {{...ALL workflows from Step 3.2, numbered sequentially...}} |
```

**Note:** Include single-endpoint workflows (Simple complexity) and all other workflows discovered during analysis. The table above is an example — your actual table should contain every workflow identified in Step 3.2.

**Impact warnings:**
If any workflow has high-impact endpoints (>10 total references):
> ⚠️ **High-Impact Workflow:** This workflow includes endpoints with 10+ references. Changes may affect multiple features.

**Guidance to user:**
> "These workflows represent distinct API resource groups in your backend. Select one workflow to optimize for performance."
>
> "**Recommendation:** Start with a Moderate complexity workflow. Simple workflows may not reveal performance bottlenecks, while Complex workflows can be overwhelming to analyze."

**Prompt:**
> "Enter the number of the workflow you want to optimize (1-N):"

**Validation:**
- Verify user input is a valid number within range
- If invalid, re-prompt

**Capture selection:**
- Store the selected workflow's details

### Step 3.4 – Auto-Populate Scenarios from Selected Workflow

Based on the selected backend workflow's endpoints, generate performance scenarios.

**For backend-only mode, scenarios are API endpoints (not browser URLs).**

For each endpoint in the workflow:

**Extract scenario details:**
- Scenario name: Derive from endpoint path and method (e.g., `GET /products` → `products-get-list`)
- Endpoint: Full endpoint path with method (e.g., `GET /api/v2/products`)
- Description: Generate from endpoint purpose (e.g., "List all products")

**Scenario name derivation rule:**
```python
def derive_scenario_name(method, path):
    # Extract resource and action from path
    parts = path.split('/').filter(Boolean)
    resource = parts[-2] if parts[-1].startswith('{') else parts[-1]
    action = "get-detail" if parts[-1].startswith('{') else f"{method.lower()}-{resource}"
    return f"{resource}-{action}"
```

**Result:** A table of scenarios matching the selected workflow's endpoints:

| Scenario Name | Endpoint | Description |
|---|---|---|
| products-get-list | GET /api/v2/products | List all products |
| products-get-detail | GET /api/v2/products/{id} | Get product details |
| products-post | POST /api/v2/products | Create new product |

### Step 3.5 – Discover Modules for Selected Workflow

For backend-only mode, modules represent handler functions or service classes.

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 3.0 and applies here.)

---

### Step 3.5-A – Discover Modules via Serena (`serena_mode = live`)

> Grep is not available in this path.

For each handler file in the selected workflow, call:

```
mcp__{serena_instance}__get_symbols_overview(
    relative_path="<handler_file>",
    depth=1
)
```

Extract functions/methods relevant to the selected workflow endpoints.
Set `discovery_method = "Serena MCP"`.

---

### Step 3.5-B – Discover Modules via Grep (`serena_mode = down | not-configured`)

For each handler file in the selected workflow:

```bash
grep -E "^(pub\s+)?async\s+fn|^fn|@handler|def\s+" "$endpoint_file" | head -20
```

Extract function signatures.
Set `discovery_method = "Grep"`.

---

**Result:** Module registry with handler functions as entries. Document `discovery_method` used.

### Step 3.6 – Stage Backend Config Changes (no file write)

**Do NOT write to `.claude/performance-config.md` here.** Collect the following values
in-context so they can be written in the single consolidated config write at Step 4.7:

| Config Field | Value Source |
|---|---|
| Performance Scenarios | generated scenarios from Step 3.4 |
| Module Registry | discovered handlers from Step 3.5 |
| Selected Workflow | workflow details from Step 3.3 |
| `metadata.workflow_selected` | `true` |
| `metadata.backend_endpoint_discovery_method` | `"serena"` or `"grep"` (from Step 3.0) |

State in your response:
> `▶ Backend config changes staged — will be written in Step 4.7 consolidated write.`

**Skip browser baseline capture:** For backend-only mode, Step 9 (Execute Baseline Capture) will be modified to generate static analysis report instead of browser metrics.

---

## Step 4 – Frontend Workflow Discovery

Analyze the frontend codebase to discover routes using Serena (if available) or Read/Grep/Glob.

### Step 4.1 – Find Router Configuration **(Workflow Discovery Only — skip if metadata.workflow_selected = true)**

Common router configuration file patterns:
- React Router: `src/routes.tsx`, `src/router/index.ts`, `src/App.tsx` (with `<Route>` components)
- Vue Router: `src/router/index.ts`, `src/router/routes.ts`
- Angular: `src/app-routing.module.ts`, `src/app/app-routing.module.ts`
- Next.js: `pages/` or `app/` directory structure (file-based routing)

Use Glob to find likely router files:
```
**/*routes*.{ts,tsx,js,jsx}
**/*router*.{ts,tsx,js,jsx}
**/App.{ts,tsx,js,jsx}
```

> **◆ Router File Coverage Self-Check — Step 4.1 (mandatory, applies regardless of Serena or Grep path)**
>
> Before proceeding to Step 4.2, answer each question explicitly in your response:
>
> **Q1 — Files found:** List every router/route configuration file the Glob returned.
>
> **Q2 — Framework coverage:** Does the set of files match the detected frontend framework?
> For example:
> - React Router → expect `routes.tsx`, `App.tsx` with `<Route>`, or a `router/index.ts`
> - Vue Router → expect `src/router/index.ts` or `src/router/routes.ts`
> - Next.js → expect a `pages/` or `app/` directory
> - Angular → expect `*-routing.module.ts`
>
> If the expected files are absent, use an additional Glob or Grep to locate them now.
>
> **Q3 — Coverage gap check:** Are there route definitions that might live outside the
> Glob patterns above? (e.g., inline `<Route>` in page components, nested routers,
> dynamic imports, code-split route configs.) Use a targeted Grep to check:
> ```
> grep -rn "<Route\|createBrowserRouter\|createHashRouter\|RouterProvider" <frontend_root> --include="*.tsx" --include="*.jsx" --include="*.ts"
> ```
> Add any newly found files to the list before continuing.
>
> **Q4 — Remediation:** If Q2 or Q3 reveals unscanned router files → add them to the
> router file list now. Do not proceed to Step 4.2 until all router files are identified.

### Step 4.2 – Extract Route Definitions **(Workflow Discovery Only — skip if metadata.workflow_selected = true)**

For each router configuration file found:

**If Serena is available:**
- Use `get_symbols_overview` to list route definitions
- Use `find_symbol` with `include_body=true` to read route arrays or objects

**If Serena is not available:**
- Use Read tool to examine router files directly
- Use Grep with **`-A 2` context lines** so the route path and component appear together
  in one block — do NOT write a parsing script to `/tmp`:
  ```
  grep -rn -A 2 "path:" <frontend_root> --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"
  grep -rn -A 2 "<Route" <frontend_root> --include="*.tsx" --include="*.jsx"
  ```
- Parse the grep output **in-context**: each block gives you the `path=` / `path:` line and
  the adjacent `component=` / `element=` line. Fill the route table row by row in your
  response — do NOT write intermediate results to a file or shell variable.

Extract for each route:
- Route path (e.g., `/`, `/products/:id`, `/dashboard`)
- Component name or file reference
- Whether the route is lazy-loaded

### Step 4.2.1 – Record Discovered Route Count

After Step 4.2 completes, **output all discovered routes as an in-context markdown table in
your response** (if not already done). Then count the rows in that table. No shell command
needed — count the table rows in your response.

State this count explicitly:

> `▶ Route extraction complete — N routes found across all router configuration files.`

This count is the **source of truth** for the grouping integrity check in Step 4.3.4.
Any grouping that does not account for all N routes is incomplete.

| # | Route Path | Component | File | Discovery Method |
|---|---|---|---|---|
| 1 | /products | ProductList | src/... | Serena MCP / Grep |

### Step 4.3 – Infer Workflows from Routes (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).

Group discovered routes into functional workflows (user journeys). A workflow is a sequence of related pages that form a cohesive user task.

#### Step 4.3.1 – Read Navigation Structure

Examine the application's navigation to understand primary workflows:

Use Grep to find navigation/sidebar components:
```
pattern: nav|menu|sidebar|NavItem
path: src/
```

If found, read the navigation component to identify top-level navigation items. These often represent primary workflows.

#### Step 4.3.2 – Group Routes by Workflow

**Important:** Discover and group ALL routes from the router configuration into workflows. Do not filter or limit the number of workflows discovered. Every route should be assigned to at least one workflow. Standalone routes (e.g., /search, /importers) that don't fit natural groupings should be presented as individual workflows.

Apply these grouping strategies to infer workflows:

**1. Path prefix grouping** — routes sharing a common prefix likely form a workflow:

Examples:
- `/products/*` routes → "Product Catalog" workflow
- `/orders/*` routes → "Order Management" workflow
- `/profile/*` routes → "User Profile" workflow

**2. List-to-detail patterns** — list view + detail view form a browse workflow:

Examples:
- `/products` + `/products/:id` → "Product Browse and Detail" workflow
- `/orders` + `/orders/:id` → "Order Browse and Detail" workflow

**3. Feature module grouping** — routes in the same feature directory:

- Examine `src/pages/` or `src/features/` directory structure
- Group routes by their page directory

**4. Upload/action workflows** — upload + scan + view patterns:

Examples:
- `/documents/upload`, `/documents/scan`, `/documents/:id` → "Document Upload and Analysis" workflow

**5. Standalone routes** — routes that don't fit into any of the above patterns:

Examples:
- `/search` → "Search" workflow (single route)
- `/importers` → "Importer Management" workflow (single route)
- `/licenses` → "License Catalog" workflow (single route)

**Important:** Standalone routes should be presented as individual workflows with Simple complexity, even if they contain only one route. Do not omit these routes.

#### Step 4.3.3 – Estimate Workflow Complexity

For each inferred workflow:

**Calculate complexity based on:**
- Number of routes in workflow:
  - 1 route (standalone) = Simple
  - 2 routes (list + detail) = Simple
  - 3-4 routes = Moderate  
  - 5+ routes = Complex
- Number of components in workflow pages:
  - Count `.tsx`/`.ts` files in page directories for this workflow
- Presence of API calls:
  - Search for `useQuery`, `useMutation`, `fetch`, `axios` in workflow components
  - Estimate API call count

**Note:** Standalone routes (single route workflows like /search, /importers) are classified as Simple complexity by default.

**Extract for each workflow:**
- Workflow name (descriptive, e.g., "Product Browse and Detail")
- Entry point URL (first route in the workflow)
- Key screens (list of route paths that form the workflow)
- Complexity (Simple/Moderate/Complex with breakdown)

**If no workflows discovered:**

Inform the user:
> "No workflows could be auto-discovered from the codebase. This may happen if:"
> - The application uses a non-standard routing structure
> - Routes are dynamically generated
> - The router configuration uses complex patterns
>
> "You will need to manually populate scenarios in `.claude/performance-config.md`."

If no workflows found, skip to Step 4 with empty workflow list.

#### Step 4.3.4 – Validate Grouping Completeness

Before presenting workflows to the user, perform an **in-context count** (count table rows —
no shell):

1. Count the total routes in your in-context route table from Step 4.2.1 → `N`
2. Count how many routes appear across all workflow groups you built in Steps 4.3.1–4.3.3 → `M`

**If N == M:** Output confirmation and proceed to Step 4.4:

> `✓ Grouping integrity check passed — N routes discovered, N routes grouped across W workflows.`

**If N ≠ M:** Output a mismatch warning and redo Steps 4.3.1–4.3.3 from scratch:

> `⚠ Grouping mismatch — N routes discovered but M routes grouped. Re-running grouping.`

Scan your route table row-by-row and identify which rows have no workflow assignment.
Re-run the Step 4.3 grouping logic in-context, placing every unassigned route into an existing
workflow or a new standalone workflow. Repeat Step 4.3.4 until N == M.

**Do not proceed to Step 4.4 until the counts match exactly. No shell scripts for this check.**

**Do not proceed to Step 4.4 until the counts match exactly.**

### Step 4.4 – Present Workflows and Prompt Selection (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).

**Display ALL discovered workflows in a numbered table.** Do not filter, limit, or omit any workflows. Every workflow discovered in Step 4.3 must be presented to the user.

```
## Discovered Workflows

| # | Workflow Name | Entry Point | Key Screens | Complexity |
|---|---|---|---|---|
| {{workflow entries - ALL workflows from Step 4.3, numbered sequentially}} |
```

**Guidance to user:**

> "These workflows represent distinct user journeys through your application. Select one workflow to optimize for performance."
>
> "**Recommendation:** Start with a Moderate complexity workflow that is business-critical. Simple workflows may not reveal performance bottlenecks, while Complex workflows can be overwhelming to analyze."

**Prompt:**

> "Enter the number of the workflow you want to optimize (1-N):"

**Validation:**
- Verify user input is a valid number within range
- If invalid, re-prompt: "Invalid selection. Please enter a number between 1 and N."

**Capture selection:**
- Store the selected workflow's details (name, entry point, key screens, complexity)

### Step 4.5 – Auto-Populate Scenarios from Selected Workflow (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).

Based on the selected workflow's key screens, automatically generate performance scenarios.

For each route in the workflow's key screens:

**Extract scenario details:**
- Scenario name: Derive from route path (e.g., `/products` → `products-list`, `/products/:id` → `products-details`)
- URL path: Use the route path
- Description: Generate from route purpose

**Scenario name derivation rule:**
```
path.split('/').filter(Boolean).map(s => s.startsWith(':') ? s.slice(1) : s).join('-')
```

**Handle dynamic route segments:**
- For routes with `:id` or other parameters, note in the scenario that a sample ID will be needed during baseline capture

**Result:** A table of scenarios that exactly matches the selected workflow's key screens.

### Step 4.6 – Discover Modules for Selected Workflow (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).

Identify code-split modules or lazy-loaded routes for the selected workflow's pages.

#### Step 4.6.1 – Find Lazy-Loaded Components

For each route in the selected workflow:

Search for the component referenced by the route in the router configuration.

Check if it's lazy-loaded:
```
React.lazy\(.*import\(['"]([^'"]+)['"]\)
import\(['"]([^'"]+)['"]\).*\.then\(
loadable\(.*import\(['"]([^'"]+)['"]\)
```

#### Step 4.6.2 – Extract Module Entry Points

For each lazy-loaded component in the workflow:

**Determine module entry point:**
- Look for `index.ts` or `index.tsx` in the component's directory
- If not found, use the lazy-loaded file path as the entry point

**Derive module name:**
- Use the page directory name (e.g., `src/app/pages/product-list` → module name: `product-list`)

**Generate module description:**
- Describe the module's purpose based on the route and component name

**Result:** A table of modules corresponding to the selected workflow's pages.

### Step 4.7 – Consolidated Config Write *(runs for ALL scopes — never skip)*

**This is the single point where `.claude/performance-config.md` is written during the
discovery phase.** It applies staged changes from Step 3.6 (backend) and/or Step 4.6
(frontend) in one atomic write. Running once here eliminates redundant writes.

**Applies to all scopes:**
- `backend-only` — applies backend staged changes; frontend sections are left as-is
- `frontend-only` — applies frontend staged changes; backend sections are left as-is
- `full-stack` — applies both backend and frontend staged changes together

---

**Step 4.7.1 – Read Current Config**

Read `.claude/performance-config.md` from the target repository. This is the base document
that will be updated.

**Step 4.7.2 – Apply Staged Changes**

Apply ALL staged changes collected in-context from Steps 3.6 and/or 4.6:

| Section | Source | Apply when |
|---|---|---|
| Performance Scenarios | Step 3.4 scenarios | `backend-only` or `full-stack` |
| Module Registry (backend) | Step 3.5 handlers | `backend-only` or `full-stack` |
| Selected Workflow (backend) | Step 3.3 selection | `backend-only` or `full-stack` |
| Performance Scenarios | Step 4.5 scenarios | `frontend-only` or `full-stack` |
| Module Registry (frontend) | Step 4.6 modules | `frontend-only` or `full-stack` |
| Selected Workflow (frontend) | Step 4.4 selection | `frontend-only` or `full-stack` |

**Selected Workflow block format (apply for whichever scope was discovered):**
```markdown
## Selected Workflow

| Property | Value |
|---|---|
| Workflow Name | {selected workflow name} |
| Entry Point | {entry point URL} |
| Key Screens | {comma-separated list of key screens} |
| Complexity | {complexity estimate} |
| Selected On | {current date in YYYY-MM-DD format} |
```

**Metadata fields to set:**
```yaml
metadata:
  workflow_selected: true
  backend_endpoint_discovery_method: "serena" | "grep"   # backend-only or full-stack
  last_updated: {current-timestamp}
```

**Step 4.7.3 – Write Config**

**Apply:** [Common Pattern: Config Write Protection](../performance/common-patterns.md#pattern-9-config-write-protection)

Write the fully merged config back to `.claude/performance-config.md` in **one write
operation**. Do not write partial sections or call Write more than once for this step.

**Step 4.7.4 – Log Update**

```
✓ Configuration written — single consolidated write complete.
  - Scope: {backend-only | frontend-only | full-stack}
  - Scenarios: {count} auto-populated
  - Modules: {count} discovered
  - Workflow: {workflow-name}
```

After this step, proceed to Step 5 (Discover Test Data).

## Step 5 – Discover Test Data

**Note:** This is the continuation point whether workflow was just selected (Step 4.7) or was already selected (Step 2.1).

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction)

Read `metadata.analysis_scope` from performance-config.md to determine discovery approach.

### Step 5.0 – Check Analysis Scope

```bash
analysis_scope=$(grep "| analysis_scope |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
```

**If `analysis_scope = "frontend-only"`:** Skip to Step 5.3 (frontend-only yes/no prompt)

**If `analysis_scope` in ["backend-only", "full-stack", "full-stack-monorepo"]:** Proceed with backend test data discovery (Step 5.1)

### Step 5.1 – Extract Workflow-Specific Scope

**Purpose:** Determine which endpoints/modules belong to the selected workflow before discovering test data.

**CRITICAL:** Discovery must be workflow-specific, not generic. If user selected "License Analysis", do NOT discover SBOM test data.

```bash
# Read selected workflow name from config
workflow_name=$(awk '/## Selected Workflow/,/^## / {
  if ($0 ~ /\| Workflow Name \|/ && $0 !~ /Property/) {
    split($0, fields, "|")
    gsub(/^[ \t]+|[ \t]+$/, "", fields[3])
    print fields[3]
    exit
  }
}' .claude/performance-config.md)

# Extract workflow endpoint paths from Performance Scenarios table
# (These are the endpoints we need test data for)
# Using POSIX-compatible awk (works with mawk, nawk, gawk)
workflow_endpoints=$(awk -F'|' '/## Performance Scenarios/,/^## / {
  if ($0 ~ /^\| [a-z]/ && $0 !~ /Scenario Name/) {
    gsub(/^[ \t]+|[ \t]+$/, "", $3)
    print $3
  }
}' .claude/performance-config.md)

# Extract handler locations from Module Registry table
handler_locations=$(awk -F'|' '/## Module Registry/,/^## / {
  if ($0 ~ /^\| [a-z]/ && $0 !~ /Module Name/) {
    gsub(/^[ \t]+|[ \t]+$/, "", $3)
    print $3
  }
}' .claude/performance-config.md)

# Extract common module directory from handler locations
# Example: modules/analysis/src/endpoints/mod.rs:44-67 → modules/analysis/src/endpoints/
# Step 1: Remove line numbers
# Step 2: Remove filename
# Step 3: Take first unique directory (alphabetically)
# NOTE: This takes the alphabetically first directory, not the longest common prefix.
#       For handlers spanning modules/analysis/src/endpoints/ and modules/analysis/src/db/,
#       this returns modules/analysis/src/db/ (alphabetically first).
#       Low risk for single-workflow runs where all handlers are typically in one directory.
workflow_module_path=$(echo "$handler_locations" | \
  sed 's/:.*$//' | \
  sed 's|/[^/]*$||' | \
  sort -u | head -1)

echo "ℹ️ Workflow: $workflow_name"
echo "   Module path: $workflow_module_path"
echo "   Endpoints: $(echo "$workflow_endpoints" | wc -l) endpoint(s)"
```

### Step 5.2 – Discover List Endpoints (Workflow-Scoped)

**Purpose:** Find list/collection endpoints within the selected workflow's module directory to query for available test data IDs.

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 3.0 and applies here.)

---

### Step 5.2-A – Discover List Endpoints via Serena (`serena_mode = live`)

> Grep is not available in this path.

Call `mcp__{serena_instance}__find_symbol` scoped to the workflow module path:

```
mcp__{serena_instance}__find_symbol(
    name_path_pattern=".*list.*|.*search.*|get_all",
    relative_path="${workflow_module_path}",
    include_body=false,
    depth=1
)
```

Look for handlers returning collection types (`Vec<T>`, `Page<T>`, `List<T>`).
Extract GET endpoints without path parameters.
Store as `list_endpoints` array. Set `discovery_method = "Serena MCP (workflow-scoped)"`.

If the call errors: mark `discovery_status: error`, proceed to Step 6 with empty `list_endpoints`.

---

### Step 5.2-B – Discover List Endpoints via Grep (`serena_mode = down | not-configured`)

```bash
# Search for GET endpoints in workflow module (scoped to selected workflow)
list_endpoints_str=$(grep -r "#\[get\(" ${workflow_module_path} | \
  grep -v "/{" | \
  grep -E "list|search|all")

# Convert multiline string to array for iteration
mapfile -t list_endpoints <<< "$list_endpoints_str"

echo "ℹ️ Discovery scoped to: ${workflow_module_path}"
echo "   Found ${#list_endpoints[@]} list endpoint candidate(s)"

# Store discovery method for reporting
discovery_method="Grep (workflow-scoped)"
```

**Validation:**

After discovery, cross-reference discovered list endpoints with workflow endpoints:

```bash
# Ensure discovered endpoints are related to workflow endpoints
# Example: If workflow has GET /api/v2/analysis/sbom/{id}, 
#          discovered list endpoint should be /api/v2/analysis/sbom (no {id})

# Strip HTTP method prefix from workflow_endpoints for comparison
# (workflow_endpoints may be "GET /api/v2/analysis/component" or just "/api/v2/analysis/component")
workflow_paths=$(echo "$workflow_endpoints" | sed 's/^[A-Z]* *//')

for discovered in "${list_endpoints[@]}"; do
  # Check if any workflow path starts with the discovered path
  # (discovered = "/api/v2/analysis/sbom", workflow path = "/api/v2/analysis/sbom/{id}")
  if ! echo "$workflow_paths" | grep -q "^${discovered}"; then
    echo "⚠️ Warning: Discovered endpoint $discovered not in workflow scope"
  fi
done
```

**Note:** list_endpoints array is stored in shell context for use in Step 8.4.B4 (deferred discovery).

Proceed to Step 6.

### Step 5.3 – Frontend-Only Test Data Prompt

**This step only runs if `analysis_scope = "frontend-only"`.**

Preserve existing behavior for frontend-only analysis:

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

Proceed to Step 6.

## Step 6 – Select Baseline Capture Mode

### Step 6.0 – Check for Existing Baseline Mode

**Apply:** [Common Pattern: Mode Consistency Enforcement](../performance/common-patterns.md#pattern-3-mode-consistency-enforcement)

**Specific actions for this skill:**
- Read `stored_mode` from Step 2.2 metadata extraction
- If `stored_mode` is not null (baseline previously captured):
  - Inform user of stored mode and consistency requirement
  - Offer: use stored mode | reset baseline | cancel
  - If user chooses stored mode, skip Step 5.1-5.3 (mode selection)
  - If user chooses reset, continue to Step 5.1 (new mode selection)
  - If user chooses cancel, stop execution
- If `stored_mode` is null (first baseline), proceed to Step 5.1

### Step 6.1 – Mode Selection

Baseline capture uses **cold-start mode**, which measures first-visit performance with an empty cache by navigating directly to each URL in your scenarios.

> ℹ️ **Baseline Mode:** cold-start
>
> Direct navigation to each URL measures worst-case performance (first-time visitors with cold cache).
> Each iteration starts with a fresh browser context to ensure true cold-start measurement.

Inform user and proceed to Step 6.2.

### Step 6.2 – Read Baseline Settings from Config

**Read baseline capture settings from performance-config.md:**

Extract from the **Baseline Capture Settings** section:
- `iterations` value (should be ≥ 20, as configured by performance-setup)
- `warmup_runs` value (default: 2)

**Validate iterations minimum:**

If `iterations < 20`:
  > ⚠️ **Warning: Insufficient iterations for valid p95 statistics**
  >
  > Configuration specifies {iterations} iterations, but minimum 20 required for meaningful p95.
  > With n={iterations}, p95 equals the {calculated_position}th-highest value, statistically too close to the maximum.
  >
  > Update `.claude/performance-config.md` Baseline Capture Settings to use ≥ 20 iterations, or proceed with limited statistical validity.
  >
  > Continue anyway? (yes/no):

If user chooses "no", stop execution and inform them to update the config.

Store `mode = "cold-start"`
Proceed to Step 7 (Check for Existing Baseline)

## Step 7 – Check for Existing Baseline

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
  
  **Step 7.1 – Read Old Baseline for Comparison**
  
  Read the existing baseline report to extract old metrics for comparison:
  
  ```
  old_baseline_content = Read({baseline-directory}/baseline-report.md)
  ```
  
  Extract aggregate metrics from the **Aggregate Metrics** section of the old report:
  - Old LCP p95: Look for line matching `| LCP | ... | ... | {value} |` and extract p95 value
  - Old FCP p95: Extract similarly from FCP row
  - Old DOM Interactive p95: Extract from DOM Interactive row
  - Old Total Load Time p95: Extract from Total Load Time row
  
  Store these values as:
  ```
  old_metrics = {
    lcp_p95: {extracted_value},
    fcp_p95: {extracted_value},
    domInteractive_p95: {extracted_value},
    totalLoadTime_p95: {extracted_value}
  }
  ```
  
  These values will be used in Step 10.3 for the comparison section.
  
  Proceed to Step 8.

- **If baseline does not exist:** 
  
  Set `old_metrics = null` (no comparison available).
  
  Proceed to Step 8.

## Step 8 – Prepare Capture Script

### Step 8.1 – Locate Plugin Cache Template

The capture script template is located in the plugin cache:

```
{plugin-cache}/sdlc-workflow/{version}/skills/performance/capture-baseline.template.mjs
```

Use the Read tool to verify the template exists at this path. If not found, inform the user:

> "Capture script template not found in plugin cache. This may indicate a corrupted plugin installation. Please reinstall the sdlc-workflow plugin."

Stop execution.

### Step 8.2 – Copy Template to Target Directory

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

### Step 8.3 – Explain Script and Prompt User Review

Before executing the capture script, inform the user about what it does and offer them a chance to review it.

Display the following message:

> ℹ️ **Baseline Capture Script Copied**
>
> The performance measurement script has been copied to:
> ```
> {baseline-directory}/capture-baseline.mjs
> ```
>
> **What this script does:**
> - Reads performance scenarios from `.claude/performance-config.md`
> - Launches a headless Chromium browser in your local environment
> - Navigates to localhost URLs specified in the configuration
> - **Waits for complete page lifecycle:**
>   1. Initial page load (HTML + initial bundle)
>   2. React/framework initialization (2 second buffer)
>   3. All network requests to complete (networkidle - no requests for 500ms)
>   4. Additional 500ms buffer for metric recording
> - Collects standard browser performance metrics using Web APIs:
>   - Navigation Timing API (LCP, FCP, DOM Interactive, Total Load Time)
>   - Resource Timing API (scripts, stylesheets, images, fetch requests)
> - Runs {iterations} iterations per scenario (with {warmup} warmup runs)
> - Outputs aggregated metrics as JSON
>
> **For React/Vue/Angular SPAs:** The script waits for ALL API requests to complete (success or error) before capturing metrics, ensuring lazy-loaded modules and async data fetching are included in measurements.
>
> **Security guarantees:**
> - Only navigates to localhost URLs (127.0.0.0/8, ::1)
> - No remote code execution or credential storage
> - Runs entirely in your local Node.js environment
> - Query strings are stripped from resource URLs (prevents token leakage)
>
> **Would you like to review the script before execution?** (yes/no)

**If user responds "yes":**

Inform the user:
> "You can review the script at: `{baseline-directory}/capture-baseline.mjs`"
>
> "The script is a standard Node.js file that uses Playwright browser automation. It contains detailed inline comments explaining each step."
>
> "When you're ready to proceed, type 'continue'."

Wait for user to type "continue", then proceed to Step 8.

**If user responds "no":**

Proceed directly to Step 8.3.5.

### Step 8.3.5 – Pre-Discovery Application Startup Prompt

Before discovering dev commands, check if the application is already running.

Display the following prompt:

> **Development Environment Check**
>
> How would you like to proceed with application startup?
>
> 1. **Application already running** - I'll provide the URL(s) manually
> 2. **Auto-discovery mode** - Discover and start commands automatically
> 3. **Exit** - Cancel baseline capture
>
> Choose (1/2/3):

**If user chooses "1" (Application already running):**

Read `metadata.analysis_scope` from config to determine which URLs to prompt for:

**Case: `analysis_scope = "frontend-only"`**

Prompt for frontend URL:

> **Frontend URL:**
>
> Where is your frontend running?
>
> 1. Default (http://localhost:3000)
> 2. Custom URL
>
> Choose (1/2):

- If user chooses "1": use `http://localhost:3000`, port `3000`
- If user chooses "2": prompt `Enter your frontend URL:` and validate format (must be http://localhost or http://127.0.0.1)

Extract port from chosen URL and verify it's listening:
```bash
nc -z localhost {port} 2>/dev/null || (echo "" | timeout 2 telnet localhost {port} 2>&1 | grep -q "Connected")
```

If port check fails:
> ❌ Application not running on port {port}
>
> Please start your application and re-run this skill.

Exit skill.

If port check succeeds:
> ✅ Frontend is running on port {port}

Store `frontend_url` and `frontend_port`, then **skip directly to Step 9** (Execute Baseline Capture).

Do NOT proceed to Step 8.4. Stop reading the skill here and jump to Step 9.

---

**Case: `analysis_scope = "backend-only"`**

Prompt for backend URL:

> **Backend URL:**
>
> Where is your backend running?
>
> 1. Default (http://localhost:8080)
> 2. Custom URL
>
> Choose (1/2):

- If user chooses "1": use `http://localhost:8080`, port `8080`
- If user chooses "2": prompt `Enter your backend URL:` and validate format (must be http://localhost or http://127.0.0.1)

Extract port from chosen URL and verify it's listening:
```bash
nc -z localhost {port} 2>/dev/null || (echo "" | timeout 2 telnet localhost {port} 2>&1 | grep -q "Connected")
```

If port check fails:
> ❌ Application not running on port {port}
>
> Please start your application and re-run this skill.

Exit skill.

If port check succeeds:
> ✅ Backend is running on port {port}

Store `backend_url` and `backend_port`, then **skip directly to Step 9** (Execute Baseline Capture).

Do NOT proceed to Step 8.4. Stop reading the skill here and jump to Step 9.

---

**Case: `analysis_scope` in ["full-stack", "full-stack-monorepo"]**

Prompt for backend URL first:

> **Backend URL:**
>
> Where is your backend running?
>
> 1. Default (http://localhost:8080)
> 2. Custom URL
>
> Choose (1/2):

- If user chooses "1": use `http://localhost:8080`, port `8080`
- If user chooses "2": prompt `Enter your backend URL:` and validate format (must be http://localhost or http://127.0.0.1)

Extract port from chosen URL and verify it's listening:
```bash
nc -z localhost {port} 2>/dev/null || (echo "" | timeout 2 telnet localhost {port} 2>&1 | grep -q "Connected")
```

If port check fails:
> ❌ Backend not running on port {port}
>
> Please start your backend and re-run this skill.

Exit skill.

If port check succeeds:
> ✅ Backend is running on port {backend_port}

Then prompt for frontend URL:

> **Frontend URL:**
>
> Where is your frontend running?
>
> 1. Default (http://localhost:3000)
> 2. Custom URL
>
> Choose (1/2):

- If user chooses "1": use `http://localhost:3000`, port `3000`
- If user chooses "2": prompt `Enter your frontend URL:` and validate format (must be http://localhost or http://127.0.0.1)

Extract port from chosen URL and verify it's listening:
```bash
nc -z localhost {port} 2>/dev/null || (echo "" | timeout 2 telnet localhost {port} 2>&1 | grep -q "Connected")
```

If port check fails:
> ❌ Frontend not running on port {port}
>
> Please start your frontend and re-run this skill.

Exit skill.

If port check succeeds:
> ✅ Frontend is running on port {frontend_port}

Store both URLs and ports, then **skip directly to Step 9** (Execute Baseline Capture).

Do NOT proceed to Step 8.4. Stop reading the skill here and jump to Step 9.

---

**If user chooses "2" (Auto-discovery mode):**

Proceed to Step 8.4 (Dev Command Discovery based on analysis scope).

---

**If user chooses "3" (Exit):**

Display:
> Baseline capture cancelled.

Stop execution.

### Step 8.4 – Conditional Dev Command Discovery (Auto-Discovery Mode Only)

**This step only runs if user chose "2" (Auto-discovery mode) in Step 8.3.5.**

Read `metadata.analysis_scope` from config to determine which commands to discover:

- `"frontend-only"` → Discover frontend command only (Case 1)
- `"backend-only"` → Discover backend command only (Case 2)
- `"full-stack"` or `"full-stack-monorepo"` → Discover backend THEN frontend with startup delay (Case 3)

---

#### Case 1: Frontend-Only Discovery (`analysis_scope = "frontend-only"`)

**Step 8.4.F1 – Check if Frontend Command Already Configured**

Read `performance-config.md`. If the Development Environment table shows a Dev Command that is not "TBD" and `dev_command_approved: true`, skip directly to Step 8.4.F3 (Start Frontend).

**Step 8.4.F2 – Discover, Approve, and Save Command**

**Apply:** [Common Pattern: Dev Command Approval](../performance/common-patterns.md#pattern-7-dev-command-approval)

**Part A – Command Discovery (first-match-wins, use Read/Glob tool in `frontend_path`):**

| Priority | Source | What to extract |
|---|---|---|
| 1 | `package.json` | `.scripts.dev` / `.scripts["start:dev"]` / `.scripts.start` → `"npm run dev"` (or `"npm run start"`) |
| 2 | `README.md` / `CONTRIBUTING.md` / `docs/development.md` | First `npm run` or `yarn` line under a "Getting Started" / "Development" / "Running Locally" heading |
| 3 | `Makefile` / `justfile` | First target named `dev`, `start`, or `run` → `make {target}` |
| 4 | Framework config file presence | `rsbuild.config.{ts,js}` or `next.config.{js,ts}` or `vite.config.{ts,js}` → `"npm run dev"` |
| 5 | None found | Ask user: "What command starts the frontend?" (set `doc_source = "Manual user input"`) |

**Part B – Port Discovery (first-match-wins):**

| Priority | Source | How to check |
|---|---|---|
| 1 | `--port=N` or `-p N` flag in the discovered command string | Parse the command string |
| 2 | `.env` / `.env.local` / `.env.development` | Read file → `PORT=N` |
| 3 | Framework config file → `port:` field | Read `rsbuild.config.ts` / `vite.config.ts` / `next.config.js` |
| 4 | Framework default | `rsbuild` or `next` → 3000, `vite` → 5173, other → 3000 |

**Part C – Approval:**

Display to user:

> **Frontend command discovered:**
>
> - **Command:** `{discovered_command}`
> - **Source:** {doc_source}
> - **Port:** {port}
>
> Reply **"approve"**, **"modify: {new command}"**, or **"exit"**.

- `approve` → use `discovered_command` as `final_command`
- `modify: {cmd}` → use provided command as `final_command`; re-derive port if `--port` flag is present in the new command
- `exit` → stop and inform user baseline capture was cancelled

**Part D – Save to Config:**

Compute hash:

```bash
echo -n "{final_command}" | sha256sum | awk '{print $1}'
```

Update the Development Environment table in `performance-config.md`:

| Field | Value |
|---|---|
| Dev Command | `{final_command}` |
| Documentation Source | `{doc_source}` |
| Port | `{port}` |
| Command Approved | `true` |
| Last Validated | `{current UTC timestamp}` |

Set metadata fields: `dev_command_approved: true`, `dev_command_hash: "{computed hash}"`.

> ✅ Frontend command approved and saved to configuration

---

**Step 8.4.F3 – Start Frontend and Verify**

Start the frontend in the background:

```bash
# Use run_in_background: true
cd {frontend_path} && {final_command}
```

Check if the server is up:

```bash
nc -z localhost {port} || curl -sf --head http://localhost:{port}
```

Retry every 2 seconds for up to 60 seconds total.

If not up after 60 seconds:

> Server did not start within 60 seconds. Reply **"wait"** to extend by 30 seconds, or **"abort"** to cancel.

If "wait": extend timeout by 30 seconds and continue checking. If "abort": stop execution.

On success:

> ✅ Frontend is running on port {port}

Proceed to Step 9.

---

#### Case 2: Backend-Only Discovery (`analysis_scope = "backend-only"`)

**Step 8.4.B1 – Check if Backend Command Already Configured**

Read `performance-config.md`. If the Development Environment table shows a Dev Command that is not "TBD" and `dev_command_approved: true`, skip directly to Step 8.4.B3 (Start Backend).

---

**Step 8.4.B2 – Discover, Approve, and Save Command**

**Apply:** [Common Pattern: Dev Command Approval](../performance/common-patterns.md#pattern-7-dev-command-approval)

**Part A – Command Discovery (first-match-wins, use Read/Glob tool in `backend_path`):**

| Priority | Source | What to extract |
|---|---|---|
| 1 | `README.md` / `CONTRIBUTING.md` / `docs/development.md` | First `cargo run`, `mvn`, `gradlew`, `python manage.py`, `uvicorn`, or `npm run start` line under a "Getting Started" / "Development" / "Running Locally" heading |
| 2 | `Cargo.toml` `[[bin]]` sections | 1 binary → `cargo run --bin {name}`; multiple → prefer binary whose name matches the repo directory name; if still ambiguous, ask user to choose |
| 3 | `pom.xml` | `mvnw` present → `./mvnw spring-boot:run`; absent → `mvn spring-boot:run` |
| 4 | `build.gradle` | `./gradlew bootRun` |
| 5 | `manage.py` | `python manage.py runserver` |
| 6 | `pyproject.toml` containing `fastapi` or `uvicorn` | `uvicorn app.main:app --reload` |
| 7 | `package.json` `.scripts.start` or `.scripts.server` | `npm run start` |
| 8 | None found | Ask user: "What command starts the backend?" (set `doc_source = "Manual user input"`) |

**Part B – Port Discovery (first-match-wins):**

| Priority | Source | How to check |
|---|---|---|
| 1 | `--port=N`, `-p N`, or `--bind` flag in the discovered command | Parse the command string |
| 2 | `.env` / `.env.local` | Read file → `PORT=N` |
| 3 | Framework config file → port field | `src/main/resources/application.properties` → `server.port=N`; `settings.py` → `PORT = N` |
| 4 | Framework default | Rust=8080, Spring/Gradle=8080, Django=8000, FastAPI=8000, Node=3001, other=8080 |

**Part C – Approval:**

Display to user:

> **Backend command discovered:**
>
> - **Command:** `{discovered_command}`
> - **Source:** {doc_source}
> - **Port:** {port}
>
> Reply **"approve"**, **"modify: {new command}"**, or **"exit"**.

- `approve` → use `discovered_command` as `final_command`
- `modify: {cmd}` → use provided command as `final_command`; re-derive port if `--port` flag is present in the new command
- `exit` → stop and inform user baseline capture was cancelled

**Part D – Save to Config:**

Compute hash:

```bash
echo -n "{final_command}" | sha256sum | awk '{print $1}'
```

Update the Development Environment table in `performance-config.md`:

| Field | Value |
|---|---|
| Dev Command | `{final_command}` |
| Documentation Source | `{doc_source}` |
| Port | `{port}` |
| Command Approved | `true` |
| Last Validated | `{current UTC timestamp}` |

Set metadata fields: `dev_command_approved: true`, `dev_command_hash: "{computed hash}"`.

> ✅ Backend command approved and saved to configuration

---

**Step 8.4.B3 – Start Backend and Verify**

Start the backend in the background:

```bash
# Use run_in_background: true
cd {backend_path} && {final_command}
```

Check if the server is up:

```bash
nc -z localhost {port} || curl -sf --head http://localhost:{port}
```

Retry every 2 seconds for up to 60 seconds total.

If not up after 60 seconds:

> Server did not start within 60 seconds. Reply **"wait"** to extend by 30 seconds, or **"abort"** to cancel.

If "wait": extend timeout by 30 seconds and continue checking. If "abort": stop execution.

On success:

> ✅ Backend is running on port {port}

**Step 8.4.B4 – Query, Verify, and Confirm Test Data**

**Guard condition:** If `.claude/performance/test-data/manifest.json` already exists from Step 5, skip to B4.2 (Verify).

**B4.1 – Discover list endpoints and generate manifest:**

**Apply:** [Common Pattern: Code Intelligence Strategy](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

**Find:** GET endpoints in `workflow_module_path` that have no path parameters (list/search endpoints — e.g. `/api/v2/products` not `/api/v2/products/{id}`).
**Store:** array of endpoint paths in `list_endpoints`. Store which method was used as `discovery_method`.

Read `workflow_module_path` from the Module Registry in `performance-config.md` (handler file paths → strip filename and line number → common directory).

Generate manifest with a single Shell block:

```bash
mkdir -p .claude/performance/test-data

entries_json="{}"
for endpoint in "${list_endpoints[@]}"; do
  response=$(curl -sf --max-time 10 -H "Accept: application/json" \
    "http://localhost:${port}${endpoint}")
  sample_id=$(echo "$response" | jq -r '
    if type == "array" then .[0]
    else (.items // .data // .results // .content // [])[0]
    end | .id // .uuid // ._id // empty' | head -1)
  test_url=$(echo "$endpoint" | sed "s|{[^}]*}|${sample_id}|g")
  entries_json=$(echo "$entries_json" | jq \
    --arg k "$endpoint" --arg url "$test_url" --arg id "$sample_id" \
    '. + {($k): {endpoint_path: $k, test_url: $url, parameters: {id: $id}}}')
done

jq -n \
  --argjson e "$entries_json" \
  --argjson port "$port" \
  --arg method "$discovery_method" \
  '{generated_at: (now | todate), backend_port: $port, discovery_method: $method, endpoints: $e}' \
  > .claude/performance/test-data/manifest.json
```

**B4.2 – Verify endpoints and display results:**

**Purpose:** Execute real HTTP requests to all discovered endpoints and display results as agent text (not bash echo, which collapses in the UI).

For each endpoint in manifest, run:

```bash
curl -sf -w "\nHTTP:%{http_code}\nTIME:%{time_total}" \
  http://localhost:{port}{test_url}
```

Collect: status code, response time (seconds), and sample data (first item or truncated JSON up to 120 chars).

Then output a markdown table as agent text:

| Endpoint | Status | Time | Sample |
|---|---|---|---|
| /api/v2/products | 200 OK | 0.12s | {count: 42, sample: {id: "abc", ...}} |
| /api/v2/orders | SLOW | 6.3s | {count: 10, sample: {id: "xyz", ...}} |

**Slow/timeout endpoints** (>5s or no response within 10s) → mark **SLOW** or **TIMEOUT** and highlight at top as optimization candidates.
**Auth errors** (401/403) → mark **AUTH ERROR** and note: "Ensure `AUTH_DISABLED=true` in dev command."
**Not found** (404) → mark **NOT FOUND**.
**Zero functional endpoints** → display error and stop.

**B4.3 – Confirm:**

> **Test data verification complete.**
>
> Reply **"yes"** to proceed with baseline capture, **"edit"** to modify the manifest manually, or **"abort"** to cancel.

- `yes` → proceed to Step 9
- `edit` → display path `.claude/performance/test-data/manifest.json`; wait for user to reply "done", then re-run B4.2–B4.3 once
- `abort` → stop execution

Proceed to Step 9.

---

#### Case 3: Full-Stack Discovery (`analysis_scope` in ["full-stack", "full-stack-monorepo"])

**Sequential execution: Backend first, then Frontend.**

**Phase 1: Backend Discovery**

Execute Steps 8.4.B1 through 8.4.B4 from Case 2 using `backend_path`.

**Note:** Step 8.4.B4 (query backend and confirm test data) runs in this phase.

After Step 8.4.B4:

> ✅ Backend is running on port {backend_port}

**Phase 2: Backend Initialization Delay**

Wait 5 seconds for the backend to fully initialise before starting the frontend.

**Note:** Backend was already verified as running in Step 8.4.B3. This delay ensures the backend is ready to handle API requests before the frontend starts.

**Phase 3: Frontend Discovery**

Execute Steps 8.4.F1 through 8.4.F3 from Case 1 using `frontend_path`.

After Step 8.4.F3:

> ✅ Frontend is running on port {frontend_port}
> ✅ Backend is running on port {backend_port}

Proceed to Step 9.

## Step 9 – Execute Baseline Capture

Read `metadata.analysis_scope` from config to determine capture method:

- **If `analysis_scope = "backend-only"`:** Apply Pattern 10 for API benchmarking (Step 9.A below) → skip to Step 10

- **If `analysis_scope = "frontend-only"`:** Proceed to Step 9.1 (browser-based capture) → skip to Step 10

- **If `analysis_scope = "full-stack"` or `"full-stack-monorepo"`:** Execute dual baseline capture (Step 9.B below) → skip to Step 10

**Note:** Full-stack modes capture BOTH frontend (Playwright) and backend (curl/bc) metrics for comprehensive cross-layer analysis.

---

### Step 9.A – API Benchmark Mode (Backend-Only)

**Apply:** [Pattern 10: API Profiling](../performance/common-patterns.md#pattern-10-api-profiling)

Wrap Pattern 10 in a shell function and generate JSON output for baseline report.

```bash
function run_backend_baseline() {
  export CALLER_SKILL="performance-baseline"
  
  # Extract port and iterations from config
  port=$(grep "| Port |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
  iterations=$(grep "| Iterations |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
  
  # Pattern 10 Step A - Check Prerequisites (curl and bc)
  # (Full code from common-patterns.md - see Pattern 10 Step A)
  
  # Pattern 10 Step B - Execute Benchmark with Cache Measurement  
  # (Full code from common-patterns.md - see Pattern 10 Step B)
  
  # After benchmarking completes, generate baseline JSON
  echo "Generating baseline report..."
  
  results_json="{"
  results_json+="\"scenarios\": ["
  
  first=true
  for scenario in "${!dynamic_results[@]}"; do
    result="${dynamic_results[$scenario]}"
    
    [ "$first" = true ] && first=false || results_json+=","
    
    p50=$(echo "$result" | jq -r '.p50_ms')
    p95=$(echo "$result" | jq -r '.p95_ms')
    p99=$(echo "$result" | jq -r '.p99_ms')
    mean=$(echo "$result" | jq -r '.mean_ms')
    test_url=$(echo "$result" | jq -r '.test_url')
    first_req=$(echo "$result" | jq -r '.first_request_ms')
    cache_pct=$(echo "$result" | jq -r '.cache_improvement_pct')
    cache_stat=$(echo "$result" | jq -r '.cache_status')
    
    results_json+=$(cat <<JSON
{
  "name": "$scenario",
  "url": "$test_url",
  "metrics": {
    "responseTime": {
      "mean": $mean,
      "p50": $p50,
      "p95": $p95,
      "p99": $p99
    }
  },
  "cache": {
    "first_request_ms": $first_req,
    "warm_mean_ms": $mean,
    "improvement_pct": $cache_pct,
    "status": "$cache_stat"
  }
}
JSON
)
  done
  
  results_json+="],"
  
  # Calculate aggregate statistics
  declare -a all_p50 all_p95 all_p99 all_mean
  for scenario in "${!dynamic_results[@]}"; do
    result="${dynamic_results[$scenario]}"
    all_p50+=($(echo "$result" | jq -r '.p50_ms'))
    all_p95+=($(echo "$result" | jq -r '.p95_ms'))
    all_p99+=($(echo "$result" | jq -r '.p99_ms'))
    all_mean+=($(echo "$result" | jq -r '.mean_ms'))
  done
  
  agg_p50=$(printf '%s\n' "${all_p50[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
  agg_p95=$(printf '%s\n' "${all_p95[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
  agg_p99=$(printf '%s\n' "${all_p99[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
  agg_mean=$(printf '%s\n' "${all_mean[@]}" | awk '{sum+=$1} END {printf "%.2f", sum/NR}')
  
  results_json+=$(cat <<JSON
"aggregate": {
  "responseTime": {
    "mean": $agg_mean,
    "p50": $agg_p50,
    "p95": $agg_p95,
    "p99": $agg_p99
  }
},
"config": {
  "iterations": $iterations,
  "warmupRuns": 2,
  "mode": "api-benchmark"
}
}
JSON
)
  
  # Write JSON to file
  mkdir -p .claude/performance/baselines
  echo "$results_json" | jq '.' > .claude/performance/baselines/benchmark-results.json
  
  echo "✅ Baseline captured: ${#dynamic_results[@]} endpoint(s)"
  echo "   Results: .claude/performance/baselines/benchmark-results.json"
}

run_backend_baseline

# Check if profiling was skipped
if [ "$skip_dynamic" = "true" ]; then
  echo "⚠️ Cannot generate backend baseline without dynamic profiling."
  echo "   Please ensure backend is running and retry."
  exit 1
fi
```

After Step 9.A completes, proceed to Step 10 (baseline report generation).

---

### Step 9.B – Dual Baseline Capture (Full-Stack Mode)

**This step ONLY runs if `analysis_scope` is "full-stack" or "full-stack-monorepo".**

**Purpose:** Capture BOTH frontend (browser metrics via Playwright) AND backend (API metrics via curl/bc) baselines for comprehensive cross-layer performance analysis.

#### Step 9.B.1 – Frontend Baseline Capture (Playwright)

Execute Steps 9.1-9.3 (Playwright browser automation) as documented below.

**Output:** Save frontend results to intermediate file `{baseline-directory}/baseline-report-frontend.json`

**Note:** This is the same Playwright capture used in frontend-only mode, but we save to a temporary file instead of generating the final report immediately.

#### Step 9.B.2 – Backend Baseline Capture (curl/bc)

Execute Step 9.A (curl/bc API Profiling) to benchmark backend endpoints.

**Output:** Save backend results to `{baseline-directory}/benchmark-results.json`

**Note:** Both frontend and backend baselines use the same port and test data from config.

#### Step 9.B.3 – Merge Baseline Reports

Combine frontend and backend metrics into a single hybrid baseline report:

1. **Read frontend metrics:**
   ```bash
   frontend_lcp_p95=$(jq -r '.aggregate.lcp.p95' {baseline-directory}/baseline-report-frontend.json)
   frontend_fcp_p95=$(jq -r '.aggregate.fcp.p95' {baseline-directory}/baseline-report-frontend.json)
   # ... extract other frontend metrics ...
   ```

2. **Read backend metrics:**
   ```bash
   backend_resp_p95=$(jq -r '.aggregate.response_time.p95' {baseline-directory}/benchmark-results.json)
   backend_throughput=$(jq -r '.aggregate.throughput' {baseline-directory}/benchmark-results.json)
   # ... extract other backend metrics ...
   ```

3. **Generate hybrid baseline report:**
   
   Use `baseline-report.template.md` with `capture_mode = "hybrid"` to generate the final report at `{baseline-directory}/baseline-report.md`.
   
   Include BOTH:
   - **Frontend Performance Metrics section** (LCP, FCP, DOM Interactive, Total Load Time)
   - **Backend API Performance Metrics section** (Response Time, Throughput, Error Rate, Cache Effectiveness)

4. **Update performance-config.md metadata:**
   ```yaml
   metadata:
     baseline_captured: true
     baseline_mode: "hybrid"
     baseline_timestamp: {current-timestamp}
     baseline_commit_sha: {git-commit-sha}
   ```

5. **Preserve both baseline files for downstream skills:**
   
   Keep both `baseline-report.md` (hybrid report for humans) and `benchmark-results.json` (raw backend data for skills) in the baseline directory.
   
   Downstream skills will read:
   - `baseline-report.md` → for frontend metrics
   - `benchmark-results.json` → for backend metrics

After Step 9.B completes, proceed to Step 10 (baseline report generation is already done in 9.B.3).

---

### Step 9.1 – Construct Command

**Auto-detect Config Path:**

The capture script can be run from any subdirectory within the repository. Auto-detect the config by walking up the directory tree (like `git` finds `.git/`):

```bash
config_path=""
current_dir=$(pwd)
max_depth=5  # Prevent infinite loop

for i in $(seq 0 $max_depth); do
  if [ $i -eq 0 ]; then
    check_path=".claude/performance-config.md"
  else
    check_path=$(printf '../%.0s' $(seq 1 $i)).claude/performance-config.md
  fi
  
  if [ -f "$check_path" ]; then
    config_path="$check_path"
    config_dir=$(dirname "$(cd "$(dirname "$check_path")" && pwd)")
    echo "✅ Found config at: $check_path"
    echo "   Repository root: $config_dir"
    break
  fi
done

if [ -z "$config_path" ]; then
  echo "❌ Could not find .claude/performance-config.md"
  echo ""
  echo "Searched from: $current_dir"
  echo "Looked in: current directory and up to $max_depth parent directories"
  echo ""
  echo "This usually means:"
  echo "  • You haven't run /sdlc-workflow:performance-setup yet"
  echo "  • You're in the wrong repository"
  echo ""
  echo "Please run /sdlc-workflow:performance-setup first, then try again."
  exit 1
fi
```

**Why auto-detection:**
- ✅ Works from any subdirectory (e.g., `client/src/`, `docs/`)
- ✅ No trial-and-error with paths
- ✅ Familiar UX pattern (git, npm, cargo all do this)
- ✅ Clear error message if config doesn't exist

Build the command to execute the capture script based on the selected mode from Step 6:

**If mode = `cold-start`:**
```
node {baseline-directory}/capture-baseline.mjs --config "$config_path" --port {port} --mode cold-start
```

Note: The script will read the Performance Scenarios table from the config and measure all configured scenarios. The workflow selection is used for filtering during report generation (Step 8).

### Step 9.2 – Execute Script and Handle Errors

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

### Step 9.3 – Parse JSON Output

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
        "domInteractive": { ... },
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
    "iterations": 20,
    "warmupRuns": 2
  }
}
```

Parse this JSON output and store it for use in Step 8.

## Step 10 – Generate Baseline Report

### Step 10.1 – Determine Report Structure Based on Mode

- **If mode = `cold-start`:** Generate standard baseline report with cold-start metrics

Read the baseline report template from the plugin cache:

```
{plugin-cache}/sdlc-workflow/{version}/skills/performance/baseline-report.template.md
```

### Step 10.2 – Filter Scenarios by Selected Workflow

From the parsed JSON output (Step 9.3), filter scenarios to include only those in the selected workflow's **Key Screens** list.

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

### Step 10.3 – Replace Template Placeholders

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
- `{{domInteractive-mean}}`, `{{domInteractive-p50}}`, `{{domInteractive-p95}}`, `{{domInteractive-p99}}` → From `aggregate.domInteractive`
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

Generate an ASCII waterfall chart for **each scenario** in the filtered list. Create a visual
timeline showing when each resource loaded relative to page start for that scenario.

For each scenario, produce a separate waterfall section in the report under a heading:
```
### Waterfall – {scenario-name}
```

Example format (repeat for every scenario):

```
0ms                 500ms               1000ms              1500ms
|-------------------|-------------------|-------------------|
[====main.js========]                                        (650ms)
  [--styles.css--]                                           (320ms)
    [***logo.png***]                                         (180ms)
    [++++api/data++++]                                       (420ms)
      [====vendor.js========]                                (780ms)
```

Replace `{{waterfall-ascii-chart}}` with the concatenated set of per-scenario waterfall sections.

**Comparison with Previous Baseline:**

If this is a re-baseline (an existing baseline was replaced), use the `old_metrics` values from Step 7.1 to generate a comparison table showing the delta between old and new metrics:

```markdown
## Comparison with Previous Baseline

| Metric | Old p95 | New p95 | Delta | Change |
|--------|---------|---------|-------|--------|
| LCP | {old_metrics.lcp_p95}ms | {new_lcp_p95}ms | {delta}ms | {percentage}% |
| FCP | {old_metrics.fcp_p95}ms | {new_fcp_p95}ms | {delta}ms | {percentage}% |
| DOM Interactive | {old_metrics.domInteractive_p95}ms | {new_domInteractive_p95}ms | {delta}ms | {percentage}% |
| Total Load Time | {old_metrics.totalLoadTime_p95}ms | {new_totalLoadTime_p95}ms | {delta}ms | {percentage}% |
```

Calculate delta as `new_value - old_value` and percentage as `((new_value - old_value) / old_value) * 100`.
Use ↑ emoji for regressions (positive delta) and ↓ emoji for improvements (negative delta).

If `old_metrics = null` (initial baseline), replace `{{comparison-section}}` with:

```markdown
_This is the initial baseline. Future re-baselines will show comparison here._
```

### Step 10.4 – Write Report to File

Write the generated report to the baseline directory:

```
{baseline-directory}/baseline-report.md
```

### Step 10.5 – Update Configuration with Baseline Data

After generating the baseline report, update the performance-config.md with baseline metadata and metrics:

**Step 10.5.1 – Read Current Configuration**

Read `.claude/performance-config.md` from the target repository.

**Step 10.5.2 – Update Metadata Section**

Capture the current git commit SHA with error handling:

```bash
baseline_commit_sha=$(git rev-parse HEAD 2>/dev/null || echo "unknown")

if [ "$baseline_commit_sha" = "unknown" ]; then
  log warning:
  > ⚠️ **Not a git repository or git command unavailable**
  >
  > Baseline commit SHA set to "unknown" - freshness checks will be skipped
  > in performance-implement-optimization.
  >
  > To enable freshness checks, initialize a git repository: `git init`
fi
```

Update the metadata frontmatter with:

```yaml
metadata:
  # ... existing fields ...
  last_updated: {current-timestamp}
  baseline_captured: true
  baseline_mode: {selected-mode from Step 5}
  baseline_timestamp: {current-timestamp}
  baseline_commit_sha: {baseline_commit_sha}  # Will be "unknown" if git unavailable
```

**Step 10.5.3 – Update Optimization Targets (If First Baseline)**

Check the metadata from the config (read in Step 10.5.1) to determine if this is the first baseline:

**If `metadata.baseline_captured: false` or field doesn't exist (first baseline):**

Update the Optimization Targets section:

| Metric | Baseline (p95) | Latest Verified (p95) | Target | Unit | Last Updated |
|---|---|---|---|---|---|
| LCP | **{lcp-p95 from aggregate}** | **{lcp-p95}** | {target} | seconds | **{timestamp}** |
| FCP | **{fcp-p95}** | **{fcp-p95}** | {target} | seconds | **{timestamp}** |
| DOM Interactive | **{domInteractive-p95}** | **{domInteractive-p95}** | {target} | seconds | **{timestamp}** |
| Total Load Time | **{total-p95}** | **{total-p95}** | {target} | seconds | **{timestamp}** |

- Populate **Baseline (p95)** column with p95 metrics from aggregate JSON output
- Set **Latest Verified (p95)** column = Baseline (p95) (initial values match)
- Keep **Target** column unchanged (from setup)
- Set **Last Updated** = current timestamp

**If `metadata.baseline_captured: true` (re-baseline):**

- Leave Baseline column unchanged (baseline is immutable)
- Update Latest Verified (p95) column with new p95 metrics (this is a re-baseline after changes)
- Update Last Updated column with current timestamp

**Step 10.5.4 – Write Updated Configuration**

**Apply:** [Common Pattern: Config Write Protection](../performance/common-patterns.md#pattern-9-config-write-protection)

Write the updated configuration back to `.claude/performance-config.md`.

**Step 10.5.5 – Log Configuration Update**

Log to user:

```
✓ Configuration auto-updated:
  - Baseline mode: {selected-mode}
  - Baseline metrics captured (p95)
  - Commit SHA: {baseline_commit_sha}
  - Last updated: {timestamp}
```

**Note:** This step ensures the configuration is kept in sync with the baseline report, enabling downstream skills to read baseline mode and validate freshness.

## Step 11 – Output Summary

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
> - **DOM Interactive:** {domInteractive-mean} ms (p95: {domInteractive-p95} ms)
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
- If DOM Interactive p95 > 3500ms: "⚠️ DOM Interactive exceeds target (3.5s)"
- If Total Load Time p95 > 4000ms: "⚠️ Total Load Time exceeds target (4.0s)"

## Important Rules

### Execution Integrity
- **Never skip a step** — every step defined above must execute in order, or be explicitly acknowledged as conditionally skipped with a reason output.
- **Never produce partial output** — every defined output (table, summary, file, console message) for a step must be produced completely before moving to the next step.
- **Never auto-answer a blocking prompt** — steps that require user confirmation must pause and wait for an explicit user response.
- **Always announce each step** before executing it using the format: `▶ Step X – <name>`
- **Always confirm step completion** after executing it, including a brief summary of what was produced and what step comes next.

### File and Scope Rules
- Never modify source code files — only create performance measurement artifacts
- Always verify selected workflow exists before proceeding
- Always prompt for test data availability before capturing baseline
- If script execution fails, provide actionable error messages with remediation steps — do not silently continue
- Ensure all URLs are localhost-only for security
- Filter scenarios to include only those in the selected workflow
- Generate waterfall visualization using ASCII art for every scenario — no external dependencies
- If re-baselining (replacing existing baseline), include comparison section with deltas
- Capture script location must be in the baseline directory, not the repository root
