import os
import logging

from pyflow.utils import (
    load_config,
    get_engine,
    timing_decorator,
    PyFlowError,
)
from pyflow.extractors import get_extractor
from pyflow.loaders import load_to_db
from pyflow.config.logging_config import setup_logging
from pyflow.transformers import (
    optimize_memory,
    handle_missing_values,
    handle_fare_outliers,
    remove_duplicate_trips,
    handle_datetime_features,
)

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration and create database engine
config = load_config()
engine = get_engine(config)


def process_file(file_path: str) -> None:
    file_name = os.path.basename(file_path)

    try:
        logger.info(f"Processing file: {file_name}")

        # Select appropriate extractor based on file type
        extractor = get_extractor(file_path, config)

        # Create a valid table name
        table_name = (
            os.path.splitext(file_name)[0]
            .replace("-", "_")
            .replace(" ", "_")
        )

        # Extract, transform, and load data in chunks
        for chunk in extractor.extract(file_path):
            # chunk = handle_datetime_features(chunk)
            chunk = handle_missing_values(chunk)
            chunk = remove_duplicate_trips(chunk)
            chunk = handle_fare_outliers(chunk)
            chunk = optimize_memory(chunk)

            load_to_db(
                chunk,
                table_name,
                engine,
                chunk_size=config["etl"]["chunk_size"],
            )

        logger.info(f"Successfully processed: {file_name}")

    except ValueError:
        logger.warning(f"Skipping unsupported file: {file_name}")

    except PyFlowError as e:
        logger.error(f"Failed processing {file_name}: {e}")

    except KeyboardInterrupt:
        raise


@timing_decorator
def run_pipeline() -> None:
    try:
        logger.info("Pipeline started.")

        data_dir = config["etl"]["input_path"]

        for file_name in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file_name)

            if os.path.isdir(file_path):
                logger.info(f"Skipping directory: {file_name}")
                continue

            process_file(file_path)

        logger.info("Pipeline completed successfully.")

    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user.")
        raise

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")


if __name__ == "__main__":
    try:
        run_pipeline()
    except KeyboardInterrupt:
        logger.info("Application stopped.")