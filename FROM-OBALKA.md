# Folded in from Obálka

These practices came from an audit of Obálka
(github.com/dorhawk-software/obalka), a React Native app for iOS and
Android, at commit 36feacb (2026-11-11). Its history before 2026-11-10 is
squashed into one commit, so the reasons come from its specs, its
constitution, file headers and the commits after the squash.

Unlike Crake's, nothing was copied verbatim: Obálka's scripts are written
for its own app (its store, its changelog languages, its native parts).
The practices were written as docs first; the shared tools are on the
[roadmap](ROADMAP.md) (phase 7).

| Here | From Obálka |
| --- | --- |
| [typescript/conventions.md](typescript/conventions.md) | `.eslintrc.js`, `tsconfig.json`, `patches/`, the constitution |
| [typescript/lints.md](typescript/lints.md) | `npm run verify`, `tools/eslint-plugin-obalka`, the case-clash guard |
| [typescript/testing.md](typescript/testing.md) | `jest.config.js`, `jest.setup.js`, `__mocks__/`, `__tests__/helpers/` |
| [mobile/releases.md](mobile/releases.md) | `scripts/release.mjs`, `.github/workflows/release.yml`, `docs/release-ci.md` |
| [mobile/ci.md](mobile/ci.md) | `.github/workflows/ci.yml`, `scripts/install-ndk.sh` |
| [mobile/devices.md](mobile/devices.md) | `specs/*/tasks.md` walk records, the platform guard tests |
| [mobile/lifecycle.md](mobile/lifecycle.md) | `src/` hooks, the constitution's principle V |
| [common/gates.md](common/gates.md) | the secret scan's canary, `scripts/audit-shipped.mjs`, `scripts/gen-attributions.mjs` |
| [common/crash-reports.md](common/crash-reports.md) | `src/services/telemetry/`, `src/services/debug/` |

The audit's six areas and its method are in
[guides/fold-in-a-project.md](guides/fold-in-a-project.md).
