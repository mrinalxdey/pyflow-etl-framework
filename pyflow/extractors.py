import pandas as pd
import os
from typing import Any, Generator
from pandas import DataFrame
from abc import ABC, abstractmethod
from utils import DataSourceError, timing_decorator, load_config

config = load_config()

class BaseExtractor(ABC):

    def __init__(self, config: dict) -> None:
        self.chunk_size = config['etl']['chunk_size']

    def validate_file(self, file_path: str):
        if not os.path.exists(file_path):
            raise DataSourceError(f"File not found: {file_path}")
    
    def chunk_dataframe(self, df):
        for start in range(0, len(df), self.chunk_size):
            yield df.iloc[start:start + self.chunk_size]

    @abstractmethod
    def extract(self, file_path: str):
        raise NotImplementedError

class CSVExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        
        for chunk in pd.read_csv(file_path, chunksize=self.chunk_size):
            yield chunk

class JSONExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)

        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.jsonl':
            for chunk in pd.read_json(file_path, lines=True, chunksize=self.chunk_size):
                yield chunk
        
        elif ext == '.json':
            df = pd.read_json(file_path)
            yield from self.chunk_dataframe(df)

class ParquetExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path: str) -> Generator[DataFrame, None, None]:
        self.validate_file(file_path)
        
        df = pd.read_parquet(file_path)
        yield from self.chunk_dataframe(df)

    

def get_extractor(file_path: str) -> BaseExtractor:
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