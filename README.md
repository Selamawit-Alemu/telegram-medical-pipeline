# telegram-medical-pipeline
# Telegram Medical Data Pipeline 📡🩺

This is an end-to-end data pipeline project that collects, transforms, and models messages and images from Ethiopian medical Telegram channels. The pipeline is designed for production use and follows best practices in data engineering and modern data stack tooling.

---

## 🧱 Project Overview

This pipeline is built using:

| Component | Tool |
|----------|------|
| 🐍 Data Collection | Python Telegram scraper |
| 🗃️ Data Storage | PostgreSQL |
| 📐 Data Modeling | dbt (Data Build Tool) |
| 🧪 Testing & Validation | dbt tests |
| 📦 Orchestration (later) | Dagster (Planned) |
| 🧠 Enrichment (later) | YOLOv8 for image object detection |
| 🚀 API Interface (later) | FastAPI |

---

## ✅ Completed Tasks

### ✅ Task 0: Project Setup
- Structured project repo
- Created virtual environment (`venv`)
- Initialized Git, PostgreSQL, and dbt

### ✅ Task 1: Data Scraping & Loading
- Scraped Telegram messages and images
- Saved in organized folder hierarchy under `data/raw/telegram_messages/YYYY-MM-DD/`
- Incremental scraping enabled using `last_scraped.json`
- Loaded messages into PostgreSQL

### ✅ Task 2: Data Modeling with dbt
- Created dbt project `telegram_dbt`
- Defined:
  - `stg_telegram_messages` (staging)
  - `dim_channels`, `dim_dates` (dimensions)
  - `fct_messages` (fact table)
- Implemented star schema design
- Applied dbt tests (unique + not null)
- All models tested and passed successfully

---

## 📂 Project Structure

    telegram-medical-pipeline/
    │
    ├── data/
    │ └── raw/
    │ └── telegram_messages/
    │ └── YYYY-MM-DD/
    │ └── channel_name.json / image.jpg
    │
    ├── metadata/
    │ └── last_scraped.json
    │
    ├── src/
    │ └── load_to_postgres.py
    │ └── telegram_scraper.py
    │
    ├── telegram_dbt/
    │ ├── dbt_project.yml
    │ ├── models/
    │ │ ├── staging/
    │ │ │ └── stg_telegram_messages.sql
    │ │ ├── marts/
    │ │ │ ├── dim_channels.sql
    │ │ │ ├── dim_dates.sql
    │ │ │ └── fct_messages.sql
    │ └── ...
    │
    ├── .gitignore
    ├── requirements.txt
    └── README.md


---

## ⚙️ Setup Instructions

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/telegram-medical-pipeline.git
cd telegram-medical-pipeline

🐍 2. Create Virtual Environment & Install Dependencies

python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

🧾 3. Configure PostgreSQL

Ensure a local PostgreSQL instance is running:



Create the database manually or via psql.
🗂 4. Load Data into PostgreSQL

python src/load_to_postgres.py

🧱 5. Run DBT Models

cd telegram_dbt
dbt run
dbt test

🔮 Upcoming Features

    ✅ Task 3: Image classification with YOLOv8

    🔄 Incremental model updates with is_incremental()

    📊 FastAPI-based analytical dashboard

    🧪 Unit tests and CI/CD integration

    🐙 Deployment-ready Dockerized setup




📄 Documentation
This project includes rich model documentation via dbt.
To view the interactive docs:

    dbt docs generate
    dbt docs serve

You can also refer to the schema.yml files for model descriptions and column-level tests.
