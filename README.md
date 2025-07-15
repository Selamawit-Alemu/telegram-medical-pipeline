1. Overview

This project develops a robust, end-to-end data platform designed to generate actionable insights into Ethiopian medical businesses. It leverages data scraped from public Telegram channels, employing a modern ELT (Extract, Load, Transform) framework. The platform ensures data reliability, scalability, and readiness for advanced analytics by integrating data scraping, dimensional modeling with dbt, data enrichment using YOLOv8 for object detection on images, and orchestration with Dagster. The final cleaned data is exposed via a FastAPI analytical API.
2. Business Need

As Data Engineers at Kara Solutions, our primary goal is to empower data analysis for Ethiopian medical businesses. This data platform is specifically designed to answer critical business questions, such as:

    What are the top 10 most frequently mentioned medical products or drugs across all channels?

    How does the price or availability of a specific product vary across different channels?

    Which channels have the most visual content (e.g., images of pills vs. creams)?

    What are the daily and weekly trends in posting volume for health-related topics?

3. Architecture

The data platform follows a layered ELT architecture:

    Extraction: Data is scraped from public Telegram channels.

    Data Lake (Raw Layer): Raw, unaltered scraped data (JSON files) is stored in a partitioned directory structure.

    Loading: Raw JSON data is loaded into a PostgreSQL database, serving as the data warehouse.

    Transformation (Staging & Data Marts): dbt is used to clean, validate, and remodel the data into a dimensional star schema (fact and dimension tables) within PostgreSQL.

    Enrichment: Images from Telegram messages are processed using YOLOv8 for object detection, and the results are integrated into the data warehouse.

    Orchestration: Dagster manages and orchestrates the entire data pipeline, ensuring reproducibility, observability, and scheduling.

    Analytical API: FastAPI provides endpoints to query the transformed data for business insights.

    Containerization: Docker and Docker Compose are used to containerize the entire application stack, ensuring a reproducible and portable environment.

4. Features & Tasks Implemented

This project addresses the following key tasks:

    Task 0: Project Setup & Environment Management

        Initialized a Git repository.

        Created requirements.txt for dependency management.

        Developed Dockerfile and docker-compose.yml for containerization.

        Implemented .env for secure credential management, loaded via python-dotenv.

        .env is correctly added to .gitignore.

    Task 1: Data Scraping and Collection (Extract & Load)

        Developed a Python script (src/scraper/main.py) to extract data from specified Telegram channels.

        Collects both text messages and images.

        Stores raw data as JSON files in data/raw/telegram_messages/YYYY-MM-DD/channel_name.json.

    Task 2: Data Modeling and Transformation (Transform)

        Script (src/db/load_to_postgres.py) to load raw JSON into a PostgreSQL raw schema.

        dbt project (telegram_dbt) initialized and connected to PostgreSQL.

        Designed and implemented a star schema with dim_channels, dim_dates, and fct_messages models.

        Includes dbt schema tests (e.g., not_null, unique) for data validation.

    Task 3: Data Enrichment with Object Detection (YOLO)

        Script (src/yolov8_detector/main.py) to scan for new images and perform object detection using YOLOv8.

        Results are integrated into the data warehouse (e.g., into an fct_image_detections table via dbt).

    Task 4: Build an Analytical API (FastAPI)

        (To be implemented: A FastAPI application (src/api/) with analytical endpoints to query the dbt marts.)

        Endpoints like /api/reports/top-products, /api/channels/{channel_name}/activity, /api/search/messages.

        Uses Pydantic for data validation.

    Task 5: Pipeline Orchestration (Dagster)

        Dagster job (telegram_pipeline_job) defined in orchestration/pipeline_job.py with ops for scrape_telegram_data, load_raw_to_postgres, run_dbt_transformations, and run_yolo_enrichment.

        Configured orchestration/repository.py as the Dagster entry point.

        Implemented a daily schedule (daily_telegram_pipeline_schedule) for the job using Dagster's scheduling features.

5. Project Structure

    telegram-medical-pipeline/
    ├── .github/
    │   └── workflows/
    │       └── ci.yml             # GitHub Actions CI workflow
    ├── data/
    │   └── raw/
    │       └── telegram_messages/ # Raw scraped JSON data lake (YYYY-MM-DD/channel_name.json)
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
    ├── telegram_dbt/              # dbt project
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
    │   └── profiles.yml           # dbt profiles for different environments (dev, ci)
    ├── .env                       # Environment variables (local, NOT committed to Git)
    ├── .env.example               # Example .env file
    ├── .gitignore                 # Specifies files/folders to ignore in Git
    ├── app.log                    # Application logs
    ├── docker-compose.yml         # Docker Compose configuration for local development
    ├── Dockerfile                 # Dockerfile for building the application image
    ├── README.md                  # This README file
    └── requirements.txt           # Python dependencies

6. Setup and Installation
Prerequisites

    Git: For version control.

    Python 3.12: Installed on your system.

    pip: Python package installer.

    Docker Desktop: (or Docker Engine for Linux) Installed and running for containerization. Ensure it's stable and authenticated with Docker Hub.

Cloning the Repository

git clone https://github.com/your-username/telegram-medical-pipeline.git
cd telegram-medical-pipeline

Local Environment Setup (without Docker Compose)

