# src/api/database.py
import os
import psycopg2
from dotenv import load_dotenv
from typing import Generator

# Load environment variables from .env file
load_dotenv()

# Environment variables
DB_HOST = os.getenv('PGHOST',)
DB_PORT = os.getenv('PGPORT')
DB_NAME = os.getenv('PGDATABASE')
DB_USER = os.getenv('PGUSER')
DB_PASSWORD = os.getenv('PGPASSWORD')
# Connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def get_db() -> Generator:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()