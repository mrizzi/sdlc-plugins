---
name: performance-baseline
description: |
  Discover workflows from the codebase, prompt user to select a target workflow, auto-populate configuration, then capture performance baseline metrics via browser automation and generate a baseline report.
argument-hint: "[target-repository-path]"
---

# performance-baseline skill

You are an AI performance baseline assistant. When no workflow has been selected yet, you discover user workflows from the codebase (by reading router configuration and inferring user journeys), prompt the user to select a target workflow, and auto-populate the Performance Scenarios and Module Registry in `performance-config.md`. Once a workflow is selected, you verify test data availability, execute browser automation to measure page load times and resource loading, and generate a baseline report for comparison during optimization.

## Guardrails

- This skill creates files in designated performance directories (`.claude/performance/baselines/`)
- This skill does NOT modify source code files — only creates performance measurement artifacts
- This skill requires Performance Analysis Configuration with a selected workflow

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

**Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-7-workflow-validation)

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

### Step 3.1 – Locate API Route Definitions

Search backend codebase for API endpoint definitions using framework-specific patterns.

**Read backend configuration from config:**
```bash
backend_path=$(grep "Backend Path" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
backend_framework=$(grep "Backend Framework" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
serena_instance=$(grep "Serena Instance" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
```

**Framework-specific search patterns:**

| Framework | Pattern | Example |
|---|---|---|
| actix-web (Rust) | `#\[get\("`, `#\[post\("`, `web::scope` | `#[get("/api/v2/products")]` |
| axum (Rust) | `Router::new\(\)`, `.route\("`, `get\(`, `post\(` | `.route("/api/v2/products", get(handler))` |
| poem (Rust) | `#\[handler\]`, `.at\("`, `Route::new\(\)` | `.at("/api/v2/products", get(handler))` |
| Spring Boot (Java) | `@RestController`, `@GetMapping`, `@PostMapping` | `@GetMapping("/api/v2/products")` |
| FastAPI (Python) | `@app.get`, `@router.post`, `APIRouter` | `@app.get("/api/v2/products")` |
| Express (Node) | `app.get\(`, `router.post\(`, `express.Router\(\)` | `app.get('/api/v2/products', ...)` |

**Discovery approach:**

**If Serena is available (serena_instance != "none"):**
1. Use `mcp__{serena_instance}__find_symbol` with pattern matching for framework decorators/macros
2. Extract: HTTP method, path pattern, handler function name, file location

**If Serena is not available:**
1. Use Grep to search for framework patterns in backend_path:
   ```bash
   # Example for Rust actix-web
   grep -r "#\[get\(\|#\[post\(\|#\[put\(\|#\[delete\(" "$backend_path/src"
   
   # Example for Java Spring Boot
   grep -r "@GetMapping\|@PostMapping\|@PutMapping\|@DeleteMapping" "$backend_path/src"
   ```
2. Parse results to extract: HTTP method, path, handler function

**Extract for each endpoint:**
- HTTP method (GET, POST, PUT, DELETE, PATCH)
- Path pattern (e.g., `/api/v2/products`, `/api/v2/products/{id}`)
- Handler function name
- File location (absolute path)

**Store endpoints in array for grouping in Step 3.2**

### Step 3.1.1 – Validate Endpoint Safety (Impact Analysis)

**For each discovered endpoint, apply impact analysis:**

**If Serena is available:**
1. Use `mcp__{serena_instance}__find_referencing_symbols` on the handler function
2. Count number of references (callers)
3. Classify impact:
   - **Low impact:** < 5 references
   - **Medium impact:** 5-10 references
   - **High impact:** > 10 references

**If Serena is not available:**
1. Use Grep to search for handler function name across codebase
2. Count occurrences
3. Classify impact using same thresholds

**Store impact classification with each endpoint:**
```
endpoint {
  path: "/api/v2/products/{id}"
  method: "GET"
  handler: "get_product_by_id"
  references: 12
  impact: "high"
}
```

**Warning to user:** High-impact endpoints will be flagged during workflow selection (Step 3.3).

### Step 3.2 – Group Endpoints into Workflows

Group discovered endpoints into logical workflows using resource-based grouping.

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

### Step 3.3 – Present Workflows and Prompt Selection

Display discovered backend workflows:

```
## Discovered Backend Workflows

| # | Workflow Name | Entry Endpoint | Key Endpoints | Complexity | Impact |
|---|---|---|---|---|---|
| 1 | Product Management | GET /api/v2/products | GET /products, GET /products/{id}, POST /products | Moderate | Medium (23 refs) |
| 2 | Order Management | GET /api/v2/orders | GET /orders, POST /orders, PUT /orders/{id} | Complex | High (45 refs) |
```

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

