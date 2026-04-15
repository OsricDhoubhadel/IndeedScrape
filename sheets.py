import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
from dotenv import load_dotenv
from storage import FIELD_ORDER

load_dotenv()

def upload_to_sheets():
    try:
        # Setup Credentials
        creds = Credentials.from_service_account_file(
            os.getenv("GOOGLE_CREDENTIALS_JSON"),
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )

        client = gspread.authorize(creds)
        sheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID")).sheet1

        # Load CSV
        csv_path = os.getenv("CSV_FILE_PATH")
        df = pd.read_csv(csv_path, dtype=str)

        # Replace NaN/Null with empty strings and keep canonical field order.
        df = df.fillna("")
        for field in FIELD_ORDER:
            if field not in df.columns:
                df[field] = ""

        ordered_columns = FIELD_ORDER + [c for c in df.columns if c not in FIELD_ORDER]
        df = df.loc[:, ordered_columns]

        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()

        # Update Sheet
        sheet.clear()
        sheet.update(data_to_upload)

        logging.info("Successfully uploaded data to Google Sheets.")

    except Exception as e:
        logging.error(f"Google Sheets error: {e}")

