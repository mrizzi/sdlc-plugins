Project key: TC
Summary: SBOM delete endpoint returns 200 but does not remove the record
Issue type ID: 10300
Labels: ai-generated-jira

Description:
### **Issue Description**

The `DELETE /api/v2/sbom/{id}` endpoint returns HTTP 200 with an empty body, but the SBOM record remains in the database. Subsequent `GET /api/v2/sbom/{id}` calls still return the SBOM data. This was discovered during verify-pr testing of the bulk delete feature — the underlying single-delete is silently failing.

### **Steps to Reproduce**

1. Create an SBOM via `POST /api/v2/sbom` with a valid CycloneDX document
2. Note the returned SBOM ID
3. Call `DELETE /api/v2/sbom/{id}`
4. Observe HTTP 200 response
5. Call `GET /api/v2/sbom/{id}`
6. Observe that the SBOM is still returned (expected 404)

### **Expected Result**

After a successful DELETE, the SBOM record is removed from the database. Subsequent GET requests for the same ID return HTTP 404.

### **Actual Result**

DELETE returns 200 but the record persists. GET still returns the full SBOM data with HTTP 200.

### **Attachments**

API request/response logs from the verify-pr test run showing the DELETE succeeding but the subsequent GET still returning data.

### **Suggested Fix**

The delete handler in `modules/fundamental/src/sbom/endpoints/mod.rs` calls `service.delete()` but does not check the return value. The service method returns `Ok(0)` (zero rows affected) when the deletion fails due to a foreign key constraint, but the handler treats any `Ok` as success. Add a check for `rows_affected > 0` and return 404 if zero rows were deleted.
