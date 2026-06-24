# Jira Issue Creation

## API Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters

- **Project key:** TC
- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Issue type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Labels:** ai-generated-jira
- **Assignee:** Unassigned (no assignee set)

## Description Content

The description contains the following sections:

- **Feature Overview** (Required) -- provided
- **Background and Strategic Fit** (Recommended) -- skipped
- **Goals** (Recommended) -- skipped
- **Requirements** (Required) -- provided
- **Non-Functional Requirements** (Recommended) -- skipped
- **Use Cases** (Recommended) -- skipped
- **Customer Considerations** (Optional) -- skipped
- **Customer Information/Supportability** (Optional) -- skipped
- **Documentation Considerations** (Optional) -- skipped
