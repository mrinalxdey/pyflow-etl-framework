import os
import logging
from utils import load_config, get_engine
from extractors import get_extractor
from loaders import load_chunk_to_db
from config.logging_config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

# Load configuration and create database engine
config = load_config()
engine = get_engine(config)

# Define file and table information
file_path = config['etl']['input_path'] + 'gdp.csv'
file_name = os.path.basename(file_path)
table_name = os.path.splitext(file_name)[0].replace('-',"_").replace(' ',"_")

# Select appropriate extractor based on file type
extractor = get_extractor(file_path)

# Execute ETL pipeline
try:
    logger.info("Pipeline started.")

    for chunk in extractor.extract(file_path):
        load_chunk_to_db(chunk, table_name, engine, chunk_size=config['etl']['chunk_size'])
    
    logger.info("Pipeline completed successfully.")

except Exception as e:
    logger.error(f"Pipeline failed: {e}")
    raise
