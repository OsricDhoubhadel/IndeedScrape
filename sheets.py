import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging
from dotenv import load_dotenv

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
        df = pd.read_csv(csv_path)

        # IMPORTANT: Replace NaN/Null with empty strings to avoid JSON errors
        # This fixes the "Out of range float values" issue
        df = df.fillna("")

        # Convert DataFrame to a list of lists for gspread
        data_to_upload = [df.columns.values.tolist()] + df.values.tolist()

        # Update Sheet
        sheet.clear()
        sheet.update(data_to_upload)
        
        logging.info("Successfully uploaded data to Google Sheets.")

    except Exception as e:
        logging.error(f"Google Sheets error: {e}")

