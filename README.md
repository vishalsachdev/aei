# Anthropic Economic Index Explorer

Interactive materials for exploring the Anthropic Economic Index (AEI) v3 data. The project is prepared to run as a Marimo notebook locally and export to a self-contained WebAssembly (WASM) bundle so students can open it directly from GitHub Pages.

## Repository layout

- `marimo/aei_app.py` – source Marimo notebook.
- `aei_app/data/` – packaged CSV assets bundled with the app.
- `aei_v3_download/` – original documentation and reference material.
- `docs/` – generated WASM bundle for sharing via GitHub Pages (created by the export step).

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Launch the interactive notebook:

```bash
make run
```

## Exporting to WASM

```bash
make export
```

The command writes a self-contained viewer into `docs/`. Commit that folder and enable GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `docs/`). Share the resulting URL with students; the page includes all data assets for offline exploration.

## Suggested extensions

- Add supplementary Marimo notebooks (e.g., separate Claude.ai vs API deep dives) in `marimo/` and export them alongside the main app.
- Layer in enrichment tables (per-capita indices, GDP joins) once the calculations are ready, keeping the derived CSVs inside `aei_app/data/` so they ship with the WASM build.
