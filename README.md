# kemana-backend

A Rust service for accounts, community and moderation. It is currently a bare skeleton: the crate builds, tests and runs, and the repository tooling is in place.

## Requirements

- [mise](https://mise.jdx.dev) for the task runner and tools (`mise install`)
- Rust 1.99.0, installed automatically by `rustup` from `rust-toolchain.toml`

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

Run `hk install --mise` once to enable the git hooks. See [CONTRIBUTING](.github/CONTRIBUTING.md) for the branch flow and commit rules.

## License

Apache-2.0. See [LICENSE](LICENSE).
