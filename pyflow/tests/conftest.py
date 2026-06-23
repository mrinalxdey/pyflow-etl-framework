import pytest
import pandas as pd

@pytest.fixture
def sample_config():
    return {
        "database": {
            "driver": "postgresql",
            "host": "localhost",
            "port": 5432,
            "db_name": "test_db"
        },
        "etl": {
            "chunk_size": 1000
        }
    }

@pytest.fixture
def sample_csv(tmp_path):
    file = tmp_path / "sample.csv"

    pd.DataFrame(
        {
            "id": [1,2,3],
            "name": ["Alice", "Bob", "Charlie"]
        }
    ).to_csv(file, index=False)

    return file

@pytest.fixture
def valid_df():
    return pd.DataFrame(
        {
            "id": [1, 2],
            "fare_amount": [10.5, 20.0]
        }
    )

@pytest.fixture
def error_file(tmp_path):
    return tmp_path / "errors.csv"

@pytest.fixture
def empty_df():
    return pd.DataFrame()