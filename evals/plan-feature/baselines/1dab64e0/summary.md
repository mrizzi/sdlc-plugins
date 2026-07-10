## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 16/16 | 0 | 100% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 14/14 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No 'Not applicable' annotations found — inapplicable conventions appear to be excluded. However, not all rationales follow the prescribed format. Task 1 includes the convention '§Module pattern' with rationale 'Applies: convention has no file-type restriction (broadly applicable).' — this is free-form prose, not the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The prescribed format requires naming a specific file and scope, but this rationale omits both. Other conventions across tasks 1-4 do follow the format correctly (e.g., 'Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust syntax scope'), but one non-conforming rationale means the assertion fails."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 5 (SbomComparePage, UI-facing) references Figma design context: 'The page follows the Figma design layout from the SBOMCompare file (Comparison View page)' and mentions specific PatternFly components (Select, ExpandableSection, Badge, Table, EmptyState, Skeleton, Button, Dropdown) with detailed visual specifications including colored badges, critical row highlighting, and layout details. However, Task 6 (compare action on SBOM list page, also UI-facing — modifies SbomListPage.tsx with checkboxes and a button) does not reference any Figma design context. It mentions PatternFly components (Table, Button) but has no Figma reference. Task 4 (API types, client function, hook) is API-layer and correctly exempt."

</details>

**Pass rate:** 98% · **Tokens:** 79,848 · **Duration:** 368s

**Baseline** (`64970afe`): 98% · 85,343 tokens · 452s

