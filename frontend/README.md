# 🛍️ Item Scraper Frontend

This is the **React-based frontend** for the [Item Scraper](https://github.com/akshaygaur2407/item-scraper) project.  
It allows users to search for a product, select a country, and view normalized product listings with AI-powered match scoring.

---

## 🚀 Features

- 🔎 Real-time product search using **Serper.dev** (Google Shopping)
- 🌍 Country-based filtering with currency conversion
- 🧠 LLM-based product title similarity matching (via Together AI)
- 💸 Price sorting + seller and thumbnail info
- 📱 Fully responsive with Bootstrap styling
- 🧾 Easy-to-read results in a scrollable table

---

## ⚙️ Tech Stack

- **React (Vite)**
- **Axios** — API requests
- **Bootstrap** — UI styling
- **country-list** — Full country dropdown
- **Deployed to**: [Vercel / Netlify / your choice]

---

## Special notes:- 
Rate Limits
- This project uses a free LLM model via Together.ai, which currently supports only 60 requests per minute, so effectively u can make 5 req/min.

- Avoid sending frequent or bulk requests in quick succession to prevent throttling or failure.

- I am only processing the cheapest 10 products that the Serper.dev api returns.


## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/akshaygaur2407/item-scraper.git
cd item-scraper/frontend
