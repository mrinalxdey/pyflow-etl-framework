import pandas as pd
import os
from pyflow.utils import DataSourceError, timing_decorator
from pyflow.utils import load_config

config = load_config()

@timing_decorator
def extract_csv(file_path, config):
    '''
    Read csv file and generate a yield

    Parameters:
    file_path : str
        Path to .csv or .txt file

    Return:
    dataframe format of the data
    '''
    chunk_size = config['etl']['chunk_size']

    if not os.path.exists(file_path):
        raise DataSourceError(f"File not found: {file_path}")
    
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk
