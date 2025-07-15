from sqlalchemy.orm import Session
from sqlalchemy import text
from src.api import schemas
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Generator, List, Dict
from psycopg2.extensions import connection as PGConnection


def get_top_channels(db: psycopg2.extensions.connection, limit: int):
    with db.cursor() as cursor:
        query = """
            SELECT channel_key, COUNT(*) as message_count
            FROM fct_messages
            GROUP BY channel_key
            ORDER BY message_count DESC
            LIMIT %s;
        """
        cursor.execute(query, (limit,))
        result = cursor.fetchall()
        return [{"channel": row[0], "message_count": row[1]} for row in result]


def get_channel_activity(db, channel_name: str):
    conn = next(db)
    query = """
        SELECT 
            date_key AS date,
            COUNT(*) AS messages_sent
        FROM fct_messages
        WHERE channel_key = %(channel_name)s
        GROUP BY date_key
        ORDER BY date_key
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, {"channel_name": channel_name})
        results = cursor.fetchall()
    return results





def search_messages(db: PGConnection, query: str) -> List[Dict]:
    like_query = f"%{query.lower()}%"
    sql = """
        SELECT id, channel, date, text
        FROM stg_telegram_messages
        WHERE LOWER(text) LIKE %(query)s
        ORDER BY date DESC
        LIMIT 50;
    """

    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, {"query": like_query})
        result = cursor.fetchall()
    return result
