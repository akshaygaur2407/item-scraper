# backend/app/config.py

import os
from dotenv import load_dotenv
import pycountry
# Load .env file at project root
load_dotenv()

# Required API keys
SERPER_API_KEY      = os.getenv("SERPER_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
EXCHANGE_API_URL = os.getenv("EXCHANGE_API_URL", "https://api.exchangerate.host")
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "10.0"))
def get_serpapi_location(country_code: str) -> str:
    """
    Convert ISO alpha‑2 to full country name via pycountry.
    Falls back to the original code if not found.
    """
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        return country.name
    except (KeyError, AttributeError):
        return country_code
