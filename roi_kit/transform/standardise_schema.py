from typing import List
import pandas as pd

from roi_kit.config import ProjectConfig


STANDARD_COLUMNS = [
    "date",
    "channel",
    "campaign",
    "spend",
    "impressions",
    "clicks",
    "conversions",
    "revenue",
]


def standardise(raw_df: pd.DataFrame, config: ProjectConfig) -> pd.DataFrame:
    """
    Standardise multiple platform exports into a canonical schema.

    Assumes raw_df includes __source_name and __channel columns.
    """
    dfs = []
    for src in config.sources:
        subset = raw_df[raw_df["__source_name"] == src.name].copy()

        # Map columns
        for std_col in STANDARD_COLUMNS:
            if std_col == "channel":
                subset[std_col] = src.channel
                continue

            src_col = src.mappings.get(std_col)
            if src_col and src_col in subset.columns:
                subset[std_col] = subset[src_col]
            else:
                # Fill missing metrics with 0
                if std_col not in subset.columns:
                    subset[std_col] = 0.0

        # parse date
        subset["date"] = pd.to_datetime(
            subset["date"], format=src.date_format, errors="coerce"
        )

        # select only standard columns
        dfs.append(subset[STANDARD_COLUMNS])

    if not dfs:
        raise ValueError("No data could be standardised.")

    df = pd.concat(dfs, ignore_index=True)

    # Ensure numeric types
    for col in ["spend", "impressions", "clicks", "conversions", "revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    df["campaign"] = df["campaign"].fillna("Unknown")

    return df
