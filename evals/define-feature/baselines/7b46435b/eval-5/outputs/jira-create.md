# Jira Create Issue Parameters

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
| cloudId | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| projectKey | TC |
| issueTypeId | 10142 |
| summary | Add automated PR review posting for eval results |
| contentFormat | markdown |
| labels | ai-generated-jira |
| assignee | _(not set — user chose unassigned)_ |
| priority | _(not set — skipped)_ |
| fixVersions | _(not set — skipped)_ |

## Description Content (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Update existing PR review when re-running evals on the same PR, or create a new review if none exists | Use PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id} to update an existing review, or POST to create a new one | Yes |
```
