import os
import json
from apify_client import ApifyClient
from dotenv import load_dotenv
import logging

load_dotenv()

def fetch_jobs():
    try:
        client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

        with open("Input/scraper_run_input.json", "r") as f:
            run_input = json.load(f)

        run = client.actor("MXLpngmVpE8WTESQr").call(run_input=run_input)

        dataset_id = run["defaultDatasetId"]

        jobs = []
        for item in client.dataset(dataset_id).iterate_items():
            jobs.append(item)

        return jobs

    except Exception as e:
        logging.error(f"Error fetching jobs: {e}")
        return []