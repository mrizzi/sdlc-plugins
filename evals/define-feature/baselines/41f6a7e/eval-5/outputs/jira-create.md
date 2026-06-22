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

## Parameters Detail

- **Cloud ID:** `2b9e35e3-6bd3-4cec-b838-f4249ee02432` (from CLAUDE.md Jira Configuration)
- **Project Key:** `TC` (from CLAUDE.md Jira Configuration)
- **Issue Type ID:** `10142` (Feature issue type from CLAUDE.md Jira Configuration)
- **Summary:** `Add automated PR review posting for eval results`
- **Content Format:** `markdown`
- **Labels:** `ai-generated-jira`
- **Assignee:** Not included (user chose to leave the Feature unassigned)

## Description Content

The description field contains the composed Feature description with the following sections:

1. **Feature Overview** -- included (Required, provided by user)
2. **Background and Strategic Fit** -- omitted (skipped by user)
3. **Goals** -- omitted (skipped by user)
4. **Requirements** -- included (Required, provided by user; corrected after API claim verification)
5. **Non-Functional Requirements** -- omitted (skipped by user)
6. **Use Cases** -- omitted (skipped by user)
7. **Customer Considerations** -- omitted (skipped by user)
8. **Customer Information/Supportability** -- omitted (skipped by user)
9. **Documentation Considerations** -- omitted (skipped by user)
