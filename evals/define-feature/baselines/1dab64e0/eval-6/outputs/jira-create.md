# Jira Issue Creation

## Request

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add automated PR review posting for eval results",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters

- **Cloud ID:** 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Project Key:** TC
- **Issue Type ID:** 10142
- **Summary:** Add automated PR review posting for eval results
- **Content Format:** markdown
- **Labels:** ai-generated-jira
- **Assignee:** Unassigned (not included in additional_fields)
- **Priority:** Not set (omitted from additional_fields)
- **Fix Version:** Not set (omitted from additional_fields)

## Description Content

The description includes the following sections:

1. **Feature Overview** -- High-level description of the CI workflow step that posts eval results as PR review comments when SKILL.md files are modified.

2. **Requirements** -- Four requirements in table format:
   - Post eval results as a GitHub PR review when SKILL.md files change (MVP)
   - Include per-assertion results in the review body (MVP)
   - Handle the case where no evals exist for the modified skill (MVP)
   - PR reviews cannot be updated after initial submission so always create a new review (MVP)

Skipped sections (omitted from description): Background and Strategic Fit, Goals, Non-Functional Requirements, Use Cases, Customer Considerations, Customer Information/Supportability, Documentation Considerations.

## Simulated Response

```json
{
  "id": "12345",
  "key": "TC-789",
  "self": "https://jira.atlassian.net/rest/api/3/issue/12345"
}
```

Note: This is a simulated response. No actual Jira API call was made.
