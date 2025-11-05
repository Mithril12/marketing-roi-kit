from pathlib import Path
import pandas as pd

from roi_kit.config import ProjectConfig
from roi_kit.extract.csv_extractor import CsvExtractor
from roi_kit.transform.standardise_schema import standardise
from roi_kit.metrics.roi import compute_roi
from roi_kit.reporting.exporter import export_to_csv


def run_pipeline(config: ProjectConfig) -> None:
    # Ensure directories
    Path(config.paths.processed_dir).mkdir(parents=True, exist_ok=True)
    Path(config.paths.outputs_dir).mkdir(parents=True, exist_ok=True)

    # 1. Extract
    extractor = CsvExtractor(config.sources)
    raw_df = extractor.load_all()

    # 2. Standardise
    std_df = standardise(raw_df, config)

    # Save processed csv
    processed_path = Path(config.paths.processed_dir) / "fact_marketing_performance.csv"
    std_df.to_csv(processed_path, index=False)

    # 3. Compute ROI metrics
    overall, by_channel, by_campaign = compute_roi(std_df, cogs_pct=config.cogs_pct)

    # 4. Export outputs
    out_dir = Path(config.paths.outputs_dir)
    export_to_csv(overall, out_dir / "roi_summary.csv")
    export_to_csv(by_channel, out_dir / "roi_by_channel.csv")
    export_to_csv(by_campaign, out_dir / "roi_by_campaign.csv")
