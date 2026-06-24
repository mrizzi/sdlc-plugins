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
| Labels | `ai-generated-jira` |
| Assignee | Unassigned (not set) |
| Content Format | markdown |

## Description Content

The description contains two sections (skipped sections are omitted):

1. **Feature Overview** -- High-level description of the CI workflow step for posting eval results as PR reviews
2. **Requirements** -- Requirements table with 4 rows, all marked MVP, with corrected language for the review update requirement

Note: The fourth requirement was corrected during External API Claim Verification. The original claim that "PR reviews cannot be updated after initial submission" was replaced with corrected language reflecting that the GitHub REST API supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a submitted review.
