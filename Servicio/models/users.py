from ..database import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from .role import Roles

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String(70), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"),nullable=False)


