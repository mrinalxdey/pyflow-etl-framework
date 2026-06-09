import json
import yaml
import time
import logging
from pathlib import Path
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        duration = end_time - start_time

        logging.info(f"{func.__name__} took {duration:.4f} seconds")

        return result

    return wrapper

@timing_decorator
def load_config(config_path='pyflow/config/config.yaml'):
    '''
    Load .yaml or .json configuration file.

    Parameters:
    config_path : str
        Path to configuration file.

    Returns:
    dict - parsed configuration
    '''
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )
    
    if config_path.suffix.lower() in ['.yaml', '.yml']:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
        
    elif config_path.suffix.lower() == '.json':
        with open(config_path, 'r') as file:
            return json.load(file)
        
    else:
        raise ValueError("Supported config formats are YAML (.yaml/.yml) and JSON (.json)")



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