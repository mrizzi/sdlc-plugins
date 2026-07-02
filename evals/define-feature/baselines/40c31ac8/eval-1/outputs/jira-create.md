# Jira Create Issue Parameters

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

## Field Details

- **Project key**: TC
- **Summary**: Add SBOM dependency graph visualization
- **Issue type ID**: 10142
- **Description**: Full composed description with all 9 sections (Feature Overview, Background and Strategic Fit, Goals, Requirements, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations)
- **Content format**: markdown
- **Labels**: `ai-generated-jira`
- **Assignee**: Current user (self-assigned) — `accountId` resolved from `atlassianUserInfo()`
- **Priority**: Major
- **Fix Versions**: 1.5.0
