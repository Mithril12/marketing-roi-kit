from dataclasses import dataclass
from typing import List, Dict, Any
import yaml
from pathlib import Path


@dataclass
class SourceConfig:
    name: str
    channel: str
    type: str
    path: str
    date_format: str
    mappings: Dict[str, str]


@dataclass
class PathsConfig:
    raw_data_dir: str
    processed_dir: str
    outputs_dir: str


@dataclass
class LTVConfig:
    enabled: bool = False
    ltv_per_conversion: float | None = None


@dataclass
class ProjectConfig:
    project_name: str
    paths: PathsConfig
    cogs_pct: float
    ltv: LTVConfig
    sources: List[SourceConfig]


def load_config(path: str) -> ProjectConfig:
    config_path = Path(path)
    with config_path.open("r") as f:
        data = yaml.safe_load(f)

    paths = data.get("paths", {})
    ltv_data = data.get("ltv", {})

    sources = [
        SourceConfig(
            name=s["name"],
            channel=s["channel"],
            type=s.get("type", "csv"),
            path=s["path"],
            date_format=s.get("date_format", "%Y-%m-%d"),
            mappings=s["mappings"],
        )
        for s in data.get("sources", [])
    ]

    project = ProjectConfig(
        project_name=data.get("project_name", "Marketing ROI Project"),
        paths=PathsConfig(
            raw_data_dir=paths.get("raw_data_dir", "data/raw"),
            processed_dir=paths.get("processed_dir", "data/processed"),
            outputs_dir=paths.get("outputs_dir", "outputs"),
        ),
        cogs_pct=float(data.get("cogs_pct", 0.4)),
        ltv=LTVConfig(
            enabled=bool(ltv_data.get("enabled", False)),
            ltv_per_conversion=ltv_data.get("ltv_per_conversion"),
        ),
        sources=sources,
    )
    return project
