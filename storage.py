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

        df.to_csv(
            CSV_FILE,
            mode='a' if file_exists else 'w',
            header=not file_exists,
            index=False
        )

    except Exception as e:
        logging.error(f"CSV write error: {e}")