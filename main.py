from sqlalchemy import text
from pyflow.utils import load_config, get_engine
from pyflow.extractors import extract_csv
from pyflow.config.logging_config import setup_logging

setup_logging()
config = load_config()
engine = get_engine(config)
file_path = config['etl']['input_path'] + 'gdp.csv'

for chunk in extract_csv(file_path, config):
    print(chunk.shape)
    break

print(type(engine))

with engine.begin() as conn:
    # result = conn.execute(text("select 1"))
    # print(result.fetchone())
    conn.execute(text("""
        create table if not exists test_etl(
                      id int,
                      name text)
    """))

with engine.begin() as conn:
    # result = conn.execute(text("select 1"))
    # print(result.fetchone())
    conn.execute(text("insert into test_etl (id, name) values (:id, :name)"),
        {"id":1, "name":"john doe"}
    )

