# Jira create_issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add SBOM dependency graph visualization",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "assignee": { "accountId": "<user-account-id>" },
    "priority": {"name": "Major"},
    "fixVersions": [{"name": "1.5.0"}]
  }
)
```

## Parameter Details

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add SBOM dependency graph visualization` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | `{ "accountId": "<user-account-id>" }` (self-assigned) |
| priority | `{"name": "Major"}` |
| fixVersions | `[{"name": "1.5.0"}]` |

## Description Field

The `description` parameter contains the full composed Feature description in Markdown format, including all 9 sections:

1. Feature Overview
2. Background and Strategic Fit
3. Goals
4. Requirements
5. Non-Functional Requirements
6. Use Cases (User Experience & Workflow)
7. Customer Considerations
8. Customer Information/Supportability
9. Documentation Considerations

The full description content is as shown in `preview.md` (everything under the **Description:** heading).
