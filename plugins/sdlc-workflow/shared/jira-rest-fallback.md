# JIRA REST API Fallback - Implementation Guide

This document provides detailed implementation guidance for sdlc-workflow skills to handle JIRA REST API v3 fallback when Atlassian MCP is unavailable.

## Overview

Skills must implement a graceful fallback pattern:
1. **Always try MCP first** (preferred method)
2. **On MCP failure, always prompt user** (even if credentials exist)
3. **Use stored credentials if available** (no re-collection needed)
4. **Support three user choices**: Use REST API, Skip JIRA, or Retry MCP

## Script Execution Context

**IMPORTANT**: The `scripts/jira-client.py` script is located in the plugin cache, not your current working directory.

When a skill is invoked, Claude Code provides the skill base directory in the invocation message:
```
Base directory for this skill: /path/to/.claude/plugins/cache/sdlc-plugins/sdlc-workflow/<version>/skills/<skill-name>
```

The **plugin root** is 2 directory levels up from the skill base:
- Skill base: `.../sdlc-workflow/0.6.0/skills/define-feature`
- Plugin root: `.../sdlc-workflow/0.6.0` (go up 2 levels)

**All JIRA REST API Python client script invocations must use this pattern:**
```bash
cd <plugin-root> && python3 scripts/jira-client.py <command>
```

Where `<plugin-root>` is extracted from the skill base directory shown in the invocation header.

**Example:**
If the skill invocation shows:
```
Base directory for this skill: /home/user/.claude/plugins/cache/sdlc-plugins/sdlc-workflow/0.6.0/skills/define-feature
```

Then plugin root is: `/home/user/.claude/plugins/cache/sdlc-plugins/sdlc-workflow/0.6.0`

Use:
```bash
cd /home/user/.claude/plugins/cache/sdlc-plugins/sdlc-workflow/0.6.0 && \
  python3 scripts/jira-client.py get_user_info
```

## Credential Storage

Credentials are stored in **`.env` file** (recommended) or **CLAUDE.md** (legacy):

**Recommended: `.env` file in repository root**
- Industry-standard approach for environment variables
- Automatically ignored by git (added to `.gitignore`)
- Easy to use with `source .env` or `direnv`
- `.env.example` provides template for other contributors
- See Ruben's recommendation in PR #70

**Legacy: CLAUDE.md `### REST API Credentials (MCP Fallback)` section**
- Still supported for backward compatibility
- Less standard than .env files
- Requires manual env var management

## Credential Collection Flow

### Step 1: Detect MCP Failure and Prompt User

When any MCP operation fails, display this prompt:

```
❌ Atlassian MCP failed: {error_message}

Would you like to use JIRA REST API v3 fallback?

Options:
1. Yes - Use REST API (requires credentials)
2. No - Skip JIRA integration for this operation
3. Retry - I'll fix MCP configuration and retry

Choose (1/2/3):
```

**Important**: Always prompt, even if credentials already exist. This ensures explicit user consent every time.

### Step 2: Check for Existing Credentials

If user chooses "1. Yes - Use REST API":

1. **Check for `.env` file** in repository root (recommended location)
   - If `.env` exists and contains `JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`:
     - Source the file: `source .env`
     - Proceed to Step 5 (use REST API)
     - Skip credential collection (Steps 3-4)

2. **Fallback to CLAUDE.md** (legacy method):
   - Read `CLAUDE.md` → `## Jira Configuration` → `### REST API Credentials (MCP Fallback)`
   - Look for: `Server URL`, `Email`, `API Token` (may be `$JIRA_API_TOKEN` reference)
   - If credentials exist:
     - Set environment variables and proceed to Step 5
     - Skip credential collection (Steps 3-4)

3. **No credentials found**:
   - Proceed to Step 3 (credential collection)

### Step 3: Collect Credentials (First Time Only)

Display guidance and collect credentials:

```
📖 To use the JIRA REST API, you'll need to provide:
   1. JIRA Server URL
   2. Your email address
   3. API token

See shared/jira-api-token-guide.md for detailed setup instructions.
Quick link to generate token: https://id.atlassian.com/manage-profile/security/api-tokens
```

