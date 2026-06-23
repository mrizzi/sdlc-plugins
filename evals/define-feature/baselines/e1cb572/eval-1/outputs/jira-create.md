# Jira Create Issue Parameters

## MCP Call: `createJiraIssue`

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
    "assignee": { "accountId": "<current-user-account-id>" }
  }
)
```

## Parameters

- **Project Key**: TC
- **Summary**: Add SBOM dependency graph visualization
- **Issue Type ID**: 10142
- **Description**: The full composed Feature description with all 9 sections (see preview.md)
- **Content Format**: markdown
- **Labels**: `ai-generated-jira`
- **Assignee**: Current user (self-assignment) — the `accountId` would be retrieved from `atlassianUserInfo()` at runtime
