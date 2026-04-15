import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

import asyncio
from pathlib import Path
from scraper import fetch_jobs
from transformer import load_resume, tailor_resume
from storage import save_jobs_to_csv
from sheets import upload_to_sheets

async def tailor_job_resume(job, resume_header, resume_text):
    """Tailor resume for a single job."""
    description = job.get("descriptionText", "")
    print(f"Tailoring resume for job: {job.get('title', 'N/A')}")
    result = await tailor_resume(description, resume_text)
    tailored_resume = f"{resume_header}\n\n{result['tailored_resume']}"
    job["tailored_resume"] = tailored_resume
    job["model_used"] = result["model_used"]
    return job

async def run_pipeline():
    logging.info("Pipeline started")

    jobs = fetch_jobs()
    if not jobs:
        logging.warning("No jobs fetched")
        return
    logging.info(f"Fetched {len(jobs)} jobs")
    logging.info(f"Starting resume tailoring")
    resume_header = Path("resume-header.md").read_text(encoding="utf-8")
    resume_text = load_resume()
    logging.info(f"Starting to tailor resumes for each job")

    # Process all jobs concurrently
    tasks = [tailor_job_resume(job, resume_header, resume_text) for job in jobs]
    enriched_jobs = await asyncio.gather(*tasks)

    logging.info(f"Finished tailoring resumes. Now saving to CSV and uploading to Google Sheets.")
    save_jobs_to_csv(enriched_jobs)
    upload_to_sheets()

    logging.info("Pipeline completed successfully")

if __name__ == "__main__":
    asyncio.run(run_pipeline())