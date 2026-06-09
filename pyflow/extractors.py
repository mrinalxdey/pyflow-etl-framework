import pandas as pd
import os
from abc import ABC, abstractmethod
from utils import DataSourceError, timing_decorator
from utils import load_config

config = load_config()

class BaseExtractor(ABC):

    def __init__(self, config):
        self.chunk_size = config['etl']['chunk_size']

    def validate_file(self, file_path):
        if not os.path.exists(file_path):
            raise DataSourceError(f"File not found: {file_path}")

    @abstractmethod
    def extract(self, file_path):
        raise NotImplementedError

class CSVExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path):
        self.validate_file(file_path)
        
        for chunk in pd.read_csv(file_path, chunksize=self.chunk_size):
            yield chunk

class JSONExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path):
        self.validate_file(file_path)

        for chunk in pd.read_json(file_path, chunksize=self.chunk_size):
            yield chunk

class ParquetExtractor(BaseExtractor):
    @timing_decorator
    def extract(self, file_path):
        self.validate_file(file_path)
        
        df = pd.read_parquet(file_path)
        for start in range(0, len(df), self.chunk_size):
            yield df.iloc[start:start + self.chunk_size]

    

def get_extractor(file_path):
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
    elif file_type == '.json':
        return JSONExtractor(config)
    elif file_type == '.parquet':
        return ParquetExtractor(config)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")