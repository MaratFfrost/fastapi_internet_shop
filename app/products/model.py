from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base

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
