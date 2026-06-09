import os
import yaml
from sqlalchemy import create_engine
from dotenv import load_dotenv
from utils import load_config

load_dotenv()

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]

config = load_config()
