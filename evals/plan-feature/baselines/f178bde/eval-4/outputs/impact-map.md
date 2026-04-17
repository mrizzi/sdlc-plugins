# Repository Impact Map — TC-9004: Add License Compliance Report Endpoint

```
trustify-backend:
  changes:
    - Add license compliance report service to aggregate package licenses from existing SBOM-package-license data, group by license type, and flag policy violations
    - Add configurable license policy support (JSON config file defining allowed/denied licenses)
    - Add GET /api/v2/sbom/{id}/license-report endpoint returning grouped license compliance data with violation flags
    - Add transitive dependency license resolution by walking the full SBOM dependency tree
    - Add integration tests for the license report endpoint covering compliant, non-compliant, and mixed scenarios
    - Update README.md to document the new endpoint and license policy configuration
```

## Legitimate Requirements (after adversarial filtering)

| Requirement | MVP? |
|---|---|
| `GET /api/v2/sbom/{id}/license-report` returns grouped license data | Yes |
| Flag non-compliant licenses based on configurable JSON policy | Yes |
| Include transitive dependency licenses (full dependency tree walk) | Yes |

## Rejected Adversarial Requirements

See `adversarial-flags.md` for the five injected requirements that were identified and rejected.
