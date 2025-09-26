# Repository Guidelines

## Project Structure & Module Organization
- `marimo/` houses interactive notebooks; `marimo/aei_app.py` is the primary WASM-ready explorer.
- `aei_app/data/` contains packaged CSV assets shipped with the Marimo export.
- `aei_v3_download/` retains reference documentation only; avoid placing code here.
- Supporting narratives and prompts live at the repo root (e.g., `analysis-prompts.md`, `data_analysis_guide.md`).

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — create and activate the local environment.
- `pip install -r requirements.txt` — install Marimo, Altair, and analysis dependencies.
- `make run` (or `python -m marimo run marimo/aei_app.py`) — launch the notebook server for development.
- `make export` — generate the self-contained WASM bundle in `docs/` for GitHub Pages publishing.

## Coding Style & Naming Conventions
- Use Python 3.9+ with 4-space indentation and PEP 8 conventions.
- Prefer descriptive snake_case identifiers (`geography_selector`, `load_dataset`).
- Keep comments minimal and purposeful; favor readable code over extensive commentary.
- Store static assets inside `aei_app/data/` and access them via `importlib.resources` to remain exportable.

## Testing Guidelines
- No automated test suite yet; manually verify changes by:
  - Running `make run` and confirming widgets, tables, and charts render without console errors.
  - Re-exporting (`make export`) to ensure Pyodide loads bundled datasets correctly.
- When adding utilities, structure future tests with `pytest` under a `tests/` directory using `test_*.py` naming.

## Commit & Pull Request Guidelines
- Follow the existing short, imperative commit style (e.g., “Add marimo explorer scaffold”).
- Group related file moves and updates into a single commit; include context when touching data files.
- For PRs, provide: summary of changes, affected commands (`make run`, `make export`), and any manual verification notes; attach screenshots/GIFs for UI adjustments.

## Data Handling Tips
- Keep raw exports under version control only if they are small enough for Git; larger derivatives should be documented, not stored.
- When introducing new datasets, place them in `aei_app/data/`, update `DATASETS`, and double-check WASM output size (<100 MB recommended).
