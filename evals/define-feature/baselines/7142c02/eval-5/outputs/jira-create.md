# Jira Create Issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<see description below>,
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

**Note:** No assignee field is included because the user chose to leave the Feature unassigned.

## Description (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Update the existing PR review when re-running evals on the same PR, or create a new review if none exists | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |
```

## Parameters Summary

| Parameter | Value |
|---|---|
| Cloud ID | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| Project Key | `TC` |
| Issue Type ID | `10142` |
| Summary | `Add automated PR review posting for eval results` |
| Content Format | `markdown` |
| Labels | `ai-generated-jira` |
| Assignee | Unassigned (not included) |
