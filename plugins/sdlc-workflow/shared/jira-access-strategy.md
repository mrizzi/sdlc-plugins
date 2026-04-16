# JIRA Access Strategy

This document defines how sdlc-workflow skills interact with JIRA for issue management.

## Quick Summary

**For Users**: When prompted for JIRA credentials, see `shared/jira-api-token-guide.md` for detailed instructions on:
- How to generate an API token
- What information you need to provide
- How to test your credentials
- Security best practices

**For Developers**: This document contains the implementation strategy for JIRA access in sdlc-workflow skills.

---

## Access Method Priority

1. **Primary: Atlassian MCP** (Model Context Protocol)
2. **Fallback: Atlassian Cloud REST API v3** (with user confirmation)

## Method 1: Atlassian MCP (Preferred)

The Atlassian MCP provides direct integration with JIRA through Claude Code's MCP system.

### When to Use MCP

- MCP is available when configured in Claude Code settings
- Provides better error handling and type safety
- Automatically handles authentication
- Recommended for all JIRA operations

## Method 2: Atlassian Cloud REST API v3 (Fallback)

Reference: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#about

### When to Use REST API

Use the REST API only when:
1. MCP operation fails
2. User confirms they want to proceed with REST API after MCP failure

### REST API Authentication

**Required Information** (see `shared/jira-api-token-guide.md` for how to obtain):
- JIRA Server URL: `https://your-domain.atlassian.net`
- Email: `email@example.com`
- API Token: See guide for generation steps

**How to get an API token**: https://id.atlassian.com/manage-profile/security/api-tokens

### Using the Python Client

All REST API operations use the Python client at `scripts/jira-client.py`.

**Script Location:**
The script is in the plugin cache. Extract the plugin root from the skill base directory (shown in the skill invocation header) and cd to it before running commands. See `shared/jira-rest-fallback.md` for details.

All examples below use `<plugin-root>` as a placeholder for the actual plugin root path.

**Environment Variables:**
```bash
export JIRA_SERVER_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
```

**Common Operations:**

```bash
# Get issue
cd <plugin-root> && \
  python3 scripts/jira-client.py get_issue TC-123 --fields "summary,status,description"

# Create issue
cd <plugin-root> && \
  python3 scripts/jira-client.py create_issue \
    --project TC \
    --summary "Issue summary" \
    --description-md "Issue description in **markdown**" \
    --issue-type Task \
    --labels ai-generated-jira

# Add comment
cd <plugin-root> && \
  python3 scripts/jira-client.py add_comment TC-123 \
    --comment-md "Comment text in markdown"

# Transition issue
cd <plugin-root> && python3 scripts/jira-client.py transition_issue TC-123 --transition-id 31

# Create issue link
cd <plugin-root> && \
  python3 scripts/jira-client.py create_link \
    --inward TC-123 \
    --outward TC-456 \
    --link-type Blocks
```

For full API reference, see `shared/jira-rest-fallback.md`.

---

## Performance Optimization JIRA Workflow

Performance optimization skills use a specialized JIRA workflow involving Epics and Tasks to group optimization work.

### Issue Hierarchy

```
Epic (Performance Optimization: {workflow-name})
  ├── Task (Bundle Size Reduction: ...)
  ├── Task (API Optimization: ...)
  ├── Task (Render Optimization: ...)
  └── Task (Resource Optimization: ...)
```

### Epic Usage

**Created by**: `performance-plan-optimization`

**Purpose**: Group all optimization tasks for a single workflow

**Issue Type**: Epic (standard Jira Epic issue type)

**Labels**:
- `ai-generated-jira` (standard label for all AI-generated issues)
- `performance-optimization` (identifies this as performance work)
- `{workflow-name}` (the workflow being optimized, e.g., `home`, `sbom-list`)

**Link Type**: **Incorporates** (Epic incorporates Tasks)

### Task Usage

**Created by**: `performance-plan-optimization`

**Purpose**: Individual optimization work item (e.g., "Reduce bundle size by lazy loading", "Eliminate N+1 queries in SBOM list")

**Issue Type**: Task (standard Jira Task issue type)

**Labels**:
- `ai-generated-jira` (standard label)
- `performance-optimization` (identifies as performance work)
- `{workflow-name}` (the workflow being optimized)
- `{category}` (optimization category: `bundle-size`, `api-optimization`, `render-optimization`, `resource-optimization`, `long-task-mitigation`)
- Layer labels: `frontend`, `backend`, or `integration` (based on where the optimization is applied)

**Link Type**: **Blocks** (for task dependencies — e.g., Task 2 depends on Task 1 completing first)

### Task Description Template Extensions

Performance optimization tasks extend the standard task description template with three additional sections:

1. **Baseline Metrics** — Current performance metrics before optimization (LCP, FCP, TTI, bundle size)
2. **Target Metrics** — Expected metrics after optimization
3. **Performance Test Requirements** — How to verify the optimization worked (e.g., "Re-run baseline capture, verify LCP < 2500ms")

