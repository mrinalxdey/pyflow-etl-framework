import os
import logging
from utils import load_config, get_engine, timing_decorator, PyFlowError
from extractors import get_extractor
from loaders import load_to_db
from config.logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration and create database engine
config = load_config()
engine = get_engine(config)


# Execute ETL pipeline
@timing_decorator
def run_pipeline() -> None:
    logger.info("Pipeline started.")

    # Define file and table information
    data_dir = config['etl']['input_path']

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)

        if os.path.isdir(file_path):
            logger.info(f"Skipping directory: {file_name}")
            continue

        try:
            logger.info(f"Processing file: {file_name}")
            
            # Select appropriate extractor based on file type
            extractor = get_extractor(file_path, config)

            table_name = os.path.splitext(file_name)[0].replace('-',"_").replace(' ',"_")

            # Loading the data into the database in chunks
            for chunk in extractor.extract(file_path):
                load_to_db(chunk, table_name, engine, chunk_size=config['etl']['chunk_size'])
        
        except ValueError as e:
            logger.warning(f"Skipping unsupported file: {file_name}")

        except PyFlowError as e:
            logger.error(f"Failed processing {file_name}: {e}")

    logger.info("Pipeline completed successfully.")

# Run the Pipeline
run_pipeline()