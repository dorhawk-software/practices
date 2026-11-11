# Changelog

What changed for the projects that use the practices. Written by hand,
newest first, in the kinds common/changelog.md describes.

## Unreleased

## 1.0.0 (2026-11-11)

### New

- **The practices, from Crake.** Ten common practices and four Rust ones,
  each with the incident that taught it, how to apply it and how to check
  it, plus guides, a worked example and a roadmap.
- **The kit.** `bin/install` puts the lint gate and its checks (private
  names, file sizes, unsafe code, coverage floors, commit messages, the
  disk floor) and git hooks into a project's `.practices/`, keeping what
  the project owns.
- **Actions and reusable workflows.** `rust-setup`, `rust-lint`,
  `rust-coverage`, `prune-caches`; `rust-ci.yml`, `rust-advisories.yml`,
  `rust-toolchain-bump.yml`; and `sync-projects.yml`, which brings kit
  updates to each project as a pull request.
- **A Claude Code plugin** with skills to adopt the kit, fix what the gate
  finds, and fold in another project's practices.

### Better

- **Checks that fail closed** where Crake's could pass silently: the
  privacy check without its terms file, a lowered coverage floor, a
  skipped scenario, `#[cfg(all(test, ...))]` test modules, untracked files
  with unsafe code.
