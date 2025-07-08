# 🛍️ Item Scraper Backend

This is the **FastAPI backend** for the Item Scraper project — a tool that fetches real-time product listings from Google Shopping (via Serper.dev), ranks them using an LLM-powered similarity model, and normalizes prices in your local currency.

---

## 🚀 Features

- 🔍 **Search any product** by name across global Google Shopping listings
- 🌍 **Country-specific search** with price normalization
- 🧠 **LLM-powered product title matching** using [Together.ai](https://together.ai)
- 💰 **Live currency conversion** using `forex-python`

---

## ⚙️ Tech Stack

- **FastAPI** — Modern async Python web framework
- **httpx** — Async HTTP client for external API calls
- **Together AI API** — LLM model: `meta-llama/Llama-3.3-70B-Instruct-Turbo-Free`
- **Serper.dev** — Google Shopping results
- **forex-python** — For currency conversion
- **Pydantic** — Data validation and parsing

---

## 📦 Installation & Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/akshaygaur2407/item-scraper.git
cd item-scraper/backend

Rate Limits
This project uses a free LLM model via Together.ai, which currently supports only 5 requests per minute.

Avoid sending frequent or bulk requests in quick succession to prevent throttling or failure.