**Collect Server URL:**
```
JIRA Server URL (e.g., https://your-company.atlassian.net):
```

Validate:
- Must start with `https://`
- Must not end with `/`
- Must be valid URL format

**Collect Email:**
```
Your Atlassian account email:
```

Validate:
- Must contain `@`
- Must be valid email format

**Collect API Token:**
```
API Token (from https://id.atlassian.com/manage-profile/security/api-tokens):
⚠️  This will be stored in CLAUDE.md - consider using an environment variable
```

Validate:
- Must be at least 20 characters long

### Step 4: Test Credentials

Before storing, validate credentials work:

```bash
# Set environment variables
export JIRA_SERVER_URL="<server-url>"
export JIRA_EMAIL="<email>"
export JIRA_API_TOKEN="<api-token>"

# Test with get_user_info
cd <plugin-root> && python3 scripts/jira-client.py get_user_info
```

On success:
```
✅ Authentication successful! Logged in as: {displayName}
```

On failure:
```
❌ Authentication failed. Please check your credentials.
```

If authentication fails, return to Step 3 to re-collect credentials.

### Step 5: Ask About Storage Preference

After successful validation, ask user:

```
Credentials validated successfully!

How would you like to store these credentials?

1. Create .env file in repository root (recommended - secure, standard)
2. Store in CLAUDE.md with $JIRA_API_TOKEN env var (legacy - less standard)
3. Don't store - ask me each time (most secure, least convenient)

Choose (1/2/3):
```

**Option 1: Create .env file (recommended)**
Create `.env` file in repository root:
```bash
# JIRA REST API v3 credentials for sdlc-workflow fallback
JIRA_SERVER_URL=https://your-domain.atlassian.net
JIRA_EMAIL=user@example.com
JIRA_API_TOKEN=ATATT3xFfGF0...actual-token-here
```

Ensure `.env` is in `.gitignore`:
```bash
echo ".env" >> .gitignore
```

Create `.env.example` template (safe to commit):
```bash
# JIRA REST API v3 credentials for sdlc-workflow fallback
# Copy this file to .env and fill in your actual values
# Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

JIRA_SERVER_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-api-token-here
```

Inform user:
```
✅ Created .env file in repository root.
   .env is in .gitignore (won't be committed)
   .env.example created as a template for other contributors

To use: source .env
Or install direnv to auto-load when entering this directory.
```

**Option 2: Store in CLAUDE.md with env var (legacy)**
Add to CLAUDE.md:
```markdown
### REST API Credentials (MCP Fallback)
- Server URL: https://your-domain.atlassian.net
- Email: user@example.com
- API Token: $JIRA_API_TOKEN
```

Inform user:
```
Set this environment variable in your shell:
  export JIRA_API_TOKEN="<your-token>"

Add to ~/.bashrc or ~/.zshrc to persist across sessions.
```

**Option 3: Don't store**
Skip credential storage. Credentials will be asked for on every MCP failure.

## Using the JIRA REST API Python Client Script

All REST API operations use `scripts/jira-client.py`.

### Environment Setup

Before calling the script, ensure environment variables are set.

**Option 1: Source .env file (recommended)**
```bash
source .env
```

**Option 2: Export manually**
```bash
export JIRA_SERVER_URL="<from-CLAUDE.md-or-collected>"
export JIRA_EMAIL="<from-CLAUDE.md-or-collected>"
export JIRA_API_TOKEN="<from-CLAUDE.md-or-env-var>"
```

### Operation Examples

**Get Issue:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py get_issue TC-123 --fields "summary,status,description,labels,assignee"
```

Returns JSON:
```json
{
  "key": "TC-123",
  "fields": {
    "summary": "Issue title",
    "status": {"name": "In Progress"},
    "description": {...ADF...},
    "labels": ["ai-generated-jira"],
    "assignee": {"displayName": "John Doe"}
  }
}
```

**Create Issue:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py create_issue \
    --project TC \
    --summary "New feature request" \
    --description-md "This is the **description** in markdown." \
    --issue-type "<issue-type-id>" \  # See "Discovering Issue Types" below
    --labels ai-generated-jira,feature
```

