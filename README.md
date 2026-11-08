# kemana-backend

A Rust service for accounts, community and moderation. It is currently a bare skeleton: the crate builds, tests and runs, and the repository tooling is in place.

## Requirements

- [mise](https://mise.jdx.dev) for the task runner and tools (`mise install`)
- Every tool version (Rust, Python, hk, cargo-llvm-cov and the linters) is pinned in `mise.toml`

## Build and run

```sh
mise run build
cargo run
```

## Test and check

```sh
mise run check     # rustfmt and clippy with warnings denied
mise run test      # commit scope tests, then cargo test
mise run coverage  # lcov.info (needs cargo-llvm-cov)
```

`mise install` also installs the git hooks (pre-commit, commit-msg and pre-push). See [CONTRIBUTING](.github/CONTRIBUTING.md) for the branch flow and commit rules.

## License

Apache-2.0. See [LICENSE](LICENSE).
