## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Address reviewer feedback on PR #747: Add a Markdown-specific documentation coverage rule to Check 6 in style-conventions.md. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since this repository defines skills and documentation primarily in Markdown, the check should verify that new Markdown sections have introductory explanatory text.

## Review Context
**PR Comment #50001** by reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- Replace the "Markdown: not applicable -- skip Markdown files" bullet in Check 6b with a Markdown-specific documentation rule that checks new `###` headings for introductory text

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the Markdown bullet with a rule such as: "**Markdown:** new `###` (or deeper) headings must have at least one paragraph of explanatory text before any sub-sections or code blocks"
- This aligns with the repository's convention of defining skills and documentation in Markdown files
- The rule should only apply to new headings introduced in the diff (consistent with 6a's "new symbol" scoping)
- Follow the same pattern as other language bullets in 6b: specify the convention, then the check criteria

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific documentation rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] Existing language-specific rules (Rust, TypeScript/Java, Python, Go) remain unchanged
