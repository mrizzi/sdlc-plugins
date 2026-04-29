# Review Comment Classification: 30004

**Comment ID:** 30004
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** code change request

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification Reasoning

This is a **code change request**. Although phrased as a question ("Have you considered...", "Is that intentional?"), the reviewer is identifying a functional gap: the GET endpoint does not filter out soft-deleted SBOMs. The task description explicitly lists `modules/fundamental/src/sbom/endpoints/get.rs` in Files to Modify with the instruction to "add `include_deleted` parameter support", and the acceptance criteria states "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" -- implying that without the parameter, soft-deleted SBOMs should be excluded. The PR diff does not include any changes to `get.rs`, meaning this is a missing implementation. The reviewer's question exposes an unimplemented acceptance criterion, making this effectively a code change request to add the `include_deleted` filtering to the GET-by-ID endpoint.
