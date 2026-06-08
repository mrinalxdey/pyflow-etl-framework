import os
import yaml
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]

with open('pyflow\config\config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# url = ""
# engine = create_engine(
#     url
# )