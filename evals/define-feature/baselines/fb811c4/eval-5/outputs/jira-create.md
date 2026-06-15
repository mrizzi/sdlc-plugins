# Jira Create Issue Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update existing eval review if one already exists; create a new review only on first run | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review | Yes |",
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## Parameters Summary

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | Add automated PR review posting for eval results |
| Content Format | markdown |
| Labels | `ai-generated-jira` |
| Assignee | Unassigned (not included in request) |
