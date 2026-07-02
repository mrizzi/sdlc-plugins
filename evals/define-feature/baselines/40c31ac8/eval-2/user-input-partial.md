<!-- SYNTHETIC TEST DATA — user input with only Required sections provided, all others skipped -->

# User Input: Partial Feature Definition

Only Required sections (Feature Overview and Requirements) are provided.
All Recommended and Optional sections are explicitly marked as SKIP to
test that skipped sections are omitted from the output rather than
appearing as empty headings.

**Feature Summary**: Add bulk SBOM delete endpoint

---

## Section 1 — Feature Overview (Required)

Add a bulk delete endpoint for SBOMs that allows users to delete multiple
SBOMs in a single API call. Currently users must delete SBOMs one at a
time, which is impractical when cleaning up hundreds of test or outdated
SBOMs. The endpoint should accept a list of SBOM IDs and return a summary
of which deletions succeeded and which failed.

## Section 2 — Background and Strategic Fit (Recommended)

SKIP

## Section 3 — Goals (Recommended)

SKIP

## Section 4 — Requirements (Required)

| Requirement | Notes | Is MVP? |
|---|---|---|
| `DELETE /api/v2/sboms/bulk` accepts a JSON array of SBOM IDs | Maximum 100 IDs per request | Yes |
| Return a response with per-ID success/failure status | Include error reason for each failed deletion | Yes |
| Require the same permissions as single SBOM delete | Reuse existing authorization checks | Yes |
| Validate all IDs before starting deletions | Return 400 if any ID is malformed | Yes |

## Section 5 — Non-Functional Requirements (Recommended)

SKIP

## Section 6 — Use Cases (Recommended)

SKIP

## Section 7 — Customer Considerations (Optional)

SKIP

## Section 8 — Customer Information/Supportability (Optional)

SKIP

## Section 9 — Documentation Considerations (Optional)

SKIP
