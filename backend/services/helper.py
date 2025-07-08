import re
from typing import Optional
import pycountry
from forex_python.converter import CurrencyCodes

def extract_price(price_str: str) -> Optional[float]:
    """
    Cleans a price string like '$1,299.99', '₹64,900', 'R$4,299.00 now'
    and returns a float value.
    """
    if not price_str:
        return None

    # Remove currency symbols and non-digit characters except . and ,
    cleaned = re.sub(r"[^\d.,]", "", price_str)

    # Handle prices like 4.299,00 (European) → convert to 4299.00
    if cleaned.count(",") > 0 and cleaned.count(".") > 0:
        if cleaned.find(".") < cleaned.find(","):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

    # If only commas exist, treat them as thousands separator or decimal
    elif "," in cleaned and "." not in cleaned:
        if len(cleaned.split(",")[-1]) == 2:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None

def get_currency_from_country(country_code: str) -> str:
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        if not country:
            return "USD"
        currency_code = CurrencyCodes().get_currency_code(country.name)
        return currency_code or "USD"
    except Exception:
        return "USD"
    
def safe_price(entry):
    try:
        return extract_price(entry.get("price", "0")) or float('inf')
    except:
        return float('inf')