# src/load_to_postgres.py

import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger

# Load .env variables
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'port': os.getenv('PGPORT', '5432'),
    'dbname': os.getenv('PGDATABASE', 'postgres'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', ''),
}

DATA_DIR = Path("data/raw/telegram_messages")

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        logger.info("Connected to PostgreSQL database.")
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_message(cur, msg):
    insert_query = """
        INSERT INTO telegram_messages (
            id, channel, date, text, views,
            has_media, is_image, image_path, raw_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """
    try:
        cur.execute(insert_query, (
            msg.get("id"),
            msg.get("channel"),
            msg.get("date"),
            msg.get("text"),
            msg.get("views"),
            msg.get("has_media"),
            msg.get("is_image"),
            msg.get("image_path"),
            json.dumps(msg)  # raw_json
        ))
    except Exception as e:
        logger.error(f"Failed to insert message ID {msg.get('id')}: {e}")

def load_all_json():
    conn = connect_db()
    cur = conn.cursor()

    for date_folder in sorted(DATA_DIR.glob("*")):
        for json_file in date_folder.glob("*.json"):
            logger.info(f"Loading {json_file}")
            messages = load_json_file(json_file)
            for msg in messages:
                insert_message(cur, msg)

    cur.close()
    conn.close()
    logger.success("All data loaded into PostgreSQL.")

if __name__ == "__main__":
    load_all_json()
