# src/yolov8_detector/main.py

import os
import glob
import logging
from dotenv import load_dotenv
from psycopg2.extras import execute_values
import psycopg2
from .detector import YOLOv8Detector
from .db import get_db_connection, save_detections
from .detector import YOLOv8Detector

load_dotenv()

logging.basicConfig(
    filename='logs/image_detection.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# DB connection params from environment variables
DB_HOST = os.getenv('PGHOST')
DB_PORT = os.getenv('PGPORT')
DB_NAME = os.getenv('PGDATABASE')
DB_USER = os.getenv('PGUSER')
DB_PASSWORD = os.getenv('PGPASSWORD')

IMAGES_DIR = 'data/raw/images/'

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

def extract_message_id_from_filename(filename: str) -> int:
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    try:
        return int(name)
    except ValueError:
        logging.warning(f"Invalid message id in filename: {filename}")
        return None

def save_detections(conn, message_id: int, detections):
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

def main():
    logging.info("Starting YOLOv8 detection")

    detector = YOLOv8Detector()

    conn = get_db_connection()

    image_files = glob.glob(os.path.join(IMAGES_DIR, '**', '*.*'), recursive=True)
    image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    logging.info(f"Found {len(image_files)} images")

    for image_path in image_files:
        message_id = extract_message_id_from_filename(image_path)
        if message_id is None:
            continue
        detections = detector.detect(image_path)
        save_detections(conn, message_id, detections)

    conn.close()
    logging.info("YOLOv8 detection completed")

if __name__ == '__main__':
    main()
