# Example: a Rust workspace that takes every practice

A complete, minimal project as it looks after
[start a new project](../../guides/start-a-new-project.md): one crate,
`hello`, that greets you, and around it every file the practices ask for.
Copy any of it into your own project.

It's also a test. The practices repository's CI copies this folder into a
fresh git repository, runs `bin/install` on it, and requires
`.practices/bin/lint` and `.practices/bin/check-coverage` to pass
(`tests/example`). If a change to the kit would fail a well-behaved project,
it fails here first.

## What each file shows

| File | What it demonstrates | Practice |
| --- | --- | --- |
| [Cargo.toml](Cargo.toml) | A workspace: resolver 3, edition 2024, `[workspace.package]` the crates inherit, `publish = false`, every lint an error | [rust/conventions.md](../../rust/conventions.md), [rust/lints.md](../../rust/lints.md) |
| [crates/hello/Cargo.toml](crates/hello/Cargo.toml) | A crate inheriting the workspace's settings and lints | [rust/conventions.md](../../rust/conventions.md) |
| [crates/hello/src/lib.rs](crates/hello/src/lib.rs) | `#![forbid(unsafe_code)]`; numbers with names (`MAX_CHEERS`); a `//!` line saying what the module is; logic in the library so tests reach it; an inline `#[cfg(test)] mod tests` (not counted by the size check) | [rust/conventions.md](../../rust/conventions.md) |
| [crates/hello/src/main.rs](crates/hello/src/main.rs) | A `main` that only calls the library: the few lines no test runs | [rust/coverage.md](../../rust/coverage.md) |
| [clippy.toml](clippy.toml) | At most 200 lines per function | [rust/lints.md](../../rust/lints.md) |
| [deny.toml](deny.toml) | cargo-deny with the permissive licence list (this example is MIT) | [rust/lints.md](../../rust/lints.md) |
| [rust-toolchain.toml](rust-toolchain.toml) | The exact Rust release, pinned | [rust/lints.md](../../rust/lints.md) |
| [.gitignore](.gitignore) | `CLAUDE.local.md` and `dev/private-terms` never committed | [common/privacy-public-repos.md](../../common/privacy-public-repos.md) |
| [.practices/config](.practices/config) | The project's settings: here, `PRIVATE_TERMS=none`, said out loud | [guides/how-it-works.md](../../guides/how-it-works.md) |
| [.practices/coverage-floors](.practices/coverage-floors) | A floor per crate and OS, just under the measured share | [rust/coverage.md](../../rust/coverage.md) |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | The whole gate in one call to `rust-ci.yml@v1`; cancel-in-progress; docs-only pushes skipped | [common/ci-caching.md](../../common/ci-caching.md) |
| [.github/workflows/advisories.yml](.github/workflows/advisories.yml) | A daily advisory check, so a new advisory doesn't block every branch at once | [rust/lints.md](../../rust/lints.md) |
| [.github/workflows/toolchain.yml](.github/workflows/toolchain.yml) | The weekly toolchain bump | [rust/lints.md](../../rust/lints.md) |
| [.github/dependabot.yml](.github/dependabot.yml) | Weekly, grouped, majors apart, a two-week cooldown | [rust/lints.md](../../rust/lints.md) |
| [CLAUDE.md](CLAUDE.md) | Rules and pointers, with each rule's origin | [common/claude-md.md](../../common/claude-md.md) |
| [CHANGELOG.md](CHANGELOG.md) | Unreleased, the five kinds, written for users | [common/changelog.md](../../common/changelog.md) |
| [docs/engineering/not-now.md](docs/engineering/not-now.md) | Deferred work, each with why and when it comes back | [common/not-now.md](../../common/not-now.md) |

## What isn't here, and why

`.practices/bin/` and `.practices/hooks/` aren't committed in this folder:
`bin/install` puts them in, from the scripts in this same repository, so the
example always tests the kit as it is now. A real project commits them (see
[how it works](../../guides/how-it-works.md)).

## Try it

```sh
cp -R examples/rust-workspace /tmp/hello && cd /tmp/hello
git init -q && bin=$OLDPWD/bin && "$bin/install" .
.practices/bin/install-hooks
cargo run -q -- Ada               # Hello, Ada!
.practices/bin/lint && echo "lint: clean"
.practices/bin/check-coverage
```

Then break a rule and watch the gate stop it: add `let x = 42;` to a
function (clippy: unused variable), or write a 701-line file under
`crates/hello/src/`.
