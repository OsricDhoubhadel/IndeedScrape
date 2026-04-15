import os
import json
import logging
import time
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")


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


def load_resume_header():
    path = os.getenv("RESUME_HEADER_FILE_PATH")
    if not path:
        logging.error("RESUME_HEADER_FILE_PATH not found in environment variables.")
        return ""
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error loading resume header: {e}")
        return ""


async def tailor_resume(job_description, resume_text):
    if not resume_text:
        logging.warning("Resume text is empty. Skipping tailoring.")
        return {"tailored_resume": "", "model_used": ""}

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logging.error("OPENROUTER_API_KEY not found in environment variables.")
        return {"tailored_resume": "", "model_used": ""}

    with open("Input/resume_tailoring_prompt.txt", "r") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(job_description=job_description, resume_text=resume_text)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    max_retries = 10
    retry_delay = 20
    model_used = ""

    async with aiohttp.ClientSession() as session:
        for attempt in range(max_retries):
            try:
                async with session.post(
                    OPENROUTER_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60),
                ) as response:
                    if response.status == 429:
                        raise aiohttp.ClientError("429 Rate limit")

                    response.raise_for_status()
                    data = await response.json()

                    model_used = data.get("model", "")
                    if model_used:
                        logging.info(f"OpenRouter model used: {model_used}")

                    choices = data.get("choices", [])
                    if not choices:
                        logging.warning("OpenRouter returned no choices.")
                        return {"tailored_resume": "", "model_used": model_used}

                    message = choices[0].get("message", {})
                    raw_content = message.get("content", "")
                    if not raw_content:
                        logging.warning("OpenRouter returned an empty message.")
                        return {"tailored_resume": "", "model_used": model_used}

                    tailored_resume = raw_content.replace("```markdown", "").replace("```", "").strip()
                    return {"tailored_resume": tailored_resume, "model_used": model_used}

            except aiohttp.ClientError as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    logging.warning(f"Rate limit hit. Retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                logging.error(f"OpenRouter error: {e}")
                return {"tailored_resume": "", "model_used": model_used}
            except asyncio.TimeoutError as e:
                if attempt < max_retries - 1:
                    logging.warning(f"OpenRouter request timeout. Retrying in {retry_delay}s (Attempt {attempt + 1}/{max_retries})...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                logging.error(f"OpenRouter request timeout: {e}")
                return {"tailored_resume": "", "model_used": model_used}
            except ValueError as e:
                logging.error(f"Failed to parse OpenRouter response: {e}")
                return {"tailored_resume": "", "model_used": model_used}

    logging.error("Max retries exceeded for OpenRouter. Skipping this job.")
    return {"tailored_resume": "", "model_used": model_used}

