# Jira Create Issue Call Parameters

## MCP Call

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

## Parameters Detail

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | Add automated PR review posting for eval results |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | _(none -- left unassigned per user request)_ |

## Description Content (Markdown)

The `description` field contains the composed Feature description with corrected language, including only the two non-skipped sections:

- `## Feature Overview` -- high-level description of the CI workflow step for posting eval results as PR reviews
- `## Requirements` -- requirements table with 4 MVP requirements, including the corrected fourth requirement that uses `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update existing reviews instead of the original incorrect claim that reviews cannot be updated

Skipped sections (Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations) are omitted from the description entirely -- no empty headings are included.
