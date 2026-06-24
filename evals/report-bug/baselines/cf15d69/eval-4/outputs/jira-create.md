## Jira `createJiraIssue` Call Parameters

```
createJiraIssue(
  cloudId="2b9e35e3-6bd3-4cec-b838-f4249ee02432",
  projectKey="TC",
  issueTypeId="10300",
  summary="SBOM delete endpoint returns 200 but does not remove the record",
  description="### **Issue Description**\n\nThe `DELETE /api/v2/sbom/{id}` endpoint returns HTTP 200 with an empty body, but the SBOM record remains in the database. Subsequent `GET /api/v2/sbom/{id}` calls still return the SBOM data. This was discovered during verify-pr testing of the bulk delete feature — the underlying single-delete is silently failing.\n\n### **Steps to Reproduce**\n\n1. Create an SBOM via `POST /api/v2/sbom` with a valid CycloneDX document\n2. Note the returned SBOM ID\n3. Call `DELETE /api/v2/sbom/{id}`\n4. Observe HTTP 200 response\n5. Call `GET /api/v2/sbom/{id}`\n6. Observe that the SBOM is still returned (expected 404)\n\n### **Expected Result**\n\nAfter a successful DELETE, the SBOM record is removed from the database. Subsequent GET requests for the same ID return HTTP 404.\n\n### **Actual Result**\n\nDELETE returns 200 but the record persists. GET still returns the full SBOM data with HTTP 200.\n\n### **Attachments**\n\nAPI request/response logs from the verify-pr test run showing the DELETE succeeding but the subsequent GET still returning data.\n\n### **Suggested Fix**\n\nThe delete handler in `modules/fundamental/src/sbom/endpoints/mod.rs` calls `service.delete()` but does not check the return value. The service method returns `Ok(0)` (zero rows affected) when the deletion fails due to a foreign key constraint, but the handler treats any `Ok` as success. Add a check for `rows_affected > 0` and return 404 if zero rows were deleted.",
  contentFormat="markdown",
  additional_fields={ "labels": ["ai-generated-jira"] }
)
```
