# open-marketing-roi-kit

A practical toolkit that turns disparate ad platform data into clean ROI, payback,
and budget insights.

## What it does

- Ingests **raw CSV exports** from ad platforms (Google Ads, Meta, etc.)
- Standardises them into a common schema:
  - `date`, `channel`, `campaign`, `spend`, `impressions`, `clicks`, `conversions`, `revenue`
- Computes:
  - ROAS (Revenue / Spend)
  - MER (Total revenue / Total marketing)
  - Net ROI ((Revenue – COGS – Spend) / Spend)
  - CAC (Spend / Conversions)
  - Simple payback period (in days) using your margin assumptions

It is NOT "yet another MMM". It's an **ROI operating layer**:
- Handles the boring data wrangling.
- Produces financial metrics.
- Can be extended to plug into MMM frameworks or BI tools.

## Quickstart

### 1. Install

From the repo root:

```bash
pip install -e .
```

This will install the `roi-kit` CLI.

### 2. Prepare a config

Copy `config_example.yml` to `config.yml` and adjust paths and mappings.
Example (simplified):

```yaml
project_name: "My Brand ROI"

paths:
  raw_data_dir: "data/raw"
  processed_dir: "data/processed"
  outputs_dir: "outputs"

cogs_pct: 0.4          # 40% of revenue is cost of goods
ltv:
  enabled: false

sources:
  - name: "google_ads"
    channel: "Google Ads"
    type: "csv"
    path: "data/raw/google_ads_example.csv"
    date_format: "%Y-%m-%d"
    mappings:
      date: "date"
      campaign: "campaign_name"
      spend: "cost"
      impressions: "impressions"
      clicks: "clicks"
      conversions: "conversions"
      revenue: "revenue"

  - name: "meta_ads"
    channel: "Meta"
    type: "csv"
    path: "data/raw/meta_ads_example.csv"
    date_format: "%Y-%m-%d"
    mappings:
      date: "date"
      campaign: "campaign"
      spend: "spend"
      impressions: "impressions"
      clicks: "clicks"
      conversions: "purchases"
      revenue: "purch_value"
```

### 3. Run the pipeline

```bash
roi-kit run --config config.yml
```

Outputs:

- `outputs/roi_summary.csv` – aggregate metrics for the whole dataset
- `outputs/roi_by_channel.csv` – per-channel view
- `outputs/roi_by_campaign.csv` – per-channel+campaign view

### 4. Use incrementality helpers (optional)

In Python:

```python
from roi_kit.metrics.incrementality import ab_lift

result = ab_lift(
    test_conversions=1200,
    test_users=50000,
    control_conversions=900,
    control_users=50000,
    spend_increment=15000.0
)

print(result)
```

Gives you incremental conversions, incremental cost per conversion, incremental ROI,
and a basic confidence interval.

## Streamlit app

You can explore your results via a simple Streamlit UI.

From the repo root:

```bash
streamlit run roi_kit/reporting/streamlit_app.py
```

By default, it looks for a `config.yml` in the project root.
You can also upload a different config file in the sidebar.

The app will:

- Run the pipeline
- Show overall, channel and campaign ROI tables
- Visualise spend and net ROI by channel

## Roadmap / Ideas

- Add connectors to pull data directly from:
  - GA4
  - Google Ads API
  - Meta Marketing API
- Optional adapters for MMM frameworks (Robyn, PyMC-Marketing, etc.)
- Budget scenario planning based on historical ROI curves

## Licence

MIT – see `LICENSE` (to be added).
