## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the Style/Conventions sub-agent. Currently, Check 6 blanket-skips Markdown files with "Markdown: not applicable -- skip Markdown files." However, this repository defines skills and documentation in Markdown, so new Markdown sections (headings) should be checked for introductory explanatory text. The new rule should verify that new `###` (and deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6b to replace the blanket Markdown exclusion with a Markdown-specific rule that checks whether new headings have introductory text

## Implementation Notes
- In Check 6b's language-specific doc comment patterns list, replace the current "Markdown: not applicable -- skip Markdown files" entry with a new Markdown rule
- The Markdown rule should: for new `###` (or deeper) headings in Markdown files, verify that at least one paragraph of explanatory text exists between the heading and the next sub-section heading or code block
- Follow the structure of the other language entries in Check 6b (Rust, TypeScript/Java, Python, Go) for consistency
- A heading with only a code block or sub-heading immediately following it (no explanatory paragraph) should be flagged as undocumented
- This is specific to documentation-heavy repositories where skills and processes are defined in Markdown

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule for documentation coverage instead of blanket-skipping Markdown files
- [ ] The Markdown rule checks that new `###` (and deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- [ ] Markdown files with new headings that lack introductory text are flagged as undocumented symbols
- [ ] Markdown files with properly documented headings (explanatory text present) pass the check
