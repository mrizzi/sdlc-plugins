---
name: performance-setup
description: |
  Initialize Performance Analysis Configuration by discovering workflows from the codebase, selecting a target workflow, and auto-populating scenarios and modules.
argument-hint: "[target-repository-path]"
---

# performance-setup skill

You are an AI performance setup assistant. You analyze a frontend application's codebase to discover user workflows (user journeys), prompt the user to select a workflow to optimize, then auto-populate performance scenarios and modules based on that workflow.

## Guardrails

- This skill creates ONE file: `.claude/performance-config.md` in the target repository
- This skill is **idempotent** — running it multiple times on an already-configured repository offers to update or skip
- This skill does NOT modify source code — only creates/updates the performance configuration file

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Detect Existing Configuration

Check if `.claude/performance-config.md` already exists in the target repository.

- **If exists:** Read the file and inform the user:
  > "Performance Analysis Configuration already exists. Would you like to update it or skip setup?"
  >
  > Options:
  > 1. Update - Re-discover workflows and regenerate configuration
  > 2. Skip - Keep existing configuration unchanged
  >
  > Choose (1/2):

  If user chooses "2. Skip", stop execution and inform them the existing config will be used.

- **If not exists:** Proceed to Step 3.

## Step 3 – Discover Routes from Router Configuration

Analyze the frontend codebase to discover routes using Serena (if available) or Read/Grep/Glob.

### Step 3.1 – Find Router Configuration

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

### Step 3.2 – Extract Route Definitions

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

## Step 4 – Infer Workflows from Routes

Group discovered routes into functional workflows (user journeys). A workflow is a sequence of related pages that form a cohesive user task.

### Step 4.1 – Read Navigation Structure

Examine the application's navigation to understand primary workflows:

Use Grep to find navigation/sidebar components:
```
pattern: nav|menu|sidebar|NavItem
path: src/
```

If found, read the navigation component to identify top-level navigation items. These often represent primary workflows.

### Step 4.2 – Group Routes by Workflow

Apply these grouping strategies to infer workflows:

**1. Path prefix grouping** — routes sharing a common prefix likely form a workflow:
- `/sbom/*` routes → "SBOM Management" workflow
- `/advisory/*` routes → "Advisory Management" workflow  
- `/package/*` routes → "Package Investigation" workflow

**2. List-to-detail patterns** — list view + detail view form a browse workflow:
- `/advisories` + `/advisories/:id` → "Advisory Browse and Detail" workflow
- `/packages` + `/packages/:id` → "Package Browse and Detail" workflow

**3. Feature module grouping** — routes in the same feature directory:
- Examine `src/pages/` or `src/features/` directory structure
- Group routes by their page directory (e.g., all routes using components from `src/pages/sbom-*` form an SBOM workflow)

**4. Upload/action workflows** — upload + scan + view patterns:
- `/sboms/upload`, `/sboms/scan`, `/sboms/:id` → "SBOM Upload and Analysis" workflow

### Step 4.3 – Estimate Workflow Complexity

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
- Workflow name (descriptive, e.g., "SBOM Browse and Detail")
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
> "You can manually create a configuration by editing `.claude/performance-config.md` after this skill completes."

If no workflows found, create a minimal config with empty scenarios and ask user to fill manually. Then stop execution.

## Step 5 – Present Workflows and Prompt User Selection

Display discovered workflows in a formatted table.

**Example output:**

```
## Discovered Workflows

| # | Workflow Name | Entry Point | Key Screens | Complexity |
|---|---|---|---|---|
| 1 | Product Catalog Browse | /products | /products, /products/:productId | Moderate (15 components, 2 API calls) |
| 2 | Order Management | /orders | /orders, /orders/:orderId | Moderate (12 components, 3 API calls) |
| 3 | User Profile | /profile | /profile, /profile/settings | Simple (8 components, 1 API call) |
```

**Note:** The actual workflows discovered will depend on your application's routes. The table above shows the format for an e-commerce application; your application may have different domains (finance, healthcare, content management, etc.).

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

## Step 6 – Auto-Populate Scenarios from Selected Workflow

Based on the selected workflow's key screens, automatically generate performance scenarios.

For each route in the workflow's key screens:

**Extract scenario details:**
- Scenario name: Derive from route path (e.g., `/sboms` → `sbom-list`, `/sboms/:sbomId` → `sbom-details`)
- URL path: Use the route path
- Description: Generate from route purpose (e.g., "SBOM list view with filtering and pagination")

**Scenario name derivation rule:**
```
path.split('/').filter(Boolean).map(s => s.startsWith(':') ? s.slice(1) : s).join('-')
```

**Handle dynamic route segments:**
- For routes with `:id` or other parameters, note in the scenario that a sample ID will be needed during baseline capture

**Result:** A table of scenarios that exactly matches the selected workflow's key screens.

## Step 7 – Discover Modules for Selected Workflow

Identify code-split modules or lazy-loaded routes for the selected workflow's pages.

### Step 7.1 – Find Lazy-Loaded Components

For each route in the selected workflow:

Search for the component referenced by the route in the router configuration.

Check if it's lazy-loaded:
```
React.lazy\(.*import\(['"]([^'"]+)['"]\)
import\(['"]([^'"]+)['"]\).*\.then\(
loadable\(.*import\(['"]([^'"]+)['"]\)
```

### Step 7.2 – Extract Module Entry Points

For each lazy-loaded component in the workflow:

**Determine module entry point:**
- Look for `index.ts` or `index.tsx` in the component's directory
- If not found, use the lazy-loaded file path as the entry point

**Derive module name:**
- Use the page directory name (e.g., `src/app/pages/product-list` → module name: `product-list`)

**Generate module description:**
- Describe the module's purpose based on the route and component name

