import os
import json
import pandas as pd
import logging
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE_PATH")

FIELD_ORDER = [
    "jobKey",
    "expired",
    "age",
    "datePublished",
    "title",
    "jobUrl",
    "applyUrl",
    "jobType",
    "descriptionText",
    "companyName",
    "companyUrl",
    "location",
    "salary",
    "benefits",
    "occupation",
    "attributes",
    "tailored_resume",
    "model_used",
    "hiringDemand",
    "isRemote",
    "locale",
    "postedToday",
    "language",
    "source",
    "rating",
    "emails",
    "companyAddresses",
    "companyLinks",
    "companyCeo",
    "requirements",
    "companyLogoUrl",
    "companyHeaderUrl",
    "companyNumEmployees",
    "companyRevenue",
    "companyDescription",
    "companyFounded",
    "companyBriefDescription",
    "numOfCandidates",
    "companyIndustry",
    "scrapingInfo",
    "descriptionHtml",
    "contacts",
    "shifts",
    "socialInsurance",
    "workingSystem",
    "shiftAndSchedule",
]

KEY_ALIASES = {
    "occupa  tion": "occupation",
}


def serialize_value(value):
    if value is None:
        return ""
    if isinstance(value, (str, bool, int, float)):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


def normalize_job_record(job):
    normalized = {}
    for key, value in job.items():
        normalized_key = KEY_ALIASES.get(key, key)
        normalized[normalized_key] = serialize_value(value)
    return normalized


def get_output_columns(normalized_jobs):
    extra_columns = []
    for record in normalized_jobs:
        for column in record.keys():
            if column not in FIELD_ORDER and column not in extra_columns:
                extra_columns.append(column)
    return FIELD_ORDER + extra_columns


def save_jobs_to_csv(jobs):
    if not jobs:
        logging.warning("No jobs provided to save_jobs_to_csv.")
        return

    if not CSV_FILE:
        logging.error("CSV_FILE_PATH environment variable is not set.")
        return

    try:
        normalized_jobs = [normalize_job_record(job) for job in jobs]
        columns = get_output_columns(normalized_jobs)
        new_df = pd.DataFrame(normalized_jobs, columns=columns)

        if os.path.isfile(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
            # Read existing data
            existing_df = pd.read_csv(CSV_FILE, dtype=str)
            # Ensure all columns are present
            for col in columns:
                if col not in existing_df.columns:
                    existing_df[col] = ""
            for col in existing_df.columns:
                if col not in columns:
                    columns.append(col)
            # Reorder to canonical
            existing_df = existing_df.reindex(columns=columns)
            # Append new data
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        combined_df.to_csv(
            CSV_FILE,
            mode='w',
            header=True,
            index=False,
            encoding='utf-8'
        )

    except Exception as e:
        logging.error(f"CSV write error: {e}")