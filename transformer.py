import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
load_dotenv()

# The client automatically looks for the GEMINI_API_KEY environment variable.
client = genai.Client()

def load_resume():
    path = os.getenv("RESUME_FILE_PATH")
    if not path:
        logging.error("RESUME_FILE_PATH not found in environment variables.")
        return ""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error loading resume: {e}")
        return ""

def tailor_resume(job_description, resume_text):
    if not resume_text:
        logging.warning("Resume text is empty. Skipping tailoring.")
        return ""

    # Define the schema to force the model to return data, not a conversation
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "resume_markdown": {"type": "STRING"}
        },
        "required": ["resume_markdown"]
    }

    # System instruction reinforces the 'No Backticks' rule
    config = types.GenerateContentConfig(
        system_instruction=(
            "You are a professional resume writer specializing in ATS optimization. "
            "Output the tailored resume as a raw Markdown string. "
            "DO NOT use markdown code blocks (```). DO NOT include any introductory or concluding remarks."
        ),
        temperature=0.3,
        response_mime_type="application/json",
        response_schema=response_schema
    )

    prompt = f"""
Tailor the following resume to match this job description. 
Focus on highlighting relevant skills and achievements while maintaining honesty.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}
"""

    try:
        # Using gemini-2.0-flash for optimal balance of speed and instruction following
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=config
        )

        if response.text:
            # Parse the structured JSON response
            response_data = json.loads(response.text)
            raw_content = response_data.get("resume_markdown", "")

            # Post-processing: Strip any rogue backticks or language identifiers
            # that might have slipped through the cracks
            clean_text = raw_content.replace("```markdown", "").replace("```", "").strip()
            
            return clean_text
        else:
            logging.warning("Model returned an empty response.")
            return ""

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
        return ""
    except Exception as e:
        logging.error(f"GenAI Client Error: {e}")
        return ""

# Example Usage:
# if __name__ == "__main__":
#     jd = "Looking for a Solutions Architect with Python and Cloud experience..."
#     current_resume = load_resume()
#     tailored_version = tailor_resume(jd, current_resume)
#     print(tailored_version)



# -----------------------------------
# OLD CODE - For reference only, not used in the current implementation

# import os
# import logging
# from dotenv import load_dotenv
# from google import genai  # New SDK import
# from google.genai import types

# # Configure logging to see errors in your console
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
# load_dotenv()

# # The client automatically looks for the GEMINI_API_KEY environment variable.
# # If your variable is named differently, use: client = genai.Client(api_key=os.getenv("YOUR_KEY"))
# client = genai.Client()

# def load_resume():
#     path = os.getenv("RESUME_FILE_PATH")
#     if not path:
#         logging.error("RESUME_FILE_PATH not found in environment variables.")
#         return ""
#     try:
#         with open(path, "r") as f:
#             return f.read()
#     except Exception as e:
#         logging.error(f"Error loading resume: {e}")
#         return ""

# def tailor_resume(job_description, resume_text):
#     if not resume_text:
#         logging.warning("Resume text is empty. Skipping tailoring.")
#         return ""

#     # Define a clear system instruction to guide the model's persona
#     config = types.GenerateContentConfig(
#         system_instruction="You are a professional resume writer specializing in ATS optimization. Keep formatting clean and professional.",
#         temperature=0.3, # Lower temperature for more consistent, professional results
#     )

#     prompt = f"""
# Tailor the following resume to match this job description. 
# Focus on highlighting relevant skills and achievements while maintaining honesty.

# JOB DESCRIPTION:
# {job_description}

# RESUME:
# {resume_text}

# Return only the updated resume in Markdown format.
# """

#     try:
#         # Using 'gemini-2.5-flash' for speed/cost or 'gemini-3.1-pro-preview' for high-reasoning
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt,
#             config=config
#         )

#         if response.text:
#             return response.text
#         else:
#             logging.warning("Model returned an empty response.")
#             return ""

#     except Exception as e:
#         logging.error(f"GenAI Client Error: {e}")
#         return ""

