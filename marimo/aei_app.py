import marimo

__generated_with = "0.15.5"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Anthropic Economic Index Explorer")


@app.cell
def __():
    import sys
    import os
    import pandas as pd
    from functools import lru_cache

    # Add current working directory to path (assuming we run from root)
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    DATASETS = {
        "Claude.ai usage": "aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv",
        "1P API usage": "aei_raw_1p_api_2025-08-04_to_2025-08-11.csv",
    }

    @lru_cache
    def load_dataset(label: str) -> pd.DataFrame:
        """Load dataset from packaged data with caching."""
        filename = DATASETS[label]

        # Try importlib.resources first
        try:
            from importlib import resources
            with resources.files("aei_app.data").joinpath(filename).open("rb") as fh:
                return pd.read_csv(fh)
        except (ImportError, ModuleNotFoundError):
            # Fallback to direct file path
            data_path = os.path.join("aei_app", "data", filename)
            return pd.read_csv(data_path)

    return DATASETS, load_dataset, pd


@app.cell
def __(DATASETS, mo):
    dataset_selector = mo.ui.radio(
        options=list(DATASETS.keys()),
        value="Claude.ai usage",
        label="Select dataset",
    )
    dataset_selector


@app.cell
def __(dataset_selector, load_dataset):
    df = load_dataset(dataset_selector.value)
    mo.md(f"**Loaded dataset:** {dataset_selector.value} with {len(df):,} rows")


@app.cell
def __(df, mo):
    mo.vstack([
        mo.md("### Dataset overview"),
        mo.stat(
            label="Rows",
            value=f"{len(df):,}",
            bordered=True
        ),
        mo.stat(
            label="Columns",
            value=", ".join(df.columns[:6]) + ("…" if len(df.columns) > 6 else ""),
            bordered=True
        ),
        mo.stat(
            label="Date range",
            value=f"{df['date_start'].min()} → {df['date_end'].max()}",
            bordered=True
        ),
    ])


@app.cell
def __(df, mo):
    # Get available geography options from the actual data
    geography_options = sorted(df['geography'].unique().tolist())

    geography_selector = mo.ui.dropdown(
        options=geography_options,
        value=geography_options[0] if geography_options else "country",
        label="Geography level",
    )
    geography_selector


@app.cell
def __(df, geography_selector, mo):
    # Get geo_id options for the selected geography level
    filtered_df = df[df['geography'] == geography_selector.value]
    # Filter out NaN values and convert to strings for consistent sorting
    geo_ids = filtered_df['geo_id'].dropna().unique()
    geo_id_options = ['ALL'] + sorted([str(x) for x in geo_ids])

    region_selector = mo.ui.dropdown(
        options=geo_id_options,
        value="ALL",
        label="Region focus",
    )
    region_selector


@app.cell
def __(df, geography_selector, mo, pd):
    # Create usage summary for the selected geography level
    geo_df = df[df['geography'] == geography_selector.value]

    # Filter for usage metrics
    usage_df = geo_df[geo_df['variable'].str.contains('usage_count|usage_pct', na=False)]

    if not usage_df.empty:
        usage_summary = usage_df.groupby('geo_id')['value'].sum().reset_index()
        usage_summary.columns = ['Region', 'Total Usage']
        usage_summary = usage_summary.sort_values('Total Usage', ascending=False).head(10)
    else:
        usage_summary = pd.DataFrame({'Region': ['No data'], 'Total Usage': [0]})

    mo.vstack([
        mo.md("### Usage concentration"),
        mo.md("Top regions by total usage in the selected geography level."),
        mo.ui.table(usage_summary, pagination=False),
    ])


@app.cell
def __(df, geography_selector, mo, pd, region_selector):
    # Create breakdown for collaboration patterns
    collab_df = df[
        (df['geography'] == geography_selector.value) &
        (df['facet'] == 'collaboration')
    ]

    if region_selector.value != 'ALL':
        collab_df = collab_df[collab_df['geo_id'] == region_selector.value]

    if not collab_df.empty:
        # Get collaboration pattern breakdown
        collab_breakdown = collab_df.groupby(['cluster_name', 'variable'])['value'].sum().reset_index()
        collab_breakdown = collab_breakdown[collab_breakdown['variable'] == 'collaboration_pct']
        collab_breakdown = collab_breakdown.sort_values('value', ascending=False)
    else:
        collab_breakdown = pd.DataFrame({
            'cluster_name': ['No data'],
            'variable': ['collaboration_pct'],
            'value': [0]
        })

    mo.vstack([
        mo.md(f"### Collaboration patterns: {region_selector.value}"),
        mo.ui.table(collab_breakdown, pagination=False),
    ])


@app.cell
def __(df, mo):
    # Show available facets for exploration
    facets = sorted(df['facet'].unique().tolist())

    facet_selector = mo.ui.dropdown(
        options=facets,
        value=facets[0] if facets else "country",
        label="Analysis dimension (facet)",
    )
    facet_selector


@app.cell
def __(df, facet_selector, mo, pd):
    # Show data for selected facet
    facet_df = df[df['facet'] == facet_selector.value]

    if not facet_df.empty:
        # Group by cluster_name and show top entries
        if 'cluster_name' in facet_df.columns:
            facet_summary = facet_df.groupby('cluster_name')['value'].sum().reset_index()
            facet_summary = facet_summary.sort_values('value', ascending=False).head(15)
            facet_summary.columns = ['Category', 'Total Value']
        else:
            facet_summary = pd.DataFrame({'Category': ['No data'], 'Total Value': [0]})
    else:
        facet_summary = pd.DataFrame({'Category': ['No facet data'], 'Total Value': [0]})

    mo.vstack([
        mo.md(f"### {facet_selector.value.title()} Analysis"),
        mo.md("Top categories in the selected analysis dimension."),
        mo.ui.table(facet_summary, pagination=False),
    ])


@app.cell
def __(mo):
    mo.md("""
    ### Discussion prompts

    - How do directive vs collaborative patterns shift between the Claude.ai and 1P API datasets?
    - Which regions show high usage concentration, and what might explain these patterns?
    - Compare collaboration patterns across different geographic regions - what differences stand out?
    - How do the different facets (country, collaboration, onet_task) reveal different aspects of AI adoption?
    """)


if __name__ == "__main__":
    app.run()