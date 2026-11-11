# Changelog

What changed for the projects that use the practices. Written by hand,
newest first, in the kinds common/changelog.md describes.

## Unreleased

### New

- **UI design practices, in `ui/`.** Window buttons where each system puts
  them: macOS draws its own on the left and the header makes room, from
  Crake's Mac fixes, with the GPUI how-to in `rust/gpui.md`. Design before
  build moved here from `common/` (its old link is gone).

### Better

- **Dependabot in a private repository.** The template shows how to group
  major updates into one pull request with at most two open, so the first
  run doesn't open one build per crate (tern's opened six).

## 1.1.1 (2026-11-11)

### Fixed

- **The version a project records.** `bin/install` wrote `v1` into
  `.practices/VERSION` when the moving `v1` tag was newer than the release
  tag on the same commit; it names the release (`v1.1.1`) now.

## 1.1.0 (2026-11-11)

### Better

- **Starting a project in any language.** The start guide is now for every
  project (identity, CLAUDE.md, privacy, the git hooks, CI's cost,
  changelog, not-now), with the Rust steps on a page of their own,
  `guides/start-a-rust-project.md`. `bin/install` puts the Rust parts
  (coverage floors, templates) only into a project with a `Cargo.toml`;
  the hooks work in any repository and never call cargo, which a test now
  checks.

### Fixed

- **Closed-source apps' own crates in cargo deny.** The closed-source
  licence list in the deny.toml template now comes with
  `[licenses.private] ignore = true`; without it, cargo deny called each
  of the app's own unpublished crates unlicensed.
- **Cache pruning in private repositories.** The `prune-caches` action
  asked GitHub's API for the default branch, which the job's token may not
  read in a private repository ("Resource not accessible by
  integration"); the workflow now passes the branch in. Found by tern's
  first CI run.
- **A quiet pre-commit hook.** check-coverage listed every test binary
  and its result even when all passed, filling an agent's context on each
  commit (found adopting tern). It lists them only in CI now.

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
