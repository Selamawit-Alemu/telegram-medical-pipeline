# src/main.py

import sys
import asyncio
from telegram_scraper import TelegramScraper

def main():
    if sys.platform == "win32":
        # Fix event loop policy for Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    scraper = TelegramScraper()
    asyncio.run(scraper.scrape_all())

if __name__ == "__main__":
    main()
