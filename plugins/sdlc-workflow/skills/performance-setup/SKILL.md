---
name: performance-setup
description: |
  Initialize Performance Analysis Configuration in a target repository by discovering routes and modules from the codebase.
argument-hint: "[target-repository-path]"
---

# performance-setup skill

You are an AI performance setup assistant. You analyze a frontend application's codebase to discover user flows and module structure, then generate a Performance Analysis Configuration file that enables performance optimization workflows.

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
  > 1. Update - Re-discover routes/modules and merge with existing config
  > 2. Skip - Keep existing configuration unchanged
  >
  > Choose (1/2):

  If user chooses "2. Skip", stop execution and inform them the existing config will be used.

- **If not exists:** Proceed to Step 3.

## Step 3 – Discover Routes and User Flows

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

Extract:
- Route path (e.g., `/`, `/products/:id`, `/dashboard`)
- Component name or file reference
- Whether the route is lazy-loaded

### Step 3.3 – Categorize Routes

Group discovered routes by type:
- **Static pages** (no dynamic segments like `:id`)
- **List views** (paths suggesting collections, e.g., `/products`, `/users`)
- **Detail views** (paths with dynamic segments, e.g., `/products/:id`)
- **Search/filter pages** (paths with query parameters or filter components)
- **Landing/home** (root path `/`)

Present the categorized routes to the user and ask them to select which routes to include as performance scenarios (suggest 4-8 key routes).

## Step 4 – Discover Module Registry

Identify code-split modules or lazy-loaded routes that can be analyzed individually.

### Step 4.1 – Find Lazy-Loaded Routes

Search for dynamic import patterns:
```
React.lazy\(.*import\(['"]([^'"]+)['"]\)
import\(['"]([^'"]+)['"]\).*\.then\(
loadable\(.*import\(['"]([^'"]+)['"]\)
```

Use Grep or Serena's `search_for_pattern` to find these patterns across the codebase.

### Step 4.2 – Find Build Configuration

Look for build tool configuration that defines code splitting:
- Webpack: `webpack.config.js` — check `optimization.splitChunks` and entry points
- Vite: `vite.config.ts` — check `build.rollupOptions.input` and manual chunks
- Next.js: Automatically splits by page (use pages/ directory structure)

Extract module entry points and chunk names.

### Step 4.3 – Present Module Candidates

Present discovered modules to the user grouped by type:
- **Route-level splits** (lazy-loaded pages)
- **Feature modules** (distinct bundles from build config)
- **Vendor chunks** (third-party library bundles)

Ask the user to select which modules to include in the registry (suggest focusing on route-level and feature modules, not vendor chunks).

## Step 5 – Collect Configuration Values

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

## Step 6 – Generate Configuration File

Read the template from `plugins/sdlc-workflow/skills/performance/performance-config.template.md` in the plugin cache.

Replace placeholders with discovered and collected values:
- `{{scenario-*}}` placeholders → selected routes with descriptive names
- `{{module-*}}` placeholders → selected modules with entry points
- Target metric values → user-provided or defaults
- Baseline capture settings → user-provided or defaults

Remove unused placeholder rows (if user selected fewer scenarios/modules than template slots).

Create target directories if they don't exist:
```bash
mkdir -p .claude/performance/baselines
mkdir -p .claude/performance/analysis
mkdir -p .claude/performance/plans
mkdir -p .claude/performance/verification
```

Write the generated configuration to `.claude/performance-config.md` in the target repository.

## Step 7 – Validate Configuration

After writing the config file:

1. Verify all URL paths are localhost-compatible (no external domains)
2. Verify all module entry points reference actual files (check file exists)
3. Verify target directories were created successfully

If any validation fails, inform the user and offer to fix the issue.

## Step 8 – Output Summary

Report to the user:
- ✅ Performance Analysis Configuration created at `.claude/performance-config.md`
- Number of scenarios configured
- Number of modules registered
- Target directories created

Suggest next steps:
> "Performance setup complete! Next steps:"
>
> "1. Start your application locally (e.g., `npm run dev`)"
> "2. Run the baseline capture:"
>    ```
>    /sdlc-workflow:performance-baseline
>    ```

## Important Rules

- Never modify source code — only create the `.claude/performance-config.md` file
- Always use actual discovered routes and modules — do not invent placeholder examples
- If route discovery finds no results, ask the user to provide route paths manually
- If module discovery finds no results, skip the module registry section (it's optional)
- Validate that discovered routes reference real components/files before including them
- Ensure all URL paths in scenarios are relative (no `http://` or `https://` — they should work with localhost)
