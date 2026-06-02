# Jira Create Issue Call Parameters

## API Call: `create_issue`

**Project Key**: TC

**Summary**: Add SBOM dependency graph visualization

**Issue Type ID**: 10142

**Description**:
The full composed description from the preview, containing all 9 sections:
1. Feature Overview
2. Background and Strategic Fit
3. Goals
4. Requirements
5. Non-Functional Requirements
6. Use Cases (User Experience & Workflow)
7. Customer Considerations
8. Customer Information/Supportability
9. Documentation Considerations

(See `preview.md` for the complete formatted description body.)

**Labels**: ["ai-generated-jira"]

**Assignee**: { "accountId": "<current-user-account-id>" }

## Raw Parameters

```json
{
  "project": "TC",
  "summary": "Add SBOM dependency graph visualization",
  "issuetype": "10142",
  "description": "<composed description from preview.md>",
  "labels": ["ai-generated-jira"],
  "assignee": { "accountId": "<current-user-account-id>" }
}
```

## Notes

- The assignee is set to the current user (self-assigned) via `myself()` API resolution
- The issue type ID 10142 corresponds to the Feature issue type configured in the project
- The project key TC and cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432 are sourced from the Project Configuration in CLAUDE.md