**If Serena is available:**
1. Use `mcp__{serena_instance}__get_symbols_overview` on handler files
2. Extract functions/methods related to selected workflow endpoints

**If Serena is not available:**
1. Use Grep to find handler functions in endpoint file locations
2. Extract function signatures

**Result:** Module registry with handler functions as entries.

### Step 3.6 – Update Config with Backend Workflow Selection

Update `.claude/performance-config.md`:

1. **Performance Scenarios section:** Replace table with generated scenarios from Step 3.4
2. **Module Registry section:** Replace table with discovered handlers from Step 3.5
3. **Selected Workflow section:** Add selected workflow details

**Set metadata fields:**
```yaml
metadata:
  workflow_selected: true
  backend_endpoint_discovery_method: "serena" | "grep"
```

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

### Step 4.2 – Extract Route Definitions **(Workflow Discovery Only — skip if metadata.workflow_selected = true)**

For each router configuration file found:

**If Serena is available:**
- Use `get_symbols_overview` to list route definitions
- Use `find_symbol` with `include_body=true` to read route arrays or objects

**If Serena is not available:**
- Use Read tool to examine router files
- Use Grep to search for route path patterns:
  ```
  path:\s*['"]([^'"]+)['"]
  <Route\s+path=['"]([^'"]+)['"]
  ```

Extract for each route:
- Route path (e.g., `/`, `/products/:id`, `/dashboard`)
- Component name or file reference
- Whether the route is lazy-loaded

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

#### Step 4.3.3 – Estimate Workflow Complexity

For each inferred workflow:

**Calculate complexity based on:**
- Number of routes in workflow:
  - 1-2 routes = Simple
  - 3-4 routes = Moderate  
  - 5+ routes = Complex
- Number of components in workflow pages:
  - Count `.tsx`/`.ts` files in page directories for this workflow
- Presence of API calls:
  - Search for `useQuery`, `useMutation`, `fetch`, `axios` in workflow components
  - Estimate API call count

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

### Step 4.4 – Present Workflows and Prompt Selection (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).


Display discovered workflows:


```
## Discovered Workflows

| # | Workflow Name | Entry Point | Key Screens | Complexity |
|---|---|---|---|---|
| {{workflow entries}} |
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

### Step 4.7 – Update Config with Workflow Selection (Workflow Discovery Only)

**This step only runs if metadata.workflow_selected = false** (determined in Step 2.0).

After workflow selection, update the performance configuration file with the selected workflow, scenarios, and modules.

Read `.claude/performance-config.md` from the target repository.

**Update sections:**

1. **Performance Scenarios** — replace empty table with generated scenarios from Step 4.5
2. **Module Registry** — replace empty table with discovered modules from Step 4.6
3. **Selected Workflow** — replace empty section with selected workflow details from Step 4.4:
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

4. **Metadata:**
   - `workflow_selected`: true
   - `last_updated`: {current-timestamp}

**Apply:** [Common Pattern: Config Write Protection](../performance/common-patterns.md#pattern-10-config-write-protection)

Write updated config back to file.

**Log to user:**
```
✓ Configuration updated with selected workflow: {workflow-name}
  - Scenarios: {count} auto-populated
  - Modules: {count} discovered
```

After this step, proceed to Step 4 (Verify Test Data Availability).

## Step 5 – Verify Test Data Availability

**Note:** This is the continuation point whether workflow was just selected (Step 4.7) or was already selected (Step 2.1).

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

### Step 6.2 – Configure Baseline Settings

**Prompt for baseline capture settings:**

> "Baseline Capture Settings:"
>
> - **Iterations** (default: 10, minimum: 10 for meaningful p95 statistics)
> - **Warmup runs** (default: 3)
>
> **Note:** p95 statistics require at least 10 iterations to be distinct from the maximum value. 
> Use 20+ iterations for stable inter-run comparisons.

Store mode: `cold-start`
Proceed to Step 6 (Check for Existing Baseline)

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
  
  Proceed to Step 7.

- **If baseline does not exist:** Proceed to Step 7.

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

Proceed directly to Step 7.4.

### Step 8.4 – Dev Command Discovery and Approval

**Purpose:** Auto-discover dev mode command, get user approval, and verify application is running before baseline capture.

**This step is skipped for backend-only mode** (no browser automation required).

**Apply:** [Common Pattern: Dev Command Approval](../performance/common-patterns.md#pattern-8-dev-command-approval)

**Specific actions for this skill:**

#### Step 7.4.1 – Check if Dev Command Already Configured

Read config to check if dev command is already approved:

```bash
if grep -q "## Development Environment" .claude/performance-config.md; then
  dev_command=$(grep "Dev Command" .claude/performance-config.md | grep -v "TBD" | awk -F'|' '{print $3}' | xargs)
  command_approved=$(grep "dev_command_approved:" .claude/performance-config.md | awk '{print $2}')
  command_hash=$(grep "dev_command_hash:" .claude/performance-config.md | awk '{print $2}' | tr -d '"')
  
  if [ -n "$dev_command" ] && [ "$dev_command" != "TBD" ]; then
    # Calculate current hash
    current_hash=$(echo -n "$dev_command" | sha256sum | awk '{print $1}')
    
    # If command unchanged and already approved, skip discovery
    if [ "$command_approved" = "true" ] && [ "$current_hash" = "$command_hash" ]; then
      echo "ℹ️ Dev command already approved: $dev_command"
      skip_discovery=true
    fi
  fi