Returns JSON:
```json
{
  "key": "TC-456",
  "id": "10001"
}
```

**Update Issue:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py update_issue TC-123 \
    --fields-json '{"labels": ["ai-generated-jira", "updated"]}'
```

**Add Comment:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py add_comment TC-123 \
    --comment-md "This is a comment with **bold** text."
```

**Transition Issue:**

Transitions are workflow-specific and must be discovered at runtime.

```bash
# Step 1: Get available transitions for the issue
cd <plugin-root> && python3 scripts/jira-client.py get_transitions TC-123
```

Example output:
```json
[
  {"id": "31", "name": "In Progress"},
  {"id": "41", "name": "In Review"},
  {"id": "51", "name": "Done"}
]
```

```bash
# Step 2: Parse output to find desired transition by name
# Extract the ID where name matches "In Review"
TRANSITION_ID=$(cd <plugin-root> && python3 scripts/jira-client.py get_transitions TC-123 | \
  python3 -c "import json,sys; transitions=json.load(sys.stdin); \
  print(next((t['id'] for t in transitions if t['name']=='In Review'), None))")

# Step 3: Apply the transition using discovered ID
cd <plugin-root> && python3 scripts/jira-client.py transition_issue TC-123 \
  --transition-id "$TRANSITION_ID"
```

**Note**: Transition IDs vary by project workflow configuration. Always discover them dynamically rather than hardcoding.

**Search with JQL:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py search_jql \
    --jql "project = TC AND status = 'In Progress'" \
    --fields "summary,status,assignee" \
    --max-results 50
```

**Create Issue Link:**
```bash
cd <plugin-root> && \
  python3 scripts/jira-client.py create_link \
    --inward TC-123 \
    --outward TC-456 \
    --link-type Incorporates
```

**Get User Info:**
```bash
cd <plugin-root> && python3 scripts/jira-client.py get_user_info
```

**Get Project Metadata:**
```bash
cd <plugin-root> && python3 scripts/jira-client.py get_project_metadata TC
```

### Discovering Issue Types

Issue type IDs are project-specific and should be discovered, not hardcoded.

**For one-time configuration** (when setting up CLAUDE.md):

Run the `/setup` skill, which uses `get_project_metadata` to discover available issue types and prompts you to select the Feature type. The ID is then stored in CLAUDE.md.

**For ad-hoc discovery**:

```bash
cd <plugin-root> && python3 scripts/jira-client.py get_project_metadata <project-key>
```

Example output (excerpt):
```json
{
  "key": "TC",
  "name": "Trustify Konveyor",
  "issueTypes": [
    {"id": "10142", "name": "Feature"},
    {"id": "10143", "name": "Task"},
    {"id": "10144", "name": "Story"}
  ]
}
```

Extract the ID for your desired issue type from the `issueTypes` array.

### Discovering Custom Fields

Custom field IDs (e.g., for Git Pull Request URLs or GitHub Issue links) are also project-specific.

**To discover custom fields**:

```bash
# Get full issue details including all custom fields
cd <plugin-root> && python3 scripts/jira-client.py get_issue <issue-key> --fields "*all"
```

Look for fields named `customfield_*` in the response. Match them to their display names by checking the field values or consulting your Jira admin.

Common custom fields used by sdlc-workflow:
- **Git Pull Request** - stores PR URLs (requires ADF format: inlineCard)
- **GitHub Issue** - stores GitHub issue URLs (plain string or ADF)

Once discovered, add them to your project's CLAUDE.md under `## Jira Configuration`.

## Error Handling

The JIRA REST API Python client script automatically maps HTTP errors to user-friendly messages:

**401 Unauthorized:**
```
❌ Authentication failed (401 Unauthorized)
Check your email and API token. Run /setup to update credentials.
```

