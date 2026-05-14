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
- **Assignee:** Unassigned (no assignee field included)
- **Labels:** `ai-generated-jira`

## Description Content

The description includes the following sections:

- **Feature Overview** (Required) -- provided
- **Background and Strategic Fit** (Recommended) -- SKIPPED
- **Goals** (Recommended) -- SKIPPED
- **Requirements** (Required) -- provided
- **Non-Functional Requirements** (Recommended) -- SKIPPED
- **Use Cases** (Recommended) -- SKIPPED
- **Customer Considerations** (Optional) -- SKIPPED
- **Customer Information/Supportability** (Optional) -- SKIPPED
- **Documentation Considerations** (Optional) -- SKIPPED

## Notes

- The user left the Feature unassigned, so no `assignee` field is included in `additional_fields`.
- An unverified external API claim exists in the Requirements section. The original wording was retained because web verification tools were unavailable.
