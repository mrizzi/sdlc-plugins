## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently, Check 6 skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but this repository's primary content is Markdown skill definitions. The check should verify that new Markdown sections (specifically new `###` headings) have at least one paragraph of introductory/explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 step 6b to replace the Markdown exclusion with a Markdown-specific rule: check whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks

## Implementation Notes
- In step 6b of Check 6, replace the current Markdown bullet ("Markdown: not applicable -- skip Markdown files") with a Markdown-specific rule
- The rule should: scan the PR diff for new `###` (or deeper) headings in Markdown files, and for each new heading, verify that at least one paragraph of explanatory text exists between the heading and the next heading or code block
- A "paragraph of explanatory text" means at least one non-empty line of prose (not a code fence, not a sub-heading, not a table, not a list item alone)
- This aligns with the repository's nature as documented in CONVENTIONS.md: "This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages"
- Follow the structure of the existing language-specific rules in step 6b (Rust, TypeScript/Java, Python, Go)
- The verdict logic in step 6c does not need modification -- PASS/WARN/N/A semantics remain the same, since Markdown sections with missing explanatory text are treated like undocumented symbols

## Acceptance Criteria
- [ ] Check 6 step 6b includes a Markdown-specific rule for verifying new headings have explanatory text
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of text before the next sub-section or code block
- [ ] The previous "Markdown: not applicable -- skip Markdown files" exclusion is removed or replaced
- [ ] The rule correctly identifies new headings from the PR diff (lines with `+` prefix)

## Test Requirements
- [ ] Verify the Markdown rule flags a new `###` heading that is immediately followed by a code block with no explanatory text
- [ ] Verify the Markdown rule passes a new `###` heading that has explanatory text before any sub-sections or code blocks
- [ ] Verify the rule does not flag existing headings that were not introduced in the PR

## Review Context
**Comment by reviewer-b on `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` line 310:**
> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
