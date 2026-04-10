import os
import pandas as pd
import logging
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE_PATH")

def save_jobs_to_csv(jobs):
    try:
        df = pd.DataFrame(jobs)

        file_exists = os.path.isfile(CSV_FILE)
        file_is_empty = file_exists and os.path.getsize(CSV_FILE) == 0

        df.to_csv(
            CSV_FILE,
            mode='a' if file_exists and not file_is_empty else 'w',
            header=not file_exists or file_is_empty,
            index=False
        )

    except Exception as e:
        logging.error(f"CSV write error: {e}")