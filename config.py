from os import environ
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = environ.get('DATABASE_URL')
