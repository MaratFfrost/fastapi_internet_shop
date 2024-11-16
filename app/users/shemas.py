from pydantic import BaseModel, EmailStr

class SUserLogin(BaseModel):
  email : EmailStr
  password: str


class SUserOrder(BaseModel):
  market_id : int
  product_id: int
  quantity: int
  adres: str
