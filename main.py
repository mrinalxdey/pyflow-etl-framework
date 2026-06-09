from pyflow.utils import load_config
from pyflow.extractors import extract_csv
from pyflow.config.logging_config import setup_logging

setup_logging()

config = load_config()

file_path = config['etl']['input_path'] + 'gdp.csv'

for row in extract_csv(file_path, config):
    print(row)