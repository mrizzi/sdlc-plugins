## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current Check 6 skips Markdown files entirely, but since sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown, new Markdown sections should be checked for introductory explanatory text. This ensures that new `###` headings (and similar) have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the "Markdown: not applicable -- skip Markdown files" rule with a Markdown-specific documentation check that verifies new headings have introductory paragraphs

## Implementation Notes
- In step 6b of Check 6, the current bullet for Markdown says "not applicable -- skip Markdown files". Replace this with a rule that checks whether new `###` (or deeper) headings in Markdown files have at least one paragraph of explanatory text before any sub-sections or code blocks.
- Follow the structure of the existing language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go) for consistency.
- The Markdown rule should detect new heading lines (lines starting with `#` at various levels) added in the diff and verify that the content immediately following the heading contains explanatory prose, not just sub-headings or fenced code blocks.
- Since Markdown does not have traditional doc comments, the rule should be framed as "introductory text" rather than "doc comment" to match the format naturally.

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule that checks new headings for introductory explanatory text
- [ ] The Markdown rule replaces the previous "not applicable -- skip Markdown files" entry
- [ ] The rule checks that new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- [ ] The rule does not apply to top-level `#` or `##` headings (only section-level headings within skill files)

## Review Context
Reviewer reviewer-b commented on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
