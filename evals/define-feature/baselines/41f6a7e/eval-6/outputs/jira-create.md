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
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## Parameters

- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Project Key:** TC
- **Issue Type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Assignee:** Unassigned (no assignee field included)
- **Labels:** ai-generated-jira

## Description Content

The description includes the following sections:

1. **Feature Overview** (Required) -- Included
2. **Background and Strategic Fit** (Recommended) -- Skipped
3. **Goals** (Recommended) -- Skipped
4. **Requirements** (Required) -- Included
5. **Non-Functional Requirements** (Recommended) -- Skipped
6. **Use Cases** (Recommended) -- Skipped
7. **Customer Considerations** (Optional) -- Skipped
8. **Customer Information/Supportability** (Optional) -- Skipped
9. **Documentation Considerations** (Optional) -- Skipped

## Simulated Response

```json
{
  "id": "10001",
  "key": "TC-101",
  "self": "https://team-instance.atlassian.net/rest/api/3/issue/10001"
}
```

> Note: This is a simulated response. No actual Jira API call was made.