These sections are read by `performance-implement-optimization` and `performance-verify-optimization` to validate target achievement.

### Label Conventions

**Standard labels** (applied to all performance issues):
- `ai-generated-jira`
- `performance-optimization`

**Workflow labels** (the workflow being optimized):
- Workflow name in lowercase (e.g., `home`, `sbom-list`, `advisory-detail`)

**Category labels** (optimization type):
- `bundle-size` — Code splitting, lazy loading, dead code elimination
- `api-optimization` — Reduce over-fetching, eliminate N+1 queries, parallel fetching
- `render-optimization` — Component memoization, virtual scrolling, layout thrashing fixes
- `resource-optimization` — Async/defer scripts, parallel loading, image compression
- `long-task-mitigation` — Web workers, async patterns, code splitting for large modules

**Layer labels** (where optimization is applied):
- `frontend` — Client-side optimizations (React components, lazy loading, bundle splitting)
- `backend` — Server-side optimizations (API response trimming, query optimization)
- `integration` — Cross-layer optimizations (parallel API calls, resource hints)

### Link to Feature Issues

Performance optimization Epics/Tasks can be linked to Feature issues using the **Relates** link type to show that performance work is related to a specific feature development effort. This is optional and depends on whether the optimization is feature-driven or general improvement.

### Example Workflow

1. User runs `performance-plan-optimization` for "Home Dashboard" workflow
2. Skill creates:
   - **Epic**: "Performance Optimization: Home Dashboard"
     - Labels: `ai-generated-jira`, `performance-optimization`, `home`
   - **Task 1**: "Bundle Size Reduction: Lazy load charts library"
     - Labels: `ai-generated-jira`, `performance-optimization`, `home`, `bundle-size`, `frontend`
     - Link: Epic **incorporates** Task 1
   - **Task 2**: "API Optimization: Reduce over-fetching in dashboard stats"
     - Labels: `ai-generated-jira`, `performance-optimization`, `home`, `api-optimization`, `backend`
     - Link: Epic **incorporates** Task 2
     - Link: Task 1 **blocks** Task 2 (dependency)
3. User runs `performance-implement-optimization TC-XXXX` for Task 1
4. User runs `performance-verify-optimization TC-XXXX` to verify Task 1

---

## Implementation Pattern for Skills

### Standard JIRA Operation Flow

```
1. Try Atlassian MCP operation
   ↓
2. If MCP fails:
   ↓
   a. Capture error message
   ↓
   b. Prompt user:
      "❌ Atlassian MCP failed: {error}
      
      Would you like to use JIRA REST API v3 fallback?
      
      Options:
      1. Yes - Use REST API (requires credentials)
      2. No - Skip JIRA integration
      3. Retry - I'll fix MCP configuration and retry
      
      Choose (1/2/3):"
   ↓
   c. If user chooses "1. Yes":
      - Check CLAUDE.md for existing credentials
      - If credentials exist: read and use them
      - If not: collect credentials → validate → store
      - Execute operation via REST API
   ↓
   d. If user chooses "2. No":
      - Skip JIRA operation
      - Continue with local plan file only
   ↓
   e. If user chooses "3. Retry":
      - Inform user to check MCP config
      - Retry MCP operation
```

## Configuration in CLAUDE.md

When REST API is used, credentials are stored in CLAUDE.md:

```markdown
## Jira Configuration

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Feature issue type ID: 10142
- Git Pull Request custom field: customfield_10875
- GitHub Issue custom field: customfield_10747

### REST API Credentials (MCP Fallback)
- Server URL: https://your-domain.atlassian.net
- Email: user@example.com
- API Token: $JIRA_API_TOKEN  # or actual token if full storage chosen
```

## Error Handling

### MCP Errors

Common MCP errors:
- `MCP not configured` - User hasn't set up Atlassian MCP
- `Authentication failed` - MCP credentials invalid
- `Permission denied` - User lacks required JIRA permissions
- `Project not found` - Invalid project key

### REST API Errors

Common REST API errors (handled by `scripts/jira-client.py`):
- `401 Unauthorized` - Invalid email/API token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Invalid project/issue key
- `400 Bad Request` - Invalid request format

### Graceful Degradation

If both MCP and REST API fail:
1. Log the error
2. Save the plan document locally (always succeeds)
3. Inform user they can create JIRA tasks manually later

## Security Considerations

**MCP:**
- Credentials managed by Claude Code MCP system
- No need to handle tokens directly in skills

**REST API:**
- API tokens should be stored securely (not in git)
- Recommend using environment variables
- Tokens don't expire automatically - rotate regularly
- Skills mask tokens in all output

**Best Practices:**
- Never log API tokens in full
- Clear sensitive data after use
- Prompt user before storing credentials in CLAUDE.md
- Recommend MCP over REST API for better security
- Always require explicit user consent before using REST API
