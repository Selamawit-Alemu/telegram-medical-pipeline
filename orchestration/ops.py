# S:\AI MAstery\week-7\orchestration\ops.py

from dagster import op
import subprocess
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

@op
def scrape_telegram_data(context) -> None: # Added context for logging
    """
    Executes the Telegram scraper script.
    Assumes src/scraper/main.py expects to be run from the project root.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # Corrected project_root
    scraper_script_path = os.path.join(project_root, "src", "scraper", "main.py")
    
    context.log.info(f"Calculated project_root: {project_root}") # Log for verification
    context.log.info(f"Launching scraper from: {scraper_script_path}")

    try:
        result = subprocess.run(
            [sys.executable, scraper_script_path], 
            check=True, 
            cwd=project_root, # Run from the *correct* project root
            capture_output=True,
            text=True
        )
        context.log.info("✅ Scraper executed successfully.")
        if result.stdout:
            context.log.info("Scraper stdout:\n" + result.stdout)
        if result.stderr:
            context.log.warning("Scraper stderr (if any):\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        context.log.error("❌ Scraper failed:")
        context.log.error(f"Command: {' '.join(e.cmd)}")
        context.log.error(f"Return Code: {e.returncode}")
        context.log.error("Scraper stdout:\n" + (e.stdout if e.stdout else "No stdout from scraper."))
        context.log.error("Scraper stderr:\n" + (e.stderr if e.stderr else "No stderr from scraper."))
        raise

@op
def load_raw_to_postgres(context) -> None:
    """
    Executes the data loading script for PostgreSQL.
    It loads .env variables and passes them to the subprocess.
    """
    python_executable = sys.executable
    # CORRECTED project_root calculation:
    # This will now be S:\AI MAstery\week-7\telegram-medical-pipeline
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Define the full path to the load_to_postgres.py script
    script_path = os.path.join(project_root, "src", "db", "load_to_postgres.py")

    # --- Load .env file explicitly in the Dagster op's environment ---
    # The .env file is now correctly located directly within this calculated project_root
    dotenv_path = os.path.join(project_root, '.env')
    
    context.log.info(f"Checking for .env file at: {dotenv_path}")
    if not os.path.exists(dotenv_path):
        context.log.error(f"❌ .env file not found at: {dotenv_path}. Please create it!")
        raise Exception(f".env file missing at {dotenv_path}")
    
    load_dotenv(dotenv_path=dotenv_path, override=True) 
    context.log.info(f"Loaded .env from: {dotenv_path}")


    # --- Prepare environment variables for the subprocess ---
    env_vars_for_subprocess = os.environ.copy()

    # Ensure RAW_DATA_DIR is passed as an absolute path to the subprocess.
    # It's relative to the project_root (S:\AI MAstery\week-7\telegram-medical-pipeline)
    if "RAW_DATA_DIR" in env_vars_for_subprocess:
        env_vars_for_subprocess["RAW_DATA_DIR"] = str(Path(project_root) / env_vars_for_subprocess["RAW_DATA_DIR"])
    else:
        env_vars_for_subprocess["RAW_DATA_DIR"] = str(Path(project_root) / "data" / "raw" / "telegram_messages")
        context.log.warning(f"RAW_DATA_DIR was not explicitly set in .env or parent env. Using default: {env_vars_for_subprocess['RAW_DATA_DIR']}")

    # Log the environment for debugging
    context.log.info(f"Subprocess will run with CWD: {project_root}")
    context.log.info(f"Subprocess will execute script: {script_path}")
    context.log.info(f"Environment variables being passed (keys only): {list(env_vars_for_subprocess.keys())}")
    context.log.info(f"Effective PGHOST: {env_vars_for_subprocess.get('PGHOST')}")
    context.log.info(f"Effective RAW_DATA_DIR: {env_vars_for_subprocess.get('RAW_DATA_DIR')}")

    try:
        context.log.info("Starting subprocess for load_to_postgres.py...")
        result = subprocess.run(
            [python_executable, script_path],
            check=True,          
            cwd=project_root,    # CWD for subprocess is now your actual project root
            capture_output=True, 
            text=True,           
            env=env_vars_for_subprocess 
        )
        context.log.info("✅ Subprocess 'load_to_postgres.py' executed successfully.")
        if result.stdout:
            context.log.info("Subprocess stdout:\n" + result.stdout)
        if result.stderr:
            context.log.warning("Subprocess stderr (if any):\n" + result.stderr)

    except subprocess.CalledProcessError as e:
        context.log.error("❌ Subprocess 'load_to_postgres.py' failed:")
        context.log.error(f"Command: {' '.join(e.cmd)}")
        context.log.error(f"Return Code: {e.returncode}")
        context.log.error("Subprocess stdout (on error):\n" + (e.stdout if e.stdout else "No stdout captured on error."))
        context.log.error("Subprocess stderr (on error):\n" + (e.stderr if e.stderr else "No stderr captured on error."))
        raise


@op
def run_dbt_transformations(context) -> None: # Added context for logging
    """
    Runs dbt transformations.
    Assumes the 'telegram_dbt' project is relative to the current working directory
    where Dagster is initiated.
    """
    # CORRECTED project_root calculation
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dbt_project_dir = os.path.join(project_root, "telegram_dbt") # Adjust if your dbt project is elsewhere

    context.log.info(f"Calculated project_root for dbt: {project_root}")
    context.log.info(f"Running dbt transformations in: {dbt_project_dir}")

    try:
        result = subprocess.run(
            ["dbt", "run", "--project-dir", dbt_project_dir], 
            check=True, 
            capture_output=True, 
            text=True
        )
        context.log.info("✅ DBT transformations completed successfully.")
        if result.stdout:
            context.log.info("DBT stdout:\n" + result.stdout)
        if result.stderr:
            context.log.warning("DBT stderr (if any):\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        context.log.error("❌ DBT transformations failed:")
        context.log.error(f"Command: {' '.join(e.cmd)}")
        context.log.error(f"Return Code: {e.returncode}")
        context.log.error("DBT stdout:\n" + (e.stdout if e.stdout else "No stdout from DBT."))
        context.log.error("DBT stderr:\n" + (e.stderr if e.stderr else "No stderr from DBT."))
        raise


@op
def run_yolo_enrichment(context) -> None: # Added context for logging
    """
    Executes the YOLOv8 enrichment script.
    Assumes src/yolov8_detector/main.py expects to be run from the project root.
    """
    # CORRECTED project_root calculation
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    yolo_script_path = os.path.join(project_root, "src", "yolov8_detector", "main.py")

    context.log.info(f"Calculated project_root for YOLO: {project_root}")
    context.log.info(f"Launching YOLO enrichment from: {yolo_script_path}")

    try:
        result = subprocess.run(
            [sys.executable, yolo_script_path], 
            check=True, 
            cwd=project_root, # Run from the *correct* project root
            capture_output=True,
            text=True
        )
        context.log.info("✅ YOLO enrichment completed successfully.")
        if result.stdout:
            context.log.info("YOLO stdout:\n" + result.stdout)
        if result.stderr:
            context.log.warning("YOLO stderr (if any):\n" + result.stderr)
    except subprocess.CalledProcessError as e:
        context.log.error("❌ YOLO enrichment failed:")
        context.log.error(f"Command: {' '.join(e.cmd)}")
        context.log.error(f"Return Code: {e.returncode}")
        context.log.error("YOLO stdout:\n" + (e.stdout if e.stdout else "No stdout from YOLO."))
        context.log.error("YOLO stderr:\n" + (e.stderr if e.stderr else "No stderr from YOLO."))
        raise