**403 Forbidden:**
```
❌ Permission denied (403 Forbidden)
Contact your JIRA admin to grant project access.
```

**404 Not Found:**
```
❌ Resource not found (404 Not Found)
Verify the issue key or endpoint path.
```

**400 Bad Request:**
```
❌ Invalid request (400 Bad Request)
  • Field 'summary' is required
  • Issue type '99999' does not exist
```

### Token Rotation

If credentials fail with 401 after previously working:

```
❌ Authentication failed (401). Your API token may have expired or been revoked.

Options:
1. Update token - I'll provide a new token
2. Skip JIRA - Continue without JIRA
3. Retry - Try again with current credentials

Choose (1/2/3):
```

If "1. Update token":
1. Collect new API token
2. Test with `get_user_info`
3. Update CLAUDE.md with new token (or inform user to update env var)
4. Retry the original operation

## Token Security

**Masking:**
The JIRA REST API Python client script automatically masks tokens in all output:
- Full token: `ATATT3xFfGF0T8JxQkVmNzY5MjE3NjE3MDk2`
- Masked: `ATATT3xF...3MDk2`

**Never log:**
- Do NOT log full tokens to stdout/stderr
- Do NOT include tokens in skill comments or output
- Do NOT display tokens to user (except during collection, then mask immediately)

**Best Practices:**
- Recommend Option 2 (env var) when asking about storage
- Remind users to rotate tokens every 90 days
- Warn users not to commit CLAUDE.md with plaintext tokens to public repos

## Markdown to ADF Conversion

The JIRA REST API Python client script automatically converts markdown to Atlassian Document Format (ADF) when creating issues or adding comments.

**Supported Markdown:**
- Headings: `# H1` and `## H2`
- Paragraphs: Plain text separated by blank lines
- Bold: `**bold**`
- Italic: `*italic*`
- Inline code: `` `code` ``
- Code blocks: ` ```language\ncode\n``` `
- Bullet lists: `- item`
- Ordered lists: `1. item`
- Links: `[text](url)`
- Horizontal rules: `---`

**Example:**

Markdown input:
```markdown
## Implementation Notes

Follow these steps:

1. Read the file
2. Modify the code
3. Run tests

See [documentation](https://example.com) for details.
```

ADF output:
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 2},
      "content": [{"type": "text", "text": "Implementation Notes"}]
    },
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Follow these steps:"}]
    },
    {
      "type": "orderedList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "Read the file"}]}
          ]
        },
        ...
      ]
    },
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "See "},
        {
          "type": "text",
          "text": "documentation",
          "marks": [{"type": "link", "attrs": {"href": "https://example.com"}}]
        },
        {"type": "text", "text": " for details."}
      ]
    }
  ]
}
```

## Skill-Specific Guidance

### define-feature Skill

When creating a Feature issue:
- Issue type ID from CLAUDE.md (`Feature issue type ID`)
- Labels: Always include `ai-generated-jira`
- Assignee: Use `get_user_info` to get current user's account ID
- Description: Convert feature template markdown to ADF

### plan-feature Skill

When creating Task issues:
- Link to Feature: Use `create_link` with `Incorporates` link type
- Dependencies: Use `create_link` with `Depend` link type
- Labels: Include `ai-generated-jira` and module-specific labels
- Custom fields: Use `custom_fields` parameter in `create_issue`

### implement-task Skill

Operations needed:
- `get_issue` - Fetch task description
- `transition_issue` - Move to "In Progress", then "In Review"
- `update_issue` - Set assignee, update custom fields (PR link)
- `add_comment` - Post implementation summary

### verify-pr Skill

Operations needed:
- `get_issue` - Fetch task acceptance criteria
- `create_issue` - Create sub-tasks for review feedback
- `create_link` - Link sub-tasks with `Blocks` or `Relates`
- `add_comment` - Post verification results

## Complete Fallback Example

Here's a complete implementation of the fallback pattern for `jira.get_issue`:

```bash
# Try MCP first
try:
  result=$(mcp__atlassian__getJiraIssue cloudId="$CLOUD_ID" issueIdOrKey="TC-123")
  echo "$result"
  exit 0
