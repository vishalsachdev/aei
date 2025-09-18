# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Anthropic Economic Index (AEI) Explorer** - an interactive Marimo notebook application for exploring AI adoption patterns from the AEI v3 report. The project is designed to run locally as an interactive notebook and export to a self-contained WebAssembly (WASM) bundle for distribution via GitHub Pages.

## Core Architecture

### Marimo App Structure
- **Main notebook**: `marimo/aei_app.py` - Single-file Marimo application with reactive cells
- **Data package**: `aei_app/data/` - Python package containing CSV datasets bundled with the app
- **Generated docs**: `docs/` - WASM export target for GitHub Pages deployment

### Data Flow Architecture
1. **Data Loading**: Uses `importlib.resources` to load packaged CSV files from `aei_app.data`
2. **Caching**: `@lru_cache` decorator on `load_dataset()` for performance
3. **Reactive UI**: Marimo cells automatically update when upstream selections change
4. **Dataset Selection**: Radio buttons toggle between Claude.ai and 1P API datasets

### Key Data Schema
The datasets follow a normalized structure where each row represents one metric value:
- `geo_id`: Geographic identifier (ISO country codes, US state codes, or "GLOBAL")
- `geography`: Level ("country", "state_us", "global")
- `facet`: Analysis dimension ("country", "onet_task", "collaboration", etc.)
- `cluster_name`: Specific entity within facet (task names, collaboration patterns)
- `variable`: Metric type (`*_count`, `*_pct`, etc.)
- `value`: Numeric metric value

## Common Development Commands

### Local Development
```bash
# Setup environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run interactive notebook
make run
# Equivalent to: python -m marimo run marimo/aei_app.py
```

### Export and Deployment
```bash
# Export to WASM for GitHub Pages
make export
# Equivalent to: python -m marimo export wasm marimo/aei_app.py --output docs

# Clean generated files
make clean
# Equivalent to: rm -rf docs
```

### Adding Data
To add new CSV files to the bundled data package:
1. Place CSV files in `aei_app/data/`
2. Update `DATASETS` dictionary in `marimo/aei_app.py`
3. Ensure `aei_app/data/__init__.py` exists for package recognition

## Data Integration Patterns

### Loading Datasets
```python
from importlib import resources

# Load from packaged data
with resources.files("aei_app.data").joinpath(filename).open("rb") as fh:
    return pd.read_csv(fh)
```

### Geographic Data Handling
The app expects these geography-related columns:
- For country-level: `geo_id` with ISO-2 codes, `geography="country"`
- For US states: `geo_id` with state codes, `geography="state_us"`
- For global: `geo_id="GLOBAL"`, `geography="global"`

### Facet-Based Analysis
Data is organized by `facet` dimension:
- `country`/`state_us`: Geographic aggregations
- `onet_task`: O*NET occupational tasks
- `collaboration`: Human-AI interaction patterns
- `request`: Request categorization
- Intersections: `onet_task::collaboration`, `request::collaboration`

## UI Component Patterns

### Reactive Selectors
```python
# Dataset selector
dataset_selector = mo.ui.radio(options=list(DATASETS.keys()))

# Geography-dependent options
geography_selector = mo.ui.select(options=geography_options_fn(df))
region_selector = mo.ui.select(options=geo_id_options_fn(df, geography_selector.value))
```

### Data Visualization
- Uses **Altair** for charts with `.interactive()` for zoom/pan
- **mo.ui.altair_chart()** for embedding in Marimo
- **mo.ui.table()** for tabular data with `max_height` for scrolling

## Deployment Architecture

### WASM Export Process
The `make export` command creates a self-contained WASM bundle:
- All Python dependencies compiled to WebAssembly
- CSV data files embedded in the bundle
- Runs entirely in browser without server requirements
- Output in `docs/` folder for GitHub Pages

### GitHub Pages Setup
1. Run `make export` to generate `docs/` folder
2. Commit the `docs/` folder to repository
3. Enable GitHub Pages: Settings → Pages → Deploy from branch `main`, folder `docs/`
4. Share the resulting URL - includes all data for offline exploration

## Extension Points

### Adding New Notebooks
- Place additional `.py` files in `marimo/` directory
- Export multiple notebooks: `python -m marimo export wasm marimo/*.py --output docs`
- Each notebook becomes a separate page in the WASM deployment

### Data Enrichment
- Add derived CSV files (per-capita indices, GDP joins) to `aei_app/data/`
- Update `DATASETS` dictionary to include new files
- New data automatically ships with WASM builds

### Custom Analysis Functions
Add new analysis functions following the pattern:
```python
def analysis_fn(df, geography_level, region_focus):
    # Filter and aggregate data
    return processed_df
```

## Dependencies and Requirements

- **marimo>=0.7.9**: Reactive notebook framework
- **pandas>=2.1**: Data manipulation
- **altair>=5.2**: Declarative visualization
- Python 3.9+ (implied by .venv structure)

The minimal dependency set ensures fast WASM compilation and small bundle sizes.