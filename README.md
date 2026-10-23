# Test Data Generation & Database Validation Pipeline

A configurable Python CLI for creating realistic customer/order fixtures, injecting controlled edge cases, validating constraints, and exporting reproducible quality reports. It can run validation without a server or persist valid rows to PostgreSQL.

## Features
- Faker-backed generation with a seed for repeatable results.
- `standard` and `edge-cases` profiles; the latter introduces missing, malformed, duplicate, out-of-range, and broken-reference data.
- Required-field, type, format, uniqueness, range, and referential-integrity validation.
- JSON summary and row-level CSV issue report.
- Optional PostgreSQL persistence for valid rows.
- GitHub Actions workflow runs a standard 500-record validation daily and on demand, then publishes report artifacts.

## Quick start
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -e '.[dev]'
data-pipeline run --count 500 --profile standard --seed 42 --output reports
```

Generate deliberately invalid examples:
```bash
data-pipeline run --count 500 --profile edge-cases --seed 42 --output reports
```

Outputs are `reports/validation-summary.json` and `reports/validation-issues.csv`.

## GitHub Actions run
The scheduled workflow runs daily at 01:17 UTC and can also be started manually from the Actions tab. Each successful run stores the JSON and CSV reports as a 14-day workflow artifact. Standard profile generation is used so the scheduled run represents a clean validation batch; the edge-case profile is available for local fault-injection demos.

## PostgreSQL
Start a local database with Docker Compose:
```bash
docker compose up -d postgres
```
Then set `DATABASE_URL=postgresql://pipeline:pipeline@localhost:5432/testdata` and run:
```bash
data-pipeline run --count 500 --profile standard --seed 42 --output reports --persist
```
The pipeline persists only valid customer/order rows and uses a transaction. Never use the sample credentials for a public deployment; provide managed secrets through your host.

## Profiles and configuration
- `--count`: customers to generate (1 through 100000).
- `--profile`: `standard` or `edge-cases`.
- `--seed`: deterministic Faker seed.
- `--output`: report directory.
- `--persist`: store the valid subset (requires `DATABASE_URL`).

See `docs/data-contract.md` for field rules and report meanings.

## License
MIT. See [LICENSE](LICENSE).
