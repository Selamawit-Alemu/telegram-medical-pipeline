from pydantic import BaseModel
from typing import List, Optional


class ProductReport(BaseModel):
    product_name: str
    mention_count: int


class ChannelActivity(BaseModel):
    date: str  # ISO format, e.g., "2025-07-14"
    message_count: int


class SearchMessage(BaseModel):
    message_id: int
    channel: str
    text: str
    date: str
    
class ProductFrequency(BaseModel):
    product: str
    frequency: int