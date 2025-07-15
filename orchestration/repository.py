# orchestration/repository.py

from dagster import Definitions

# Import both the job and the schedule that you defined in pipeline_job.py
from orchestration.pipeline_job import telegram_pipeline_job, daily_telegram_schedule

# Use the Definitions object to group your jobs and schedules
defs = Definitions(
    jobs=[telegram_pipeline_job],      # List all your jobs here
    schedules=[daily_telegram_schedule], # List all your schedules here
)