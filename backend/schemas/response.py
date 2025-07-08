from typing import Optional
from pydantic import BaseModel

class ProductEntry(BaseModel):
    link: str
    price: float
    currency: str
    productName: str
    thumbnail: Optional[str] = None
    seller:   Optional[str] = None
    matchScore: float
