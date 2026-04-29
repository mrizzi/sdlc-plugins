# Feature Preview

**Summary (title):** Add automated PR review posting for eval results

**Assignee:** Unassigned

**Labels:** `ai-generated-jira`

---

## Description

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

---

### Sections Included

- Feature Overview
- Requirements

### Sections Skipped

- Background and Strategic Fit
- Goals
- Non-Functional Requirements
- Use Cases (User Experience & Workflow)
- Customer Considerations
- Customer Information/Supportability
- Documentation Considerations

---

> **Note:** An unverified claim was detected in the Requirements section regarding the GitHub API's ability to update PR reviews. Web tools were unavailable to verify this claim. The original wording has been retained. Please verify manually before proceeding.

---

Ready to create this Feature in Jira? You can also request changes to any section before I create it.
