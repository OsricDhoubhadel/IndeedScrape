# Apify Indeed Scraper

A Python-based tool that scrapes job listings from Indeed using Apify, tailors resumes for each job using AI, and uploads the results to Google Sheets.

## Features

- **Job Scraping**: Uses Apify's Indeed scraper to fetch job listings
- **Resume Tailoring**: Automatically tailors your resume for each job using AI (OpenAI/Gemini)
- **Data Storage**: Saves results to CSV and uploads to Google Sheets
- **Asynchronous Processing**: Concurrently processes multiple jobs for efficiency

## Prerequisites

- Python 3.8+
- Apify account and API token
- Google Cloud service account credentials
- OpenAI API key (or Gemini API key)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OsricDhoubhadel/IndeedScrape.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
    APIFY_API_TOKEN=your_apify_api_token
    OPENROUTER_API_KEY=your_openrouter_api_key
    GOOGLE_SHEET_ID=your_google_sheet_id

    # INPUT
    GOOGLE_CREDENTIALS_JSON='./Input/credentials.json'
    RESUME_FILE_PATH='./Input/resume.md'
    RESUME_HEADER_FILE_PATH='./Input/resume-header.md'

    # OUTPUT
    CSV_FILE_PATH='./Output/jobs.csv'
    LOG_FILE_PATH='./Output/app.log'
   ```

4. Configure credentials:
   - Place your Google service account credentials JSON in `Input/credentials.json`
   - Update `Input/scraper_run_input.json` with your Indeed search parameters

5. Prepare resume files:
   - `Input/resume-header.md`: Your resume header/contact info
   - `Input/resume.md`: Your resume content
   - `Input/resume_tailoring_prompt.txt`: Instructions for AI tailoring

## Usage

Run the main pipeline:
```bash
python main.py
```

This will:
1. Fetch jobs from Indeed using Apify
2. Tailor your resume for each job
3. Save results to `Output/jobs.csv`
4. Upload to Google Sheets

## Configuration

### Indeed Search Parameters
Edit `Input/scraper_run_input.json` to customize your job search:
```json
{
  "searchTerms": "python developer",
  "location": "remote",
  "maxItems": 10
}
```

### Google Sheets
The script will create/update a sheet named "Job Applications" in your Google account.

## File Structure

```
├── main.py                 # Main pipeline script
├── scraper.py             # Apify job fetching
├── transformer.py         # Resume tailoring logic
├── storage.py             # CSV saving
├── sheets.py              # Google Sheets upload
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── Input/
│   ├── credentials.json           # Google service account (dummy)
│   ├── resume.md                  # Resume content (dummy)
│   ├── resume-header.md           # Resume header (dummy)
│   ├── resume_tailoring_prompt.txt # AI instructions
│   └── scraper_run_input.json     # Indeed search config
└── Output/
    ├── jobs.csv           # Processed job data
    └── app.log            # Application logs
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Disclaimer

This tool is for personal use only. Respect Indeed's terms of service and job application etiquette. Do not spam applications.