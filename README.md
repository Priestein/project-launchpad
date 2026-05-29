# Project Launchpad

Project Launchpad is a production-ready FastAPI and CLI toolkit for scanning local repositories for TODO markers, leaked secrets, and oversized files. It is designed as a recruiter-friendly portfolio project with clean architecture, tests, documentation, and report generation.

## Features

- FastAPI health and scan endpoints
- CLI scanner for local folders
- Secret-pattern detection
- TODO/FIXME discovery
- Markdown and JSON report generation
- Clean modular package structure
- Pytest test coverage

## Tech Stack

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- Pytest

## Repository Structure

- `src/launchpad` - application package
- `docs/` - documentation and report outputs
- `assets/screenshots/` - screenshot placeholders
- `tests/` - automated tests
- `examples/` - usage examples

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Run the API

```bash
uvicorn launchpad.api:app --reload
```

### Scan a directory from the CLI

```bash
python -m launchpad.cli scan . --json-output docs/reports/report.json --markdown-output docs/reports/report.md
```

### Open API docs

Visit `http://127.0.0.1:8000/docs` after starting the server.

## Troubleshooting

- If imports fail, confirm the virtual environment is active.
- If tests cannot find `launchpad`, ensure `pip install -r requirements.txt` completed successfully.
- If the scan returns no findings, try scanning a directory with known TODO comments or test secrets.

## Roadmap

- Add GitHub Actions CI
- Add SARIF export
- Add file type ignore rules
- Add richer risk scoring and policy profiles

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Add tests for your change.
4. Run the test suite.
5. Open a pull request.

## License

MIT License
