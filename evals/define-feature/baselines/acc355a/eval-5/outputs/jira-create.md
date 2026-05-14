# Jira Create Issue Call Parameters

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

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | Add automated PR review posting for eval results |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | _(not included -- user chose to leave unassigned)_ |

## Description Content

The description contains only the non-skipped sections:

1. **Feature Overview** -- included
2. **Background and Strategic Fit** -- skipped (omitted)
3. **Goals** -- skipped (omitted)
4. **Requirements** -- included (with corrected API claim language)
5. **Non-Functional Requirements** -- skipped (omitted)
6. **Use Cases** -- skipped (omitted)
7. **Customer Considerations** -- skipped (omitted)
8. **Customer Information/Supportability** -- skipped (omitted)
9. **Documentation Considerations** -- skipped (omitted)

Note: No assignee field is included in `additional_fields` because the user chose to leave the Feature unassigned.