catch mcp_error:
  # MCP failed - prompt user
  echo "❌ Atlassian MCP failed: $mcp_error"
  echo ""
  echo "Would you like to use JIRA REST API v3 fallback?"
  echo ""
  echo "Options:"
  echo "1. Yes - Use REST API (requires credentials)"
  echo "2. No - Skip JIRA integration for this operation"
  echo "3. Retry - I'll fix MCP configuration and retry"
  echo ""
  read -p "Choose (1/2/3): " choice
  
  if [ "$choice" = "1" ]; then
    # Check for .env file first (recommended)
    if [ -f ".env" ]; then
      source .env
    # Fallback to CLAUDE.md (legacy)
    elif grep -q "### REST API Credentials" CLAUDE.md; then
      # Credentials exist - extract and use them
      SERVER_URL=$(grep "Server URL:" CLAUDE.md | sed 's/.*: //')
      EMAIL=$(grep "Email:" CLAUDE.md | sed 's/.*: //')
      TOKEN_LINE=$(grep "API Token:" CLAUDE.md | sed 's/.*: //')
      
      if [[ "$TOKEN_LINE" == "\$JIRA_API_TOKEN" ]]; then
        # Use env var
        export JIRA_API_TOKEN="$JIRA_API_TOKEN"
      else
        # Use stored token
        export JIRA_API_TOKEN="$TOKEN_LINE"
      fi
      
      export JIRA_SERVER_URL="$SERVER_URL"
      export JIRA_EMAIL="$EMAIL"
    else
      # No credentials - collect them
      # (See Step 3 above for full collection flow)
      ...
    fi
    
    # Use REST API
    result=$(python3 scripts/jira-client.py get_issue TC-123 --fields "*all")
    echo "$result"
    
  elif [ "$choice" = "2" ]; then
    echo "Skipping JIRA integration."
    exit 0
    
  elif [ "$choice" = "3" ]; then
    echo "Please fix MCP configuration and run the skill again."
    exit 1
  fi
fi
```

## Testing Your Implementation

1. **Test MCP path** (no changes needed):
   - Run skill with MCP configured
   - Verify MCP operations succeed
   - Verify no fallback prompts appear

2. **Test first-time REST API fallback**:
   - Disable MCP in Claude Code settings
   - Remove REST credentials from CLAUDE.md
   - Run skill
   - Verify user prompted (options 1/2/3)
   - Choose "1. Yes"
   - Provide credentials
   - Verify validation succeeds
   - Verify CLAUDE.md updated correctly
   - Verify operation completes via REST API

3. **Test subsequent REST API fallback**:
   - MCP still disabled, credentials in CLAUDE.md
   - Run skill again
   - Verify user still prompted (always prompt!)
   - Choose "1. Yes"
   - Verify no credential collection (reuses stored)
   - Verify operation completes via REST API

4. **Test token rotation**:
   - Invalidate token (revoke in Atlassian admin)
   - Run skill
   - Choose "1. Yes"
   - Verify 401 error detected
   - Verify rotation prompt appears
   - Provide new token
   - Verify operation retries and succeeds

5. **Test skip JIRA**:
   - Run skill
   - Choose "2. No"
   - Verify skill continues without JIRA
   - Verify plan saved locally (if applicable)

## Troubleshooting

**Credentials not found:**
```
❌ Missing credentials: JIRA_SERVER_URL, JIRA_EMAIL, JIRA_API_TOKEN
Set these environment variables before running this command.
```
→ Run credential collection flow again

**Connection error:**
```
❌ Connection error: [Errno 11001] getaddrinfo failed
Check that https://your-domain.atlassian.net is accessible.
```
→ Verify server URL is correct and accessible

**Invalid token format:**
```
❌ Authentication failed (401 Unauthorized)
```
→ Regenerate API token and update credentials

For more help, see `shared/jira-api-token-guide.md`.
