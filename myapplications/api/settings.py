from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
PGADMIN_EMAIL = os.getenv("PGADMIN_EMAIL")
PGADMIN_PASSWORD = os.getenv("PGADMIN_PASSWORD")