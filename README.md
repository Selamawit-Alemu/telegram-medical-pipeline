🩺 Telegram Medical Data Pipeline

An end-to-end data engineering project that collects, stores, transforms, and models Telegram messages and media from Ethiopian medical channels. Designed for production, this pipeline follows best practices using modern data tooling and a modular architecture.
📌 Project Overview
Component	Tool / Technology
📥 Data Ingestion	Python + Telethon
🗃️ Raw Storage	Local JSON + image files
🛢️ Data Warehouse	PostgreSQL
🧱 Data Transformation	dbt (Data Build Tool)
✅ Data Validation	dbt built-in + custom tests
⚙️ Orchestration (Next)	Dagster
🧠 Enrichment (Next)	YOLOv8 for image detection
🚀 API (Planned)	FastAPI
✅ Completed Tasks
✅ Task 0: Project Setup

    Organized modular project layout

    Configured .env for secrets and connection variables

    Set up requirements.txt and Python virtual environment

    Initialized Git and version control

    Added .gitignore (excludes target/, __pycache__/, virtual env, etc.)

✅ Task 1: Data Collection

    Used Telethon to scrape messages from Telegram medical channels

    Incremental scraping using metadata/last_scraped.json

    Saved raw JSON messages and images in data/raw/telegram_messages/YYYY-MM-DD/

    Enabled rich logging with loguru

✅ Task 2: Data Modeling & Transformation

    Loaded scraped messages into PostgreSQL using load_to_postgres.py

    Initialized telegram_dbt/ as a dbt project

    Created:

        stg_telegram_messages (staging layer)

        dim_channels, dim_dates (dimension tables)

        fct_messages (fact table)

    Implemented star schema with primary/foreign key constraints

    Applied 14 dbt tests: not_null, unique, custom test no_null_text_with_media, and future date check

    Generated docs using dbt docs generate

🗂 Project Structure

telegram-medical-pipeline/
    ├── data/
    │   └── raw/telegram_messages/YYYY-MM-DD/channel_data.json
    ├── metadata/
    │   └── last_scraped.json
    ├── src/
    │   ├── telegram_scraper.py
    │   └── load_to_postgres.py
    ├── telegram_dbt/
    │   ├── models/
    │   │   ├── staging/stg_telegram_messages.sql
    │   │   └── marts/
    │   │       ├── dim_channels.sql
    │   │       ├── dim_dates.sql
    │   │       └── fct_messages.sql
    │   ├── tests/no_null_text_with_media.sql
    │   └── dbt_project.yml
    ├── .env
    ├── requirements.txt
    ├── README.md
    └── .gitignore

## ⚙️ Local Setup
## ⚠️ Important Notes

- The `target/` folder is included in `.gitignore` because it contains auto-generated dbt build files and docs. To generate this folder locally, run:


    cd telegram_dbt
    dbt run
    dbt test
    dbt docs generate

1. Clone the repository

    git clone https://github.com/YOUR_USERNAME/telegram-medical-pipeline.git
    cd telegram-medical-pipeline

2. Set up Python environment

    python -m venv venv
    source venv/bin/activate  # Windows: .\venv\Scripts\activate
    pip install -r requirements.txt

3. Configure PostgreSQL

        Create a PostgreSQL database and user.

        Update .env with connection details.

4. Run the Scraper

    python src/telegram_scraper.py

5. Load to PostgreSQL

    python src/load_to_postgres.py

6. Transform with dbt

    cd telegram_dbt
    dbt run
    dbt test

7. View dbt Docs

    dbt docs generate
    dbt docs serve

🧪 Testing Summary

    14 dbt tests implemented:

        not_null, unique tests on keys

        Custom test: no_null_text_with_media

        Logic test: no_future_dates in fct_messages

    All tests pass or catch data integrity issues early

