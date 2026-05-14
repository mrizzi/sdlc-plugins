# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

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
| Update existing PR review when re-running evals on the same PR, or create a new review if none exists | Use the GitHub REST API `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` endpoint to update an existing review body | Yes |

---

**Sections included:** Feature Overview, Requirements

**Sections skipped:** Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations

---

> **Note:** Requirement #4 was corrected during External API Claim Verification. The original claim that "PR reviews cannot be updated after initial submission" and "The GitHub API does not support modifying a submitted review" was found to be incorrect. The GitHub REST API supports `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update a submitted review. The requirement language has been updated to reflect the actual API capability.
