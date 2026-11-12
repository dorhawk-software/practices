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

The shared practices, a line per rule (the detail is in .practices/docs/):
@.practices/rules.md

This project's own settings:
- Coverage floors per crate in `.practices/coverage-floors`.
- Every number has a name (`MAX_CHEERS`), or a comment saying why not.
