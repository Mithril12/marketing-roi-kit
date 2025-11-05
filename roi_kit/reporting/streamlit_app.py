import streamlit as st
import pandas as pd
from pathlib import Path
import io
from roi_kit.config import load_config
from roi_kit.pipeline import run_pipeline


def load_outputs(outputs_dir: Path):
    roi_summary = pd.read_csv(outputs_dir / "roi_summary.csv")
    roi_channel = pd.read_csv(outputs_dir / "roi_by_channel.csv")
    roi_campaign = pd.read_csv(outputs_dir / "roi_by_campaign.csv")
    return roi_summary, roi_channel, roi_campaign


def main():
    st.set_page_config(page_title="Marketing ROI Kit", layout="wide")
    st.title("📊 Open Marketing ROI Kit")

    st.sidebar.header("Configuration")

    default_config_path = Path("config.yml")
    config_path_str = st.sidebar.text_input(
        "Config path",
        value=str(default_config_path) if default_config_path.exists() else "",
        help="Path to a YAML config file on the server filesystem.",
    )

    uploaded_config = st.sidebar.file_uploader(
        "…or upload a config.yml",
        type=["yml", "yaml"],
        help="If provided, this overrides the path above for this session.",
    )

    run_button = st.sidebar.button("Run pipeline")

    if run_button:
        with st.spinner("Running pipeline…"):
            if uploaded_config is not None:
                # Save uploaded config to a temp path
                cfg_bytes = uploaded_config.read()
                cfg_temp = Path("config_streamlit_temp.yml")
                cfg_temp.write_bytes(cfg_bytes)
                cfg_to_use = cfg_temp
            else:
                if not config_path_str:
                    st.error("Please provide a config path or upload a config file.")
                    return
                cfg_to_use = Path(config_path_str)
                if not cfg_to_use.exists():
                    st.error(f"Config file not found at {cfg_to_use}")
                    return

            config = load_config(str(cfg_to_use))
            run_pipeline(config)

            outputs_dir = Path(config.paths.outputs_dir)
            try:
                roi_summary, roi_channel, roi_campaign = load_outputs(outputs_dir)
            except FileNotFoundError as e:
                st.error(f"Expected output file not found: {e}")
                return

            st.success("Pipeline completed.")

            st.subheader("Overall ROI summary")
            st.dataframe(roi_summary)

            st.subheader("ROI by channel")
            st.dataframe(roi_channel)

            st.subheader("ROI by channel & campaign")
            st.dataframe(roi_campaign)

            # Simple charts
            if "channel" in roi_channel.columns:
                st.markdown("### Spend and Net ROI by channel")
                chart_df = roi_channel.copy()
                # Only keep useful columns
                chart_df = chart_df[["channel", "spend", "net_roi"]]
                chart_df = chart_df.set_index("channel")
                st.bar_chart(chart_df[["spend"]])
                st.bar_chart(chart_df[["net_roi"]])

            # Download links
            st.markdown("### Download outputs")
            for name, df in [
                ("roi_summary.csv", roi_summary),
                ("roi_by_channel.csv", roi_channel),
                ("roi_by_campaign.csv", roi_campaign),
            ]:
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label=f"Download {name}",
                    data=csv_bytes,
                    file_name=name,
                    mime="text/csv",
                )


if __name__ == "__main__":
    main()
