# Jira Feature Creation

## API Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## Parameters

- **Project Key:** TC
- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Issue Type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Labels:** ai-generated-jira
- **Assignee:** Unassigned (no assignee set)

## Description Content

The description includes the following sections:

1. **Feature Overview** (Required) -- included
2. **Background and Strategic Fit** (Recommended) -- skipped
3. **Goals** (Recommended) -- skipped
4. **Requirements** (Required) -- included
5. **Non-Functional Requirements** (Recommended) -- skipped
6. **Use Cases** (Recommended) -- skipped
7. **Customer Considerations** (Optional) -- skipped
8. **Customer Information/Supportability** (Optional) -- skipped
9. **Documentation Considerations** (Optional) -- skipped
