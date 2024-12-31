from typing import Optional
from pydantic import BaseModel

class SProduct(BaseModel):
    category_id: Optional[int] = None
    markets_id: Optional[int] = None
    limit: Optional[int] = None
