"""Interactive AEI explorer built with marimo."""

from functools import lru_cache
from importlib import resources

import altair as alt
import marimo as mo
import pandas as pd


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


def geo_id_options(
    df: pd.DataFrame, geography: str, top_n: int = 25
) -> list[str]:
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


def usage_summary(
    df: pd.DataFrame, geography: str, top_n: int = 10
) -> pd.DataFrame:
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
    df: pd.DataFrame,
    geography: str,
    geo_id: str,
) -> pd.DataFrame:
    mask = (
        (df["geography"] == geography)
        & (df["facet"] == "collaboration")
        & (df["variable"] == "collaboration_pct")
        & (df["geo_id"] == geo_id)
    )
    breakdown = (
        df.loc[mask, ["cluster_name", "value"]]
        .rename(
            columns={
                "cluster_name": "Collaboration pattern",
                "value": "Share %",
            }
        )
        .query("`Collaboration pattern` != 'not_classified'")
        .sort_values("Share %", ascending=False)
    )
    return breakdown.reset_index(drop=True)


def collaboration_chart(data: pd.DataFrame) -> alt.Chart:
    if data.empty:
        return alt.Chart(
            pd.DataFrame({"Share %": [], "Collaboration pattern": []})
        )

    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("Share %", title="Share of conversations (%)"),
            y=alt.Y(
                "Collaboration pattern",
                sort="-x",
                title="Pattern",
            ),
            tooltip=[
                "Collaboration pattern",
                alt.Tooltip("Share %", format=".2f"),
            ],
        )
        .properties(height=280)
    )


app = mo.App(width="full")


@app.cell
def title(mo=mo):
    title = mo.md("# Anthropic Economic Index Explorer")
    return title


@app.cell
def dataset_selector(datasets=DATASETS, mo=mo):
    dataset_selector = mo.ui.radio(
        options=list(datasets.keys()),
        value="Claude.ai usage",
        label="Select dataset",
    )
    return dataset_selector


@app.cell
def df(dataset_selector, load_dataset=load_dataset):
    df = load_dataset(dataset_selector.value)
    return df


@app.cell
def dataset_overview(df, mo=mo):
    dataset_overview = mo.vstack(
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
    return dataset_overview


@app.cell
def geography_selector(
    df,
    geography_options_fn=geography_options,
    mo=mo,
):
    geo_options = geography_options_fn(df)
    geo_initial = "country" if "country" in geo_options else geo_options[0]
    geography_selector = mo.ui.select(
        options=geo_options,
        value=geo_initial,
        label="Geography level",
    )
    return geography_selector


@app.cell
def region_selector(
    df,
    geography_selector,
    geo_id_options_fn=geo_id_options,
    mo=mo,
):
    region_options = geo_id_options_fn(df, geography_selector.value)
    region_initial = region_options[0] if region_options else "GLOBAL"
    region_selector = mo.ui.select(
        options=region_options,
        value=region_initial,
        label="Region focus",
    )
    return region_selector


@app.cell
def usage_view(
    df,
    geography_selector,
    usage_summary_fn=usage_summary,
    mo=mo,
):
    summary_table = usage_summary_fn(df, geography_selector.value)
    usage_view = mo.vstack(
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
    return usage_view


@app.cell
def collaboration_view(
    df,
    geography_selector,
    region_selector,
    breakdown_fn=collaboration_breakdown,
    chart_fn=collaboration_chart,
    mo=mo,
):
    breakdown = breakdown_fn(df, geography_selector.value, region_selector.value)
    chart = chart_fn(breakdown)
    collaboration_view = mo.vstack(
        [
            mo.md(f"### Collaboration patterns: {region_selector.value}"),
            mo.ui.altair_chart(chart, key="collab-chart"),
            mo.ui.table(breakdown, max_height=280),
        ],
        gap="medium",
    )
    return collaboration_view


@app.cell
def discussion_prompts(mo=mo):
    discussion_prompts = mo.md(
        """
### Discussion prompts

- How do directive vs collaborative patterns shift between the Claude.ai and 1P API datasets?
- Which regions sit above the global usage share, and how might local industries explain that concentration?
- Compare two regions of interest: what collaboration pattern differences stand out and what workflows could they reflect?
"""
    )
    return discussion_prompts


if __name__ == "__main__":
    app.run()
