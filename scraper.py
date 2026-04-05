import os
from apify_client import ApifyClient
from dotenv import load_dotenv
import logging

load_dotenv()

def fetch_jobs():
    try:
        client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

        run_input = {
            "country": "ca",
            "enableUniqueJobs": True,
            "fromDays": "3",
            "includeSimilarJobs": True,
            # "jobType": "freelance",
            "location": "Canada",
            "maxRows": 15,
            "query": "(Python OR Javascript)  -jobbank -cybersecurity -French -\"Développeur\" -\"Spécialiste\" -\"ingénierie\" -\"Professionnel\" -\"Analyste\" -\"Architecte\" -\"Administrateur\" -\"Support\" -\"Technicien\" -\"Testeur\" -\"QA\" -\"Assurance Qualité\" -\"développement\" -\"Programmeur\" -\"Spécialiste\"",
            "radius": "100",
            "sort": "date"
        }

        run = client.actor("MXLpngmVpE8WTESQr").call(run_input=run_input)

        dataset_id = run["defaultDatasetId"]

        jobs = []
        for item in client.dataset(dataset_id).iterate_items():
            jobs.append(item)

        return jobs

    except Exception as e:
        logging.error(f"Error fetching jobs: {e}")
        return []