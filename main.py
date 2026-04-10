import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

import time
from pathlib import Path
from scraper import fetch_jobs
from transformer import load_resume, tailor_resume
from storage import save_jobs_to_csv
from sheets import upload_to_sheets

def run_pipeline():
    logging.info("Pipeline started")

    jobs = fetch_jobs()
    if not jobs:
        logging.warning("No jobs fetched")
        return
    logging.info(f"Fetched {len(jobs)} jobs")
    logging.info(f"Starting resume tailoring")
    resume_header = Path("resume-header.md").read_text(encoding="utf-8")
    resume_text = load_resume()
    enriched_jobs = []
    logging.info(f"Starting to tailor resumes for each job")

    for job in jobs:
        description = job.get("descriptionText", "")
        print(f"Tailoring resume for job: {job.get('title', 'N/A')}")
        tailored_resume = tailor_resume(description, resume_text)
        tailored_resume = f"{resume_header}\n\n{tailored_resume}"

        job["tailored_resume"] = tailored_resume

        enriched_jobs.append(job)

        time.sleep(5)  # To avoid hitting API rate limits

    logging.info(f"Finished tailoring resumes. Now saving to CSV and uploading to Google Sheets.")
    save_jobs_to_csv(enriched_jobs)
    upload_to_sheets()

    logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()