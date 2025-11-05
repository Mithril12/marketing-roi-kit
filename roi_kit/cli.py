import argparse
from roi_kit.config import load_config
from roi_kit.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        prog="roi-kit",
        description="Open Marketing ROI Kit CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the ROI pipeline")
    run_parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to config YAML file",
    )

    args = parser.parse_args()

    if args.command == "run":
        config = load_config(args.config)
        run_pipeline(config)


if __name__ == "__main__":
    main()
