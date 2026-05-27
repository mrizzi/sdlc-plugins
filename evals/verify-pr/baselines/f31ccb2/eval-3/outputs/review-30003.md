## Review Comment 30003 — Classification

### Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/mod.rs`, line 18
**Text**: "Nit: `context(\"SBOM not found\")` is misleading here because `.context()` wraps the error message for the anyhow chain -- it doesn't mean the SBOM wasn't found. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the next line. Consider changing the context message to something like `\"Failed to fetch SBOM\"` to avoid confusion in error logs."

### Classification: Nit

### Reasoning
The reviewer explicitly labels this comment as "Nit:" at the start of the message. The language is advisory ("Consider changing") rather than directive. The issue is about the clarity of an error context string in logs, not a functional or correctness concern. The existing code works correctly -- the 404 is properly returned by the `ok_or` call. This is a minor style/clarity improvement for developer experience when reading error logs.

### Action
No sub-task created. Nits are non-blocking feedback and do not require sub-task creation. The PR author may address this at their discretion.
