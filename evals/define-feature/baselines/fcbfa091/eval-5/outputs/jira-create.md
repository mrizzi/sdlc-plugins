# Jira Create Issue Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed-description-below>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

**Notes:**
- Assignee is omitted because the user chose to leave the Feature unassigned.
- Priority is omitted because the user did not select a priority (skipped).
- fixVersions is omitted because the user did not select a fix version (skipped).

## Composed Description (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Create a new review for each eval run rather than updating a previous review | Preserves review history so reviewers can compare results across runs. Note: the GitHub API does support updating reviews via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, but creating new reviews provides better auditability. | Yes |
```

## Sections Included

- Feature Overview (Required)
- Requirements (Required)

## Sections Skipped

- Background and Strategic Fit (Recommended) -- skipped by user
- Goals (Recommended) -- skipped by user
- Non-Functional Requirements (Recommended) -- skipped by user
- Use Cases (Recommended) -- skipped by user
- Customer Considerations (Optional) -- skipped by user
- Customer Information/Supportability (Optional) -- skipped by user
- Documentation Considerations (Optional) -- skipped by user
