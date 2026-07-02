# Jira Create Issue Parameters

## MCP Call: createJiraIssue

```
createJiraIssue(
  cloudId = "2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey = "TC",
  issueTypeId = "10142",
  summary = "Add automated PR review posting for eval results",
  description = "<composed description — see preview.md>",
  contentFormat = "markdown",
  additional_fields = {
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters Detail

| Parameter | Value |
|---|---|
| cloudId | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| projectKey | TC |
| issueTypeId | 10142 |
| summary | Add automated PR review posting for eval results |
| contentFormat | markdown |
| labels | ai-generated-jira |
| assignee | _(omitted -- user chose unassigned)_ |
| priority | _(omitted -- user skipped priority selection)_ |
| fixVersions | _(omitted -- user skipped fixVersion selection)_ |

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
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |
```

## Notes

- The label `ai-generated-jira` is included as required by the skill specification.
- Assignee is omitted because the user chose to leave the Feature unassigned.
- Priority and fixVersion are omitted because the user skipped those selections.
- Skipped sections (Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations) are not included in the description.
