## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: plan-feature should verify that documentation coverage checks cover the repository's primary file format. Task TC-9106 added a Documentation Coverage check (Check 6) to the style-conventions sub-agent but explicitly excluded Markdown files ("Markdown: not applicable -- skip Markdown files"). However, this repository's primary content is Markdown -- skills are defined in SKILL.md files, not in traditional programming languages. The plan-feature skill should include a method-level check when generating tasks for documentation tooling: verify that the proposed documentation check covers the repository's primary file format rather than blindly applying language-only heuristics.

## Files to Modify
- `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- add guidance in the task generation phase to verify that documentation-related checks and tooling account for the repository's primary file format, not just traditional programming language doc comment patterns

## Implementation Notes
- This is a plan-feature skill gap: the task spec for TC-9106 included an explicit Markdown exclusion without checking whether the target repository primarily uses Markdown
- The CONVENTIONS.md for this repository documents: "No source code: This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages"
- The plan-feature skill should include a method-level check: when generating tasks related to documentation coverage, verify that the proposed check covers the repository's primary file format
- This is a universal method (applies to any repository): "Ensure documentation checks cover the repository's primary content format" -- it does not require language-specific knowledge
- Look for the existing repository analysis phase in plan-feature where file types and project structure are assessed; add a cross-check between the proposed documentation tooling and the repository's dominant file format

## Acceptance Criteria
- [ ] plan-feature includes guidance to verify documentation-related checks cover the target repository's primary file format
- [ ] The guidance is method-level (applicable to any repository, not specific to Markdown)
- [ ] The guidance triggers when a task involves documentation coverage, doc comment checking, or similar documentation tooling
