# Contributing to kemana-backend

Thank you for contributing. Keep changes focused, tested and easy to review.

## Before you start

1. Search existing issues and pull requests.
2. For a new feature or an architectural change, open an issue first so the approach can be agreed.
3. Run `mise install` and `hk install --mise` so the git hooks run locally.

## Branch flow

```text
feature/*, fix/*  →  develop  →  release/*  →  main
hotfix/*          →  main
```

| Branch | Created from | Merged into | Merge method |
|---|---|---|---|
| `feature/*` | `develop` | `develop` | Squash |
| `fix/*` | `develop` | `develop` | Squash |
| `release/*` | `develop` | `main`, then back into `develop` | Merge commit into `main` |
| `hotfix/*` | `main` | `main`, then back into `develop` | Merge commit into `main` |

`develop` and `main` are protected: changes go through pull requests, and force pushes and deletions are blocked. Merged branches are deleted automatically.

## Commit messages

Commits follow [Conventional Commits](https://www.conventionalcommits.org) and are checked by the `commit-msg` hook:

```text
type(scope): summary
```

- **Types:** `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `revert`. Add `!` after the scope for a breaking change.
- **Scope:** a Cargo package or workspace member name read from `Cargo.toml` (such as `kemana-backend`), or one of the areas `build`, `ci`, `deps`, `tooling`, `docs`, `release`. The scope is optional for `ci` and `docs`.
- **Summary:** imperative, starts with a lowercase letter, no trailing period. The whole header is at most 72 characters.

Examples:

```text
feat(kemana-backend): add the health endpoint
fix(kemana-backend): reject empty display names
docs: describe the release flow
```

## Pull requests

- Use the pull request template.
- The pull request title must be a valid commit header: it becomes the squash commit on `develop`.
- One pull request is one complete change: logic, wiring and tests together. Keep unrelated refactors out.
- Resolve all review conversations before merging.

## Code style

- Rust is formatted by rustfmt on commit. Run `mise run format` to format manually.
- Prefer clear names and small functions over comments. Comment only on a non-obvious reason.
- Write tests first.

## Local verification

```sh
mise run check
mise run test
```

The `pre-push` hook runs both. On every pull request CI runs rustfmt, clippy with warnings denied, the commit scope tests, and the Rust tests with coverage uploaded to Codecov. CI must pass before a pull request is merged.

## Secrets

Never commit tokens, keys or personal data. Configuration that differs per environment belongs in untracked `.env` files or CI secrets.
