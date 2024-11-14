from sqlalchemy import Boolean, Column, Computed, ForeignKey, Integer, String, select
from app.database import Base
from app.products.model import Product

class Order(Base):
  __tablename__ = "orders"

  id = Column(Integer, primary_key=True)
  user_id = Column(ForeignKey("user.id"))
  market_id = Column(ForeignKey("markets.id"))
  product_id = Column(ForeignKey("product.id"))
  quantity = Column(Integer, nullable=False)
  total_price = Column(Integer, nullable=False)
  is_paid = Column(Boolean, nullable=False)
  adres = Column(String, nullable=False)
