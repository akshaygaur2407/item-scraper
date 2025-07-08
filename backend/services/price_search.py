import os, httpx, asyncio
from schemas.response import ProductEntry
from utils.http_client import async_client
from config import SERPER_API_KEY, EXCHANGE_API_URL, HTTP_TIMEOUT, get_serpapi_location
from typing import Optional, List
import together
import re
from services.helper import extract_price, get_currency_from_country, safe_price
from forex_python.converter import CurrencyRates

async def fetch_from_serper(country: str, query: str) -> list[dict]:
    location = get_serpapi_location(country)
    gl = country.lower()

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "gl": gl,
        "hl": "en",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://google.serper.dev/shopping",
            json=payload,
            headers=headers
        )

        response.raise_for_status()
        data = response.json()
        items = data.get("shopping", [])
        results = []
        for item in items:
            results.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "link": item.get("link"),
                "thumbnail": item.get("imageUrl"),
                "seller": item.get("source"),
            })

        return results


def match_and_build(entry: dict, raw_query: str) -> Optional[ProductEntry]:
    title = entry.get("title", "")
    price = extract_price(entry.get("price", "0")) or 0.0
    currency = entry.get("currency", "")
    link = entry.get("link", "")
    seller= entry.get("seller")
    thumbnail= entry.get("thumbnail")

    prompt = f"""
                You are an AI tool designed to compare product names and output a similarity score.
                You must return a single float between 0 and 1 ONLY — no explanation, no code.

                Product Name 1: {raw_query}
                Product Name 2: {title}

                Just return the score:
            """

    try:
        response = together.Complete.create(
            prompt=prompt,
            model="lgai/exaone-3-5-32b-instruct",
            max_tokens=10,
            temperature=0.0,
        )

        raw_output = response.get("choices", [])[0].get("text", "").strip()
        print(f"Raw Together Output: {raw_output}")

        match = re.search(r"\b([0-1](\.\d+)?)\b", raw_output)
        if not match:
            print("No valid score found in response.")
            return None

        score = float(match.group(1))
        if score < 0.9:
            return None

        return ProductEntry(
            link=link,
            price=price,
            currency=currency,
            productName=title,
            matchScore=score,
            seller= seller,
            thumbnail=thumbnail
        )

    except Exception as e:
        print(f"Together AI Error: {e}")
        return None


currency_rates = CurrencyRates()

async def convert_currency(entries: list[ProductEntry], target="USD"):
    if not entries:
        return []

    for e in entries:
        try:
            if not e.currency or e.currency == target:
                continue

            rate = currency_rates.get_rate(e.currency, target)
            e.price = round(e.price * rate, 2)
            e.currency = target

        except Exception as err:
            print(f"[Currency Conversion Error]: {e.productName} | {err}")

    return entries


    
async def search_prices(country: str, query: str) -> List[ProductEntry]:
    raw = await fetch_from_serper(country, query)
    top_10_raw = sorted(raw, key=safe_price)[:10]
    print(top_10_raw)
    matches = await asyncio.gather(
        *[asyncio.to_thread(match_and_build, item, query) for item in top_10_raw],
        return_exceptions=True
    )

    filtered = [m for m in matches if isinstance(m, ProductEntry)]

    target_currency = get_currency_from_country(country.upper())
    normalized = await convert_currency(filtered, target=target_currency)

    return sorted(normalized, key=lambda x: x.price)