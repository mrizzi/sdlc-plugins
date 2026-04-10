# JIRA REST API Fallback - Required Details & Setup Guide

This guide explains what information you need for the REST API fallback and how to obtain it.

## Required Details for REST API Fallback

When Atlassian MCP fails and you choose to use the REST API fallback, you'll need to provide:

| Detail | Description | Example |
|--------|-------------|---------|
| **JIRA Server URL** | Your Atlassian Cloud instance URL | `https://your-company.atlassian.net` |
| **Email Address** | The email associated with your Atlassian account | `you@yourcompany.com` |
| **API Token** | Personal API token for authentication | `ATATT3xFfGF0...` (24+ characters) |
| **Project Key** | The JIRA project key for your tasks | `PERF`, `TRUST`, etc. |

---

## How to Retrieve Your API Token

### Step 1: Navigate to Atlassian Account Settings

1. Go to your Atlassian account: **https://id.atlassian.com/manage-profile/security/api-tokens**
2. Or navigate manually:
   - Visit https://id.atlassian.com
   - Click on your profile icon (top-right)
   - Select **"Account Settings"**
   - Go to the **"Security"** tab
   - Click **"Create and manage API tokens"**

### Step 2: Create a New API Token

1. Click the **"Create API token"** button
2. Enter a label for your token (e.g., "agentune-performance-analysis")
3. Click **"Create"**
4. **IMPORTANT**: Copy the token immediately - you won't be able to see it again!

### Step 3: Store Your Token Securely

The API token will look like this:
```
ATATT3xFfGF0T8JxQkVmNzY5MjE3NjE3MDk2OjE5MjE3NjE3MDk2OjE5MjE3NjE3MDk2
```

**Security Best Practices:**
- ✅ Store in a password manager (1Password, LastPass, Bitwarden, etc.)
- ✅ Use environment variables in your shell
- ✅ Store in CLAUDE.md (not committed to git - should be in .gitignore)
- ❌ DO NOT commit to git repositories
- ❌ DO NOT share in chat logs or screenshots
- ❌ DO NOT email or send via unencrypted channels

---

## Finding Your JIRA Server URL

Your JIRA Server URL is the base URL of your Atlassian instance.

### For Atlassian Cloud:
```
https://[your-subdomain].atlassian.net
```

**How to find it:**
1. Log in to JIRA in your web browser
2. Look at the URL in the address bar
3. Copy everything before `/jira/` or `/browse/`

**Examples:**
- Full URL: `https://acme-corp.atlassian.net/jira/software/projects/PERF/boards/1`
- Server URL: `https://acme-corp.atlassian.net`

### For Atlassian Server/Data Center (Self-Hosted):
```
https://jira.yourcompany.com
```
or
```
https://issues.yourcompany.com
```

**How to find it:**
1. Ask your JIRA administrator
2. Or look at the URL when you access JIRA in your browser

---

## Finding Your Project Key

The Project Key is a short uppercase identifier for your JIRA project.

**How to find it:**
1. Go to your JIRA project in the browser
2. Look at the issue keys - they start with the project key
   - Example: `PERF-123` → Project Key is `PERF`
   - Example: `TRUST-456` → Project Key is `TRUST`
3. Or go to **Project Settings** → **Details** → Look for "Key"

---

## Testing Your Credentials

Before using them with agentune, you can test your credentials:

### Using curl:

```bash
# Set your credentials (don't save these in bash history!)
JIRA_EMAIL="you@yourcompany.com"
JIRA_TOKEN="your-api-token-here"
JIRA_SERVER="https://your-company.atlassian.net"

# Test authentication - list yourself
curl -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  -H "Accept: application/json" \
  "$JIRA_SERVER/rest/api/3/myself"

# If successful, you'll see your user details as JSON
# If failed, you'll see an error message
```

### Expected Success Response:
```json
{
  "accountId": "5b10ac8d82e05b22cc7d4ef5",
  "emailAddress": "you@yourcompany.com",
  "displayName": "Your Name",
  ...
}
```

### Common Errors:

| Error Code | Meaning | Solution |
|------------|---------|----------|
| **401 Unauthorized** | Wrong email or token | Regenerate token, check email spelling |
| **403 Forbidden** | No permission | Ask JIRA admin for project access |
| **404 Not Found** | Wrong server URL | Verify your Atlassian instance URL |

---

## Storing Credentials for agentune

When the skill prompts you for credentials, they will be stored in your project's CLAUDE.md file:

```markdown
## JIRA Configuration

**Access Method**: REST API v3 (Atlassian MCP not available)

**Server Details:**
- Server URL: https://your-company.atlassian.net
- Email: you@yourcompany.com
- API Token: [Stored securely - use environment variable]

**Project Configuration:**
- Project Key: PERF
- Default Issue Type: Task
- Epic Type: Epic
```

