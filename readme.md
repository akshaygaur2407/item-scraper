# 🛍️ Item Scraper

This is a **Full Stack Project** for the [Item Scraper](https://github.com/akshaygaur2407/item-scraper) project.  
It allows users to search for a product, select a country, and view normalized product listings with AI-powered match scoring.

---

## Special notes:- 
Rate Limits
- This project uses a free LLM model via Together.ai, which currently supports only 60 requests per minute, so effectively u can make 5 req/min.

- Avoid sending frequent or bulk requests in quick succession to prevent throttling or failure.

- I am only processing the cheapest 10 products that the Serper.dev api returns.


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
- **React (Vite)**
- **Axios** — API requests
- **Bootstrap** — UI styling
- **country-list** — Full country dropdown
- **Deployed to**: [Vercel/Render]


## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/akshaygaur2407/item-scraper.git
cd item-scraper/frontend
npm i
npm run dev

```bash
cd item-scraper/backend
pip install -r requirements.txt