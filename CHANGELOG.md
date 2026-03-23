# Changelog

All notable changes to the sdlc-workflow plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-03-23

### Fixed

- Use inlineCard ADF node for Git Pull Request custom field

## [0.4.0] - 2026-03-20

### Added

- `verify-pr` skill for PR verification against Jira tasks

### Changed

- Added CONVENTIONS.md fill-in prompt to setup skill

### Fixed

- Added markdown footnote to verify-pr GitHub PR comment

### Documentation

- Added version bump decision guide with y-stream vs z-stream criteria

## [0.3.2] - 2026-03-20

### Changed

- Enhanced comment footer with plugin link, skill name, and version
- Added loop detection guidance to implement-task skill
- Added CONVENTIONS.md lookup to plan-feature, implement-task, and setup skills

### Documentation

- Added GitHub release creation step to releasing guide

## [0.3.1] - 2026-03-20

### Changed

- Enhanced `/setup` skill to ship a `constraints.md` template
- Enhanced `/plan-feature` with constraint-aware task generation
- Clarified PR link fallback in `/implement-task` when custom field is not configured

### Documentation

- Added workflow, tools, and conventions documentation
- Added documentation table of contents to CLAUDE.md
- Added PR description format to conventions-spec
- Added release process and changelog entries for v0.2.0 and v0.2.2

## [0.3.0] - 2025-03-20

### Added

- `/setup` skill for project configuration validation
- Project config template and reference documentation

### Changed

- Bumped version to 0.3.0

## [0.2.4] - 2025-03-19

### Added

- Self-verification step in implement-task before commit
- Verification Commands section in plan-feature task template
- Metrics definitions for AI-assisted SDLC workflow
- Architectural constraints document

## [0.2.3] - 2025-03-18

### Added

- Assign-to-me on task start in implement-task

### Fixed

- Removed hardcoded Git Pull Request custom field ID from implement-task

## [0.2.2] - 2025-03-17

### Added

- GitHub Actions workflow for plugin validation
- CLAUDE.md with version sync instructions

### Fixed

- Added version and author fields to plugin manifest
- Updated Git Pull Request custom field ID to customfield_10875
- Removed smoke-test job that requires authentication
- Fixed version reference and marketplace add command in README
- Removed invalid skills array from plugin manifest

## [0.2.1] - 2025-03-17

### Fixed

- Added missing description field to skill entries

## [0.2.0] - 2025-03-16

### Changed

- Genericized skill files to use project configuration contract references

## [0.1.0] - 2025-03-16

### Added

- Initial release of the sdlc-workflow plugin
- `plan-feature` skill — generate implementation plans and Jira tasks from a feature
- `implement-task` skill — implement Jira tasks with structured descriptions
- Plugin marketplace repository structure
- Project configuration contract documentation
- SDLC methodology documentation
- README with installation guide
