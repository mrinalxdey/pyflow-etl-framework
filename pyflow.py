import argparse
import logging

from pyflow.main import run_pipeline
from pyflow.watcher import watch_directory
from pyflow.utils import load_config
from pyflow.config.logging_config import setup_logging


def main():
    parser = argparse.ArgumentParser(
        description="PyFlow ETL Framework"
    )

    parser.add_argument(
        "--config",
        default="pyflow/config/config.yaml",
        help="Path to configuration file"
    )

    parser.add_argument(
        "--mode",
        choices=["full", "incremental"],
        default="full",
        help="ETL execution mode"
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Start file watcher"
    )

    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Using config: {args.config}")
    logger.info(f"Running in {args.mode} mode")

    config = load_config(args.config)

    if args.watch:
        logger.info("Starting watcher...")
        watch_directory()
    else:
        run_pipeline()


if __name__ == "__main__":
    main()