import os
import logging
from utils import load_config, get_engine
from extractors import get_extractor
from loaders import load_chunk_to_db
from config.logging_config import setup_logging

setup_logging()
config = load_config()
engine = get_engine(config)
logger = logging.getLogger(__name__)

file_path = config['etl']['input_path'] + 'yellow_tripdata_2024-01.parquet'
file_name = os.path.basename(file_path)
table_name = os.path.splitext(file_name)[0].replace('-',"_").replace(' ',"_")

extractor = get_extractor(file_path)

try:
    for chunk in extractor.extract(file_path):
        load_chunk_to_db(chunk, table_name, engine, chunk_size=config['etl']['chunk_size'])
    
except Exception as e:
    logger.error(f"Pipeline failed: {e}")
    raise