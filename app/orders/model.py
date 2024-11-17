from sqlalchemy import Boolean, Column, Computed, ForeignKey, Integer, String, select
from app.database import Base
from sqlalchemy.orm import relationship

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


  markets = relationship("Market", back_populates="orders")
  products = relationship("Product", back_populates="orders")
  users = relationship("User", back_populates="orders")


  def __str__(self):
    return  f"Order {self.id}"
