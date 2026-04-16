# Figma Design Context: SBOM Comparison View

**File**: SBOMCompare (mock123)
**Page**: Comparison View
**Source**: Extracted via `get_design_context` from Figma MCP

## UI Structure

The comparison view is a full-page layout with a header toolbar and a vertically stacked
set of collapsible diff sections.

### Header Toolbar

- **Left SBOM selector**: a PatternFly `Select` dropdown showing SBOM name and version
  (e.g., "my-product-sbom v2.3.1"). Pre-populated from URL query param `left`.
- **Right SBOM selector**: identical `Select` dropdown for the second SBOM. Pre-populated
  from URL query param `right`.
- **"Compare" button**: primary action button, disabled until both selectors have values.
  Triggers the diff API call.
- **"Export" dropdown**: secondary button with options "Export JSON" and "Export CSV".
  Disabled until a comparison result is loaded.

### Diff Sections

Each section is a PatternFly `ExpandableSection` with a title, count badge, and a data
table inside. Sections appear in this order:

1. **Added Packages** — packages present in the right SBOM but not in the left.
   Table columns: Package Name, Version, License, Advisories (count).
   Count badge color: green.

2. **Removed Packages** — packages present in the left SBOM but not in the right.
   Table columns: Package Name, Version, License, Advisories (count).
   Count badge color: red.

3. **Version Changes** — packages present in both SBOMs but with different versions.
   Table columns: Package Name, Left Version, Right Version, Direction (upgrade/downgrade).
   Count badge color: blue.

4. **New Vulnerabilities** — advisories affecting the right SBOM that did not affect the left.
   Table columns: Advisory ID, Severity (using `SeverityBadge` component), Title, Affected Package.
   Count badge color: red. Rows with severity "Critical" have a highlighted background.

5. **Resolved Vulnerabilities** — advisories that affected the left SBOM but not the right.
   Table columns: Advisory ID, Severity, Title, Previously Affected Package.
   Count badge color: green.

6. **License Changes** — packages whose license changed between the two SBOMs.
   Table columns: Package Name, Left License, Right License.
   Count badge color: yellow.

### Empty State

When no comparison has been performed yet (page load without query params), show a
PatternFly `EmptyState` with:
- Icon: `ComparisonIcon` (use PatternFly `CodeBranchIcon` as fallback)
- Title: "Select two SBOMs to compare"
- Body: "Choose an SBOM for each side and click Compare to see what changed."

### Loading State

While the comparison API call is in progress, each diff section shows a
`Skeleton` placeholder (PatternFly). The header toolbar is disabled during loading.

## Component Mapping

| Figma Element | PatternFly Component | Notes |
|---|---|---|
| SBOM selector | `Select` (single, typeahead) | Fetches SBOM list via existing `useSboms` hook |
| Diff section | `ExpandableSection` | Default expanded for sections with >0 items |
| Count badge | `Badge` | Color varies by section (see above) |
| Data table | `Table` (composable) | Sortable columns, no pagination (virtualized for >100 rows) |
| Severity indicator | `SeverityBadge` | Existing shared component in `src/components/` |
| Empty state | `EmptyState` | Standard PatternFly empty state pattern |
| Export button | `Dropdown` | Two items: JSON, CSV |

## Backend Interactions

- **Load SBOM list for selectors**: `GET /api/v2/sbom` — existing endpoint, use `useSboms` hook
- **Perform comparison**: `GET /api/v2/sbom/compare?left={id1}&right={id2}` — new endpoint (must be created in backend)
- **Expected response shape**:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
