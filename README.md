
# Telegram Medical Data Pipeline

## Overview

This project develops a robust, end-to-end data platform designed to generate actionable insights into Ethiopian medical businesses. It leverages data scraped from public Telegram channels, employing a modern ELT (Extract, Load, Transform) framework. The platform ensures data reliability, scalability, and readiness for advanced analytics by integrating data scraping, dimensional modeling with dbt, data enrichment using YOLOv8 for object detection on images, and orchestration with Dagster. The final cleaned data is exposed via a FastAPI analytical API.

## Business Need

As Data Engineers at Kara Solutions, our primary goal is to empower data analysis for Ethiopian medical businesses. This data platform is designed to answer critical business questions, including:

- What are the top 10 most frequently mentioned medical products or drugs across all channels?
- How does the price or availability of a specific product vary across different channels?
- Which channels have the most visual content (e.g., images of pills vs. creams)?
- What are the daily and weekly trends in posting volume for health-related topics?

## Architecture

The data platform follows a layered ELT architecture:

1. **Extraction:** Data is scraped from public Telegram channels.
2. **Data Lake (Raw Layer):** Raw, unaltered scraped data (JSON files) is stored in a partitioned directory structure.
3. **Loading:** Raw JSON data is loaded into a PostgreSQL database, serving as the data warehouse.
4. **Transformation (Staging & Data Marts):** dbt is used to clean, validate, and remodel the data into a dimensional star schema (fact and dimension tables) within PostgreSQL.
5. **Enrichment:** Images from Telegram messages are processed using YOLOv8 for object detection; results are integrated into the data warehouse.
6. **Orchestration:** Dagster manages and orchestrates the entire data pipeline, ensuring reproducibility, observability, and scheduling.
7. **Analytical API:** FastAPI provides endpoints to query the transformed data for business insights.
8. **Containerization:** Docker and Docker Compose containerize the entire application stack, ensuring a reproducible and portable environment.

## Features & Tasks Implemented

### Task 0: Project Setup & Environment Management

- Initialized Git repository.
- Created `requirements.txt` for dependency management.
- Developed `Dockerfile` and `docker-compose.yml` for containerization.
- Implemented `.env` for secure credential management, loaded via `python-dotenv`.
- Ensured `.env` is added to `.gitignore`.

### Task 1: Data Scraping and Collection (Extract & Load)

- Developed Python script (`src/scraper/main.py`) to extract data from specified Telegram channels.
- Collects both text messages and images.
- Stores raw data as JSON files in `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`.

### Task 2: Data Modeling and Transformation (Transform)

- Script (`src/db/load_to_postgres.py`) to load raw JSON into a PostgreSQL raw schema.
- Initialized dbt project (`telegram_dbt`) connected to PostgreSQL.
- Designed and implemented a star schema with `dim_channels`, `dim_dates`, and `fct_messages` models.
- Included dbt schema tests (e.g., `not_null`, `unique`) for data validation.

### Task 3: Data Enrichment with Object Detection (YOLO)

- Script (`src/yolov8_detector/main.py`) to scan new images and perform object detection using YOLOv8.
- Integrated detection results into the data warehouse (e.g., into an `fct_image_detections` table via dbt).

### Task 4: Build an Analytical API (FastAPI)

- (To be implemented) FastAPI application (`src/api/`) with analytical endpoints to query dbt marts.
- Planned endpoints include:
  - `/api/reports/top-products`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages`
- Uses Pydantic for data validation.

### Task 5: Pipeline Orchestration (Dagster)

- Defined Dagster job (`telegram_pipeline_job`) in `orchestration/pipeline_job.py` with ops for scraping, loading, transforming, and enriching data.
- Configured `orchestration/repository.py` as Dagster repository entry point.
- Implemented a daily schedule (`daily_telegram_pipeline_schedule`) for automated pipeline execution.

## Project Structure

```bash
telegram-medical-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI workflow
├── data/
│   └── raw/
│       └── telegram_messages/  # Raw scraped JSON data lake (YYYY-MM-DD/channel_name.json)
        └── images/
