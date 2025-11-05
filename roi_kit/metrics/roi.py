from typing import Tuple
import pandas as pd


def compute_roi(
    df: pd.DataFrame,
    cogs_pct: float = 0.4,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Compute ROI metrics at:
      - overall level
      - by channel
      - by channel+campaign
    """

    if df.empty:
        raise ValueError("No data provided for ROI computation.")

    df = df.copy()

    # Aggregate at different levels
    # Overall
    overall = _compute_aggregated_metrics(
        df.groupby(lambda idx: 0), cogs_pct=cogs_pct
    )
    overall["level"] = "overall"

    # By channel
    by_channel = _compute_aggregated_metrics(df.groupby("channel"), cogs_pct=cogs_pct)
    by_channel["level"] = "channel"

    # By channel + campaign
    by_campaign = _compute_aggregated_metrics(
        df.groupby(["channel", "campaign"]), cogs_pct=cogs_pct
    )
    by_campaign["level"] = "channel_campaign"

    return overall.reset_index(drop=True), by_channel.reset_index(), by_campaign.reset_index()


def _compute_aggregated_metrics(grouped, cogs_pct: float) -> pd.DataFrame:
    agg = grouped.agg(
        spend=("spend", "sum"),
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        conversions=("conversions", "sum"),
        revenue=("revenue", "sum"),
    )

    agg["mer"] = agg["revenue"] / agg["spend"].replace(0, float("nan"))
    agg["roas"] = agg["revenue"] / agg["spend"].replace(0, float("nan"))

    # Net profit = revenue - COGS - marketing spend
    agg["cogs"] = agg["revenue"] * cogs_pct
    agg["net_profit"] = agg["revenue"] - agg["cogs"] - agg["spend"]
    agg["net_roi"] = agg["net_profit"] / agg["spend"].replace(0, float("nan"))

    # CAC
    agg["cac"] = agg["spend"] / agg["conversions"].replace(0, float("nan"))

    # Simple payback (days)
    agg["payback_days"] = agg["spend"] / agg["net_profit"].replace(0, float("nan"))

    return agg
