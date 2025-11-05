from pathlib import Path
import pandas as pd


def export_to_csv(df: pd.DataFrame, path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)