├── orchestration/
│   ├── __init__.py
│   ├── ops.py                 # Dagster ops definitions
│   ├── pipeline_job.py        # Dagster job and schedule definitions
│   └── repository.py          # Dagster repository definition
├── src/
│   ├── api/                   # FastAPI application (Task 4)
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   ├── db/
│   │   └── load_to_postgres.py # Script to load raw data to PostgreSQL
│   ├── scraper/
│   │   └── main.py             # Telegram scraping script
│   └── yolov8_detector/
│       └── main.py             # YOLOv8 object detection script
├── telegram_dbt/              # dbt project directory
│   ├── analyses/
│   ├── dbt_packages/
│   ├── logs/
│   ├── macros/
│   ├── models/                # dbt models (staging, marts)
│   ├── seeds/
│   ├── snapshots/
│   ├── target/
│   ├── tests/
│   ├── .gitignore
│   ├── dbt_project.yml
│   └── profiles.yml           # dbt profiles for environments (dev, ci)
├── .env                       # Environment variables (local, NOT committed to Git)
├── .env.example               # Example .env file
├── .gitignore                 # Git ignore rules
├── app.log                    # Application logs
├── docker-compose.yml         # Docker Compose config for local dev
├── Dockerfile                 # Dockerfile for building app image
├── README.md                  # This README file
└── requirements.txt           # Python dependencies
````

## Setup and Installation

### Prerequisites

* Git
* Python 3.12
* pip
* Docker Desktop (or Docker Engine for Linux), running and logged into Docker Hub

### Clone the Repository

```bash
git clone https://github.com/your-username/telegram-medical-pipeline.git
cd telegram-medical-pipeline
```

### Local Environment Setup (without Docker Compose)

```bash
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
pip install pytz  # For timezone support in Dagster schedules
```

### Configure Environment Variables

* Copy `.env.example` to `.env` in project root.
* Fill in your actual credentials and configuration, for example:

```env
TELEGRAM_API_ID=YOUR_TELEGRAM_API_ID
TELEGRAM_API_HASH=YOUR_TELEGRAM_API_HASH
CHANNELS=channel_name1,channel_name2
PGUSER=selam
PGPASSWORD=mypwd
PGDATABASE=telegram_medical
POSTGRES_HOST=localhost
PGPORT=5432
PHONE=+1234567890
RAW_DATA_DIR=data/raw/telegram_messages
```

### PostgreSQL Setup

* Ensure PostgreSQL 15 is installed and running.
* Create database and user according to `.env` credentials.

### Dockerized Environment Setup (Recommended)

* Ensure Docker Desktop is running and stable.
* Verify Docker Hub login.
* From project root, optionally clean Docker state:

```bash
docker system prune --all --volumes --force
```

* Build and start containers:

```bash
docker-compose up --build
```

This will start services for PostgreSQL, Dagster, and your application code.

## Running the Pipeline

### Locally (without Docker Compose)

* Activate virtual environment
* Start Dagit UI:

```bash
dagster dev -f orchestration/repository.py
```

* Open [http://localhost:3000](http://localhost:3000), select `telegram_pipeline_job`, and launch a run.

### Using Docker Compose

* Run:

```bash
docker-compose up
```

* Open [http://localhost:3000](http://localhost:3000), select the job, and launch.

## Scheduling

* In Dagit UI, go to "Automation" or "Schedules".
* Enable `daily_telegram_pipeline_schedule`.
* Pipeline runs daily at 1:00 AM EAT.

## Analytical API Usage (Task 4)

* When implemented, FastAPI will be accessible at `http://localhost:8000`.

* Example endpoints:

  * `GET /api/reports/top-products?limit=10`
  * `GET /api/channels/{channel_name}/activity`
  * `GET /api/search/messages?query=paracetamol`

* To run locally:

```bash
cd src/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Continuous Integration (CI)

* GitHub Actions workflow located in `.github/workflows/ci.yml`.
* Runs on pushes and pull requests to `main` and `develop` branches.
* Performs environment setup, runs dbt tests, and prepares for Python & API testing.

### GitHub Secrets Required

* `TELEGRAM_API_ID`
* `TELEGRAM_API_HASH`
* `CHANNELS`
* `PGUSER`
* `PGPASSWORD`
* `PGDATABASE`
* `PGPORT`
* `PHONE`

## Testing

* **dbt Tests:** schema validation (not\_null, unique).
* **Python Unit Tests:** to be implemented with `pytest`.
* **API Tests:** to be implemented for FastAPI endpoints.

---

Thank you for exploring this project! Contributions and feedback are welcome.


