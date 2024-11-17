from sqlalchemy import  Column, Integer, String
from app.database import Base

from sqlalchemy.orm import relationship

class Category(Base):
  __tablename__ = "category"

  id = Column(Integer,  primary_key=True)
  name = Column(String, nullable=False)

  markets = relationship("Market", back_populates="categories")
  products = relationship("Product", back_populates="categories")

  def __str__(self) -> str:
    return f"{self.name}"
