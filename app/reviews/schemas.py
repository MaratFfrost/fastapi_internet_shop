from pydantic import BaseModel, EmailStr

class SReviews(BaseModel):
  product_id: int
  stars: int
  detail: str
