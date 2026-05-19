## Feature Overview

Add an interactive dependency graph visualization to the SBOM detail page.
Users should be able to explore package dependencies as a zoomable,
searchable graph where nodes represent packages and edges represent
dependency relationships. The graph should highlight packages with known
vulnerabilities and allow filtering by severity level. This reduces the
time security teams spend manually tracing transitive dependency chains
from hours to seconds.

## Background and Strategic Fit

Dependency graph visualization is a key differentiator for SBOM management
platforms. Competitors like Snyk and Sonatype offer similar capabilities.
Our platform already ingests and stores full dependency trees during SBOM
processing, but currently only displays them as flat lists on the package
detail page. Surfacing this data as an interactive graph aligns with the
product roadmap goal of "making vulnerability impact assessment intuitive"
and directly supports the Q3 OKR for reducing mean-time-to-triage.

## Goals

- **Who benefits**: Security analysts and engineering leads reviewing
  transitive dependency exposure
- **Current state**: Dependencies are shown as a flat, paginated list on
  the SBOM detail page. Users must manually click through packages to
  trace transitive chains. There is no visual representation of the
  dependency tree structure.
- **Target state**: An interactive graph view on the SBOM detail page
  renders the full dependency tree with visual indicators for vulnerable
  packages. Users can zoom, pan, search, and filter the graph.
- **Goal statements**:
  - Enable security teams to trace transitive vulnerability paths in
    under 30 seconds
  - Provide a visual overview of dependency depth and breadth at a glance
  - Support filtering by vulnerability severity to prioritize remediation

## Requirements

| Requirement | Notes | Is MVP? |
|---|---|---|
| Display SBOM dependencies as an interactive directed graph | Use a force-directed layout with zoom and pan controls | Yes |
| Highlight packages with known vulnerabilities using color coding | Red for critical/high, orange for medium, grey for low/none | Yes |
| Support filtering graph nodes by vulnerability severity | Filter controls in a sidebar panel | Yes |
| Provide a search box to locate specific packages in the graph | Search highlights matching nodes and centers the viewport | Yes |
| Show package details on node click | Display name, version, license, and vulnerability count in a popover | Yes |
| Export graph as SVG or PNG | Download button in the graph toolbar | No |
| Support collapsing/expanding subtrees | Click to collapse a node's children for large graphs | No |

## Non-Functional Requirements

- Graph rendering must handle SBOMs with up to 2,000 packages without
  visible lag (initial render < 3 seconds, interaction response < 100ms)
- The graph component must be accessible — keyboard navigation between
  nodes and screen reader announcements for node focus changes
- Memory usage must not exceed 200MB for the largest expected graphs
- The feature must work in the latest versions of Chrome, Firefox, and
  Safari

## Use Cases (User Experience & Workflow)

### UC-1: Investigate transitive vulnerability exposure

**Persona**: Security analyst
**Pre-conditions**: SBOM has been ingested with vulnerability data linked
to packages
**Steps**:
1. Analyst navigates to SBOM detail page and clicks "Graph View" tab
2. Graph renders showing all packages as nodes with vulnerability coloring
3. Analyst filters to show only critical/high severity packages
4. Analyst clicks a vulnerable package node to see details
5. Analyst traces the path from the vulnerable package back to the root
   to understand the transitive dependency chain

**Expected outcome**: Analyst identifies which direct dependencies bring
in the vulnerable transitive package and can recommend a remediation path

### UC-2: Assess dependency tree breadth

**Persona**: Engineering lead
**Pre-conditions**: SBOM ingested for a new service before production
deployment
**Steps**:
1. Lead opens the dependency graph for the service's SBOM
2. Lead visually assesses the overall structure — depth, breadth, and
   clustering
3. Lead searches for a specific package to check if it is present
4. Lead exports the graph as PNG for inclusion in a review document

**Expected outcome**: Lead has a clear picture of dependency complexity
and can make informed decisions about dependency management

## Customer Considerations

- Large SBOMs (1,000+ packages) may require performance tuning — consider
  progressive rendering or level-of-detail approaches
- Organizations using air-gapped environments need the graph library
  bundled (no CDN dependencies)
- Users with color vision deficiency need non-color indicators (shapes or
  patterns) in addition to the color coding

## Customer Information/Supportability

- Add graph rendering performance metrics to the existing frontend
  Grafana dashboard (render time, node count, interaction latency)
- Monitor for browser memory issues on large SBOMs — add a client-side
  memory guard that shows a warning if the graph exceeds the threshold
- Customer feedback channel: existing "Feature Requests" board in the
  support portal

## Documentation Considerations

- **Doc Impact**: New Content — document the graph view feature, controls,
  and keyboard shortcuts
- **Updates to existing content**: Update the SBOM detail page
  documentation to reference the new Graph View tab
- **Release Notes**: Include as a highlight feature in the next release
  notes
- **User purpose**: Security analysts need to understand how to read and
  navigate the dependency graph effectively
- **Reference material**: Link to the graph library documentation for
  advanced customization options
