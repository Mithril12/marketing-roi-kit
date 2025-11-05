from pathlib import Path
from typing import List
import pandas as pd

from roi_kit.config import SourceConfig


class CsvExtractor:
    """
    Simple CSV extractor that loads multiple platform exports and tags them with channel.
    """

    def __init__(self, sources: List[SourceConfig]):
        self.sources = sources

    def load_all(self) -> pd.DataFrame:
        frames = []
        for src in self.sources:
            if src.type != "csv":
                # Future extension: other extractors (APIs, warehouses, etc.)
                continue

            p = Path(src.path)
            if not p.exists():
                raise FileNotFoundError(f"Source file not found: {p}")

            df = pd.read_csv(p)
            df["__source_name"] = src.name
            df["__channel"] = src.channel
            frames.append(df)

        if not frames:
            raise ValueError("No CSV sources found or loaded.")

        combined = pd.concat(frames, ignore_index=True)
        return combined
