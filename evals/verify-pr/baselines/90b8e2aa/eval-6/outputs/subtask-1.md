# Sub-Task: Add Markdown-specific documentation rule to Check 6

## Type: review-feedback

## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation check to Check 6 (Documentation Coverage) in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but sdlc-plugins is a documentation-heavy repository where skills are defined in Markdown. Check 6 should verify that new Markdown sections have introductory explanatory text.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6b to replace the Markdown skip rule with a Markdown-specific documentation check for new `###` headings

## Implementation Notes
- Replace the current "Markdown: not applicable -- skip Markdown files" rule in Check 6b with a Markdown-specific rule
- The Markdown rule should check whether new `###` headings (identified by `+` prefixed lines in the diff starting with `###`) have at least one paragraph of explanatory text before any sub-sections or code blocks
- A "paragraph of explanatory text" means at least one non-empty, non-heading, non-code-fence line between the heading and the next heading or code block
- Follow the structure of the other language-specific rules in Check 6b (Rust, TypeScript/Java, Python, Go)

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule instead of skipping Markdown files
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text before sub-sections or code blocks
- [ ] Existing Check 6 behavior for non-Markdown languages is unchanged

## Review Context
**Comment ID:** 50001
**Reviewer:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md (line 310)
**Comment:** "The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks."

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
