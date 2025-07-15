# src/yolov8_detector/db.py
import os
import logging
import psycopg2
from psycopg2.extras import execute_values
from typing import List, Tuple

DB_HOST = os.getenv('PGHOST')
DB_PORT = os.getenv('PGPORT')
DB_NAME = os.getenv('PGDATABASE')
DB_USER = os.getenv('PGUSER')
DB_PASSWORD = os.getenv('PGPASSWORD')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logging.info("Connected to database")
        return conn
    except Exception as e:
        logging.error(f"DB connection error: {e}")
        raise

def save_detections(conn, message_id: int, detections: List[Tuple[str, float]]):
    if not detections:
        return
    try:
        with conn.cursor() as cur:
            records = [(message_id, cls, conf) for cls, conf in detections]
            query = """
                INSERT INTO fct_image_detections (message_id, detected_object_class, confidence_score)
                VALUES %s
            """
            execute_values(cur, query, records)
        conn.commit()
        logging.info(f"Saved {len(detections)} detections for message_id {message_id}")
    except Exception as e:
        logging.error(f"Error saving detections: {e}")
        conn.rollback()
