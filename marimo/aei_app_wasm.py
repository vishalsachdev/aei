import marimo

__generated_with = "0.15.5"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md("# Anthropic Economic Index Explorer (Demo)")


@app.cell
def __():
    import io
    import pandas as pd
    from functools import lru_cache

    # Embedded sample data for WASM deployment
    CLAUDE_DATA = """geo_id,geography,date_start,date_end,platform_and_product,facet,level,variable,cluster_name,value
AD,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,not_classified,25.0
AD,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,not_classified,62.5
AD,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,task iteration,15.0
AD,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,task iteration,37.5
US,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,not_classified,15420.0
US,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,not_classified,58.2
US,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,task iteration,11080.0
US,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,task iteration,41.8
GB,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,not_classified,2150.0
GB,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,not_classified,61.4
CA,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_count,not_classified,1890.0
CA,country,2025-08-04,2025-08-11,Claude AI (Free and Pro),collaboration,0,collaboration_pct,not_classified,59.8"""

    API_DATA = """geo_id,geography,date_start,date_end,platform_and_product,facet,level,variable,cluster_name,value
US,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_count,not_classified,8540.0
US,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_pct,not_classified,67.2
US,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_count,task iteration,4170.0
US,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_pct,task iteration,32.8
GB,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_count,not_classified,1230.0
GB,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_pct,not_classified,71.5
CA,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_count,not_classified,890.0
CA,country,2025-08-04,2025-08-11,1P API,collaboration,0,collaboration_pct,not_classified,68.9"""

    DATASETS = {
        "Claude.ai usage": CLAUDE_DATA,
        "1P API usage": API_DATA,
    }

    @lru_cache
    def load_dataset(label: str) -> pd.DataFrame:
        """Load dataset from embedded data with caching."""
        data_string = DATASETS[label]
        return pd.read_csv(io.StringIO(data_string))

    return DATASETS, load_dataset, pd


@app.cell
def __(mo):
    mo.md("⚠️ **Demo Version**: This uses sample data for web deployment. The full dataset contains 100K+ rows.")


@app.cell
def __(DATASETS, mo):
    dataset_selector = mo.ui.radio(
        options=list(DATASETS.keys()),
        value="Claude.ai usage",
        label="Select dataset",
    )
    dataset_selector


@app.cell
def __(dataset_selector, load_dataset, mo):
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
    geography_options = sorted(df['geography'].unique().tolist())

    geography_selector = mo.ui.dropdown(
        options=geography_options,
        value=geography_options[0] if geography_options else "country",
        label="Geography level",
    )
    geography_selector


@app.cell
def __(df, geography_selector, mo):
    filtered_df = df[df['geography'] == geography_selector.value]
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
    geo_df = df[df['geography'] == geography_selector.value]
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
    collab_df = df[
        (df['geography'] == geography_selector.value) &
        (df['facet'] == 'collaboration')
    ]

    if region_selector.value != 'ALL':
        collab_df = collab_df[collab_df['geo_id'] == region_selector.value]

    if not collab_df.empty:
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
    facets = sorted(df['facet'].unique().tolist())

    facet_selector = mo.ui.dropdown(
        options=facets,
        value=facets[0] if facets else "country",
        label="Analysis dimension (facet)",
    )
    facet_selector


@app.cell
def __(df, facet_selector, mo, pd):
    facet_df = df[df['facet'] == facet_selector.value]

    if not facet_df.empty:
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
    ### Demo Discussion

    This is a demo version with sample data showing:
    - How collaboration patterns differ between Claude.ai and 1P API usage
    - Usage concentration across different regions
    - Interactive exploration of different analysis dimensions

    **Full version**: Contains 100K+ rows with complete geographic and task breakdowns
    """)


if __name__ == "__main__":
    app.run()