This setup is for running Dagster and your Python scripts directly on your host machine.

    Create a Python Virtual Environment:

    python -m venv venv

    Activate the Virtual Environment:

        Windows: .\venv\Scripts\activate

        macOS/Linux: source venv/bin/activate

    Install Python Dependencies:

    pip install -r requirements.txt
    pip install pytz # For timezone support in Dagster schedules

    Create .env file:

        Copy .env.example to .env in the project root.

        Fill in your actual credentials and configurations.

        Example .env content:

        TELEGRAM_API_ID=YOUR_TELEGRAM_API_ID
        TELEGRAM_API_HASH=YOUR_TELEGRAM_API_HASH
        CHANNELS=channel_name1,channel_name2 # Comma-separated list of channel usernames or IDs
        PGUSER=selam
        PGPASSWORD=mypwd
        PGDATABASE=telegram_medical
        POSTGRES_HOST=localhost # Or your PostgreSQL host if not local
        PGPORT=5432
        PHONE=+1234567890 # Your Telegram phone number for authentication
        PGHOST=localhost # For local direct connection
        RAW_DATA_DIR=data/raw/telegram_messages

    Set up PostgreSQL Database:

        Ensure a PostgreSQL 15 database named telegram_medical exists and is accessible with the selam user and mypwd password.

        If running locally, you can use psql to create the database and user.

Dockerized Environment Setup (Recommended)

This uses Docker Compose to run all services (PostgreSQL, Dagster code, Dagit UI) in containers, ensuring a consistent environment.

    Ensure Docker Desktop is running and stable.

        Verify it shows "Engine running" in the UI.

        If you faced proxy issues, ensure your Docker Desktop proxy settings are correct:

            HTTP/HTTPS Proxy: http://http.docker.internal:3128 (or your actual proxy)

            Bypass: localhost,127.0.0.1,registry-1.docker.io,auth.docker.io

        Ensure you are logged into Docker Hub via Docker Desktop.

    Open your terminal (outside of venv).

    Navigate to your project root:

    cd S:\AI MAstery\week-7\telegram-medical-pipeline

    Clean up any old Docker state (optional, but recommended if you had issues):

    docker system prune --all --volumes --force

    Build and Start Services:

    docker-compose up --build

    This will:

        Build the app image (containing your Python code).

        Pull postgres:15 and dagster/dagit images.

        Start the PostgreSQL database container (db).

        Start the Dagster code server container (dagster_code).

        Start the Dagit UI container (dagit).

7. Running the Pipeline
Running Locally (without Docker Compose)

    Activate your virtual environment.

    Start Dagit:

    dagster dev -f orchestration/repository.py

    Open your browser to http://localhost:3000.

    Navigate to the "Overview" or "Jobs" tab, select telegram_pipeline_job, and click "Launch Run".

Running with Docker Compose

    Ensure Docker Compose services are running:

    docker-compose up

    (If they are already running, you don't need --build unless you made changes to Dockerfile or requirements.txt).

    Open your browser to http://localhost:3000.

    Navigate to the "Overview" or "Jobs" tab, select telegram_pipeline_job, and click "Launch Run".

8. Scheduling the Pipeline

The telegram_pipeline_job is configured with a daily schedule.

    Ensure Dagit is running (either locally or via Docker Compose).

    Open your browser to http://localhost:3000.

    Navigate to the "Automation" tab (or "Schedules" in older Dagster versions).

    Locate daily_telegram_pipeline_schedule.

    Toggle the switch to "On" to enable the schedule.

        The schedule is set to run daily at 1:00 AM EAT.

9. Analytical API Usage

(This section assumes Task 4 is implemented in src/api/ and the app service in docker-compose.yml is configured to run it, or you run it separately.)

To run the FastAPI application:

    If running with Docker Compose (as app service): The API should be accessible at http://localhost:8000.

    If running locally (outside Docker Compose):

        Activate your virtual environment.

        Navigate to the src/api directory.

        Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
        (You might need to adjust main:app based on your FastAPI entry point).

Example Endpoints (as per Task 4 requirements):

    Top Products: GET /api/reports/top-products?limit=10

    Channel Activity: GET /api/channels/{channel_name}/activity

    Search Messages: GET /api/search/messages?query=paracetamol

Refer to the src/api/ directory for exact endpoint definitions and usage.
10. Continuous Integration (CI)

This project uses GitHub Actions for Continuous Integration. The workflow is defined in .github/workflows/ci.yml.

    Triggers: Runs on push to main or develop branches, and on pull_request to the same branches.

    Steps:

        Checks out code.

        Sets up Python environment and installs dependencies.

        Creates a .env file from GitHub Repository Secrets (for sensitive credentials).

        Sets up a PostgreSQL service container for testing.

        Runs dbt tests and builds models.

        (Placeholders for Python unit tests and FastAPI tests).

GitHub Secrets Configuration:
You must configure the following as GitHub Repository Secrets (Settings -> Secrets and variables -> Actions -> New repository secret):

    TELEGRAM_API_ID

    TELEGRAM_API_HASH

    CHANNELS

    PGUSER

    PGPASSWORD

    PGDATABASE

    PGPORT

    PHONE

11. Testing

    dbt Tests: Schema tests (not_null, unique) are defined in dbt model YAML files. Custom data tests can be added.

    Python Unit Tests: (To be implemented using pytest for src/scraper, src/db, src/yolov8_detector components).

    API Tests: (To be implemented for src/api/ endpoints).