fi
```

If `skip_discovery=true`, jump to Step 7.4.7 (Verify Application is Running).

#### Step 7.4.2 – Discover Dev Command

Search for dev mode command in multiple sources (priority order):

**1. package.json scripts:**
```bash
if [ -f "package.json" ]; then
  dev_script=$(jq -r '.scripts.dev // .scripts.start // .scripts.serve // "null"' package.json)
  if [ "$dev_script" != "null" ]; then
    discovered_command="npm run dev"
    doc_source="package.json (scripts.dev)"
  fi
fi
```

**2. README.md / CONTRIBUTING.md:**
Look for "Getting Started", "Development", "Running Locally" sections:
```bash
for readme in README.md CONTRIBUTING.md docs/development.md; do
  if [ -f "$readme" ] && [ -z "$discovered_command" ]; then
    # Extract commands from markdown code blocks
    discovered_command=$(grep -A 5 "Getting Started\|Development\|Running Locally" "$readme" | grep "npm run\|yarn dev\|cargo run" | head -1 | sed 's/[$`]//')
    if [ -n "$discovered_command" ]; then
      doc_source="$readme"
      break
    fi
  fi
done
```

**3. Makefile / justfile:**
```bash
for makefile in Makefile justfile; do
  if [ -f "$makefile" ] && [ -z "$discovered_command" ]; then
    target=$(grep "^dev:\|^start:\|^run:" "$makefile" | head -1 | sed 's/:.*//')
    if [ -n "$target" ]; then
      discovered_command="make $target"
      doc_source="$makefile"
      break
    fi
  fi
done
```

**4. Framework defaults:**
```bash
if [ -z "$discovered_command" ]; then
  if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    discovered_command="npm run dev"
    doc_source="Next.js framework default"
  elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    discovered_command="npm run dev"
    doc_source="Vite framework default"
  elif [ -f "Cargo.toml" ]; then
    discovered_command="cargo run"
    doc_source="Rust framework default"
  elif [ -f "pom.xml" ]; then
    discovered_command="mvn spring-boot:run"
    doc_source="Spring Boot framework default"
  elif [ -f "manage.py" ]; then
    discovered_command="python manage.py runserver"
    doc_source="Django framework default"
  fi
fi
```

**If no command found:**
```bash
if [ -z "$discovered_command" ]; then
  echo "⚠️ Could not auto-discover dev command from package.json, README, Makefile, or framework conventions."
  echo "Please enter the command to start your application:"
  read -p "> " discovered_command
  doc_source="Manual user input"
fi
```

#### Step 7.4.4 – Extract Port Number

Extract port from multiple sources (priority order):

**1. Command flags:**
```bash
if echo "$discovered_command" | grep -qE -- "--port|-p"; then
  port=$(echo "$discovered_command" | grep -oE -- "--port[= ]([0-9]+)|-p[= ]([0-9]+)" | grep -oE "[0-9]+")
fi
```

**2. Environment files:**
```bash
if [ -z "$port" ]; then
  for envfile in .env .env.local .env.development; do
    if [ -f "$envfile" ]; then
      port=$(grep "^PORT=" "$envfile" | cut -d= -f2)
      [ -n "$port" ] && break
    fi
  done
fi
```

**3. Config files:**
```bash
if [ -z "$port" ]; then
  if [ -f "vite.config.ts" ]; then
    port=$(grep "port:" vite.config.ts | grep -oE "[0-9]+" | head -1)
  elif [ -f "next.config.js" ]; then
    port=$(grep "port:" next.config.js | grep -oE "[0-9]+" | head -1)
  fi
fi
```

**4. Framework defaults:**
```bash
if [ -z "$port" ]; then
  if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    port=3000
  elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    port=5173
  elif [ -f "Cargo.toml" ]; then
    port=8080
  elif [ -f "pom.xml" ]; then
    port=8080
  elif [ -f "manage.py" ]; then
    port=8000
  else
    port=3000
  fi
