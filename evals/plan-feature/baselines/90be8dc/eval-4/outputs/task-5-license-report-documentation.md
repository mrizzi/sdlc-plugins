## Repository
trustify-backend

## Description
Document the license compliance report endpoint and the license policy configuration. This includes API usage documentation for the `GET /api/v2/sbom/{id}/license-report` endpoint and a guide for configuring the license policy JSON file that controls which licenses are flagged as compliant or non-compliant.

## Files to Modify
- `README.md` — Add a section on the license compliance report feature, including endpoint URL, example request/response, and a link to policy configuration details

## Files to Create
- `docs/license-policy.md` — Documentation for the license policy configuration file format, including the JSON schema, examples of allowed/denied license lists, and guidance on common license compliance scenarios (e.g., permissive vs copyleft)

## Implementation Notes
Reference the existing `README.md` for documentation style and structure. The endpoint documentation should include:

1. Endpoint URL: `GET /api/v2/sbom/{id}/license-report`
2. Example response showing the `groups` array with `license`, `packages`, and `compliant` fields
3. Description of how compliance is determined based on the policy configuration
4. Reference to the SPDX license identifier list for standardized license names

The license policy documentation should explain:
1. Location and format of the policy JSON file
2. The `allowed_licenses` and `denied_licenses` fields and their precedence rules
3. How unlisted licenses are treated (compliant by default unless an `allowed_licenses` list is provided)
4. Example configurations for common scenarios

## Acceptance Criteria
- [ ] Endpoint usage is documented with URL, method, path parameters, and example response
- [ ] License policy configuration format is documented with JSON schema and examples
- [ ] Precedence rules for allowed vs denied lists are clearly explained
- [ ] Documentation references SPDX license identifiers

## Documentation Updates
- `README.md` — Add license compliance report section with endpoint reference and link to policy docs
- `docs/license-policy.md` — New document covering policy configuration format, examples, and guidance

## Dependencies
- Depends on: Task 4 — Add integration tests for license report endpoint
