# File 6: docs/api.md (conditional)

**Action**: MODIFY (only if the file exists and documents advisory or SBOM endpoints)

**Purpose**: Add documentation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Detailed Changes

This modification is conditional -- per Step 6's "Documentation impact" section and Step 9's "Documentation currency" check, API documentation should be updated if it exists and covers the modified domain.

### Addition

Add an entry for the new endpoint in the appropriate section of the API documentation:

```markdown
### GET /api/v2/sbom/{id}/advisory-summary

Returns aggregated advisory severity counts for the specified SBOM.

**Path Parameters:**
- `id` (required) -- The SBOM identifier

**Response (200 OK):**
```json
{
  "critical": 3,
  "high": 12,
  "medium": 8,
  "low": 2,
  "total": 25
}
```

**Error Responses:**
- `404 Not Found` -- The specified SBOM ID does not exist

**Notes:**
- Counts only unique advisories (deduplicates by advisory ID)
- All severity levels default to 0 when no advisories exist at that level
```

### Conventions Applied

- Documentation format would match the existing style in `docs/api.md`
- This is a lightweight documentation update scoped to the new endpoint only
- If `docs/api.md` does not document individual endpoints at this level of detail, this update would be skipped