**Result:** A table of modules corresponding to the selected workflow's pages.

## Step 7.5 – Discover Backend Repository (Optional)

Check if a backend repository is configured in the Project Configuration.

### Step 7.5.1 – Check for Repository Registry

Read CLAUDE.md in the target repository and look for the `## Repository Registry` section.

If found, extract repositories where the "Role" column contains "backend" or "api" or "server" (case-insensitive).

If no Repository Registry found or no backend repositories found, skip to Step 8.

### Step 7.5.2 – Prompt User for Backend Configuration

If backend repository candidates found, ask the user:

> "I found the following backend repository candidates:
>
> 1. {{repo-1-name}} — {{role}} (Serena: {{instance or 'none'}})
> 2. {{repo-2-name}} — {{role}} (Serena: {{instance or 'none'}})
>
> Would you like to enable backend source code analysis for comprehensive over-fetching detection and backend anti-pattern detection?
>
> Options:
> 1. Yes - Configure backend repository
> 2. No - Frontend-only analysis"

**If user selects "Yes":**

1. **Select repository** (if multiple candidates):
   - Prompt: "Enter the number of the backend repository to use (1-N):"
   - Validate selection

2. **Ask for backend framework type:**
   - Prompt: "What backend framework does this repository use?"
   - Provide examples: actix-web, axum, spring-boot, express, fastapi, django, rails, asp.net
   - Validate input (any text accepted, but suggest common frameworks)

3. **Ask for API base path:**
   - Prompt: "What is the API base path? (default: /api/v2)"
   - If empty, use `/api/v2` as default
   - Validate path starts with `/`

4. **Verify Serena instance availability:**
   - Check if the backend repo has a Serena instance configured
   - If yes: Note that full analysis will use Serena for accurate handler location and schema extraction
   - If no: Note that analysis will fall back to Grep-based search (less accurate but functional)

5. **Store backend configuration values:**
   - Backend repository name
   - Backend absolute path (from Repository Registry)
   - Backend framework
   - Serena instance name (or "none")
   - API base path

**If user selects "No" or no backend repos found:**
- Skip backend configuration
- Set `backend_configured = false`
- Continue with frontend-only analysis

## Step 8 – Collect Configuration Values

Prompt the user for:

**Baseline Capture Settings:**
- Iterations (default: 5)
- Warmup runs (default: 2)
- Confirm metrics to collect (default: LCP, FCP, TTI, Total Load Time, Resource Timing)

**Optimization Targets:**
- LCP target (default: 2.5s, Google's "Good" threshold)
- FCP target (default: 1.8s)
- TTI target (default: 3.5s)
- Total Load Time target (default: 4.0s)

Explain that Current (Baseline) values will be filled in automatically after running the `performance-baseline` skill.

Offer choice:
> "Use recommended defaults? (yes/no)"

If yes, skip prompts and use defaults. If no, prompt for each value.

## Step 9 – Generate Configuration File

Read the template from `plugins/sdlc-workflow/skills/performance/performance-config.template.md` in the plugin cache.

**Generate configuration with:**

1. **Performance Scenarios section** — populated with scenarios from Step 6
2. **Baseline Capture Settings section** — populated with values from Step 8
3. **Target Directories section** — standard directories
4. **Optimization Targets section** — populated with targets from Step 8
5. **Module Registry section** — populated with modules from Step 7
6. **Backend Repository Configuration section** — populated with backend values from Step 7.5 (if configured), otherwise use placeholder text "Not Configured"
7. **Selected Workflow section** — workflow details from Step 5

**Workflow section format:**

```markdown
## Selected Workflow

The following workflow has been selected for performance optimization:

| Property | Value |
|---|---|
| Workflow Name | {selected workflow name} |
| Entry Point | {entry point URL} |
| Key Screens | {comma-separated list of key screens} |
| Complexity | {complexity estimate} |
| Selected On | {current date in YYYY-MM-DD format} |
```

Create target directories if they don't exist:
```bash
mkdir -p .claude/performance/baselines
mkdir -p .claude/performance/analysis
mkdir -p .claude/performance/plans
mkdir -p .claude/performance/verification
```

Write the generated configuration to `.claude/performance-config.md` in the target repository.

## Step 10 – Validate Configuration

After writing the config file:

1. Verify all URL paths are localhost-compatible (no external domains)
2. Verify all module entry points reference actual files (check file exists)
3. Verify target directories were created successfully
4. Verify scenario URLs match the selected workflow's key screens

If any validation fails, inform the user and offer to fix the issue.

## Step 11 – Output Summary

Report to the user:

> ✅ **Performance Analysis Configuration created!**
>
> **Selected Workflow:** {workflow name}
> **Complexity:** {complexity}
> **Scenarios configured:** {count} (auto-populated from workflow)
> **Modules registered:** {count} (auto-populated from workflow pages)
>
> **Configuration saved to:** `.claude/performance-config.md`
>
> **Next Steps:**
>
> 1. **Load test data** — Ensure your application has test data for this workflow to enable consistent measurements
> 2. **Start your application** — Run your dev server (e.g., `npm run dev`)
> 3. **Capture baseline:**
>    ```
>    /sdlc-workflow:performance-baseline
>    ```

## Important Rules

- Never modify source code — only create the `.claude/performance-config.md` file
- Always use actual discovered routes and modules — do not invent placeholder examples
- Scenarios and modules are **automatically derived** from the selected workflow — do not ask user to select scenarios separately
- If route discovery finds no results, create minimal config and inform user to edit manually
- If module discovery finds no results, scenarios are still valid (modules section can be empty)
- Validate that discovered routes reference real components/files before including them
- Ensure all URL paths in scenarios are relative (no `http://` or `https://` — they should work with localhost)
- Present workflows in order of estimated business value/traffic (if determinable from route names)
