from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base


class Market(Base):
  __tablename__ = "markets"

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  category_id = Column(ForeignKey("category.id"))
  description = Column(String)
