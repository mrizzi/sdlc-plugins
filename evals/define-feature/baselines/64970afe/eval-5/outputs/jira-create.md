# Jira Create Issue Parameters

## MCP Call: createJiraIssue

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add automated PR review posting for eval results",
  description = "<composed description from preview — Feature Overview and Requirements sections>",
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"]
  }
)
```

## Field Details

| Field | Value | Notes |
|---|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | From CLAUDE.md Jira Configuration |
| projectKey | `TC` | From CLAUDE.md Jira Configuration |
| issueTypeId | `10142` | Feature issue type ID from CLAUDE.md |
| summary | `Add automated PR review posting for eval results` | User-provided feature summary |
| contentFormat | `markdown` | Description provided as Markdown |
| labels | `["ai-generated-jira"]` | Required label for AI-generated issues |
| assignee | _(omitted)_ | User chose to leave unassigned |
| priority | _(omitted)_ | Not set / skipped |
| fixVersions | _(omitted)_ | Not set / skipped |

## Description Content

The description contains only the two provided sections (skipped sections are omitted):

1. **Feature Overview** -- High-level description of the CI workflow for posting eval results as PR reviews
2. **Requirements** -- Four requirements with corrected language reflecting that GitHub REST API supports updating submitted PR reviews via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
