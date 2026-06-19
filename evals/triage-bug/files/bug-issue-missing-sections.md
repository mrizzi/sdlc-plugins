<!-- SYNTHETIC TEST DATA — Bug issue with missing required sections for triage-bug eval testing -->

# Mock Jira Bug Issue (Incomplete)

**Key**: ACME-501
**Summary**: API returns 500 on malformed input
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Labels**: production-incident
**Component**: api-gateway
**Web URL**: https://mock-jira.example.com/browse/ACME-501

---

## Description

### **Issue Description**

The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of
returning a 400 Bad Request with a descriptive error message.

### **Actual Result**

HTTP 500 Internal Server Error with a stack trace in the response body.

### **Attachments**

None.
