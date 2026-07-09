# Jira Create Issue Call Parameters

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

## Parameter Details

- **cloudId:** `2b9e35e3-6bd3-4cec-b838-f4249ee02432` (from Jira Configuration)
- **projectKey:** `TC` (from Jira Configuration)
- **issueTypeId:** `10142` (Feature issue type ID from Jira Configuration)
- **summary:** `Add bulk SBOM delete endpoint`
- **description:** The composed markdown description containing only Feature Overview and Requirements sections (skipped sections omitted)
- **contentFormat:** `markdown`
- **additional_fields:**
  - `labels`: `["ai-generated-jira"]`
  - `priority`: `{"name": "Normal"}` — default applied silently from Jira Field Defaults (`Prompt for priority: false`, `Default priority: Normal`)
  - No `assignee` — user left Feature unassigned
  - No `fixVersions` — prompt suppressed (`Prompt for fixVersion: false`) and no default configured

## Composed Description (markdown)

```markdown
## Feature Overview

Add a bulk delete endpoint for SBOMs that allows users to delete multiple
SBOMs in a single API call. Currently users must delete SBOMs one at a
time, which is impractical when cleaning up hundreds of test or outdated
SBOMs. The endpoint should accept a list of SBOM IDs and return a summary
of which deletions succeeded and which failed.

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| `DELETE /api/v2/sboms/bulk` accepts a JSON array of SBOM IDs | Maximum 100 IDs per request | Yes |
| Return a response with per-ID success/failure status | Include error reason for each failed deletion | Yes |
| Require the same permissions as single SBOM delete | Reuse existing authorization checks | Yes |
| Validate all IDs before starting deletions | Return 400 if any ID is malformed | Yes |
```
