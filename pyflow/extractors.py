import pandas as pd
import os
import json
import logging
from typing import Any, Generator
from pandas import DataFrame
from abc import ABC, abstractmethod
from config.logging_config import setup_logging
from utils import DataSourceError, ValidationError, load_config
from validators import validate_csv_structure

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

config = load_config()

class BaseExtractor(ABC):

    def __init__(self, config: dict) -> None:
        self.chunk_size = config['etl']['chunk_size']

    def detect_encoding(self, file_path: str) -> str:
        encodings = ['utf-8', 'latin1', "cp1252"]

        with open(file_path, "rb") as f:
            sample = f.read(10000)

        for encoding in encodings:
            try:
                sample.decode(encoding)
                logger.info(f"Detected encoding '{encoding}' for {file_path}")
                return encoding
            
            except UnicodeDecodeError:
                continue

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
        compression = None
        dtype_mapping = config.get("dtypes")

        if file_path.endswith(".gz"):
            compression = "gzip"
        elif file_path.endswith(".zip"):
            compression = "zip"

        if file_path.endswith((".gz", ".zip")):
            encoding = "utf-8"
        else:
            encoding = self.detect_encoding(file_path)
        if not file_path.endswith((".gz", ".zip")):
            bad_rows = validate_csv_structure(
                file_path=file_path,
                encoding=encoding,
                error_file=os.path.join("pyflow","logs",f"{os.path.basename(file_path)}_errors.log")
            )

            if bad_rows:
                logger.warning(f"Found {bad_rows} malformed rows in {file_path}")
        
        for chunk in pd.read_csv(file_path, 
                                 dtype=dtype_mapping, 
                                 compression=compression, 
                                 on_bad_lines='skip', 
                                 encoding=encoding, 
                                 chunksize=self.chunk_size):
            yield chunk

class JSONExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        encoding = self.detect_encoding(file_path)
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.jsonl':
            for chunk in pd.read_json(file_path, encoding=encoding, lines=True, chunksize=self.chunk_size):
                yield pd.json_normalize(
                    chunk.to_dict(orient='records')
                )
        
        elif ext == '.json':
            with open(file_path, encoding=encoding) as f:
                data = json.load(f)
            df = pd.json_normalize(data)
            yield from self.chunk_dataframe(df)

class ParquetExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        logger.info(f"Extracting Parquet file: {file_path}")
        df = pd.read_parquet(file_path)
        yield from self.chunk_dataframe(df)

class ExcelExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        self.log_extraction_start(file_path)

        sheets = pd.read_excel(file_path, sheet_name=None)
        dfs = []

        for sheet_name, df in sheets.items():
            df['source_sheet'] = sheet_name
            dfs.append(df)
        
        merged_df = pd.concat(
            dfs,
            ignore_index=True
        )

        yield from self.chunk_dataframe(merged_df)


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

    if file_type in ['.csv', '.gz', '.zip']:
        return CSVExtractor(config)
    elif file_type in ['.json', '.jsonl']:
        return JSONExtractor(config)
    elif file_type == '.parquet':
        return ParquetExtractor(config)
    elif file_type in ['.xlsx', '.xls']:
        return ExcelExtractor(config)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")