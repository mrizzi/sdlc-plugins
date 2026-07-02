# Jira Create Issue Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add bulk SBOM delete endpoint",
  description=<composed-description>,
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"],
    "priority": {"name": "Normal"}
  }
)
```

## Field Notes

- **priority**: Set to `Normal` via Jira Field Defaults (Default priority: Normal, Prompt for priority: false -- applied silently without prompting the user).
- **fixVersions**: Not included. Prompt for fixVersion is false and no default fixVersion is configured, so fixVersion is left unset.
- **assignee**: Not included. The user chose to leave the Feature unassigned.