fi
```

#### Step 7.4.5 – Explain and Prompt for Approval

Display to user:

> ℹ️ **Development Mode Command Discovered**
>
> **Command:** `{discovered_command}`
>
> **Source:** {doc_source}
>
> **Port:** {port}
>
> **What this command does:**
> - Starts application in development mode
> - Runs on port {port} (http://localhost:{port})
>
> **Security guarantees:**
> - Runs in your local environment only
> - No credentials required
> - Standard development tooling
>
> **Documentation reference:** {doc_source}
>
> **Additional instructions (optional):**
> Enter modifications (e.g., "AUTH_DISABLED=true npm run dev") or press Enter to use as-is:

Read user input:
```bash
read -p "> " user_modifications

if [ -n "$user_modifications" ]; then
  final_command="$user_modifications"
else
  final_command="$discovered_command"
fi
```

Display final command and request approval:
> **Final command:** `{final_command}`
>
> Approve this command? (yes/no)

```bash
read -p "> " approval

if [ "$approval" != "yes" ]; then
  echo "❌ Command not approved. Please start your application manually."
  echo "After starting your application, re-run this skill."
  exit 1
fi
```

#### Step 7.4.6 – Update Config with Approved Command

Calculate SHA-256 hash for change detection:
```bash
command_hash=$(echo -n "$final_command" | sha256sum | awk '{print $1}')
current_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
```

Update Development Environment section in config:
```bash
# Update table values in Development Environment section
sed -i "/## Development Environment/,/^##/ s/| Dev Command | TBD |/| Dev Command | $final_command |/" .claude/performance-config.md
sed -i "/## Development Environment/,/^##/ s/| Documentation Source | TBD |/| Documentation Source | $doc_source |/" .claude/performance-config.md
sed -i "/## Development Environment/,/^##/ s/| Port | TBD |/| Port | $port |/" .claude/performance-config.md
sed -i "/## Development Environment/,/^##/ s/| Command Approved | false |/| Command Approved | true |/" .claude/performance-config.md
sed -i "/## Development Environment/,/^##/ s/| Last Validated | - |/| Last Validated | $current_timestamp |/" .claude/performance-config.md
```

Update metadata:
```bash
sed -i "s/dev_command_approved: false/dev_command_approved: true/" .claude/performance-config.md
sed -i "s/dev_command_hash: null/dev_command_hash: \"$command_hash\"/" .claude/performance-config.md
```

Echo success:
> ✅ Dev command approved and saved to configuration

#### Step 7.4.7 – Verify Application is Running

Display manual start instructions:

> **Please start your application manually:**
>
> ```
> {final_command}
> ```
>
> Wait for successful start (watch for "ready", "listening", or similar message), then press Enter to continue...

```bash
read -p ""
```

Verify port is listening:
```bash
echo "Verifying application is running on port $port..."

if nc -z localhost $port 2>/dev/null || (echo "" | telnet localhost $port 2>&1 | grep -q "Connected"); then
  echo "✅ Application is running on port $port"
else
  echo "❌ Application not running on port $port"
  echo ""
  echo "Please:"
  echo "1. Start your application: $final_command"
  echo "2. Wait for it to fully start"
  echo "3. Re-run this skill"
  exit 1
fi
```

Proceed to Step 8.

## Step 9 – Execute Baseline Capture

### Step 9.1 – Construct Command

Build the command to execute the capture script based on the selected mode from Step 6:

**If mode = `cold-start`:**
```
node {baseline-directory}/capture-baseline.mjs --config {path-to-performance-config.md} --port {port} --mode cold-start
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
    "iterations": 5,
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

If this is a re-baseline (an existing baseline was replaced), include a comparison section showing the delta between old and new metrics. Otherwise, replace `{{comparison-section}}` with:

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

Check if the Optimization Targets table has "TBD" in the Baseline (p95) column:

**If Baseline column = "TBD" (first baseline):**

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

**If Baseline column already has values (re-baseline):**

- Leave Baseline column unchanged (baseline is immutable)
- Update Latest Verified (p95) column with new p95 metrics (this is a re-baseline after changes)
- Update Last Updated column with current timestamp

**Step 10.5.4 – Write Updated Configuration**

**Apply:** [Common Pattern: Config Write Protection](../performance/common-patterns.md#pattern-10-config-write-protection)

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

- Never modify source code files — only create performance measurement artifacts
- Always verify selected workflow exists before proceeding
- Always prompt for test data availability before capturing baseline
- If script execution fails, provide actionable error messages with clear remediation steps
- Ensure all URLs are localhost-only for security
- Filter scenarios to include only those in the selected workflow
- Generate waterfall visualization using ASCII art for every scenario — no external dependencies
- If re-baselining (replacing existing baseline), include comparison section with deltas
- Capture script location must be in the baseline directory, not the repository root
