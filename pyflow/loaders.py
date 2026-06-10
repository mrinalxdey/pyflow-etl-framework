from sqlalchemy import Engine
from pandas import DataFrame
import logging
from utils import load_config, get_engine, timing_decorator, LoadError

config = load_config()
engine = get_engine(config)
logger = logging.getLogger(__name__)


@timing_decorator
def load_chunk_to_db(df: DataFrame, table_name: str, engine: Engine, chunk_size: int =10000) -> None:
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