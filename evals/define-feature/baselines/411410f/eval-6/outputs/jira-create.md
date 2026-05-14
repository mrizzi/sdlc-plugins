# Jira Issue Creation

## API Call Details

**Method:** `createJiraIssue` (MCP) or `python3 scripts/jira-client.py create_issue` (REST fallback)

**Parameters:**

- **Cloud ID:** `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **Project Key:** `TC`
- **Issue Type ID:** `10142`
- **Summary:** `Add automated PR review posting for eval results`
- **Content Format:** `markdown`
- **Labels:** `["ai-generated-jira"]`
- **Assignee:** Unassigned (not included in request)

## Description (Markdown)

```markdown
## Feature Overview

Add a CI workflow step that posts eval results as a PR review comment on pull requests that modify skill definitions. When a PR changes a SKILL.md file, the CI pipeline should run the corresponding eval suite and post a summary of pass/fail assertions as a PR review. This gives reviewers immediate visibility into whether skill behavior changes break existing eval expectations.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Post eval results as a GitHub PR review when SKILL.md files change | Use the GitHub REST API to create a review with pass/fail summary | Yes |
| Include per-assertion results in the review body | Format as a Markdown checklist | Yes |
| Handle the case where no evals exist for the modified skill | Post an informational comment instead of a review | Yes |
| PR reviews cannot be updated after initial submission so always create a new review | The GitHub API does not support modifying a submitted review (UNVERIFIED — could not verify this claim against official documentation; please confirm manually) | Yes |
```

## MCP Call (if available)

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<description above>,
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```

## REST API Fallback (if MCP unavailable)

```bash
python3 scripts/jira-client.py create_issue \
  --project TC \
  --summary "Add automated PR review posting for eval results" \
  --description-md "<description above>" \
  --issue-type "10142" \
  --labels ai-generated-jira
```

Note: No `--assignee-id` flag because the user chose to leave the Feature unassigned.
