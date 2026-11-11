# Hello

A greeting program: the example consumer of github.com/dorhawk-software/practices.
It shows the shape of a CLAUDE.md that holds rules and pointers, with the
detail in docs/engineering/ (common/claude-md.md).

## Git rules

- Commit as the identity configured in this repository.
- No session IDs or session links in commits; the commit-msg hook refuses them.
- Push once work is done and tested (asked for 2026-11-11).

## Read first

- docs/engineering/not-now.md: what we decided not to do yet.

## Practices

Each line is the rule; the practices repository has the why and the how.

- Lints are errors: `.practices/bin/lint` after every build (the Claude
  hook runs it). Fix, never silence (rust/lints.md).
- Coverage floors per crate in `.practices/coverage-floors`; raise them as
  tests grow, never lower one (rust/coverage.md).
- Every number has a name (`MAX_CHEERS`), or a comment saying why not.
- Every user-facing change adds a line under "Unreleased" in CHANGELOG.md,
  in the same commit (common/changelog.md).
- Whatever we decide not to do now goes in docs/engineering/not-now.md, in
  the same commit (common/not-now.md).
