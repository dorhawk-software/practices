# Practices

The public source of truth for how dorhawk.software builds software:
practices (common/, ui/ and one folder per language), and the kit that
enforces them (scripts/, hooks/, actions/, .github/workflows/, plugin/).
README.md is the map; read it first.

## Rules for this repository

- **Documentation is the product** (the owner, 2026-11-11: "extremely well
  documented with examples, guides, todos"). A change to the kit changes
  its doc, guide, example and ROADMAP.md in the same commit, and adds a
  line under "Unreleased" in CHANGELOG.md.
- **Every practice has four parts**: What, Why (the incident, its cost,
  and a link to the commit that paid for it), Apply, Check. No essays:
  plain words, sentences under 25 words.
- **Public repository.** No client or company names from private work,
  no real hosts or non-documentation addresses, no email addresses or
  account names, no people's names (roles only). Examples use ACME,
  Globex, Initech, `*.example`, 192.0.2.x / 198.51.100.x / 203.0.113.x.
- **The checkers are tested.** A change to a script in scripts/ or hooks/
  comes with a case in tests/run that fails without it. Scripts run on
  bash 3.2 (macOS) and BSD tools: no mapfile, no associative arrays, no
  GNU-only flags. A check that can't do its work fails; it never says
  "clean".
- **Pin third-party actions by commit SHA** (with the version in a
  comment), choosing releases at least two weeks old.
- **Never break `@v1`.** A change that would break a project using the
  actions or workflows is a new major version.
- Commits: the subject is the outcome; the body says why. Co-Authored-By
  is fine; never a session ID or session link (CI refuses them).

## Checks

```sh
tests/run       # the kit's checks on throwaway projects (seconds)
tests/links     # every relative link in the docs resolves
tests/example   # the kit end to end on examples/rust-workspace (needs Rust)
shellcheck -x -P SCRIPTDIR scripts/lib.sh scripts/lint scripts/check-* scripts/claude-hook \
  scripts/disk-guard scripts/install-hooks hooks/* bin/install tests/*
```

CI (.github/workflows/ci.yml) runs all of them, tests/run on Linux and
macOS, plus actionlint and the commit-message check.

## Adding a practice or a project

guides/fold-in-a-project.md. Next in line: Obálka (React Native, a
`typescript/` folder) and the dorhawk.software website (`web/`).
