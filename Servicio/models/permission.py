from ..database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text 
from sqlalchemy.orm import relationship

class Permissions(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True)
    permission_name = Column(Text , nullable=False)
    role_id = Column(Integer,ForeignKey("roles.role_id"), nullable=False)

   