# Jira create_issue Call Parameters

```
cloud_id: "2b9e35e3-6bd3-4cec-b838-f4249ee02432"
project_key: "TC"
issue_type_id: "10142"
summary: "Add bulk SBOM delete endpoint"
description: (see below)
additional_fields: {
  "labels": ["ai-generated-jira"]
}
```

## Description Field

```
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

## Notes

- **Priority** is not included in `additional_fields` because the user skipped it.
- **Fix Version** is not included in `additional_fields` because the user skipped it.
- **Assignee** is not included because the user left it unassigned.
- Only `labels` is present in `additional_fields`.
