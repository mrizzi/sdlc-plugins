# Sub-Task: Root-cause: implement-task skill should ensure convention upgrade eligibility is always evaluated and documented for suggestion-classified comments

## Type: root-cause

## Repository
sdlc-plugins

## Target Branch
main

## Description
The eval-3 assertion failures reveal that the verify-pr skill's implementation does not always evaluate convention upgrade eligibility for suggestion-classified comments. When a review comment is classified as a suggestion, the Style/Conventions sub-agent's Check 1 (Convention Upgrade) should explicitly attempt a CONVENTIONS.md lookup and codebase pattern analysis, and document the result in the classification output -- even when no convention match is found. The current behavior skips this analysis in some cases, leading to missed upgrades and missing sub-task creation.

This is a method-based skill gap in the implement-task phase. The knowledge required -- "always evaluate and document convention upgrade eligibility for every suggestion" -- is universally applicable (it applies to any project with a convention system, not just this repository). The implement-task skill should have ensured that the convention upgrade path was exercised for all suggestion-classified comments.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- strengthen the Convention Upgrade check (Check 1) to make explicit that every suggestion must be evaluated for convention match and the analysis must be documented in the output, regardless of whether a match is found

## Implementation Notes
- In Check 1 (Convention Upgrade), add explicit language that for every suggestion-classified comment, the sub-agent must: (1) check CONVENTIONS.md for a matching convention, (2) check codebase patterns for demonstrated usage, and (3) record the analysis result (match found or no match) in the findings output
- The existing Check 1d "Upgrade Decision" section says suggestions that do not match remain as suggestions, but it does not require the analysis to be documented -- add a requirement to document the analysis regardless of outcome
- This ensures that eval assertions checking for convention upgrade eligibility documentation will pass

## Acceptance Criteria
- [ ] Check 1 explicitly requires convention upgrade eligibility to be evaluated for every suggestion-classified comment
- [ ] Check 1 requires the analysis result (match or no match) to be documented in the output for each suggestion
- [ ] The documented analysis must include what was checked (CONVENTIONS.md sections searched, codebase patterns counted)
