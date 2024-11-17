from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "user"

  id = Column(Integer,  primary_key=True)
  email = Column(String, nullable=False)
  hashed_password = Column(String, nullable=False)
  is_admin = Column(Boolean, nullable=False)

  orders = relationship("Order", back_populates="users")

  def __str__(self) -> str:
    return f"{self.email}"
