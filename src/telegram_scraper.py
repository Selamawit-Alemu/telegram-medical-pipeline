# src/telegram_scraper.py

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from loguru import logger
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv


class TelegramScraper:
    def __init__(self):
        load_dotenv()
        self.api_id: int = int(os.getenv('TELEGRAM_API_ID', '0'))
        self.api_hash: str = os.getenv('TELEGRAM_API_HASH', '0')
        self.phone: Optional[str] = os.getenv('PHONE')
        self.session_name: str = "scraper_session"
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

        self.channels: List[str] = [
            'CheMed123',
            'lobelia4cosmetics',
            'tikvahpharma',
        ]

        self.image_channels: List[str] = [
            'CheMed123',
            'lobelia4cosmetics',
        ]

        self.base_path: Path = Path("data/raw")
        self.metadata_path: Path = Path("metadata")
        self.metadata_path.mkdir(exist_ok=True)

        # Load or init last scraped timestamps (per channel)
        self.last_scraped_file: Path = self.metadata_path / "last_scraped.json"
        self.last_scraped: Dict[str, str] = self._load_last_scraped()

        # Setup logger
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.add("logs/scraping.log", rotation="1 week", retention="1 month", enqueue=True)

    def _load_last_scraped(self) -> Dict[str, str]:
        if self.last_scraped_file.exists():
            try:
                with open(self.last_scraped_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded last scraped metadata: {data}")
                    return data
            except Exception as e:
                logger.error(f"Failed to load last scraped file: {e}")
                return {}
        return {}

    def _save_last_scraped(self):
        try:
            with open(self.last_scraped_file, 'w', encoding='utf-8') as f:
                json.dump(self.last_scraped, f, indent=2)
            logger.info(f"Saved last scraped metadata: {self.last_scraped}")
        except Exception as e:
            logger.error(f"Failed to save last scraped file: {e}")

    async def _ensure_directories(self, channel: str, date_str: str):
        msg_dir = self.base_path / "telegram_messages" / date_str
        img_dir = self.base_path / "images" / date_str / channel
        msg_dir.mkdir(parents=True, exist_ok=True)
        img_dir.mkdir(parents=True, exist_ok=True)
        return msg_dir, img_dir

    async def _process_message(self, message, channel: str, img_dir: Path) -> Dict:
        msg_data = {
            'id': message.id,
            'date': message.date.isoformat() if message.date else None,
            'text': message.text or "",
            'views': message.views or 0,
            'channel': channel,
            'has_media': bool(message.media),
            'is_image': False,
            'image_path': None,
        }

        if (channel in self.image_channels and
            isinstance(message.media, MessageMediaPhoto)):
            img_path = img_dir / f"{message.id}.jpg"
            try:
                await message.download_media(file=str(img_path))
                msg_data['is_image'] = True
                msg_data['image_path'] = str(img_path.relative_to(self.base_path))
                logger.info(f"[{channel}] Saved image {img_path.name}")
            except Exception as e:
                logger.error(f"[{channel}] Failed to save image {message.id}: {e}")

        return msg_data

    async def scrape_channel(self, channel: str, limit: int = 1000):
        logger.info(f"Starting scrape for channel: {channel}")

        last_scraped_iso = self.last_scraped.get(channel)
        last_scraped_dt = datetime.fromisoformat(last_scraped_iso) if last_scraped_iso else None
        messages = []

        try:
            async for message in self.client.iter_messages(channel, limit=limit, reverse=True):
                if message.date is None:
                    continue

                # Skip already scraped messages
                if last_scraped_dt and message.date <= last_scraped_dt:
                    continue

                date_str = message.date.strftime('%Y-%m-%d')
                msg_dir, img_dir = await self._ensure_directories(channel, date_str)

                msg_data = await self._process_message(message, channel, img_dir)
                messages.append(msg_data)

                # Update last scraped time
                if (not last_scraped_dt) or (message.date > last_scraped_dt):
                    last_scraped_dt = message.date
                    self.last_scraped[channel] = last_scraped_dt.isoformat()

                await asyncio.sleep(0.2)  # rate limit

            # Save messages JSON if we scraped any new messages
            if messages:
                output_path = msg_dir / f"{channel}.json"
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)
                logger.success(f"[{channel}] Saved {len(messages)} new messages to {output_path}")
            else:
                logger.info(f"[{channel}] No new messages to save.")

            self._save_last_scraped()

        except Exception as e:
            logger.error(f"Failed to scrape channel {channel}: {e}")

    async def scrape_all(self):
        logger.info("Connecting to Telegram...")
        await self.client.start(phone=self.phone)
        logger.info("Telegram client connected.")

        for channel in self.channels:
            await self.scrape_channel(channel)
            await asyncio.sleep(5)  # avoid rate limits

        await self.client.disconnect()
        logger.info("Disconnected Telegram client.")
