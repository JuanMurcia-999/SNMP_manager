from ..database import Base
from sqlalchemy import Column, Integer, String


class Roles(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)

  
