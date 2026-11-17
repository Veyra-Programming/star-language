# Contributing to Star

Thank you for your interest in contributing to the Star Programming Language!

## Guiding Principles

1. **Specification First**: The [Language Specification](STAR_SPEC.md) is the single source of truth. Changes to syntax or semantics must begin with an amendment to `STAR_SPEC.md`.
2. **Human-Centric Diagnostics**: Any new syntax or runtime feature must provide precise, helpful, and friendly error messages.
3. **Conformance Testing**: All new features and bug fixes must include corresponding tests in `conformance/`.

## Development Workflow

1. Fork and clone the repository.
2. Ensure you have Python 3.8+ installed for the reference bootstrap engine.
3. Run the test suite:
   ```bash
   python tests/run_tests.py
   ```
4. Add new conformance tests to `conformance/` for any new language capability.
5. Submit a clean pull request with detailed rationale.
