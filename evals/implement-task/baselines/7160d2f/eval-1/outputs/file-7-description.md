# File 7: docs/api.md

**Action**: MODIFY (conditional -- only if this file documents REST endpoints)

**Purpose**: Document the new GET /api/v2/sbom/{id}/advisory-summary endpoint in the REST API reference.

## Detailed Changes

Would add a new section documenting the endpoint, following the format of existing endpoint documentation in the file:

```markdown
### GET /api/v2/sbom/{id}/advisory-summary

Returns aggregated advisory severity counts for the specified SBOM.

**Path Parameters:**
- `id` (required) -- The SBOM identifier

**Response:**
- `200 OK` -- Returns severity summary
- `404 Not Found` -- SBOM with the given ID does not exist

**Response Body:**
```json
{
  "critical": 2,
  "high": 5,
  "medium": 3,
  "low": 1,
  "total": 11
}
```

| Field | Type | Description |
|---|---|---|
| critical | integer | Number of advisories with Critical severity |
| high | integer | Number of advisories with High severity |
| medium | integer | Number of advisories with Medium severity |
| low | integer | Number of advisories with Low severity |
| total | integer | Total number of unique advisories |
```

## Conventions Followed

- Would inspect the existing `docs/api.md` format before adding content to match its documentation style.
- This is an out-of-scope file (not listed in Files to Modify or Files to Create), so would flag it to the user during Step 9 scope containment check and ask for approval before including it.

## Notes

- This change is driven by SKILL.md Step 6's "Documentation impact" guidance: "If public APIs, CLI commands, or endpoints were added or changed, update related API docs."
- If `docs/api.md` does not document individual endpoints (e.g., if it only links to auto-generated OpenAPI docs), this update would be skipped.
