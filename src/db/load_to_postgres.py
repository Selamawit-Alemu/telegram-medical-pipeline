
# src/load_to_postgres.py

import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from typing import Any, Dict, List
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Load environment variables
load_dotenv()

# DB configuration from environment
DB_CONFIG = {
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT"),
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
}

# Raw data path from .env
DATA_DIR = Path(os.getenv("RAW_DATA_DIR", "data/raw/telegram_messages"))

def connect_db() -> psycopg2.extensions.connection:
    """Establishes a PostgreSQL connection using environment config."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        logger.info("✅ Connected to PostgreSQL.")
        return conn
    except Exception as e:
        logger.error(f"❌ DB connection failed: {e}")
        raise

def load_json_file(filepath: Path) -> List[Dict[str, Any]]:
    """Loads a JSON file and returns the list of messages."""
    try:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ Failed to load {filepath}: {e}")
        return []

def insert_message(cur: psycopg2.extensions.cursor, msg: Dict[str, Any]) -> None:
    """Inserts a message into telegram_messages table."""
    query = """
        INSERT INTO telegram_messages (
            id, channel, date, text, views,
            has_media, is_image, image_path, raw_json
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """
    try:
        cur.execute(query, (
            msg.get("id"),
            msg.get("channel"),
            msg.get("date"),
            msg.get("text"),
            msg.get("views"),
            msg.get("has_media"),
            msg.get("is_image"),
            msg.get("image_path"),
            json.dumps(msg),
        ))
    except Exception as e:
        logger.error(f"❌ Failed insert for ID {msg.get('id')}: {e}")

def load_all_json() -> None:
    """Scans and loads all JSON files into the database."""
    conn = connect_db()
    cur = conn.cursor()
    count = 0

    for date_folder in sorted(DATA_DIR.glob("*")):
        if not date_folder.is_dir():
            continue
        for json_file in date_folder.glob("*.json"):
            logger.info(f"📂 Loading {json_file}")
            messages = load_json_file(json_file)
            for msg in messages:
                insert_message(cur, msg)
                count += 1

    cur.close()
    conn.close()
    logger.success(f"✅ Loaded {count} messages into PostgreSQL.")

if __name__ == "__main__":
    load_all_json()
