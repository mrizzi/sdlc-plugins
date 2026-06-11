## Review Comment 30004 -- Classification: question

**Comment:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

**File:** modules/fundamental/src/sbom/endpoints/get.rs, line 1

**Classification reasoning:**

The reviewer asks a clarifying question about the intended behavior of the GET endpoint for soft-deleted SBOMs. The comment is structured as two questions:
- "Have you considered what happens when..." -- asking whether the author has thought about this scenario
- "Is that intentional?" -- explicitly asking for clarification on whether the current behavior is by design

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning a direct GET request for a deleted SBOM would still return it. However, the reviewer does not request a code change -- they ask whether this is the intended design. Notably, the task description states: "The SBOM... remains accessible via direct GET with a `?include_deleted=true` parameter", which suggests the GET endpoint should support the parameter. The reviewer is surfacing a potential gap but framing it as a question, not a directive.

This meets the definition of **question**: the reviewer asks for clarification and no code change is explicitly requested.

**Action:** No sub-task created.
