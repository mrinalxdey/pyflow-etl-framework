from sqlalchemy import text
import logging
from utils import load_config, get_engine

config = load_config()
engine = get_engine(config)
logger = logging.getLogger(__name__)

class LoadError(Exception):
    """Raised when data loading fails."""
    pass

def load_chunk_to_db(df, table_name, engine, chunk_size=10000):
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