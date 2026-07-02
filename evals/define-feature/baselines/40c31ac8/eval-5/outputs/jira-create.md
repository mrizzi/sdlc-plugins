# Jira create_issue Parameters

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

## Parameter Details

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add automated PR review posting for eval results` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | _(not set -- user chose unassigned)_ |
| priority | _(not set -- skipped)_ |
| fixVersions | _(not set -- skipped)_ |

## Description Content

The `description` field contains the Markdown-formatted Feature description with only the non-skipped sections:

- Feature Overview (included)
- Requirements (included, with corrected API claim language)

Skipped sections (omitted from description):
- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations
