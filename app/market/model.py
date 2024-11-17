from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Market(Base):
  __tablename__ = "markets"

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  category_id = Column(ForeignKey("category.id"))
  description = Column(String)


  orders = relationship("Order", back_populates="markets")
  categories = relationship("Category", back_populates="markets")
  products = relationship("Product", back_populates="markets")

  def __str__(self):
    return  f"Market {self.name}"
