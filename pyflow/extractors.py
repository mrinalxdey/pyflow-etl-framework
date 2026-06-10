import pandas as pd
import os
import logging
from typing import Any, Generator
from pandas import DataFrame
from abc import ABC, abstractmethod
from config.logging_config import setup_logging
from utils import DataSourceError, ValidationError

# Configure logging
logger = logging.getLogger(__name__)

class BaseExtractor(ABC):

    def __init__(self, config: dict) -> None:
        self.chunk_size = config['etl']['chunk_size']

    def validate_file(self, file_path: str):
        if not os.path.exists(file_path):
            raise DataSourceError(f"File not found: {file_path}")
        
        if os.path.getsize(file_path) == 0:
            raise ValidationError(
                f"File is empty: {file_path}"
            )

        logger.info(f"Validated file: {file_path}")

    def chunk_dataframe(self, df: DataFrame) -> Generator[DataFrame, None, None]:
        for start in range(0, len(df), self.chunk_size):
            yield df.iloc[start:start + self.chunk_size]

    def log_extraction_start(self, file_path: str) -> None:
        logger.info(f"Starting extraction from {file_path}")

    @abstractmethod
    def extract(self, file_path: str):
        raise NotImplementedError

class CSVExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        for chunk in pd.read_csv(file_path, chunksize=self.chunk_size):
            yield chunk

class JSONExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.jsonl':
            for chunk in pd.read_json(file_path, lines=True, chunksize=self.chunk_size):
                yield chunk
        
        elif ext == '.json':
            df = pd.read_json(file_path)
            yield from self.chunk_dataframe(df)

class ParquetExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        logger.info(f"Extracting Parquet file: {file_path}")
        df = pd.read_parquet(file_path)
        yield from self.chunk_dataframe(df)

    

def get_extractor(file_path: str, config: dict) -> BaseExtractor:
    '''
    Gets the required extractor for the provided file

    Parameters:
    file_path : str
        the path to the dataset

    Returns:
    Class containing the required extractor
    '''
    file_type = os.path.splitext(file_path)[1].lower()

    if file_type == '.csv':
        return CSVExtractor(config)
    elif file_type == '.json' or file_type == '.jsonl':
        return JSONExtractor(config)
    elif file_type == '.parquet':
        return ParquetExtractor(config)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")