# MCP Tool Catalog

This document describes the MCP servers used by the sdlc-workflow plugin skills. All tool references use the generic naming convention — see your project's CLAUDE.md for concrete instance names.

---

## Jira MCP (Atlassian)

**Purpose:** Task management, issue tracking, and workflow state.

**Tool prefix:** `mcp__atlassian__`

**Access method:** MCP-first with REST API v3 fallback

### Key Operations

| Operation | Tool | Used By |
|---|---|---|
| Fetch issue details | `mcp__atlassian__getJiraIssue` | plan-feature, implement-task |
| Create issue | `mcp__atlassian__createJiraIssue` | plan-feature |
| Edit issue fields | `mcp__atlassian__editJiraIssue` | implement-task |
| Add comment | `mcp__atlassian__addCommentToJiraIssue` | plan-feature, implement-task |
| Transition issue | `mcp__atlassian__transitionJiraIssue` | implement-task |
| Get transitions | `mcp__atlassian__getTransitionsForJiraIssue` | implement-task |
| Create issue link | `mcp__atlassian__createIssueLink` | plan-feature |
| Get current user | `mcp__atlassian__atlassianUserInfo` | implement-task |
| Search issues (JQL) | `mcp__atlassian__searchJiraIssuesUsingJql` | plan-feature |

### REST API Fallback

When Atlassian MCP is unavailable (e.g., due to organizational policies restricting localhost access), skills automatically fall back to JIRA REST API v3.

**How it works:**
1. Skills always try MCP first (preferred method)
2. If MCP fails, user is **always prompted** to choose: Use REST API, Skip JIRA, or Retry MCP
3. If user chooses REST API:
   - Skills check CLAUDE.md for existing REST API credentials
   - If credentials exist: Use them (with user confirmation)
   - If credentials don't exist: Collect from user, validate, and optionally store
4. All operations use `scripts/jira-client.py` (Python stdlib only, no external dependencies)

**Credential storage:**
Credentials are stored in CLAUDE.md under `## Jira Configuration` → `### REST API Credentials (MCP Fallback)`. Users can choose:
- Store all in CLAUDE.md (convenient, less secure)
- Store URL/email only, use `$JIRA_API_TOKEN` env var (recommended, more secure)
- Don't store (ask each time)

**Documentation:**
- Setup guide: `plugins/sdlc-workflow/shared/jira-api-token-guide.md`
- Implementation guide: `plugins/sdlc-workflow/shared/jira-rest-fallback.md`
- Access strategy: `plugins/sdlc-workflow/shared/jira-access-strategy.md`

### ADF Note

Several Jira operations require Atlassian Document Format (ADF) rather than plain text. This applies to:
- Issue descriptions (when using `contentFormat: "adf"`)
- Comments (when using `contentFormat: "adf"`)
- Custom fields (e.g., Git Pull Request custom field)

The REST API fallback automatically converts markdown to ADF when needed.

Refer to your project's CLAUDE.md for field IDs and formatting details specific to your Jira instance.

---

## Figma MCP

**Purpose:** Design inspection during the planning phase.

**Tool prefix:** `mcp__figma__`

### Key Operations

| Operation | Tool | Used By |
|---|---|---|
| Get file structure | `mcp__figma__get_file` | plan-feature |
| Get specific nodes | `mcp__figma__get_nodes` | plan-feature |

### Usage

Figma is used exclusively during `plan-feature` to extract:
- UI structure and component hierarchy
- Components involved in the feature
- Possible backend interactions implied by the design

Figma URLs can be provided as a skill argument or discovered from the Jira issue description.

---

## Serena LSP MCP

**Purpose:** Code intelligence — symbol search, impact analysis, and symbolic editing.

**Tool prefix:** `mcp__<instance>__` where `<instance>` is the Serena instance name from the Repository Registry in your project's CLAUDE.md.

Each target repository has a dedicated Serena MCP server instance. Look up the correct instance name in the **Repository Registry** table of your project's CLAUDE.md.

### Key Operations

| Operation | Tool | Used By |
|---|---|---|
| File/module structure overview | `mcp__<instance>__get_symbols_overview` | plan-feature, implement-task |
| Find symbols by name | `mcp__<instance>__find_symbol` | plan-feature, implement-task |
| Find callers/references | `mcp__<instance>__find_referencing_symbols` | plan-feature, implement-task |
| Search for patterns | `mcp__<instance>__search_for_pattern` | plan-feature, implement-task |
| Replace symbol body | `mcp__<instance>__replace_symbol_body` | implement-task |
| Insert code after symbol | `mcp__<instance>__insert_after_symbol` | implement-task |
| Insert code before symbol | `mcp__<instance>__insert_before_symbol` | implement-task |
| Rename symbol | `mcp__<instance>__rename_symbol` | implement-task |
| Get diagnostics | `mcp__<instance>__get_diagnostics` | setup |

### Workflow

**During planning** (read-only):
1. `get_symbols_overview` — understand module structure without reading entire files
2. `find_symbol` — locate types, functions, endpoints by name
3. `find_referencing_symbols` — discover callers and integration points
4. `search_for_pattern` — find string literals, config keys, route definitions

**During implementation** (read + write):
1. Use the same read operations to understand code before modifying
2. `replace_symbol_body` — rewrite functions, methods, structs, or components
3. `insert_after_symbol` / `insert_before_symbol` — add new code relative to existing symbols
4. `rename_symbol` — rename and automatically update all references

### Fallback

If no Serena instance is available for a repository, skills fall back to Read, Grep, and Glob tools for code inspection, and Edit/Write tools for modification.

### Limitations

Check the **Code Intelligence** > **Limitations** section in your project's CLAUDE.md for per-instance limitations (e.g., language server features that are not supported).

---

## Playwright

**Purpose:** Browser automation for performance baseline capture.

**Installation:**

```bash
npm install -D @playwright/test
npx playwright install
```

**Used By:** performance-baseline skill

### How It Works

The `performance-baseline` skill uses Playwright to:
1. Launch a headless Chromium browser
2. Navigate to each scenario in the selected workflow
3. Measure Web Vitals (LCP, FCP, TTI) and total load time
4. Capture resource timing (scripts, stylesheets, images)
5. Generate a baseline report with metrics and waterfall visualization

**Baseline Capture Mode:**

Baseline capture uses **cold-start mode**: direct URL navigation with empty browser cache using Playwright. This measures worst-case (first-visit) performance and provides stable, reproducible baseline metrics.

### Requirements

- **Application running:** The target application must be running on localhost before capturing baseline
- **Test data loaded:** Scenarios must have test data available for accurate measurements
- **Valid URLs:** Scenario URLs must be valid localhost addresses (e.g., `http://localhost:3000/home`)

### Graceful Degradation

If Playwright is not installed or cannot run, the skill:
1. Detects the missing dependency
2. Provides installation instructions
3. Offers to exit gracefully and resume after installation

**Alternative:** Manual performance testing using browser DevTools and manual metric recording (skill does not support this flow, but users can capture baseline manually if needed).
