# \orchestration\pipeline_job.py


from dagster import job, ScheduleDefinition

# Import all your ops
from .ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment
)

@job
def telegram_pipeline_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

daily_telegram_schedule = ScheduleDefinition(
    job=telegram_pipeline_job,
    cron_schedule="0 1 * * *", # This will be interpreted as 1:00 AM UTC
    name="daily_telegram_pipeline_schedule",
    description="Schedules the Telegram data pipeline to run daily at 1:00 AM UTC (4:00 AM EAT)."
    # REMOVED: timezone="Africa/Addis_Ababa"
)