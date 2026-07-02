# Jira Create Issue Call Parameters

## MCP Call: createJiraIssue

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update the existing eval review on subsequent runs rather than creating duplicate reviews | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters Breakdown

| Parameter | Value | Source |
|---|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` | CLAUDE.md Jira Configuration |
| projectKey | `TC` | CLAUDE.md Jira Configuration |
| issueTypeId | `10142` | CLAUDE.md Feature issue type ID |
| summary | `Add automated PR review posting for eval results` | User input |
| contentFormat | `markdown` | Skill specification |
| labels | `ai-generated-jira` | Skill specification |
| assignee | _(omitted — user chose unassigned)_ | Step 4 |
| priority | _(omitted — skipped)_ | Step 3.5 |
| fixVersions | _(omitted — skipped)_ | Step 3.5 |

## Notes

- The description includes only the two provided sections (Feature Overview and Requirements). All skipped sections are omitted entirely — no empty headings.
- The fourth requirement was corrected after External API Claim Verification found the original claim ("PR reviews cannot be updated after initial submission") to be incorrect. The corrected requirement reflects that the GitHub REST API does support updating submitted reviews via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`.
- No assignee is set because the user chose to leave the Feature unassigned.
- Priority and fixVersion are omitted from `additional_fields` because they were not selected.
