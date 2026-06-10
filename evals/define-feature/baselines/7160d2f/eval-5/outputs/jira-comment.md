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
| Update the existing eval review on subsequent runs instead of creating duplicate reviews | Use `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}` to update an existing review; store the review ID to enable updates on re-runs | Yes |

### API Claim Verification

The original requirement stated that "PR reviews cannot be updated after initial submission" and that "The GitHub API does not support modifying a submitted review." This was verified as **incorrect**. The GitHub REST API supports updating a submitted review via `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`. The requirement has been corrected to leverage this capability.

---
*This Feature was defined using [sdlc-workflow/define-feature](https://github.com/mrizzi/sdlc-plugins) v0.9.2*
