from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base

class User(Base):
  __tablename__ = "user"

  id = Column(Integer,  primary_key=True)
  email = Column(String, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_admin = Column(Boolean, nullable=False)
