from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base

from sqlalchemy.orm import relationship

class Product(Base):
  __tablename__="product"

  id = Column(Integer, primary_key=True)
  category_id = Column(ForeignKey('category.id'))
  market_id = Column(ForeignKey("markets.id"))
  name = Column(String, nullable=False)
  description = Column(String, nullable=False)
  amount = Column(Integer, nullable=False)
  price = Column(Integer, nullable=False)
  product_image_id = Column(Integer)

  categories = relationship("Category", back_populates="products" )
  markets = relationship("Market", back_populates="products")
  orders = relationship("Order", back_populates="products")

  def __str__(self) -> str:
    return f"{self.name}"
