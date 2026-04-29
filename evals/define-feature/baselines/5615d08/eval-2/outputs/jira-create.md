# Jira Create Issue Call

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10142",
  summary="Add bulk SBOM delete endpoint",
  description="## Feature Overview\n\nAdd a bulk delete endpoint for SBOMs that allows users to delete multiple SBOMs in a single API call. Currently users must delete SBOMs one at a time, which is impractical when cleaning up hundreds of test or outdated SBOMs. The endpoint should accept a list of SBOM IDs and return a summary of which deletions succeeded and which failed.\n\n## Requirements\n\n| Requirement | Notes | Is MVP? |\n|---|---|---|\n| `DELETE /api/v2/sboms/bulk` accepts a JSON array of SBOM IDs | Maximum 100 IDs per request | Yes |\n| Return a response with per-ID success/failure status | Include error reason for each failed deletion | Yes |\n| Require the same permissions as single SBOM delete | Reuse existing authorization checks | Yes |\n| Validate all IDs before starting deletions | Return 400 if any ID is malformed | Yes |",
  contentFormat="markdown",
  additional_fields={
    "labels": ["ai-generated-jira"]
  }
)
```

## Parameters

- **cloudId**: `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **projectKey**: `TC`
- **issueTypeId**: `10142`
- **summary**: `Add bulk SBOM delete endpoint`
- **contentFormat**: `markdown`
- **labels**: `["ai-generated-jira"]`
- **assignee**: not set (unassigned)
