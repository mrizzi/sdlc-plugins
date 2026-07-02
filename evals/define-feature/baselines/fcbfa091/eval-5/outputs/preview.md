# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

**Priority:** Not set

**Fix Version:** Not set

**Assignee:** Unassigned

**Labels:** `ai-generated-jira`

---

**Description:**

## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| Create a new review for each eval run rather than updating a previous review | Preserves review history so reviewers can compare results across runs. Note: the GitHub API does support updating reviews via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`, but creating new reviews provides better auditability. | Yes |
