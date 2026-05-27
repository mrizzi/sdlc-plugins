# Jira Create Issue Call Parameters

## MCP Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description="## Feature Overview\n\nAdd a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |\n| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |\n| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |\n| Update the existing eval review if one was previously posted; create a new review only on the first run | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update existing reviews | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters Breakdown

| Parameter | Value |
|---|---|
| cloudId | `2b9e35e3-6bd3-4cec-b838-f4249ee02432` |
| projectKey | `TC` |
| issueTypeId | `10142` |
| summary | `Add automated PR review posting for eval results` |
| contentFormat | `markdown` |
| labels | `["ai-generated-jira"]` |
| assignee | *(unassigned — not included)* |

## Notes

- The user chose to leave the Feature unassigned, so no `assignee` field is included in `additional_fields`.
- The description includes only the two non-skipped sections: Feature Overview and Requirements.
- The Requirements section reflects the corrected language after External API Claim Verification (Requirement #4 was revised to use the `PUT` endpoint for updating reviews instead of always creating new ones).
