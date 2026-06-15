# Jira Create Issue Call Parameters

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
    "assignee": { "accountId": "<user-account-id>" }
  }
)
```

## Parameter Details

- **cloudId**: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **projectKey**: `TC`
- **issueTypeId**: `10142`
- **summary**: `Add SBOM dependency graph visualization`
- **description**: The full composed Feature description (all 9 sections included, formatted in Markdown with section headings as shown in preview.md)
- **contentFormat**: `markdown`
- **labels**: `["ai-generated-jira"]`
- **assignee**: `{ "accountId": "<user-account-id>" }` (self-assignment -- account ID retrieved from `atlassianUserInfo()`)

## Sections Included in Description

1. Feature Overview (Required) -- included
2. Background and Strategic Fit (Recommended) -- included
3. Goals (Recommended) -- included
4. Requirements (Required) -- included
5. Non-Functional Requirements (Recommended) -- included
6. Use Cases (Recommended) -- included
7. Customer Considerations (Optional) -- included
8. Customer Information/Supportability (Optional) -- included
9. Documentation Considerations (Optional) -- included

All 9 sections provided; none skipped.
