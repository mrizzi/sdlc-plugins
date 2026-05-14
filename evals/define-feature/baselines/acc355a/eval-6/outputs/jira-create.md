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
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## Parameters

- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Project Key:** TC
- **Issue Type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Assignee:** Unassigned (not included in additional_fields)
- **Labels:** ai-generated-jira

## Description Content

The description includes the following sections:

1. **Feature Overview** (Required) -- included
2. **Background and Strategic Fit** (Recommended) -- skipped
3. **Goals** (Recommended) -- skipped
4. **Requirements** (Required) -- included
5. **Non-Functional Requirements** (Recommended) -- skipped
6. **Use Cases** (Recommended) -- skipped
7. **Customer Considerations** (Optional) -- skipped
8. **Customer Information/Supportability** (Optional) -- skipped
9. **Documentation Considerations** (Optional) -- skipped

## Composed Description (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on
pull requests that modify skill definitions. When a PR changes a SKILL.md
file, the CI pipeline should run the corresponding eval suite and post a
summary of pass/fail assertions as a PR review. This gives reviewers
immediate visibility into whether skill behavior changes break existing
eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review | Yes |
```
