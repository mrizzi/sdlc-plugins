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

### Using the JIRA REST API Python Client

All REST API operations use the JIRA REST API Python client script at `scripts/jira-client.py`.

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
# Step 1: Get available transitions for the issue
cd <plugin-root> && python3 scripts/jira-client.py get_transitions TC-123
# Output: [{"id": "31", "name": "In Progress"}, {"id": "41", "name": "In Review"}, ...]

# Step 2: Find the transition ID for your desired status by name
# Example: Extract ID for "In Review"
TRANSITION_ID=$(cd <plugin-root> && python3 scripts/jira-client.py get_transitions TC-123 | \
  python3 -c "import json,sys; transitions=json.load(sys.stdin); \
  print(next((t['id'] for t in transitions if t['name']=='In Review'), None))")

# Step 3: Apply the transition
cd <plugin-root> && python3 scripts/jira-client.py transition_issue TC-123 \
  --transition-id "$TRANSITION_ID"

# Create issue link
cd <plugin-root> && \
  python3 scripts/jira-client.py create_link \
    --inward TC-123 \
    --outward TC-456 \
    --link-type Blocks
```

For full API reference, see `shared/jira-rest-fallback.md`.

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
- Feature issue type ID: 10142  # Discovered via /setup skill → get_project_metadata
- Git Pull Request custom field: customfield_10875  # Optional - discovered via get_project_metadata
- GitHub Issue custom field: customfield_10747  # Optional - discovered via get_project_metadata

<!-- Note: Transition IDs are NOT stored in CLAUDE.md. They vary by workflow
     and must be discovered at runtime via get_transitions. -->

### REST API Credentials (MCP Fallback)
- Server URL: https://your-domain.atlassian.net
- Email: user@example.com
- API Token: $JIRA_API_TOKEN  # or actual token if full storage chosen
```

### Configuration Categories

Values in Jira Configuration fall into two categories:

**1. Project-level configuration** (stored in CLAUDE.md, discovered once via `/setup`):
- Project key - identifies your Jira project (e.g., `TC`, `PROJ`)
- Cloud ID - your Jira instance identifier
- Feature issue type ID - discovered via `get_project_metadata` during setup
- Custom field IDs (optional) - discovered via `get_project_metadata`

**2. Runtime discovery** (queried dynamically as needed):
- Transition IDs - vary by issue type and workflow, discovered via `get_transitions`
- User account IDs - discovered via `get_user_info` when assigning issues
- Available statuses for an issue - queried via `get_transitions` before each transition

Skills never hardcode transition IDs or assume specific workflow configurations.
They always query available transitions and match by status name (e.g., "In Review").

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
