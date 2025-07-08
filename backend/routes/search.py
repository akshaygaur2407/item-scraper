# backend/app/routes/search.py
from fastapi import APIRouter, HTTPException, Request
from typing import List

from limiter import limiter          # ← import your instance
from schemas.request import PriceRequest
from schemas.response import ProductEntry
from services.price_search import search_prices

router = APIRouter()

@router.post("/search", response_model=List[ProductEntry])
@limiter.limit("60/minute")               # ← call the instance’s .limit()
async def search_endpoint(request: Request, req: PriceRequest):
    try:
        return await search_prices(req.country, req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))