### Using Environment Variables (Recommended)

Instead of storing the token directly in CLAUDE.md, use an environment variable:

```bash
# Add to your ~/.bashrc or ~/.zshrc
export JIRA_API_TOKEN="your-token-here"
```

Then reference it in CLAUDE.md:
```markdown
- API Token: $JIRA_API_TOKEN
```

---

## Required JIRA Permissions

Your account needs these permissions to use agentune with JIRA:

| Operation | Required Permission |
|-----------|-------------------|
| View issues | Browse Projects |
| Create issues | Create Issues |
| Edit issues | Edit Issues |
| Add comments | Add Comments |
| Link issues | Link Issues |
| Create Epics | Create Issues + Epic available in project |
| Transition issues | Transition Issues |

**How to check your permissions:**
1. Go to your JIRA project
2. Click **Project Settings** → **Permissions**
3. Find your role and verify you have the permissions above

**If you lack permissions:**
- Contact your JIRA administrator
- Request "Contributor" or "Developer" role on the project

---

## Revoking/Rotating API Tokens

### When to rotate your token:
- ✅ Every 90 days (security best practice)
- ✅ If you suspect it was exposed
- ✅ When leaving a project
- ✅ If you see unauthorized API usage

### How to revoke a token:
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Find the token by label
3. Click **"Revoke"**
4. Create a new token and update your configuration

---

## Troubleshooting

### "Authentication failed" error:

```bash
# Check if your credentials work with a simple API call
curl -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "$JIRA_SERVER/rest/api/3/myself"
```

**Common issues:**
- Extra spaces in email or token (copy-paste error)
- Token expired or revoked
- Wrong server URL (missing `https://` or wrong subdomain)
- Email doesn't match the account that created the token

### "Project not found" error:

```bash
# List all projects you have access to
curl -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "$JIRA_SERVER/rest/api/3/project" | jq '.[].key'
```

This will show all project keys you can access.

### "Issue type not found" error:

```bash
# List available issue types for your project
curl -u "$JIRA_EMAIL:$JIRA_TOKEN" \
  "$JIRA_SERVER/rest/api/3/project/YOURKEY/statuses" | jq '.[].name'
```

Replace `YOURKEY` with your project key.

---

## Security Considerations

### Token Scope & Limitations

- API tokens have **full access** to everything your account can do
- There's no way to limit a token to specific projects or operations
- Atlassian Cloud tokens don't expire automatically (unless you revoke them)

### Best Practices

1. **Use Atlassian MCP when possible** - More secure, managed by Claude Code
2. **Rotate tokens regularly** - Every 90 days minimum
3. **Use unique tokens** - Create separate tokens for different tools/purposes
4. **Monitor usage** - Check your API usage in Atlassian admin console
5. **Revoke immediately if compromised** - Better safe than sorry

### What NOT to do

- ❌ Don't use your personal account token on shared machines
- ❌ Don't commit CLAUDE.md with tokens to public repositories
- ❌ Don't share tokens via email, Slack, or chat
- ❌ Don't use the same token across multiple tools

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│ JIRA REST API Fallback - Quick Reference                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Required Details:                                           │
│  • Server URL: https://[subdomain].atlassian.net           │
│  • Email: [your-email]@[company.com]                       │
│  • API Token: Get from https://id.atlassian.com            │
│  • Project Key: Found in issue keys (e.g., PERF-123)      │
│                                                             │
│ Get API Token:                                             │
│  1. Visit: https://id.atlassian.com/manage-profile/security/api-tokens │
│  2. Click "Create API token"                               │
│  3. Label it (e.g., "agentune")                           │
│  4. Copy immediately (won't show again!)                   │
│                                                             │
│ Test Credentials:                                          │
│  curl -u "email:token" \                                   │
│    "https://[server]/rest/api/3/myself"                   │
│                                                             │
│ Revoke Token:                                              │
│  Visit same page, click "Revoke" next to token            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Additional Resources

- **Atlassian API Tokens**: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
- **JIRA REST API v3 Docs**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- **Authentication Guide**: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
- **Permissions Reference**: https://support.atlassian.com/jira-cloud-administration/docs/manage-project-permissions/

---

## Support

If you encounter issues:

1. **Check MCP first**: Try configuring Atlassian MCP instead of using REST API fallback
2. **Test credentials**: Use the curl commands above to verify your setup
3. **Check permissions**: Verify you have required JIRA permissions
4. **Check logs**: Look for specific error messages in skill output
5. **Ask JIRA admin**: They can help with permissions and project configuration

For Claude Code and Atlassian MCP setup:
- https://github.com/anthropics/claude-code
