# Jira create_issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add SBOM dependency graph visualization",
  description = "<full composed description — see preview.md>",
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<current-user-account-id>" }
  }
)
```

## Parameters Detail

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | `Add SBOM dependency graph visualization` |
| Content Format | `markdown` |
| Labels | `ai-generated-jira` |
| Assignee | Self-assigned (current user's accountId from `atlassianUserInfo()`) |

## Description

The description field contains the full composed Feature description with all 9 sections as shown in `preview.md`, formatted in Markdown with the following section headings:

1. `## Feature Overview`
2. `## Background and Strategic Fit`
3. `## Goals`
4. `## Requirements`
5. `## Non-Functional Requirements`
6. `## Use Cases (User Experience & Workflow)`
7. `## Customer Considerations`
8. `## Customer Information/Supportability`
9. `## Documentation Considerations`
