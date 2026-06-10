import os
import json
import yaml
import time
import logging
from pathlib import Path
from typing import Callable, Any
from functools import wraps
from sqlalchemy import create_engine, Engine
from dotenv import load_dotenv

load_dotenv()

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]

def timing_decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        duration = end_time - start_time

        logging.info(f"{func.__name__} took {duration:.4f} seconds")

        return result

    return wrapper


def load_config(config_path: str ='pyflow/config/config.yaml') -> dict[str, Any]:
    '''
    Load .yaml or .json configuration file.

    Parameters:
    config_path : str
        Path to configuration file.

    Returns:
    dict - parsed configuration
    '''
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )
    
    if path.suffix.lower() in ['.yaml', '.yml']:
        with open(path) as file:
            return yaml.safe_load(file)
        
    elif path.suffix.lower() == '.json':
        with open(path, 'r') as file:
            return json.load(file)
        
    else:
        raise ValueError("Supported config formats are YAML (.yaml/.yml) and JSON (.json)")

def get_engine(config: dict) -> Engine:
    '''
    Creates an engine/connection to postgresql

    Parameters:
    config : dict
        dictionary containing database credentials

    Returns:
    create_engine()
        a function with connection string to the database
    '''
    db = config['database']
    return create_engine(
        f"{db['driver']}://{username}:{password}@{db['host']}:{db['port']}/{db['db_name']}"
    )

class PyFlowError(Exception):
    """Base exception for PyFlow"""
    pass

class DataSourceError(PyFlowError):
    """Raised when data extraction fails"""
    pass

class ValidationError(PyFlowError):
    """Raised when validation fails"""
    pass

class TransformationError(PyFlowError):
    """Raised when transformation fails"""
    pass

class LoadError(PyFlowError):
    """Raised when loading to DB fails"""
    pass