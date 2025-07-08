import os, httpx, asyncio
from schemas.response import ProductEntry
from utils.http_client import async_client
from config import SERPER_API_KEY, EXCHANGE_API_URL, HTTP_TIMEOUT, get_serpapi_location
from typing import Optional, List
import together
import re
from services.helper import extract_price, get_currency_from_country, safe_price

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
        print(items)
        for item in items:
            results.append({
                "title": item.get("title"),
                "price": item.get("price"),
                "link": item.get("link"),
                "thumbnail": item.get("imageUrl"),
                "seller": item.get("source"),
            })

        return results


async def match_and_build(entry: dict, raw_query: str) -> Optional[ProductEntry]:
    title = entry.get("title", "")
    price = extract_price(entry.get("price", "0")) or 0.0
    currency = entry.get("currency", "")
    link = entry.get("link", "")
    source= entry.get("source")
    thumbnail= entry.get("imageUrl")

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
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
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
        if score < 0.8:
            return None

        return ProductEntry(
            link=link,
            price=price,
            currency=currency,
            productName=title,
            matchScore=score,
            source= source,
            thumbnail=thumbnail
        )

    except Exception as e:
        print(f"Together AI Error: {e}")
        return None


async def convert_currency(entries: list[ProductEntry], target="USD"):
    base_currency = entries[0].currency
    if base_currency == target:
        return entries
    r = await async_client().get(
        f"{EXCHANGE_API_URL}/latest",
        params={"base": base_currency}
    )
    rates = r.json().get("rates", {})
    rate = rates.get(target, 1)

    for e in entries:
        if e.currency != target:
            e.price = round(e.price * rate, 2)
            e.currency = target

    return entries
    
async def search_prices(country: str, query: str) -> List[ProductEntry]:
    raw = await fetch_from_serper(country, query)
    breakpoint()
    top_10_raw = sorted(raw, key=safe_price)[:8]
    filtered: List[ProductEntry] = []
    for item in top_10_raw:
        entry = await match_and_build(item, query)
        if entry:
            filtered.append(entry)
    target_currency = get_currency_from_country(country.upper())
    normalized = await convert_currency(filtered, target=target_currency)

    return sorted(normalized, key=lambda x: x.price)