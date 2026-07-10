## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable --- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown sections (identified by `###` headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` --- update Check 6 step 6b to replace the Markdown "not applicable" exemption with a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- In step 6b of Check 6, replace the current Markdown bullet ("**Markdown:** not applicable --- skip Markdown files") with a Markdown-specific documentation rule
- The Markdown rule should check for new `###` (or deeper) headings introduced in the PR diff and verify each has at least one paragraph of explanatory text before the next heading or code block
- A "paragraph of explanatory text" means at least one non-empty line of prose (not a heading, not a code fence, not a list item alone) between the heading and any sub-section or code block
- Follow the structure of the existing language-specific patterns in step 6b
- The verdict logic in step 6c does not need to change --- undocumented Markdown sections count the same as undocumented symbols (contribute to WARN verdict)

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule instead of the "not applicable" exemption
- [ ] The Markdown rule checks whether new `###` headings have at least one paragraph of explanatory text
- [ ] New Markdown sections without introductory text are flagged as undocumented symbols
- [ ] Existing Markdown handling (sections with explanatory text) produces no false positives

## Test Requirements
- [ ] Verify the Markdown rule flags a new `###` heading immediately followed by a code block or sub-heading with no explanatory text
- [ ] Verify the Markdown rule does not flag a new `###` heading that has a paragraph of explanatory text before sub-sections

## Review Context
**PR Comment ID:** 50001
**Author:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310
**Comment:**
> The Check 6 description says 'Markdown: not applicable --- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/RHEcosystemAppEng/sdlc-plugins/pull/747
