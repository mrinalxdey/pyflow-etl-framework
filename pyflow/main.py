import os
from sqlalchemy import text
from utils import load_config, get_engine
from extractors import get_extractor
from config.logging_config import setup_logging

setup_logging()
config = load_config()
engine = get_engine(config)

file_path = config['etl']['input_path'] + 'yellow_tripdata_2024-01.parquet'
file_name = os.path.basename(file_path)
table_name = os.path.splitext(file_name)[0]
print(table_name)

extractor = get_extractor(file_path)

# with engine.begin() as conn:
#     # result = conn.execute(text("select 1"))
#     # print(result.fetchone())
#     conn.execute(text("""
#         create table if not exists gdp(
#                       id int,
#                       name text)
#     """))

# with engine.begin() as conn:
#     # result = conn.execute(text("select 1"))
#     # print(result.fetchone())
#     conn.execute(text("insert into test_etl (id, name) values (:id, :name)"),
#         {"id":1, "name":"john doe"}
#     )

# with engine.begin() as conn:
#     # result = conn.execute(text("select 1"))
#     # print(result.fetchone())
#     conn.execute(text("drop table if exists test_etl"))


for chunk in extractor.extract(file_path):
    print(chunk)
    break
