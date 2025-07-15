from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api import crud, schemas
from src.api.database import get_db
import psycopg2

app = FastAPI(
    title="Telegram Medical Analytics API",
    description="Provides analytical insights from Telegram messages and image detections",
    version="1.0.0"
)


@app.get("/api/reports/top-channels")
def read_top_channels(limit: int = 10, db: psycopg2.extensions.connection = Depends(get_db)):
    return crud.get_top_channels(db, limit)



@app.get("/api/channels/{channel_name}/activity")
def read_channel_activity(channel_name: str):
    db = get_db()
    try:
        return crud.get_channel_activity(db, channel_name)
    finally:
        db.close()


@app.get("/api/search/messages")
def search_messages(query: str, db=Depends(get_db)):
    return crud.search_messages(db, query)



@app.get("/")
async def root():
    return {"message": "Welcome to the Telegram Medical Pipeline API"}
