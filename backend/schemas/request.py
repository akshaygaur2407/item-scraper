# request.py
from pydantic import BaseModel, Field

class PriceRequest(BaseModel):
    country: str = Field(..., min_length=2, max_length=2, description="ISO alpha‑2")
    query: str = Field(..., description="Product query, e.g. 'iPhone 16 Pro, 128GB'")
