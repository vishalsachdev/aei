"""Interactive AEI explorer built with marimo."""

import marimo as mo
import pandas as pd
import altair as alt

from functools import lru_cache
from importlib import resources


DATASETS = {
    "Claude.ai usage": "aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv",
    "1P API usage": "aei_raw_1p_api_2025-08-04_to_2025-08-11.csv",
}


@lru_cache
def load_dataset(label: str) -> pd.DataFrame:
    filename = DATASETS[label]
    with resources.files("aei_app.data").joinpath(filename).open("rb") as fh:
        return pd.read_csv(fh)


def geography_options(df: pd.DataFrame) -> list[str]:
    return sorted(df["geography"].unique())


def geo_id_options(df: pd.DataFrame, geography: str, top_n: int = 25) -> list[str]:
    mask = (
        (df["geography"] == geography)
        & (df["facet"] == geography)
        & (df["variable"] == "usage_pct")
    )
    summary = (
        df.loc[mask, ["geo_id", "value"]]
        .sort_values("value", ascending=False)
        .head(top_n)
    )
    return summary["geo_id"].tolist()


def usage_summary(df: pd.DataFrame, geography: str, top_n: int = 10) -> pd.DataFrame:
    mask = (
        (df["geography"] == geography)
        & (df["facet"] == geography)
        & (df["variable"] == "usage_pct")
    )
    summary = (
        df.loc[mask, ["geo_id", "value"]]
        .rename(columns={"geo_id": "Region", "value": "Usage %"})
        .sort_values("Usage %", ascending=False)
        .head(top_n)
    )
    return summary.reset_index(drop=True)


def collaboration_breakdown(
    df: pd.DataFrame, geography: str, geo_id: str
) -> pd.DataFrame:
    mask = (
        (df["geography"] == geography)
        & (df["facet"] == "collaboration")
        & (df["variable"] == "collaboration_pct")
        & (df["geo_id"] == geo_id)
    )
    breakdown = (
        df.loc[mask, ["cluster_name", "value"]]
        .rename(columns={"cluster_name": "Collaboration pattern", "value": "Share %"})
        .query("`Collaboration pattern` != 'not_classified'")
        .sort_values("Share %", ascending=False)
    )
    return breakdown.reset_index(drop=True)


def collaboration_chart(data: pd.DataFrame) -> alt.Chart:
    if data.empty:
        return alt.Chart(pd.DataFrame({"Share %": [], "Collaboration pattern": []}))

    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("Share %", title="Share of conversations (%)"),
            y=alt.Y("Collaboration pattern", sort="-x", title="Pattern"),
            tooltip=["Collaboration pattern", alt.Tooltip("Share %", format=".2f")],
        )
        .properties(height=280)
    )


app = mo.App(width="full")


@app.cell
def title():
    return mo.md("# Anthropic Economic Index Explorer")


@app.cell
def dataset_selector():
    selector = mo.ui.radio(
        options=list(DATASETS.keys()),
        value="Claude.ai usage",
        label="Select dataset",
    )
    return selector


@app.cell
def df(dataset_selector):
    return load_dataset(dataset_selector.value)


@app.cell
def dataset_overview(df):
    return mo.vstack(
        [
            mo.md("### Dataset overview"),
            mo.stat.value(label="Rows", value=f"{len(df):,}"),
            mo.stat.text(
                label="Columns",
                text=", ".join(df.columns[:6])
                + ("…" if len(df.columns) > 6 else ""),
            ),
            mo.stat.text(
                label="Date range",
                text=f"{df['date_start'].min()} → {df['date_end'].max()}",
            ),
        ],
        gap="small",
    )


@app.cell
def geography_selector(df):
    geo_options = geography_options(df)
    geo_initial = "country" if "country" in geo_options else geo_options[0]
    return mo.ui.select(
        options=geo_options,
        value=geo_initial,
        label="Geography level",
    )


@app.cell
def region_selector(df, geography_selector):
    region_options = geo_id_options(df, geography_selector.value)
    region_initial = region_options[0] if region_options else "GLOBAL"
    return mo.ui.select(
        options=region_options,
        value=region_initial,
        label="Region focus",
    )


@app.cell
def usage_view(df, geography_selector):
    summary_table = usage_summary(df, geography_selector.value)
    return mo.vstack(
        [
            mo.hstack(
                [
                    mo.md("### Usage concentration"),
                    mo.md(
                        "Use the controls above to explore adoption patterns."
                        " The table shows top regions by share of conversations."
                    ),
                ],
                align="top",
                gap="large",
            ),
            mo.ui.table(summary_table, max_height=320),
        ]
    )


@app.cell
def collaboration_view(df, geography_selector, region_selector):
    breakdown = collaboration_breakdown(
        df, geography_selector.value, region_selector.value
    )
    chart = collaboration_chart(breakdown)
    return mo.vstack(
        [
            mo.md(f"### Collaboration patterns: {region_selector.value}"),
            mo.ui.altair_chart(chart, key="collab-chart"),
            mo.ui.table(breakdown, max_height=280),
        ],
        gap="medium",
    )


@app.cell
def discussion_prompts():
    return mo.md(
        """
### Discussion prompts

- How do directive vs collaborative patterns shift between the Claude.ai and 1P API datasets?
- Which regions sit above the global usage share, and how might local industries explain that concentration?
- Compare two regions of interest: what collaboration pattern differences stand out and what workflows could they reflect?
"""
    )


if __name__ == "__main__":
    app.run()
