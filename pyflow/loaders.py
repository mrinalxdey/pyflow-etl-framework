from sqlalchemy import Engine
from pandas import DataFrame
from pathlib import Path
import logging
from pyflow.utils import timing_decorator, LoadError

logger = logging.getLogger(__name__)

@timing_decorator
def load_to_db(df: DataFrame, table_name: str, engine: Engine, chunk_size: int =10000) -> None:
    try:
        df.to_sql(
            name = table_name,
            con = engine,
            if_exists = 'append',
            index = False
        )
        logger.info(f"Loaded {len(df)} data into {table_name}")

    except Exception as e:
        logger.error(
            f"Failed to load chunk into {table_name}: {e}"
        )

        raise LoadError(
            f"Could not load data into table '{table_name}'"
        ) from e
    
def export_data(df: DataFrame, output_path: str) -> None:
    path = Path(output_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        df.to_csv(path, index=False, compression="gzip")

    elif suffix == ".json":
        df.to_json(path, orient="records", indent=4, compression="gzip")

    elif suffix == ".parquet":
        df.to_parquet(path, index=False, compression="snappy")

    elif suffix in (".xlsx", ".xls"):
        df.to_excel(path, index=False)

    else:
        raise ValueError(f"Unsupported file format: {suffix}")